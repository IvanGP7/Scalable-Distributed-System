#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_workers> <num_requests>"
    exit 1
fi

NUM_WORKERS=$1
NUM_REQUESTS=$2
if ! pgrep -f "redis-server" > /dev/null; then
    echo "Iniciando Redis..."
    redis-server &
    sleep 5
else
    echo "Redis ya está en ejecución."
fi


# Iniciar workers
#for i in $(seq 1 $NUM_WORKERS); do
#    echo "Iniciando Worker: $i"
#    python workers/worker.py & > /dev/null 2>&1
#    # Esperar inicialización
#    sleep 1
#done


# Ejecutar clientes
python insult_client.py $NUM_REQUESTS $NUM_WORKERS > /dev/null 2>&1
echo "Insult Cliente finalizado: $NUM_REQUESTS IT, $NUM_WORKERS ND"
python filter_client.py $NUM_REQUESTS $NUM_WORKERS > /dev/null 2>&1
echo "Insult Filter finalizado: $NUM_REQUESTS IT, $NUM_WORKERS ND"

# Limpieza
#kill -9 $(ps aux | grep "workers/worker" | grep -v grep | awk '{print $2}')
