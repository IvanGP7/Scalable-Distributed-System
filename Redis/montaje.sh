#!/bin/bash

# Configuración
REDIS_CONTAINER="my-redis"
NUM_REQUESTS=$1
NUM_THREADS=$2

# Iniciar Redis en Docker
docker start $REDIS_CONTAINER
sleep 1  # Esperar inicialización

# Iniciar servidor en segundo plano
# python servidor.py &
sleep 5

# Ejecutar clientes
echo -e "\n=== Ejecutando pruebas ==="
python insult_client.py $NUM_REQUESTS $NUM_THREADS
python filter_client.py $NUM_REQUESTS $NUM_THREADS

# Mostrar resultados
echo -e "\n=== Resultados ==="
cat tiempos_clientes.log

python get_insults.py

# Limpieza
docker stop $REDIS_CONTAINER > /dev/null

echo -e "\nSistema detenido correctamente"