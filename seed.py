"""Seed script to create admin user and sample products."""
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.product import Product
from app.auth.jwt import hash_password

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

PRODUCTS = [
    # School Uniform
    {
        "name": "Boys School White Shirt",
        "description": "Classic white school uniform shirt for boys. Premium cotton fabric, easy to iron.",
        "price": 999,
        "discount_price": 799,
        "stock": 100,
        "category": "School Uniform",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    {
        "name": "Girls School Pinafore Dress",
        "description": "Navy blue pinafore school dress for girls. Durable fabric with adjustable straps.",
        "price": 1299,
        "discount_price": 999,
        "stock": 80,
        "category": "School Uniform",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    {
        "name": "School Track Suit",
        "description": "Comfortable school track suit in maroon color. Includes jacket and pants.",
        "price": 1999,
        "discount_price": 1599,
        "stock": 60,
        "category": "School Uniform",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    # Kids Suit
    {
        "name": "Boys Formal Suit Set",
        "description": "Elegant formal suit for boys. Includes blazer, shirt and trousers.",
        "price": 3499,
        "discount_price": 2999,
        "stock": 40,
        "category": "Kids Suit",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    {
        "name": "Girls Party Frock",
        "description": "Beautiful party frock for girls with sequin details. Fluffy tulle skirt.",
        "price": 2999,
        "discount_price": 2499,
        "stock": 35,
        "category": "Kids Suit",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Traditional Kurta Pajama",
        "description": "Traditional kurta pajama set for kids. Cotton fabric with embroidery work.",
        "price": 1999,
        "discount_price": 1599,
        "stock": 50,
        "category": "Kids Suit",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    # Summer Cloth
    {
        "name": "Men's Linen Shalwar Kameez",
        "description": "Comfortable linen shalwar kameez for men. Perfect for summer.",
        "price": 2999,
        "discount_price": 2499,
        "stock": 55,
        "category": "Summer Cloth",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Cotton Maxi Dress",
        "description": "Flowy cotton maxi dress for summer. Floral prints with comfortable fit.",
        "price": 2799,
        "discount_price": 2299,
        "stock": 45,
        "category": "Summer Cloth",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Cotton Shorts Set",
        "description": "Comfortable cotton shorts and t-shirt set for kids. Breathable summer wear.",
        "price": 1299,
        "discount_price": 999,
        "stock": 70,
        "category": "Summer Cloth",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    # Winter Cloth
    {
        "name": "Woolen Sweater Men",
        "description": "Warm woolen sweater for men. Premium quality wool with comfortable fit.",
        "price": 3499,
        "discount_price": 2999,
        "stock": 40,
        "category": "Winter Cloth",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cda3a0d?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Velvet Kurti",
        "description": "Elegant velvet kurti for women. Warm and stylish with embroidery work.",
        "price": 3999,
        "discount_price": 3499,
        "stock": 35,
        "category": "Winter Cloth",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cda3a0d?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Hoodie Set",
        "description": "Cozy hoodie set for kids. Soft fleece material with warm lining.",
        "price": 1999,
        "discount_price": 1599,
        "stock": 60,
        "category": "Winter Cloth",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500&h=500&fit=crop",
    },
    # Shoes
    {
        "name": "Men's Peshawari Chappal",
        "description": "Classic Peshawari chappal in pure leather. Handcrafted with traditional design.",
        "price": 1999,
        "discount_price": 1599,
        "stock": 70,
        "category": "Shoes",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
    },
    {
        "name": "Men's Formal Oxford Shoes",
        "description": "Premium leather Oxford shoes for men. Classic formal design.",
        "price": 4999,
        "discount_price": 3999,
        "stock": 35,
        "category": "Shoes",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Embroidered Khussa",
        "description": "Traditional hand-embroidered khussa for women. Genuine leather with mirror work.",
        "price": 1499,
        "discount_price": 1199,
        "stock": 80,
        "category": "Shoes",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Block Heel Sandals",
        "description": "Stylish block heel sandals for women. Comfortable for all-day wear.",
        "price": 2499,
        "discount_price": 1999,
        "stock": 50,
        "category": "Shoes",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Velcro Sneakers",
        "description": "Easy-to-wear velcro sneakers for kids. Cushioned sole for comfort.",
        "price": 1299,
        "discount_price": 999,
        "stock": 90,
        "category": "Shoes",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Cartoon Sandals",
        "description": "Fun cartoon print sandals for kids. Soft rubber sole. Anti-slip design.",
        "price": 799,
        "discount_price": 599,
        "stock": 100,
        "category": "Shoes",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
    },
    # Marriage Suit
    {
        "name": "Bridal Red Lehenga Choli",
        "description": "Stunning red bridal lehenga with heavy embroidery and mirror work.",
        "price": 29999,
        "discount_price": 24999,
        "stock": 10,
        "category": "Marriage Suit",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500&h=500&fit=crop",
    },
    {
        "name": "Walima Reception Dress",
        "description": "Elegant gold and maroon reception dress. Heavy formal suit with zardozi work.",
        "price": 19999,
        "discount_price": 16999,
        "stock": 15,
        "category": "Marriage Suit",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500&h=500&fit=crop",
    },
    {
        "name": "Mehndi Outfit Green",
        "description": "Beautiful green mehndi dress with colorful embroidery.",
        "price": 14999,
        "discount_price": 12999,
        "stock": 20,
        "category": "Marriage Suit",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=500&h=500&fit=crop",
    },
    # Jacket
    {
        "name": "Men's Leather Jacket",
        "description": "Classic black leather jacket for men. Genuine leather with satin lining.",
        "price": 8999,
        "discount_price": 7499,
        "stock": 25,
        "category": "Jacket",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Denim Jacket",
        "description": "Stylish denim jacket for women. Vintage wash with button closure.",
        "price": 3999,
        "discount_price": 3499,
        "stock": 40,
        "category": "Jacket",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Winter Puffer Jacket",
        "description": "Warm puffer jacket for kids. Water-resistant with hood.",
        "price": 2999,
        "discount_price": 2499,
        "stock": 50,
        "category": "Jacket",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&h=500&fit=crop",
    },
    # Suit
    {
        "name": "Men's Classic Two-Piece Suit",
        "description": "Professional two-piece suit in navy blue. Includes blazer and trousers.",
        "price": 9999,
        "discount_price": 7999,
        "stock": 30,
        "category": "Suit",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop",
    },
    {
        "name": "Men's Three-Piece Formal Suit",
        "description": "Premium three-piece suit with waistcoat. Charcoal grey color.",
        "price": 14999,
        "discount_price": 12999,
        "stock": 20,
        "category": "Suit",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Corporate Blazer Set",
        "description": "Professional blazer and trouser set for women. Tailored fit.",
        "price": 7999,
        "discount_price": 6499,
        "stock": 25,
        "category": "Suit",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&h=500&fit=crop",
    },
    # Slipper
    {
        "name": "Men's Casual Flip Flops",
        "description": "Comfortable rubber flip flops for men. Arch support with non-slip sole.",
        "price": 599,
        "discount_price": 449,
        "stock": 150,
        "category": "Slipper",
        "gender": "Male",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&h=500&fit=crop",
    },
    {
        "name": "Women's Fancy Slippers",
        "description": "Stylish flat slippers for women with embellishments.",
        "price": 899,
        "discount_price": 699,
        "stock": 120,
        "category": "Slipper",
        "gender": "Female",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&h=500&fit=crop",
    },
    {
        "name": "Kids Soft Sole Slippers",
        "description": "Soft foam slippers for kids. Cartoon characters with anti-slip sole.",
        "price": 499,
        "discount_price": 399,
        "stock": 200,
        "category": "Slipper",
        "gender": "Kids",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop",
    },
]


def seed():
    db = SessionLocal()
    try:
        # Create admin
        admin = User(
            username="admin",
            email="admin@muga.com",
            hashed_password=hash_password("admin123"),
            full_name="Admin",
            phone="03001234567",
            address="Muga Office",
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        print("Admin created: username=admin, password=admin123")

        # Create products
        for p in PRODUCTS:
            product = Product(**p)
            db.add(product)
        db.commit()
        print(f"{len(PRODUCTS)} products added successfully!")

        # Set some products as featured
        featured_names = [
            "Bridal Red Lehenga Choli",
            "Men's Classic Two-Piece Suit",
            "Women's Embroidered Khussa",
            "Cotton Lawn Printed Suit",
        ]
        for name in featured_names:
            p = db.query(Product).filter(Product.name == name).first()
            if p:
                p.is_featured = True

        # Set some products as new arrivals
        new_arrival_names = [
            "Men's Leather Jacket",
            "Girls Party Frock",
            "Kids Velcro Sneakers",
            "Women's Corporate Blazer Set",
            "Men's Peshawari Chappal",
        ]
        for name in new_arrival_names:
            p = db.query(Product).filter(Product.name == name).first()
            if p:
                p.is_new_arrival = True

        db.commit()
        print(f"Set {len(featured_names)} products as featured, {len(new_arrival_names)} as new arrivals")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
