import redis
import time

def get_and_save_insults():
    # Conexión a Redis
    r = redis.Redis(host='localhost', port=6379, db=0)

    try:
        # Obtener todos los insultos
        insults = r.lrange("global_insults", 0, -1)

        # Guardar en archivo
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"insults_backup_{timestamp}.txt"

        with open(filename, "w") as f:
            f.write("=== LISTA COMPLETA DE INSULTOS ===\n")
            for i, insult in enumerate(insults, 1):
                f.write(f"{i}. {insult.decode('utf-8')}\n")

        print(f"✓ {len(insults)} insultos guardados en {filename}")
        print("Contenido:")
        print(open(filename).read())

    except Exception as e:
        print(f"✗ Error: {str(e)}")
    finally:
        # Cerrar conexión (opcional en Redis)
        r.close()

if __name__ == "__main__":
    print("\nObteniendo lista de insultos...")
    get_and_save_insults()