import redis
from Functions_insult import InsultManager

# Configuración
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

def start_server():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    insult_manager = InsultManager(r)
    
    print("=== Servidor de Insultos ===")
    print(f"Conectado a Redis en {REDIS_HOST}:{REDIS_PORT}")
    print("Lista inicial:", insult_manager.insult_list())
    print("\nServidor listo. Presiona Ctrl+C para detener.")
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")

if __name__ == "__main__":
    start_server()