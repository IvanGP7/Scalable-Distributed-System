#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_workers> <num_requests>"
    exit 1
fi

NUM_WORKERS=$1
NUM_REQUESTS=$2

> insults.txt
> censored.txt

echo "Iniciando RabbitMQ..."
docker start rabbitmq

# Esperar inicialización con verificación
echo "Esperando inicialización de RabbitMQ..."
for i in {1..10}; do
    if docker logs rabbitmq | tail -15 | grep -q "Server startup complete"; then
        echo "RabbitMQ listo"
        break
    fi
    sleep 2
    if [ $i -eq 10 ]; then
        echo "Error: RabbitMQ no se inició correctamente después de 20 segundos"
        exit 1
    fi
done

# Iniciar workers
WORKER_PIDS=()
for i in $(seq 1 $NUM_WORKERS); do
    echo "Iniciando worker $i..."
    python worker.py $i > /dev/null 2>&1 &
    WORKER_PIDS+=($!)
    sleep 0.5
done

# Ejecutar clientes
echo "Ejecutando clientes..."
python insult_client.py $NUM_REQUESTS $NUM_WORKERS > insults.txt
python filter_client.py $NUM_REQUESTS $NUM_WORKERS > censored.txt

# Dar tiempo a procesar
sleep 3

# Mostrar resultados
echo -e "\n=== INSULTOS REGISTRADOS ==="
#cat insults.txt
echo "-- Comentado --"
echo -e "\n=== TIEMPOS DE EJECUCIÓN ==="
cat tiempos_clientes.log

# Detener contenedor
echo -e "\nDeteniendo RabbitMQ..."
docker stop rabbitmq

# Limpieza
echo -e "\nDeteniendo workers..."
sleep 3


#for pid in "${WORKER_PIDS[@]}"; do
#    kill -9 $pid 2>/dev/null
#done