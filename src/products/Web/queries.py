from itertools import islice

from ariadne import QueryType
from src.products.Web.data import ingredients, products


def get_page(items, items_per_page, page):
    page = page - 1
    start = items_per_page * page if page > 0 else page
    stop = start + items_per_page
    return list(islice(items, start, stop))


query = QueryType()


@query.field("allIngredients")
def resolve_all_ingredients(*_):
    return ingredients


@query.field("allProducts")
def resolve_all_products(*_):
    return products


@query.field("products")
def resolve_products(*_, input=None):
    filtered = list(products)
    if input is None:
        return filtered
    # 在庫状況に応じて商品を絞り込み
    filtered = [
        product for product in filtered if product["available"] is input["available"]
    ]
    # minPriceで商品を絞り込み
    if input.get("minPrice") is not None:
        filtered = [
            product for product in filtered if product["price"] >= input["minPrice"]
        ]
    # maxPriceで商品を絞り込み
    if input.get("maxPrice") is not None:
        filtered = [
            product for product in filtered if product["price"] <= input["maxPrice"]
        ]
    # ソート
    filtered.sort(
        key=lambda product: product.get(input["sortBy"], 0),
        reverse=input["sort"] == "DESCENDING",
    )
    return get_page(filtered, input["resultsPerPage"], input["page"])
