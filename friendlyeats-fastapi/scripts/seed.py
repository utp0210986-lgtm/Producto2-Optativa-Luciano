from app.core.firebase import db

PHOTO_1 = "https://images.unsplash.com/photo-1552566626-52f8b828add9"
PHOTO_2 = "https://images.unsplash.com/photo-1513104890138-7c749659a591"

# (name, category, city, price, photoUrl, avgRating, numRatings)
rows = [
    ("La Abuela", "Mexicana", "Puebla", 2, PHOTO_1, 4.5, 20),
    ("Pizza Central", "Pizza", "Puebla", 1, PHOTO_2, 4.0, 12),
    ("Mole del Centro", "Mexicana", "Puebla", 2, None, 4.7, 41),
    ("Tacos El Güero", "Tacos", "Puebla", 1, None, 4.3, 58),
    ("Cemitas Doña Lupe", "Mexicana", "Puebla", 1, None, 4.6, 33),
    ("Sushi Kame", "Japonesa", "Puebla", 3, None, 4.1, 17),
    ("Trattoria Roma", "Italiana", "Cholula", 3, None, 4.4, 25),
    ("Café La Esquina", "Cafetería", "Cholula", 1, None, 4.2, 30),
    ("Marisquería El Puerto", "Mariscos", "Atlixco", 2, None, 3.9, 14),
    ("Parrilla Don Beto", "Carnes", "Atlixco", 3, None, 4.5, 22),
]

for name, category, city, price, photo, rating, num in rows:
    db.collection("restaurants").add({
        "name": name, "category": category, "city": city, "price": price,
        "photoUrl": photo, "avgRating": rating, "numRatings": num,
    })

print(f"Datos semilla creados: {len(rows)} restaurantes")
