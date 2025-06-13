import redis
import time
import sys

# Texto de prueba para censurar
TEST_TEXT = "Eres un idiota y un tonto del culo."

def main():
    if len(sys.argv) != 3:
        print("Uso: python insult_client.py <num_peticiones> <num_threads>")
        return

    num_requests = int(sys.argv[1])
    num_threads = int(sys.argv[2])
    client_name = "insult"

    # Conexión con Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Reiniciar el contador en Redis
    r.set(f"{client_name}_done", 0)

    print(f"\nInsultClient: {num_requests} peticiones delegadas a insult_queue")
    print(f"Texto de prueba: '{TEST_TEXT}'")

    start_time = time.time()

    # Enviar las tareas
    for _ in range(num_requests):
        r.rpush("insult_queue", TEST_TEXT)

    # Calcular y guardar la tasa estimada de llegada
    duration = time.time() - start_time
    lambda_est = num_requests / duration if duration > 0 else 0
    r.set("lambda_estimate", lambda_est)

    # Esperar hasta que todas las tareas sean procesadas
    while int(r.get(f"{client_name}_done") or 0) < num_requests:
        time.sleep(0.1)

    total_time = time.time() - start_time

    # Registrar en el log
    with open("tiempos_clientes.log", "a") as f:
        f.write(f"InsultClient,{num_threads},{num_requests},{total_time:.4f}\n")

    print(f"Finalizado en {total_time:.2f} segundos")

if __name__ == "__main__":
    main()
