import redis

def export_and_clear():
    try:
        # Conexión a Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # 1. Exportar a archivo
        insults = r.lrange("lista_insultos", 0, -1)
        with open("insultos.txt", "w", encoding="utf-8") as f:
            for insult in insults:
                f.write(f"{insult.decode('utf-8')}\n")
        
        print(f"Exportados {len(insults)} insultos a insultos.txt")

        # 2. Limpiar lista
        r.delete("lista_insultos")
        print("Lista de insultos limpiada")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Ejecutando exportación y limpieza...")
    export_and_clear()
    print("Operación completada")