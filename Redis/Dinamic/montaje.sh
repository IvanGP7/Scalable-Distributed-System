#!/bin/bash
parar(){
    # Limpieza
    docker stop $REDIS_CONTAINER > /dev/null

    if ps -p $WORKER_PID > /dev/null 2>&1; then
        kill $WORKER_PID
        wait $WORKER_PID 2>/dev/null
    fi

    echo -e "\nSistema detenido correctamente"

    exit 1
}

trap parar SIGINT

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_workers> <num_requests>"
    exit 1
fi

REDIS_CONTAINER="my-redis"
NUM_REQUESTS=$2
NUM_THREADS=$1
echo -e "\n$0 $1 $2" >> worker.log
# Iniciar Redis
docker start $REDIS_CONTAINER
sleep 2
python Limpiar.py
sleep 1
# Iniciar worker dinámico
python worker.py &
WORKER_PID=$!
sleep 5

# Ejecutar pruebas
echo -e "\n=== Ejecutando pruebas ==="
python insult_client.py $NUM_REQUESTS $NUM_THREADS
sleep 1
python filter_client.py $NUM_REQUESTS $NUM_THREADS


# Resultados
echo -e "\n=== Resultados ==="
cat tiempos_clientes.log

# Limpieza
docker stop $REDIS_CONTAINER > /dev/null

if ps -p $WORKER_PID > /dev/null 2>&1; then
    kill $WORKER_PID
    wait $WORKER_PID 2>/dev/null
fi

echo -e "\nSistema detenido correctamente"
