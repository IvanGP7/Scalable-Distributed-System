import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import io

# Configuración para evitar problemas de encoding en Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuración de estilo
plt.style.use('seaborn-v0_8') if 'seaborn-v0_8' in plt.style.available else plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 12
colors = {'InsultClient': '#4C72B0', 'FilterClient': '#DD8452'}

def load_data(file_path):
    """Carga los datos manejando posibles errores de encoding"""
    try:
        # Leer con encoding UTF-8 y manejar posibles BOM
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        # Procesamiento manual para mayor robustez
        data = []
        for line in lines:
            line = line.strip()
            if line:  # Ignorar líneas vacías
                parts = line.split(',')
                if len(parts) == 4:
                    try:
                        data.append({
                            'type': parts[0],
                            'iterations': int(parts[1]),
                            'nodes': int(parts[2]),
                            'time': float(parts[3])
                        })
                    except ValueError as e:
                        print(f"⚠ Línea ignorada (formato inválido): {line}")
        
        if not data:
            raise ValueError("El archivo no contiene datos válidos")
            
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"\nERROR: No se pudo cargar {file_path}")
        print(f"Razón: {str(e)}")
        print("\nAsegúrate de que:")
        print("1. El archivo existe en la ubicación correcta")
        print("2. Tiene el formato: Tipo,Iteraciones,Nodos,Tiempo")
        print("3. Ejemplo válido: InsultClient,25,1,1.4938")
        sys.exit(1)

def create_plots(df):
    """Genera los gráficos de análisis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Gráfico 1: Tiempo vs Iteraciones
    for client_type, color in colors.items():
        subset = df[df['type'] == client_type]
        if not subset.empty:
            for nodes in sorted(subset['nodes'].unique()):
                node_data = subset[subset['nodes'] == nodes].sort_values('iterations')
                ax1.plot(node_data['iterations'], node_data['time'], 
                        marker='o' if client_type == 'InsultClient' else 's',
                        linestyle='--',
                        label=f'{client_type} ({nodes} nodos)',
                        color=color,
                        alpha=0.7)
    
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Número de Iteraciones (log scale)', fontweight='bold')
    ax1.set_ylabel('Tiempo de Ejecución (segundos, log scale)', fontweight='bold')
    ax1.set_title('ESCALABILIDAD DEL SISTEMA\nTiempo vs Carga de Trabajo', fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.02, 1), framealpha=1)
    ax1.grid(True, which="both", linestyle='--', alpha=0.5)
    
    # Gráfico 2: Speedup
    speedup_added = False
    for (client_type, iterations), group in df.groupby(['type', 'iterations']):
        baseline = group[group['nodes'] == 1]
        if not baseline.empty:
            baseline_time = baseline['time'].iloc[0]
            speedup_data = group[group['nodes'] > 1].copy()
            speedup_data['speedup'] = baseline_time / speedup_data['time']
            
            if not speedup_data.empty:
                speedup_added = True
                ax2.plot(speedup_data['nodes'], speedup_data['speedup'],
                        marker='^' if client_type == 'InsultClient' else 'v',
                        linestyle='-',
                        label=f'{client_type} ({iterations} iter)',
                        color=colors[client_type],
                        alpha=0.7)
    
    if speedup_added:
        ax2.set_xlabel('Número de Nodos Workers', fontweight='bold')
        ax2.set_ylabel('Speedup (Tiempo_1nodo / Tiempo_Nnodos)', fontweight='bold')
        ax2.set_title('EFICIENCIA DE PARALELIZACIÓN\nGanancia al aumentar nodos', fontweight='bold')
        ax2.legend(bbox_to_anchor=(1.02, 1), framealpha=1)
        ax2.grid(True, linestyle='--', alpha=0.5)
    else:
        ax2.text(0.5, 0.5, 'No hay datos suficientes\npara calcular speedup',
                ha='center', va='center', fontsize=12)
    
    plt.tight_layout()
    output_file = 'performance_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n Gráficos generados correctamente en: {output_file}")

if __name__ == "__main__":
    # Configuración para Windows
    if sys.platform == 'win32':
        import locale
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    
    print("=== ANÁLISIS DE PERFORMANCE ===")
    data_file = 'tiempos_clientes.log'
    print(f"\nCargando datos desde: {data_file}")
    
    try:
        data = load_data(data_file)
        print("\nDatos cargados exitosamente!")
        print(f"Total de registros: {len(data)}")
        print("\nResumen estadístico:")
        print(data.groupby(['type', 'iterations', 'nodes'])['time'].mean().unstack())
        
        print("\nGenerando gráficos...")
        create_plots(data)
    except Exception as e:
        print(f"\n Error durante la ejecución: {str(e)}")
        sys.exit(1)