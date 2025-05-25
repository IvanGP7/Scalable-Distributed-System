#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_workers> <num_requests>"
    exit 1
fi

NUM_WORKERS=$1
NUM_REQUESTS=$2

#python -m Pyro4.naming --host localhost --port 9090 &

sleep 3
# Iniciar servicios base
echo "Iniciando servidores..."
python NameServer/nameserver.py &
python StorageServer/storage.py &
python SyncService/sync.py &

# Esperar inicialización
sleep 3

echo "Iniciando workers..."
# Iniciar workers
for i in $(seq 1 $NUM_WORKERS); do
    echo "Iniciando Worker: $i"
    python WorkerNodes/worker.py $i &
    sleep 0.5
done

# Esperar registro
sleep 3

# Ejecutar tests
python Clients/insult_client.py $NUM_REQUESTS
python Clients/filter_client.py $NUM_REQUESTS

kill -9 $(ps aux | grep "SyncService/sync" | grep -v grep | awk '{print $2}')
kill -9 $(ps aux | grep "WorkerNodes/worker" | grep -v grep | awk '{print $2}')
kill -9 $(ps aux | grep "NameServer/nameserver" | grep -v grep | awk '{print $2}')
kill -9 $(ps aux | grep "StorageServer/storage" | grep -v grep | awk '{print $2}')

#kill -9 $(ps aux | grep "Pyro4.naming" | grep -v grep | awk '{print $2}')
