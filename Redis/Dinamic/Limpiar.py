import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.delete("insult_queue", "filter_queue", "insult_done", "filter_done", "lambda_estimate")
print("Redis limpiado correctamente.")
