import redis
import json
import time
from Functions_insult import InsultManager

def process_insult_task(manager, payload, r):
    insult = payload.get("insult")
    manager.add_insult(insult)
    r.incr("insult_done")

def process_filter_task(manager, payload, r):
    text = payload.get("text")
    manager.censor_text(text)
    r.incr("filter_done")

def main():
    r = redis.Redis(host='localhost', port=6379, db=0)
    manager = InsultManager(r)

    print("Worker activo. Escuchando tareas...")

    while True:
        task = r.blpop(["insult_queue", "filter_queue"], timeout=5)
        if task:
            queue_name, data = task
            payload = json.loads(data)

            if queue_name.decode() == "insult_queue":
                process_insult_task(manager, payload, r)
            elif queue_name.decode() == "filter_queue":
                process_filter_task(manager, payload, r)
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()
