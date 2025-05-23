import Pyro4

def test_system():
    server = Pyro4.Proxy("PYRONAME:servidor.insultos")
    
    print("\n=== TEST CLIENTE ===")
    print("Lista actual:", server.insult_list())
    
    # Test añadir insulto
    new_insult = "Tontolaba"
    print(f"\nAñadiendo '{new_insult}'...")
    if server.add_insult(new_insult):
        print("¡Añadido con éxito!")
    else:
        print("Ya existía")
    
    # Test de censura
    test_text = "Eres un bobo, un ZoQuete y un TONTOlaba de mierda"
    print("\n=== TEST CENSURA ===")
    print("Texto original:", test_text)
    print("Texto censurado:", server.censor_text(test_text))
    

if __name__ == "__main__":
    test_system()