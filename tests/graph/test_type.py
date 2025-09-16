from recommender.graph.type import Product

def test_product_pretty():
    # Given
    product = Product(title="Hello", description="Description")

    # When
    result = product.pretty()

    # Then
    assert result == "Product name: Hello, Product description: Description"