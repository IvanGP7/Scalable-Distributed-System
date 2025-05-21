import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

# Configurar el backend para evitar problemas en Windows
plt.switch_backend('agg')

# Configuración de estilo
try:
    plt.style.use('seaborn-v0_8')
except:
    plt.style.use('ggplot')

plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 12
colors = {'InsultClient': '#4C72B0', 'FilterClient': '#DD8452'}

def load_data(file_path):
    """Carga los datos desde el archivo log"""
    try:
        df = pd.read_csv(file_path, 
                        header=None, 
                        names=['type', 'iterations', 'nodes', 'time'],
                        encoding='utf-8')
        return df
    except FileNotFoundError:
        print(f"\nError: No se encontró el archivo {file_path}")
        print("Asegúrate de que el archivo existe y tiene el formato correcto:")
        print("Formato esperado: InsultClient,25,1,1.4938 (por línea)")
        sys.exit(1)

def create_plots(df):
    """Crea los gráficos de análisis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Gráfico 1: Tiempo vs Iteraciones
    for client_type, color in colors.items():
        subset = df[df['type'] == client_type]
        for nodes in sorted(subset['nodes'].unique()):
            node_data = subset[subset['nodes'] == nodes]
            ax1.plot(node_data['iterations'], node_data['time'], 
                    marker='o', linestyle='--',
                    label=f'{client_type} - {nodes} nodos',
                    color=color, alpha=0.7)
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Número de Iteraciones (log)')
    ax1.set_ylabel('Tiempo de Ejecución (seg, log)')
    ax1.set_title('Tiempo de Ejecución vs Carga de Trabajo')
    ax1.legend(bbox_to_anchor=(1.05, 1))
    ax1.grid(True, which="both", ls="--")
    
    # Gráfico 2: Speedup
    for iterations in sorted(df['iterations'].unique()):
        for client_type, color in colors.items():
            subset = df[(df['type'] == client_type) & 
                       (df['iterations'] == iterations)]
            if not subset.empty:
                baseline = subset[subset['nodes'] == 1]['time'].values[0]
                speedup = baseline / subset['time']
                ax2.plot(subset['nodes'], speedup,
                        marker='s', linestyle='-',
                        label=f'{client_type} - {iterations} iter',
                        color=color, alpha=0.7)
    
    ax2.set_xlabel('Número de Nodos Workers')
    ax2.set_ylabel('Speedup (Tiempo_1nodo / Tiempo_Nnodos)')
    ax2.set_title('Ganancia de Paralelización')
    ax2.legend(bbox_to_anchor=(1.05, 1))
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    print("\nGráficos generados correctamente en 'performance_analysis.png'")

if __name__ == "__main__":
    # Cambiar por 'tiempos_clientes.log' si es diferente
    log_file = 'tiempos_clientes.log'  
    
    print(f"Cargando datos desde {log_file}...")
    data = load_data(log_file)
    
    print("\nResumen de datos cargados:")
    print(data.groupby(['type', 'iterations', 'nodes']).describe())
    
    print("\nGenerando gráficos...")
    create_plots(data)