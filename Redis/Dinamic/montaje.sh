#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_workers> <num_requests>"
    exit 1
fi

REDIS_CONTAINER="my-redis"
NUM_REQUESTS=$1
NUM_THREADS=$2
echo -e "\n$0 $1 $2" >> worker.log
# Iniciar Redis
docker start $REDIS_CONTAINER
sleep 2

# Iniciar worker dinámico
python worker.py &
WORKER_PID=$!
sleep 5

# Ejecutar pruebas
echo -e "\n=== Ejecutando pruebas ==="
python filter_client.py $NUM_REQUESTS $NUM_THREADS

# Resultados
echo -e "\n=== Resultados ==="
cat tiempos_clientes.log

# Limpieza
docker stop $REDIS_CONTAINER > /dev/null
kill $WORKER_PID
wait $WORKER_PID 2>/dev/null

echo -e "\nSistema detenido correctamente"