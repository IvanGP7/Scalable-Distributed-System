import xmlrpc.client

def test_insult_service():
    server = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")
    
    # Test Insult Service
    print("=== Insult Service Test ===")
    print("Lista inicial:", server.insult_list())
    server.add_insult("Tonto")
    print("Lista actualizada:", server.insult_list())
    print("Insulto aleatorio:", server.random_insult())

    # Test Insult Filter
    print("\n=== Insult Filter Test ===")
    test_text = "Eres un tonto y un bobo"
    print("Texto original:", test_text)
    print("Texto censurado:", server.censor_text(test_text))

test_insult_service()
