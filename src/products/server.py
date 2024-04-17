from ariadne.asgi import GraphQL
from src.products.Web.schema import schema

server = GraphQL(schema, debug=True)
