MOCK_PRODUCTS = [
    # SHOES
    {
        "id": "1",
        "name": "Classic White Sneakers",
        "category": "shoes",
        "brand": "Nike",
        "price": 89.99,
        "attributes": {
            "color": "white",
            "size": ["7", "8", "9", "10", "11"],
            "material": "leather",
            "style": "casual",
            "gender": "unisex"
        },
        "description": "Classic white leather sneakers perfect for everyday wear"
    },
    {
        "id": "2",
        "name": "Running Shoes",
        "category": "shoes", 
        "brand": "Adidas",
        "price": 129.99,
        "attributes": {
            "color": "black",
            "size": ["7", "8", "9", "10", "11", "12"],
            "material": "mesh",
            "style": "athletic",
            "gender": "unisex"
        },
        "description": "High-performance running shoes with responsive cushioning"
    },
    {
        "id": "3",
        "name": "High Heel Pumps",
        "category": "shoes",
        "brand": "Christian Louboutin",
        "price": 695.00,
        "attributes": {
            "color": "red",
            "size": ["6", "7", "8", "9", "10"],
            "material": "patent leather",
            "style": "formal",
            "gender": "women",
            "heel_height": "4 inches"
        },
        "description": "Elegant red patent leather pumps with signature red sole"
    },
    {
        "id": "4",
        "name": "Hiking Boots",
        "category": "shoes",
        "brand": "Timberland",
        "price": 189.99,
        "attributes": {
            "color": "brown",
            "size": ["8", "9", "10", "11", "12", "13"],
            "material": "leather",
            "style": "outdoor",
            "gender": "men",
            "waterproof": True
        },
        "description": "Durable waterproof hiking boots for outdoor adventures"
    },
    {
        "id": "5",
        "name": "Canvas Sneakers",
        "category": "shoes",
        "brand": "Converse",
        "price": 55.00,
        "attributes": {
            "color": "black",
            "size": ["6", "7", "8", "9", "10", "11"],
            "material": "canvas",
            "style": "casual",
            "gender": "unisex"
        },
        "description": "Classic black canvas high-top sneakers"
    },
    {
        "id": "6",
        "name": "Ballet Flats",
        "category": "shoes",
        "brand": "Tory Burch",
        "price": 228.00,
        "attributes": {
            "color": "nude",
            "size": ["6", "7", "8", "9", "10"],
            "material": "leather",
            "style": "casual",
            "gender": "women"
        },
        "description": "Comfortable nude leather ballet flats with logo detail"
    },
    {
        "id": "7",
        "name": "Oxford Dress Shoes",
        "category": "shoes",
        "brand": "Cole Haan",
        "price": 280.00,
        "attributes": {
            "color": "black",
            "size": ["8", "9", "10", "11", "12"],
            "material": "leather",
            "style": "formal",
            "gender": "men"
        },
        "description": "Classic black leather oxford shoes for formal occasions"
    },
    {
        "id": "8",
        "name": "Sandals",
        "category": "shoes",
        "brand": "Birkenstock",
        "price": 135.00,
        "attributes": {
            "color": "brown",
            "size": ["6", "7", "8", "9", "10", "11"],
            "material": "leather",
            "style": "casual",
            "gender": "unisex"
        },
        "description": "Comfortable brown leather sandals with cork footbed"
    },

    # CLOTHING
    {
        "id": "9", 
        "name": "Denim Jacket",
        "category": "clothing",
        "brand": "Levi's",
        "price": 79.99,
        "attributes": {
            "color": "blue",
            "size": ["S", "M", "L", "XL"],
            "material": "denim",
            "style": "casual",
            "gender": "unisex"
        },
        "description": "Classic blue denim jacket with vintage styling"
    },
    {
        "id": "10",
        "name": "Cotton T-Shirt",
        "category": "clothing",
        "brand": "Uniqlo",
        "price": 19.99,
        "attributes": {
            "color": "white",
            "size": ["XS", "S", "M", "L", "XL", "XXL"],
            "material": "cotton",
            "style": "basic",
            "gender": "unisex"
        },
        "description": "Basic cotton t-shirt in classic white"
    },
    {
        "id": "11",
        "name": "Wool Sweater",
        "category": "clothing",
        "brand": "J.Crew",
        "price": 98.00,
        "attributes": {
            "color": "navy",
            "size": ["XS", "S", "M", "L", "XL"],
            "material": "wool",
            "style": "casual",
            "gender": "unisex"
        },
        "description": "Cozy navy wool sweater perfect for fall weather"
    },
    {
        "id": "12",
        "name": "Silk Blouse",
        "category": "clothing",
        "brand": "Equipment",
        "price": 248.00,
        "attributes": {
            "color": "cream",
            "size": ["XS", "S", "M", "L"],
            "material": "silk",
            "style": "formal",
            "gender": "women"
        },
        "description": "Elegant cream silk blouse for professional wear"
    },
    {
        "id": "13",
        "name": "Skinny Jeans",
        "category": "clothing",
        "brand": "7 For All Mankind",
        "price": 189.00,
        "attributes": {
            "color": "dark blue",
            "size": ["24", "25", "26", "27", "28", "29", "30", "31", "32"],
            "material": "denim",
            "style": "casual",
            "gender": "women"
        },
        "description": "Premium dark wash skinny jeans with stretch"
    },
    {
        "id": "14",
        "name": "Hoodie",
        "category": "clothing",
        "brand": "Champion",
        "price": 45.00,
        "attributes": {
            "color": "gray",
            "size": ["S", "M", "L", "XL", "XXL"],
            "material": "cotton blend",
            "style": "casual",
            "gender": "unisex"
        },
        "description": "Comfortable gray cotton blend hoodie"
    },
    {
        "id": "15",
        "name": "Dress Shirt",
        "category": "clothing",
        "brand": "Brooks Brothers",
        "price": 89.50,
        "attributes": {
            "color": "white",
            "size": ["14.5", "15", "15.5", "16", "16.5", "17"],
            "material": "cotton",
            "style": "formal",
            "gender": "men"
        },
        "description": "Classic white cotton dress shirt for business wear"
    },
    {
        "id": "16",
        "name": "Little Black Dress",
        "category": "clothing",
        "brand": "Diane von Furstenberg",
        "price": 368.00,
        "attributes": {
            "color": "black",
            "size": ["0", "2", "4", "6", "8", "10", "12"],
            "material": "jersey",
            "style": "formal",
            "gender": "women"
        },
        "description": "Timeless black jersey wrap dress"
    },
    {
        "id": "17",
        "name": "Chinos",
        "category": "clothing",
        "brand": "Bonobos",
        "price": 88.00,
        "attributes": {
            "color": "khaki",
            "size": ["28", "30", "32", "34", "36", "38"],
            "material": "cotton",
            "style": "casual",
            "gender": "men"
        },
        "description": "Comfortable khaki cotton chinos with tailored fit"
    },
    {
        "id": "18",
        "name": "Cardigan",
        "category": "clothing",
        "brand": "Madewell",
        "price": 78.00,
        "attributes": {
            "color": "beige",
            "size": ["XS", "S", "M", "L", "XL"],
            "material": "cotton",
            "style": "casual",
            "gender": "women"
        },
        "description": "Soft beige cotton cardigan with button closure"
    },

    # ELECTRONICS
    {
        "id": "19",
        "name": "Wireless Headphones",
        "category": "electronics",
        "brand": "Sony",
        "price": 199.99,
        "attributes": {
            "color": "black",
            "connectivity": "bluetooth",
            "battery_life": "30 hours",
            "noise_cancelling": True
        },
        "description": "Premium wireless headphones with noise cancellation"
    },
    {
        "id": "20",
        "name": "Smartphone",
        "category": "electronics",
        "brand": "Apple",
        "price": 999.00,
        "attributes": {
            "color": "space gray",
            "storage": "128GB",
            "screen_size": "6.1 inches",
            "5g_enabled": True
        },
        "description": "Latest iPhone with advanced camera system and 5G connectivity"
    },
    {
        "id": "21",
        "name": "Laptop",
        "category": "electronics",
        "brand": "Dell",
        "price": 1299.00,
        "attributes": {
            "color": "silver",
            "processor": "Intel i7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "screen_size": "15.6 inches"
        },
        "description": "High-performance laptop for work and gaming"
    },
    {
        "id": "22",
        "name": "Tablet",
        "category": "electronics",
        "brand": "Samsung",
        "price": 649.99,
        "attributes": {
            "color": "black",
            "storage": "256GB",
            "screen_size": "11 inches",
            "stylus_included": True
        },
        "description": "Versatile tablet with S Pen for productivity and creativity"
    },
    {
        "id": "23",
        "name": "Smart Watch",
        "category": "electronics",
        "brand": "Apple",
        "price": 399.00,
        "attributes": {
            "color": "silver",
            "band_material": "sport band",
            "gps_enabled": True,
            "water_resistant": True
        },
        "description": "Advanced smartwatch with health monitoring features"
    },
    {
        "id": "24",
        "name": "Bluetooth Speaker",
        "category": "electronics",
        "brand": "JBL",
        "price": 129.95,
        "attributes": {
            "color": "blue",
            "battery_life": "12 hours",
            "waterproof": True,
            "portable": True
        },
        "description": "Portable waterproof Bluetooth speaker with powerful sound"
    },
    {
        "id": "25",
        "name": "Gaming Console",
        "category": "electronics",
        "brand": "Sony",
        "price": 499.99,
        "attributes": {
            "color": "white",
            "storage": "825GB",
            "4k_gaming": True,
            "backwards_compatible": True
        },
        "description": "Next-generation gaming console with 4K gaming capabilities"
    },
    {
        "id": "26",
        "name": "Wireless Earbuds",
        "category": "electronics",
        "brand": "Apple",
        "price": 249.00,
        "attributes": {
            "color": "white",
            "noise_cancelling": True,
            "battery_life": "6 hours",
            "wireless_charging": True
        },
        "description": "Premium wireless earbuds with spatial audio"
    },

    # HOME & KITCHEN
    {
        "id": "27",
        "name": "Coffee Maker",
        "category": "home",
        "brand": "Keurig",
        "price": 89.99,
        "attributes": {
            "color": "black",
            "capacity": "12 cups",
            "programmable": True,
            "auto_shutoff": True
        },
        "description": "Programmable coffee maker with auto-shutoff feature"
    },
    {
        "id": "28",
        "name": "Throw Pillow",
        "category": "home",
        "brand": "West Elm",
        "price": 39.00,
        "attributes": {
            "color": "navy",
            "material": "velvet",
            "size": "20x20 inches",
            "removable_cover": True
        },
        "description": "Luxurious navy velvet throw pillow with removable cover"
    },
    {
        "id": "29",
        "name": "Area Rug",
        "category": "home",
        "brand": "Rugs USA",
        "price": 199.00,
        "attributes": {
            "color": "gray",
            "material": "wool",
            "size": "8x10 feet",
            "pattern": "geometric"
        },
        "description": "Modern gray wool area rug with geometric pattern"
    },
    {
        "id": "30",
        "name": "Table Lamp",
        "category": "home",
        "brand": "CB2",
        "price": 149.00,
        "attributes": {
            "color": "brass",
            "material": "metal",
            "height": "24 inches",
            "bulb_included": False
        },
        "description": "Modern brass table lamp with clean lines"
    },
    {
        "id": "31",
        "name": "Blender",
        "category": "home",
        "brand": "Vitamix",
        "price": 449.95,
        "attributes": {
            "color": "black",
            "capacity": "64 oz",
            "variable_speed": True,
            "dishwasher_safe": True
        },
        "description": "Professional-grade blender for smoothies and food prep"
    },
    {
        "id": "32",
        "name": "Candle",
        "category": "home",
        "brand": "Diptyque",
        "price": 68.00,
        "attributes": {
            "scent": "Baies",
            "burn_time": "60 hours",
            "size": "6.5 oz",
            "natural_wax": True
        },
        "description": "Luxury scented candle with blackcurrant and rose fragrance"
    },

    # BEAUTY & PERSONAL CARE
    {
        "id": "33",
        "name": "Moisturizer",
        "category": "beauty",
        "brand": "Cetaphil",
        "price": 16.99,
        "attributes": {
            "skin_type": "all skin types",
            "spf": False,
            "size": "16 fl oz",
            "fragrance_free": True
        },
        "description": "Gentle daily moisturizer for all skin types"
    },
    {
        "id": "34",
        "name": "Lipstick",
        "category": "beauty",
        "brand": "MAC",
        "price": 19.00,
        "attributes": {
            "color": "Ruby Woo",
            "finish": "matte",
            "long_wearing": True,
            "cruelty_free": True
        },
        "description": "Iconic red matte lipstick with long-wearing formula"
    },
    {
        "id": "35",
        "name": "Shampoo",
        "category": "beauty",
        "brand": "Olaplex",
        "price": 28.00,
        "attributes": {
            "hair_type": "damaged hair",
            "sulfate_free": True,
            "size": "8.5 fl oz",
            "color_safe": True
        },
        "description": "Bond-building shampoo for damaged and chemically treated hair"
    },
    {
        "id": "36",
        "name": "Perfume",
        "category": "beauty",
        "brand": "Chanel",
        "price": 132.00,
        "attributes": {
            "scent_family": "floral",
            "size": "1.7 fl oz",
            "concentration": "eau de parfum",
            "gender": "women"
        },
        "description": "Timeless floral fragrance with notes of jasmine and rose"
    },
    {
        "id": "37",
        "name": "Sunscreen",
        "category": "beauty",
        "brand": "EltaMD",
        "price": 37.00,
        "attributes": {
            "spf": "30",
            "broad_spectrum": True,
            "size": "3 oz",
            "zinc_oxide": True
        },
        "description": "Broad-spectrum sunscreen with zinc oxide protection"
    },

    # SPORTS & OUTDOORS
    {
        "id": "38",
        "name": "Yoga Mat",
        "category": "sports",
        "brand": "Lululemon",
        "price": 88.00,
        "attributes": {
            "color": "purple",
            "material": "natural rubber",
            "thickness": "5mm",
            "non_slip": True
        },
        "description": "Premium yoga mat with superior grip and cushioning"
    },
    {
        "id": "39",
        "name": "Water Bottle",
        "category": "sports",
        "brand": "Hydro Flask",
        "price": 44.95,
        "attributes": {
            "color": "mint",
            "capacity": "32 oz",
            "insulated": True,
            "bpa_free": True
        },
        "description": "Insulated stainless steel water bottle keeps drinks cold for 24 hours"
    },
    {
        "id": "40",
        "name": "Resistance Bands",
        "category": "sports",
        "brand": "Bodylastics",
        "price": 29.95,
        "attributes": {
            "resistance_levels": "5 levels",
            "material": "latex",
            "portable": True,
            "door_anchor_included": True
        },
        "description": "Set of resistance bands for full-body workouts"
    },
    {
        "id": "41",
        "name": "Tennis Racket",
        "category": "sports",
        "brand": "Wilson",
        "price": 199.00,
        "attributes": {
            "weight": "11.2 oz",
            "head_size": "100 sq in",
            "string_pattern": "16x19",
            "grip_size": "4 3/8"
        },
        "description": "Professional tennis racket with power and control"
    },
    {
        "id": "42",
        "name": "Camping Tent",
        "category": "sports",
        "brand": "REI Co-op",
        "price": 299.00,
        "attributes": {
            "capacity": "4 person",
            "seasons": "3 season",
            "waterproof": True,
            "weight": "8 lbs"
        },
        "description": "Spacious 4-person tent for camping adventures"
    },

    # BOOKS
    {
        "id": "43",
        "name": "The Great Gatsby",
        "category": "books",
        "brand": "Scribner",
        "price": 15.99,
        "attributes": {
            "author": "F. Scott Fitzgerald",
            "genre": "classic literature",
            "pages": 180,
            "format": "paperback"
        },
        "description": "Classic American novel about the Jazz Age"
    },
    {
        "id": "44",
        "name": "Atomic Habits",
        "category": "books",
        "brand": "Avery",
        "price": 18.00,
        "attributes": {
            "author": "James Clear",
            "genre": "self-help",
            "pages": 320,
            "format": "hardcover"
        },
        "description": "Practical guide to building good habits and breaking bad ones"
    },
    {
        "id": "45",
        "name": "Dune",
        "category": "books",
        "brand": "Ace",
        "price": 16.99,
        "attributes": {
            "author": "Frank Herbert",
            "genre": "science fiction",
            "pages": 688,
            "format": "paperback"
        },
        "description": "Epic science fiction novel set on the desert planet Arrakis"
    },

    # JEWELRY & ACCESSORIES
    {
        "id": "46",
        "name": "Gold Necklace",
        "category": "jewelry",
        "brand": "Tiffany & Co.",
        "price": 325.00,
        "attributes": {
            "material": "18k gold",
            "length": "16 inches",
            "pendant": "heart",
            "gender": "women"
        },
        "description": "Elegant 18k gold heart pendant necklace"
    },
    {
        "id": "47",
        "name": "Leather Wallet",
        "category": "accessories",
        "brand": "Coach",
        "price": 150.00,
        "attributes": {
            "color": "black",
            "material": "leather",
            "card_slots": 8,
            "gender": "men"
        },
        "description": "Classic black leather bifold wallet with multiple card slots"
    },
    {
        "id": "48",
        "name": "Sunglasses",
        "category": "accessories",
        "brand": "Ray-Ban",
        "price": 154.00,
        "attributes": {
            "color": "black",
            "lens_type": "polarized",
            "frame_material": "acetate",
            "uv_protection": True
        },
        "description": "Classic black aviator sunglasses with polarized lenses"
    },
    {
        "id": "49",
        "name": "Silk Scarf",
        "category": "accessories",
        "brand": "Hermès",
        "price": 395.00,
        "attributes": {
            "color": "multicolor",
            "material": "silk",
            "size": "35x35 inches",
            "pattern": "floral"
        },
        "description": "Luxurious silk scarf with vibrant floral pattern"
    },
    {
        "id": "50",
        "name": "Baseball Cap",
        "category": "accessories",
        "brand": "New Era",
        "price": 34.99,
        "attributes": {
            "color": "navy",
            "material": "cotton",
            "adjustable": True,
            "team": "New York Yankees"
        },
        "description": "Official New York Yankees baseball cap in navy blue"
    }
]
