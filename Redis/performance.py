import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el archivo de log
df = pd.read_csv("Redis/tiempos_clientes.log", header=None, names=["Client", "Nodos", "Iteraciones", "Tiempo"])

# Configurar estilo de gráficos
sns.set(style="whitegrid")

# === Gráficos Tiempo vs Nodos ===
for client in df["Client"].unique():
    plt.figure()
    for iteracion in sorted(df["Iteraciones"].unique()):
        subset = df[(df["Client"] == client) & (df["Iteraciones"] == iteracion)]
        plt.plot(subset["Nodos"], subset["Tiempo"], marker='o', label=f"{iteracion} iter")
    plt.title(f"Tiempo vs Nodos - {client}")
    plt.xlabel("Nodos")
    plt.ylabel("Tiempo (s)")
    plt.legend(title="Iteraciones")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"Redis/tiempo_vs_nodos_{client}.png")  # Guarda cada gráfico en un archivo

# === Gráficos Speedup vs Nodos ===
for client in df["Client"].unique():
    plt.figure()
    for iteracion in sorted(df["Iteraciones"].unique()):
        subset = df[(df["Client"] == client) & (df["Iteraciones"] == iteracion)].copy()
        tiempo_nodo_1 = subset[subset["Nodos"] == 1]["Tiempo"].values[0]
        subset["Speedup"] = tiempo_nodo_1 / subset["Tiempo"]
        plt.plot(subset["Nodos"], subset["Speedup"], marker='o', label=f"{iteracion} iter")
    plt.title(f"Speedup vs Nodos - {client}")
    plt.xlabel("Nodos")
    plt.ylabel("Speedup (T1 / Tn)")
    plt.legend(title="Iteraciones")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"Redis/speedup_vs_nodos_{client}.png")  # Guarda cada gráfico en un archivo

print("Graficos generados y guardados como PNG.")
