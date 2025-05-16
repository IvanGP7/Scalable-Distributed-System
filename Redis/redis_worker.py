import redis
import threading

class RedisWorker:
    def __init__(self, worker_id):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.worker_id = worker_id
        self.insults_key = "global_insults"

        # Inicializar con valores por defecto
        if not self.r.exists(self.insults_key):
            self.r.rpush(self.insults_key, *["BOBO", "TONTOLABA"])

    def add_insult(self, insult):
        if not self.r.lrem(self.insults_key, 0, insult):
            self.r.rpush(self.insults_key, insult)
            return True
        return False

    def censor_text(self, text):
        insults = [i.decode('utf-8') for i in self.r.lrange(self.insults_key, 0, -1)]
        if not insults:
            return text

        import re
        pattern = re.compile('|'.join(map(re.escape, insults)), re.IGNORECASE)
        return pattern.sub('CENSORED', text)

if __name__ == "__main__":
    import sys
    worker_id = sys.argv[1] if len(sys.argv) > 1 else "1"
    worker = RedisWorker(worker_id)
    print(f"Redis Worker {worker_id} listo")