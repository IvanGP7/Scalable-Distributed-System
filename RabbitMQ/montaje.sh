#!/bin/bash

# Iniciar RabbitMQ en Docker
docker run rabbitmq
sleep 5  # Esperar inicialización

# Iniciar worker
python mq_worker.py &
WORKER_PID=$!
sleep 2

# Ejecutar clientes
python insult_producer.py
python filter_producer.py

# Dar tiempo a procesar
sleep 3

# Mostrar resultados
echo -e "\n=== INSULTOS REGISTRADOS ==="
cat insults.txt

# Limpieza
kill -9 $WORKER_PID
docker stop rabbitmq