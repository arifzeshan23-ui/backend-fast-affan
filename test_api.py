"""Quick test script for the API."""
import requests

BASE = "http://localhost:8000"

# Login as admin
r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"})
data = r.json()
token = data["access_token"]
print("Login OK:", data["user"]["username"], "- admin:", data["user"]["is_admin"])

# Create product
headers = {"Authorization": f"Bearer {token}"}
r = requests.post(
    f"{BASE}/api/products/",
    json={
        "name": "Mobile Phone",
        "description": "Latest smartphone",
        "price": 50000,
        "discount_price": 45000,
        "stock": 100,
        "category": "Electronics",
    },
    headers=headers,
)
print("Create Product:", r.status_code, r.json().get("name", "") if r.ok else r.json())

# List products
r = requests.get(f"{BASE}/api/products/")
print("Products:", r.json())

# Register user
r = requests.post(
    f"{BASE}/api/auth/register",
    json={
        "username": "ali",
        "email": "ali@test.com",
        "password": "ali123",
        "full_name": "Ali Khan",
        "phone": "03001112233",
        "address": "Lahore",
    },
)
user_token = r.json()["access_token"]
print("User registered:", r.json()["user"]["username"])

# Add to cart
headers = {"Authorization": f"Bearer {user_token}"}
r = requests.post(f"{BASE}/api/cart/add", json={"product_id": 1, "quantity": 2}, headers=headers)
print("Add to cart:", r.json())

# View cart
r = requests.get(f"{BASE}/api/cart/", headers=headers)
print("Cart items:", len(r.json()["items"]), "- total:", r.json()["total"])

# Add to wishlist
r = requests.post(f"{BASE}/api/wishlist/add", json={"product_id": 1}, headers=headers)
print("Add to wishlist:", r.json())

# Place order
r = requests.post(
    f"{BASE}/api/orders/place",
    json={"payment_method": "cash_on_delivery", "shipping_address": "Lahore", "phone": "03001112233"},
    headers=headers,
)
print("Place order:", r.status_code, r.json().get("order_status", "") if r.ok else r.json())

# Get user orders
r = requests.get(f"{BASE}/api/orders/", headers=headers)
print("My orders:", len(r.json()))

# Admin: update order status
headers_admin = {"Authorization": f"Bearer {token}"}
r = requests.put(
    f"{BASE}/api/admin/orders/1/status",
    json={"order_status": "confirmed"},
    headers=headers_admin,
)
print("Admin confirm order:", r.json())

# Admin: deliver order
r = requests.put(
    f"{BASE}/api/admin/orders/1/status",
    json={"order_status": "delivered"},
    headers=headers_admin,
)
print("Admin deliver order:", r.json())

print("\nALL API TESTS PASSED!")
