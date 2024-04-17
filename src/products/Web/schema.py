from pathlib import Path

from ariadne import make_executable_schema
from src.products.Web.mutations import mutation
from src.products.Web.queries import query
from src.products.Web.types import (
    datetime_scalar,
    ingredient_type,
    product_interface,
    product_type,
    supplier_type,
)

schema = make_executable_schema(
    (Path(__file__).parent / "products.graphql").read_text(),
    [
        query,
        mutation,
        product_interface,
        product_type,
        ingredient_type,
        supplier_type,
        datetime_scalar,
    ],
)
