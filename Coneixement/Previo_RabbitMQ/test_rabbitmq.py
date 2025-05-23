import pika
from Functions_insult import InsultManager

def test_insult_service():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    manager = InsultManager(channel)
    
    # Test Insult Service
    print("=== Insult Service Test ===")
    print("Lista inicial:", manager.insult_list())
    manager.add_insult("Tonto")
    print("Lista actualizada:", manager.insult_list())
    print("Insulto aleatorio:", manager.random_insult())

    # Test Insult Filter
    print("\n=== Insult Filter Test ===")
    test_text = "Eres un tonto y un bobo"
    print("Texto original:", test_text)
    print("Texto censurado:", manager.censor_text(test_text))

test_insult_service()