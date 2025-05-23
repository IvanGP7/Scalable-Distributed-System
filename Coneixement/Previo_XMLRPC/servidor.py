from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from Functions_insult import *

# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler,
                        allow_none=True) as server:
    server.register_introspection_functions()
    
    # Registrar todas las funciones
    server.register_function(add_insult)
    server.register_function(random_insult)
    server.register_function(insult_list)
    server.register_function(clear_insults)
    server.register_function(censor_text)

    print("Servidor listo en http://localhost:8000")
    print("Insultos iniciales:", lista_insultos)
    server.serve_forever()