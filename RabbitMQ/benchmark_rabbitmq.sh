#!/bin/bash

RABBITMQ_CONTAINER="rabbitmq"
NUM_REQUESTS=300
TEST_TEXT="Eres un bobo y un tonto"

# Verificar si RabbitMQ está corriendo
if ! docker ps | grep -q $RABBITMQ_CONTAINER; then
    echo "⚠️  Iniciando contenedor RabbitMQ..."
    docker start $RABBITMQ_CONTAINER
    sleep 10
fi

# Crear la cola si no existe
docker exec $RABBITMQ_CONTAINER rabbitmqadmin declare queue name=insults durable=false > /dev/null 2>&1

echo "Iniciando pruebas de rendimiento para RabbitMQ..."
echo "----------------------------------------"

# Prueba 1: Publicar mensajes
total_time=0
for ((i=1; i<=NUM_REQUESTS; i++)); do
    start_time=$(date +%s%3N)
    docker exec $RABBITMQ_CONTAINER rabbitmqadmin publish exchange=amq.default routing_key=insults payload="insulto_$i" > /dev/null
    end_time=$(date +%s%3N)
    total_time=$((total_time + end_time - start_time))
done
avg_time=$((total_time / NUM_REQUESTS))
echo "InsultService (Publicación):"
echo "  - Requests: $NUM_REQUESTS"
echo "  - Tiempo total: ${total_time}ms"
echo "  - Tiempo promedio: ${avg_time}ms"

# Prueba 2: Consumir mensajes (sin requeue)
total_time=0
for ((i=1; i<=NUM_REQUESTS; i++)); do
    start_time=$(date +%s%3N)
    docker exec $RABBITMQ_CONTAINER rabbitmqadmin get queue=insults count=1 > /dev/null
    end_time=$(date +%s%3N)
    total_time=$((total_time + end_time - start_time))
done
avg_time=$((total_time / NUM_REQUESTS))
echo "InsultFilter (Consumo):"
echo "  - Requests: $NUM_REQUESTS"
echo "  - Tiempo total: ${total_time}ms"
echo "  - Tiempo promedio: ${avg_time}ms"

echo "----------------------------------------"
echo "Pruebas completadas."
