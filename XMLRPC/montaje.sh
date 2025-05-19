#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <num_servers> <num_requests>"
    exit 1
fi

NUM_SERVERS=$1
NUM_REQUESTS=$2

# Limpiar archivos previos
> servidores.log
# Iniciar NameServer
python NameServer/nameserver.py >> servidores.log 2>&1 &
NAME_PID=$!
sleep 2

# Iniciar StorageServer
python StorageServer/storage.py >> servidores.log 2>&1 &
STORAGE_PID=$!
sleep 2

# Iniciar Servidores
for ((i=0; i<NUM_SERVERS; i++)); do
    PORT=$((8000+i))
    python Servidores/server.py $PORT >> servidores.log 2>&1 &
    echo "Servidor en puerto $PORT iniciado"
    sleep 1
done

# Esperar inicialización completa
sleep 5  # Tiempo para sincronización inicial

# Ejecutar Clientes
echo "Iniciando clientes..."
python Clientes/insult_client.py $NUM_REQUESTS
python Clientes/filter_client.py $NUM_REQUESTS

# Resultados
echo -e "\n=== RESULTADOS ==="
cat tiempos_clientes.log

# Limpieza
kill $NAME_PID $STORAGE_PID 2>/dev/null
pkill -f "python Servidores/server.py" 2>/dev/null