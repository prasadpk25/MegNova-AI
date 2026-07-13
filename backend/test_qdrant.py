from App.ai.vector_store import create_collection, client

create_collection()

print(client.get_collections())