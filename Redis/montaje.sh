#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_workers> <num_requests>"
    exit 1
fi

NUM_WORKERS=$1
NUM_REQUESTS=$2
REDIS_CONTAINER="my-redis"

# Iniciar Redis
echo "Iniciando Redis..."
docker start $REDIS_CONTAINER
sleep 2

# Iniciar workers en segundo plano
echo "Lanzando $NUM_WORKERS workers..."
PIDS=()
for ((i=0; i<NUM_WORKERS; i++)); do
    python worker.py &
    PIDS+=($!)
done

# Esperar un poco a que se estabilicen los workers
sleep 2

# Ejecutar los clientes
echo "Ejecutando clientes..."
python insult_client.py $NUM_REQUESTS $NUM_WORKERS
python filter_client.py $NUM_REQUESTS $NUM_WORKERS

# Mostrar resultados
echo -e "\nResultados:"
cat tiempos_clientes.log

# Esperar a que terminen las tareas (opcional: sleep más largo según volumen)
sleep 2

# Detener workers
echo "Deteniendo workers..."
for pid in "${PIDS[@]}"; do
    kill $pid 2>/dev/null
done

# Detener Redis
docker stop $REDIS_CONTAINER > /dev/null

echo -e "\nSistema detenido correctamente"
