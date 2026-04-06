import random

brands = ["ASUS", "Gigabyte", "MSI", "Corsair", "Kingston", "Intel", "AMD", "NVIDIA", "Samsung", "EVGA", "Logitech", "Razer"]

categories_config = [
    ("GPU", 1800, 12000),
    ("CPU", 600, 5000),
    ("RAM", 150, 1500),
    ("SSD M.2", 200, 2500),
    ("Motherboard", 500, 4000),
    ("Power Supply", 300, 1800),
    ("Water Cooler", 250, 1200)
]

inventory_initial = []

for i in range(5000):
    category_name, p_min, p_max = random.choice(categories_config)
    brand = random.choice(brands)
    model_suffix = f"v{random.randint(10, 99)}-{i}"
    full_name = f"{brand} {category_name} {model_suffix}"
    price = round(random.uniform(p_min, p_max), 2)
    
    inventory_initial.append({
        "nome": full_name,
        "categoria": category_name,
        "preco": price
    })