import re
import matplotlib.pyplot as plt
import pandas as pd

log_path = "Redis/Dinamic/worker.log"

# Nueva expresión adaptada a tus líneas reales
pattern_test = re.compile(r"\./montaje\.sh\s+(\d+)\s+(\d+)")
pattern_worker = re.compile(r"Escalando a (\d+) workers")

tests = []
current_test = None
max_workers = 0

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        print("LINE:", line)  # Depuración

        test_match = pattern_test.search(line)
        if test_match:
            if current_test:
                current_test["max_workers"] = max_workers
                tests.append(current_test)
            current_test = {
                "threads": int(test_match.group(1)),
                "iterations": int(test_match.group(2))
            }
            max_workers = 0  # Reiniciar el contador para este test

        else:
            worker_match = pattern_worker.search(line)
            if worker_match:
                n_workers = int(worker_match.group(1))
                if n_workers > max_workers:
                    max_workers = n_workers

# Guardar el último test pendiente
if current_test:
    current_test["max_workers"] = max_workers
    tests.append(current_test)

# Convertir a DataFrame
df = pd.DataFrame(tests)
print(df)  # Verifica que tenga datos válidos

if not df.empty:
    plt.figure(figsize=(10, 6))
    for thread in sorted(df["threads"].unique()):
        subset = df[df["threads"] == thread]
        plt.plot(subset["iterations"], subset["max_workers"], marker="o", label=f"{thread} threads")

    plt.xlabel("Iteraciones")
    plt.ylabel("Máximo número de workers")
    plt.title("Escalado de Workers en función de Iteraciones y Threads")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("No se encontraron datos válidos en el log.")
