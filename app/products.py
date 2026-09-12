"""
Product catalog shown on the Purchase Order screen.

This mirrors the original hard-coded list from PurchaseOrder2.py.
It's kept as a simple in-app constant (matching the original design)
but is also seeded into the PRODUCT table (see db/schema.sql) so that
PRODUCTORDER.pid can be a real foreign key.
"""
from .config import asset_path

PRODUCTS = [
    {
        "pid": "P-01",
        "name": "Cap",
        "desc": "This product is made from at least 50% recycled polyester fiber",
        "price": 100.00,
        "image": asset_path("cap.png"),
    },
    {
        "pid": "P-02",
        "name": "Linen Shoe",
        "desc": "You will wear it again and again, This shoe is remarkable and loyal<br>just like you",
        "price": 1200.00,
        "image": asset_path("linen-shoe.jpg"),
    },
    {
        "pid": "P-03",
        "name": "Hoodie",
        "desc": "Durably stitched surfaces, clean finishes and the perfect amount<br>of shine to make you dazzle",
        "price": 800.00,
        "image": asset_path("hoodie.png"),
    },
]
