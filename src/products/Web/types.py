import copy
from datetime import datetime

from ariadne import InterfaceType, ObjectType, ScalarType, UnionType
from src.products.Web.data import ingredients, products, suppliers

product_interface = InterfaceType("ProductInterface")
product_type = UnionType("Product")
ingredient_type = ObjectType("Ingredient")
supplier_type = ObjectType("Supplier")


# product型リゾルバ
@product_type.type_resolver
def resolve_porduct_type(obj, *_):  # リゾルバの最初の位置引数をojbとして捕捉
    if "hasFilling" in obj:
        return "Cake"
    return "Beverage"


# ScalarTypeクラスを使ってDatetimeのバインド可能オブジェクトを作成
datetime_scalar = ScalarType("Datetime")


# Datetime型のシリアライザ
@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


# Datetime型のパーサー
@datetime_scalar.value_parser
def parser_datetime(date):  # 日付を引数で受け取る
    return datetime.fromisoformat(date)


@product_interface.field("ingredients")
def resolve_product_ingredients(product, _):
    recipe = [copy.copy(ingredient) for ingredient in product.get("ingredients", [])]
    for ingredient_recipe in recipe:
        for ingredient in ingredients:
            if ingredient["id"] == ingredient_recipe["ingredient"]:
                ingredient_recipe["ingredient"] = ingredient
    return recipe


@ingredient_type.field("supplier")
def resolve_ingredient_suppliers(ingredient, _):
    if ingredient.get("supplier") is not None:
        for supplier in suppliers:
            if supplier["id"] == ingredient["supplier"]:
                return supplier


@ingredient_type.field("products")
def resolve_ingredient_products(ingredient, _):
    return [
        product
        for product in products
        if ingredient["id"] in product.get("ingredients", [])
    ]


@supplier_type.field("ingredients")
def resolve_supplier_ingredients(supplier, _):
    return [
        ingredient
        for ingredient in ingredients
        if supplier["id"] in ingredient.get("suppliers", [])
    ]
