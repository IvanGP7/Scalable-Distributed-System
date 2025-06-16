# Práctica 1 – Sistemas Distribuidos

# Práctica 1 – Sistemas Distribuidos

## Descripción del proyecto

Este proyecto forma parte de la primera práctica de la asignatura de Sistemas Distribuidos y tiene como objetivo aplicar de forma práctica los fundamentos del procesamiento concurrente, la comunicación entre nodos y el diseño de arquitecturas distribuidas escalables.

La práctica gira en torno al diseño y evaluación de un sistema que gestiona y censura insultos. Este sistema está compuesto por dos tipos principales de clientes:
- **InsultClient**: que se encarga de insertar insultos en el sistema.
- **FilterClient**: que se encarga de filtrar textos y censurar palabras ofensivas usando la lista de insultos almacenada.

El sistema completo debe ser capaz de recibir múltiples peticiones concurrentes, delegarlas entre varios nodos o procesos conocidos como *workers*, y garantizar tanto la coherencia de la información (en especial, la lista de insultos) como el rendimiento bajo carga.

Para ello, se han desarrollado diferentes versiones del sistema utilizando tecnologías de middleware distribuido:
- **XML-RPC**: basada en llamadas remotas a procedimientos entre cliente y servidor.
- **Pyro4**: una solución orientada a objetos que extiende el paradigma RPC con descubrimiento dinámico de nodos mediante NameServer.
- **Redis**: con dos variantes:
  - **Multi-nodo**: con un conjunto fijo de workers que consumen de colas compartidas.
  - **Dinámico**: con escalado automático de workers en función del volumen de peticiones.
- **RabbitMQ**: utilizando colas de mensajes AMQP para la distribución de tareas entre productores (clientes) y consumidores (workers).

Cada implementación aborda aspectos clave del diseño distribuido: sincronización, escalabilidad, eficiencia, balanceo de carga y tolerancia a fallos. En particular, el sistema basado en Redis dinámico introduce un mecanismo de escalado automático que ajusta en tiempo real el número de workers activos, dependiendo de la tasa de llegada de tareas y la longitud de las colas pendientes, lo que permite una respuesta más eficiente bajo cargas variables.

El rendimiento de cada tecnología se ha medido mediante scripts automatizados que ejecutan múltiples iteraciones con distintos niveles de concurrencia (número de hilos y número de peticiones). Los resultados se almacenan en un fichero de log y posteriormente son analizados gráficamente para comparar el *speed-up* alcanzado por cada arquitectura, así como su capacidad de adaptación a la carga.

Este proyecto no solo sirve como ejercicio práctico de implementación, sino también como una plataforma de análisis comparativo entre modelos distribuidos, ayudando a comprender mejor sus diferencias operativas y el impacto que tienen en la eficiencia global del sistema.


## Requisitos

- Python 3.10 o superior
- pip
- Docker
- Git

Instalar dependencias (de forma automática):

```bash
pip install -r requirements.txt

