#!/bin/bash

# Configuración
REDIS_CONTAINER="my-redis"  # Nombre del contenedor Docker
NUM_REQUESTS=300             # Número de peticiones de prueba
TEST_TEXT="Eres un bobo y un tonto"  # Texto para probar censura

# Función para ejecutar comandos Redis en el contenedor
redis_cli() {
    docker exec $REDIS_CONTAINER redis-cli "$@"
}

# Iniciar Redis en Docker (si no está corriendo)
if ! docker ps | grep -q $REDIS_CONTAINER; then
    echo "Iniciando contenedor Redis..."
    docker start $REDIS_CONTAINER > /dev/null
    sleep 2  # Esperar inicialización
fi

echo "Iniciando pruebas de rendimiento para Redis..."
echo "----------------------------------------"

# Prueba 1: InsultService (añadir insultos)
total_time=0
for ((i=1; i<=NUM_REQUESTS; i++)); do
    start_time=$(date +%s%3N)
    redis_cli RPUSH lista_insultos "insulto_$i" > /dev/null
    end_time=$(date +%s%3N)
    total_time=$((total_time + end_time - start_time))
done
avg_time=$((total_time / NUM_REQUESTS))
echo "InsultService (RPUSH):"
echo "  - Requests: $NUM_REQUESTS"
echo "  - Tiempo total: ${total_time}ms"
echo "  - Tiempo promedio: ${avg_time}ms"

# Prueba 2: InsultFilter (censurar texto)
total_time=0
for ((i=1; i<=NUM_REQUESTS; i++)); do
    # Obtener lista de insultos primero
    insults=$(redis_cli LRANGE lista_insultos 0 -1 | tr '\n' '|' | sed 's/|$//')
    start_time=$(date +%s%3N)
    echo "$TEST_TEXT" | awk -v pat="$insults" '{gsub(pat, "CENSORED")}1' > /dev/null
    end_time=$(date +%s%3N)
    total_time=$((total_time + end_time - start_time))
done
avg_time=$((total_time / NUM_REQUESTS))
echo "InsultFilter (censura):"
echo "  - Requests: $NUM_REQUESTS"
echo "  - Tiempo total: ${total_time}ms"
echo "  - Tiempo promedio: ${avg_time}ms"

echo "----------------------------------------"
echo "Pruebas completadas."