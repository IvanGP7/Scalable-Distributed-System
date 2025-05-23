import pika
from Functions_insult import InsultManager

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
insult_manager = InsultManager(channel)

def test_system():
    print("\n=== TEST CLIENTE ===")
    print("Lista actual de insultos:", insult_manager.insult_list())
    
    # Test añadir insulto
    new_insult = "TONTOLABA"
    print(f"\nAñadiendo '{new_insult}'...")
    if insult_manager.add_insult(new_insult):
        print("¡Añadido con éxito!")
    else:
        print("Ya existía")
    
    # Test censura de texto
    test_text = "Eres un bobo y un zoquete, además de medio tontolaba"
    print("\n=== TEST CENSURA ===")
    print("Texto original:", test_text)
    censored_text = insult_manager.censor_text(test_text)
    print("Texto censurado:", censored_text)
    
if __name__ == "__main__":
    test_system()
    connection.close()