from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Sample data
products = [
    {
        "name": "Laptop",
        "varieties": [
            {
                "id": 1, "name": "Dell Inspiron 15", "price": 50000,
                "image_url": "https://source.unsplash.com/400x300/?laptop,Dell",
                "details": {
                    "RAM": "8GB DDR4",
                    "CPU": "Intel Core i5 11th Gen",
                    "GPU": "Intel Iris Xe",
                    "Storage": "512GB SSD",
                    "Display": "15.6\" FHD"
                },
                "discount": 10,
                "occasion": "Diwali"
            },
            {
                "id": 2, "name": "HP Pavilion x360", "price": 62000,
                "image_url": "https://source.unsplash.com/400x300/?laptop,HP",
                "details": {
                    "RAM": "16GB DDR4",
                    "CPU": "Intel Core i7 12th Gen",
                    "GPU": "Intel Iris Xe",
                    "Storage": "1TB SSD",
                    "Display": "14\" FHD Touch"
                },
                "discount": 0
            },
            {
                "id": 3, "name": "Apple MacBook Air", "price": 95000,
                "image_url": "https://source.unsplash.com/400x300/?laptop,Apple",
                "details": {
                    "RAM": "8GB Unified",
                    "CPU": "Apple M1",
                    "GPU": "Integrated 7-core",
                    "Storage": "256GB SSD",
                    "Display": "13.3\" Retina"
                }
            }
        ]
    },
    {
        "name": "Smartphone",
        "varieties": [
            {
                "id": 4, "name": "Samsung Galaxy S23", "price": 70000,
                "image_url": "https://source.unsplash.com/400x300/?smartphone,samsung",
                "details": {
                    "RAM": "8GB",
                    "CPU": "Snapdragon 8 Gen 2",
                    "Storage": "256GB",
                    "Camera": "50MP Triple",
                    "Display": "6.1\" FHD+ AMOLED"
                },
                "discount": 15,
                "occasion": "Republic Day"
            },
            {
                "id": 5, "name": "iPhone 14", "price": 80000,
                "image_url": "https://source.unsplash.com/400x300/?smartphone,iphone",
                "details": {
                    "RAM": "6GB",
                    "CPU": "Apple A15 Bionic",
                    "Storage": "128GB",
                    "Camera": "12MP Dual",
                    "Display": "6.1\" Super Retina XDR"
                }
            },
            {
                "id": 6, "name": "OnePlus 11", "price": 60000,
                "image_url": "https://source.unsplash.com/400x300/?smartphone,oneplus",
                "details": {
                    "RAM": "8GB",
                    "CPU": "Snapdragon 8 Gen 2",
                    "Storage": "128GB",
                    "Camera": "50MP Triple",
                    "Display": "6.7\" QHD+ AMOLED"
                }
            }
        ]
    },
    {
        "name": "Headphones",
        "varieties": [
            {
                "id": 7, "name": "Sony WH-1000XM4", "price": 25000,
                "image_url": "https://source.unsplash.com/400x300/?headphones,sony",
                "details": {
                    "Type": "Over-ear Wireless",
                    "Battery": "30 hours",
                    "Noise Cancellation": "Industry Leading",
                    "Connectivity": "Bluetooth 5.0, NFC",
                    "Color": "Black",
                    "Features": "Quick Charge, Touch Controls"
                },
                "discount": 0
            },
            {
                "id": 8, "name": "Boat Rockerz 450", "price": 1500,
                "image_url": "https://source.unsplash.com/400x300/?headphones,boat",
                "details": {
                    "Type": "Over-ear Wireless",
                    "Battery": "15 hours",
                    "Driver": "50mm",
                    "Connectivity": "Bluetooth 5.0",
                    "Color": "Black/Red",
                    "Features": "Bass Boost, Voice Assistant"
                },
                "discount": 20,
                "occasion": "Music Festival"
            },
            {
                "id": 9, "name": "JBL Tune 510BT", "price": 3500,
                "image_url": "https://source.unsplash.com/400x300/?headphones,jbl",
                "details": {
                    "Type": "Over-ear Wireless",
                    "Battery": "40 hours",
                    "Driver": "32mm",
                    "Connectivity": "Bluetooth 5.0",
                    "Color": "Blue/White/Black",
                    "Features": "JBL Pure Bass, Multi-point Connect"
                },
                "discount": 15,
                "occasion": "Audio Week"
            }
        ]
    },
    {
        "name": "Book",
        "varieties": [
            {
                "id": 10, "name": "Atomic Habits", "price": 500,
                "image_url": "https://source.unsplash.com/400x300/?book,reading",
                "details": {
                    "Author": "James Clear",
                    "Pages": "320 pages",
                    "Language": "English",
                    "Format": "Paperback",
                    "Genre": "Self-Help",
                    "Publisher": "Random House"
                },
                "discount": 0
            },
            {
                "id": 11, "name": "The Alchemist", "price": 400,
                "image_url": "https://source.unsplash.com/400x300/?book,adventure",
                "details": {
                    "Author": "Paulo Coelho",
                    "Pages": "208 pages",
                    "Language": "English",
                    "Format": "Paperback",
                    "Genre": "Fiction/Philosophy",
                    "Publisher": "HarperOne"
                },
                "discount": 10,
                "occasion": "Reading Week"
            },
            {
                "id": 12, "name": "Rich Dad Poor Dad", "price": 450,
                "image_url": "https://source.unsplash.com/400x300/?book,finance",
                "details": {
                    "Author": "Robert Kiyosaki",
                    "Pages": "336 pages",
                    "Language": "English",
                    "Format": "Paperback",
                    "Genre": "Personal Finance",
                    "Publisher": "Warner Books"
                },
                "discount": 15,
                "occasion": "Financial Literacy Month"
            }
        ]
    },
    {
        "name": "Smartwatch",
        "varieties": [
            {
                "id": 13, "name": "Apple Watch SE", "price": 32000,
                "image_url": "https://source.unsplash.com/400x300/?smartwatch,apple",
                "details": {
                    "Display": "40mm/44mm Retina",
                    "Battery": "18 hours",
                    "Connectivity": "GPS + Cellular",
                    "Sensors": "Heart Rate, ECG, Blood Oxygen",
                    "Color": "Space Gray/Silver/Gold",
                    "Features": "Water Resistant, Sleep Tracking"
                },
                "discount": 0
            },
            {
                "id": 14, "name": "Samsung Galaxy Watch 5", "price": 28000,
                "image_url": "https://source.unsplash.com/400x300/?smartwatch,samsung",
                "details": {
                    "Display": "1.4\" AMOLED",
                    "Battery": "50 hours",
                    "Connectivity": "Bluetooth, Wi-Fi",
                    "Sensors": "Heart Rate, SpO2, GPS",
                    "Color": "Black/Silver/Pink Gold",
                    "Features": "Samsung Pay, Bixby Voice"
                },
                "discount": 12,
                "occasion": "Tech Week"
            },
            {
                "id": 15, "name": "Noise ColorFit Pro", "price": 3500,
                "image_url": "https://source.unsplash.com/400x300/?smartwatch,noise",
                "details": {
                    "Display": "1.55\" HD Color",
                    "Battery": "10 days",
                    "Connectivity": "Bluetooth 5.0",
                    "Sensors": "Heart Rate, SpO2",
                    "Color": "Black/Blue/Pink",
                    "Features": "IP68 Water Resistant, 150+ Watch Faces"
                },
                "discount": 18,
                "occasion": "Fitness Month"
            }
        ]
    },
    {
        "name": "Bluetooth Speaker",
        "varieties": [
            {
                "id": 16, "name": "JBL Flip 5", "price": 8000,
                "image_url": "https://source.unsplash.com/400x300/?speaker,jbl",
                "details": {
                    "Power": "20W",
                    "Battery": "12 hours",
                    "Connectivity": "Bluetooth 4.2",
                    "Waterproof": "IPX7",
                    "Color": "Black/Blue/Red/Pink",
                    "Features": "JBL Connect+, Voice Assistant"
                },
                "discount": 0
            },
            {
                "id": 17, "name": "Boat Stone 650", "price": 1800,
                "image_url": "https://source.unsplash.com/400x300/?speaker,boat",
                "details": {
                    "Power": "10W",
                    "Battery": "8 hours",
                    "Connectivity": "Bluetooth 5.0",
                    "Waterproof": "IPX5",
                    "Color": "Black/Blue/Red",
                    "Features": "Bass Boost, TWS Connect"
                },
                "discount": 15,
                "occasion": "Party Season"
            },
            {
                "id": 18, "name": "Sony SRS-XB13", "price": 3500,
                "image_url": "https://source.unsplash.com/400x300/?speaker,sony",
                "details": {
                    "Power": "16W",
                    "Battery": "16 hours",
                    "Connectivity": "Bluetooth 5.0",
                    "Waterproof": "IP67",
                    "Color": "Black/Blue/Pink/Orange",
                    "Features": "Extra Bass, Party Connect"
                },
                "discount": 10,
                "occasion": "Music Week"
            }
        ]
    },
    {
        "name": "Backpack",
        "varieties": [
            {
                "id": 19, "name": "Wildcraft 35L", "price": 1200,
                "image_url": "https://source.unsplash.com/400x300/?backpack,wildcraft",
                "details": {
                    "Capacity": "35L",
                    "Material": "Ripstop Nylon",
                    "Compartments": "Main + 3 Pockets",
                    "Color": "Black/Blue/Green",
                    "Features": "Water Resistant, Laptop Compartment",
                    "Weight": "1.2kg"
                },
                "discount": 0
            },
            {
                "id": 20, "name": "Skybags Brat", "price": 1400,
                "image_url": "https://source.unsplash.com/400x300/?backpack,skybags",
                "details": {
                    "Capacity": "30L",
                    "Material": "Polyester",
                    "Compartments": "Main + 2 Pockets",
                    "Color": "Black/Red/Blue",
                    "Features": "Anti-theft, USB Charging Port",
                    "Weight": "1.0kg"
                },
                "discount": 12,
                "occasion": "Travel Week"
            },
            {
                "id": 21, "name": "American Tourister", "price": 1800,
                "image_url": "https://source.unsplash.com/400x300/?backpack,tourister",
                "details": {
                    "Capacity": "40L",
                    "Material": "Nylon + PVC",
                    "Compartments": "Main + 4 Pockets",
                    "Color": "Black/Navy/Red",
                    "Features": "TSA Lock, Expandable",
                    "Weight": "1.5kg"
                },
                "discount": 8,
                "occasion": "Back to School"
            }
        ]
    },
    {
        "name": "Desk Lamp",
        "varieties": [
            {
                "id": 22, "name": "Philips LED Desk Lamp", "price": 900,
                "image_url": "https://source.unsplash.com/400x300/?lamp,philips",
                "details": {
                    "Power": "5W LED",
                    "Brightness": "400 Lumens",
                    "Color Temperature": "3000K-6500K",
                    "Color": "White/Silver",
                    "Features": "Touch Control, USB Charging Port",
                    "Warranty": "2 years"
                },
                "discount": 0
            },
            {
                "id": 23, "name": "Wipro Garnet", "price": 1100,
                "image_url": "https://source.unsplash.com/400x300/?lamp,wipro",
                "details": {
                    "Power": "8W LED",
                    "Brightness": "600 Lumens",
                    "Color Temperature": "2700K-6500K",
                    "Color": "Black/White",
                    "Features": "Dimmable, Memory Function",
                    "Warranty": "3 years"
                },
                "discount": 10,
                "occasion": "Study Week"
            },
            {
                "id": 24, "name": "Syska Table Lamp", "price": 850,
                "image_url": "https://source.unsplash.com/400x300/?lamp,syska",
                "details": {
                    "Power": "6W LED",
                    "Brightness": "500 Lumens",
                    "Color Temperature": "3000K-6000K",
                    "Color": "Black/Silver",
                    "Features": "3-Level Dimming, Flexible Arm",
                    "Warranty": "1 year"
                },
                "discount": 15,
                "occasion": "Office Setup"
            }
        ]
    },
    {
        "name": "Wireless Mouse",
        "varieties": [
            {
                "id": 25, "name": "Logitech M235", "price": 700,
                "image_url": "https://source.unsplash.com/400x300/?mouse,logitech",
                "details": {
                    "Connectivity": "Wireless 2.4GHz",
                    "Battery": "12 months",
                    "DPI": "1000",
                    "Color": "Black/Red/Blue",
                    "Features": "Ergonomic Design, Silent Click",
                    "Compatibility": "Windows, Mac, Linux"
                },
                "discount": 0
            },
            {
                "id": 26, "name": "HP X200", "price": 650,
                "image_url": "https://source.unsplash.com/400x300/?mouse,hp",
                "details": {
                    "Connectivity": "Wireless 2.4GHz",
                    "Battery": "15 months",
                    "DPI": "1200",
                    "Color": "Black/Silver",
                    "Features": "Plug & Play, Energy Saving",
                    "Compatibility": "Windows, Mac"
                },
                "discount": 8,
                "occasion": "Office Week"
            },
            {
                "id": 27, "name": "Dell WM126", "price": 800,
                "image_url": "https://source.unsplash.com/400x300/?mouse,dell",
                "details": {
                    "Connectivity": "Wireless 2.4GHz",
                    "Battery": "18 months",
                    "DPI": "1000",
                    "Color": "Black/White",
                    "Features": "Nano Receiver, Scroll Wheel",
                    "Compatibility": "Universal"
                },
                "discount": 12,
                "occasion": "Tech Sale"
            }
        ]
    },
    {
        "name": "Water Bottle",
        "varieties": [
            {
                "id": 28, "name": "Milton Thermosteel", "price": 900,
                "image_url": "https://source.unsplash.com/400x300/?bottle,milton",
                "details": {
                    "Capacity": "1L",
                    "Material": "Stainless Steel",
                    "Insulation": "24 hours hot, 12 hours cold",
                    "Color": "Silver/Black/Blue",
                    "Features": "Leak-proof, BPA Free",
                    "Weight": "350g"
                },
                "discount": 0
            },
            {
                "id": 29, "name": "Cello Puro", "price": 400,
                "image_url": "https://source.unsplash.com/400x300/?bottle,cello",
                "details": {
                    "Capacity": "750ml",
                    "Material": "BPA Free Plastic",
                    "Insulation": "Basic",
                    "Color": "Blue/Green/Pink",
                    "Features": "Leak-proof, Lightweight",
                    "Weight": "150g"
                },
                "discount": 15,
                "occasion": "Fitness Week"
            },
            {
                "id": 30, "name": "Borosil Hydra", "price": 650,
                "image_url": "https://source.unsplash.com/400x300/?bottle,borosil",
                "details": {
                    "Capacity": "1L",
                    "Material": "Borosilicate Glass",
                    "Insulation": "Silicone Sleeve",
                    "Color": "Clear/Blue/Green",
                    "Features": "Heat Resistant, Easy Grip",
                    "Weight": "400g"
                },
                "discount": 10,
                "occasion": "Health Month"
            }
        ]
    },
    {
        "name": "Dress (Men)",
        "varieties": [
            {
                "id": 31, "name": "Formal Shirt", "price": 1200,
                "image_url": "https://source.unsplash.com/400x300/?men,shirt",
                "details": {
                    "Material": "100% Cotton",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "White/Blue/Black/Striped",
                    "Fit": "Regular Fit",
                    "Features": "Wrinkle Free, Easy Care",
                    "Occasion": "Office, Formal Events"
                },
                "discount": 0
            },
            {
                "id": 32, "name": "Casual T-Shirt", "price": 600,
                "image_url": "https://source.unsplash.com/400x300/?men,t-shirt",
                "details": {
                    "Material": "Cotton Blend",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/White/Blue/Red/Green",
                    "Fit": "Regular Fit",
                    "Features": "Pre-shrunk, Machine Washable",
                    "Occasion": "Casual, Daily Wear"
                },
                "discount": 20,
                "occasion": "Summer Sale"
            },
            {
                "id": 33, "name": "Jeans", "price": 1500,
                "image_url": "https://source.unsplash.com/400x300/?men,jeans",
                "details": {
                    "Material": "Denim",
                    "Size": "28, 30, 32, 34, 36, 38",
                    "Color": "Blue/Black/Dark Blue",
                    "Fit": "Slim/Regular/Relaxed",
                    "Features": "Stretch Denim, Fade Resistant",
                    "Occasion": "Casual, Party"
                },
                "discount": 15,
                "occasion": "Fashion Week"
            },
            {
                "id": 34, "name": "Kurta", "price": 900,
                "image_url": "https://source.unsplash.com/400x300/?men,kurta",
                "details": {
                    "Material": "Cotton",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "White/Beige/Blue/Maroon",
                    "Fit": "Regular Fit",
                    "Features": "Handcrafted, Traditional Design",
                    "Occasion": "Festival, Traditional Events"
                },
                "discount": 12,
                "occasion": "Festival Season"
            }
        ]
    },
    {
        "name": "Dress (Women)",
        "varieties": [
            {
                "id": 35, "name": "Saree", "price": 2000,
                "image_url": "https://source.unsplash.com/400x300/?women,saree",
                "details": {
                    "Material": "Silk/Cotton/Georgette",
                    "Size": "5.5 meters length",
                    "Color": "Red/Blue/Green/Pink/Maroon",
                    "Design": "Printed/Embroidered/Plain",
                    "Features": "Blouse Piece Included, Ready to Wear",
                    "Occasion": "Wedding, Festival, Party"
                },
                "discount": 0
            },
            {
                "id": 36, "name": "Kurti", "price": 800,
                "image_url": "https://source.unsplash.com/400x300/?women,kurti",
                "details": {
                    "Material": "Cotton/Rayon",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Blue/Green/Pink/Orange/Black",
                    "Length": "Knee Length/Ankle Length",
                    "Features": "Comfortable Fit, Easy Care",
                    "Occasion": "Casual, Office, Festival"
                },
                "discount": 25,
                "occasion": "Festival Collection"
            },
            {
                "id": 37, "name": "Western Dress", "price": 1800,
                "image_url": "https://source.unsplash.com/400x300/?women,dress",
                "details": {
                    "Material": "Polyester/Cotton Blend",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/Red/Blue/Green/White",
                    "Style": "A-line/Fit & Flare/Shift",
                    "Features": "Machine Washable, Wrinkle Free",
                    "Occasion": "Party, Office, Date"
                },
                "discount": 18,
                "occasion": "Party Wear"
            },
            {
                "id": 38, "name": "Leggings", "price": 400,
                "image_url": "https://source.unsplash.com/400x300/?women,leggings",
                "details": {
                    "Material": "Cotton Lycra",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/Navy/Blue/Green/Pink",
                    "Fit": "High Waist, Stretchy",
                    "Features": "Opaque, Comfortable",
                    "Occasion": "Casual, Gym, Daily Wear"
                },
                "discount": 20,
                "occasion": "Activewear Sale"
            }
        ]
    },
    {
        "name": "Shoes",
        "varieties": [
            {
                "id": 46, "name": "Nike Running Shoes", "price": 3500,
                "image_url": "https://source.unsplash.com/400x300/?shoes,nike",
                "details": {
                    "Type": "Running Shoes",
                    "Size": "6, 7, 8, 9, 10, 11, 12",
                    "Color": "Black/White/Blue/Red",
                    "Material": "Mesh Upper, Rubber Sole",
                    "Features": "Air Cushioning, Breathable",
                    "Occasion": "Running, Gym, Casual"
                },
                "discount": 0
            },
            {
                "id": 47, "name": "Adidas Sneakers", "price": 4000,
                "image_url": "https://source.unsplash.com/400x300/?shoes,adidas",
                "details": {
                    "Type": "Casual Sneakers",
                    "Size": "6, 7, 8, 9, 10, 11, 12",
                    "Color": "White/Black/Blue/Green",
                    "Material": "Leather/Synthetic Upper",
                    "Features": "Boost Technology, Comfortable",
                    "Occasion": "Casual, Daily Wear, Sports"
                },
                "discount": 15,
                "occasion": "Sports Week"
            },
            {
                "id": 48, "name": "Bata Formal Shoes", "price": 1800,
                "image_url": "https://source.unsplash.com/400x300/?shoes,formal",
                "details": {
                    "Type": "Formal Leather Shoes",
                    "Size": "6, 7, 8, 9, 10, 11, 12",
                    "Color": "Black/Brown",
                    "Material": "Genuine Leather",
                    "Features": "Polished Finish, Comfortable",
                    "Occasion": "Office, Formal Events, Business"
                },
                "discount": 10,
                "occasion": "Office Wear"
            }
        ]
    },
    {
        "name": "Sunglasses",
        "varieties": [
            {
                "id": 49, "name": "Ray-Ban Aviator", "price": 6500,
                "image_url": "https://source.unsplash.com/400x300/?sunglasses,rayban",
                "details": {
                    "Style": "Aviator",
                    "Lens Color": "Green/Gray/Brown",
                    "Frame Color": "Gold/Silver/Black",
                    "Lens Material": "Glass",
                    "Features": "UV Protection, Polarized",
                    "Occasion": "Fashion, Outdoor, Driving"
                },
                "discount": 0
            },
            {
                "id": 50, "name": "Fastrack Wayfarer", "price": 1200,
                "image_url": "https://source.unsplash.com/400x300/?sunglasses,fastrack",
                "details": {
                    "Style": "Wayfarer",
                    "Lens Color": "Black/Brown/Blue",
                    "Frame Color": "Black/Brown/Tortoise",
                    "Lens Material": "Polycarbonate",
                    "Features": "UV Protection, Lightweight",
                    "Occasion": "Casual, Fashion, Daily Wear"
                },
                "discount": 20,
                "occasion": "Summer Sale"
            },
            {
                "id": 51, "name": "Vincent Chase Round", "price": 900,
                "image_url": "https://source.unsplash.com/400x300/?sunglasses,round",
                "details": {
                    "Style": "Round",
                    "Lens Color": "Black/Brown/Green",
                    "Frame Color": "Black/Brown/Gold",
                    "Lens Material": "CR-39",
                    "Features": "UV Protection, Scratch Resistant",
                    "Occasion": "Fashion, Vintage Style, Casual"
                },
                "discount": 15,
                "occasion": "Fashion Week"
            }
        ]
    },
    {
        "name": "Kitchen Appliances",
        "varieties": [
            {
                "id": 91, "name": "Mixer Grinder 750W", "price": 4500,
                "image_url": "https://source.unsplash.com/400x300/?kitchen,mixer",
                "details": {
                    "Power": "750W",
                    "Jars": "3 Stainless Steel",
                    "Speed": "3 Speed Control",
                    "Features": "Overload Protection"
                },
                "discount": 10,
                "occasion": "Kitchen Upgrade"
            },
            {
                "id": 92, "name": "Electric Kettle 1.5L", "price": 1800,
                "image_url": "https://source.unsplash.com/400x300/?kitchen,kettle",
                "details": {
                    "Capacity": "1.5L",
                    "Material": "Stainless Steel",
                    "Power": "1500W",
                    "Features": "Auto Shut-off, Boil Dry Protection"
                },
                "discount": 0
            },
            {
                "id": 93, "name": "Air Fryer 4.2L", "price": 8500,
                "image_url": "https://source.unsplash.com/400x300/?kitchen,airfryer",
                "details": {
                    "Capacity": "4.2L",
                    "Power": "1500W",
                    "Temperature": "80-200°C",
                    "Features": "Digital Display, Timer"
                },
                "discount": 22,
                "occasion": "Healthy Cooking"
            }
        ]
    },
    {
        "name": "Home Decor",
        "varieties": [
            {
                "id": 94, "name": "LED Strip Lights 5m", "price": 800,
                "image_url": "https://source.unsplash.com/400x300/?decor,led",
                "details": {
                    "Length": "5 meters",
                    "Color": "RGB",
                    "Control": "Remote + App",
                    "Features": "Waterproof, Adhesive"
                },
                "discount": 30,
                "occasion": "Festival Lighting"
            },
            {
                "id": 95, "name": "Wall Clock Modern", "price": 1200,
                "image_url": "https://source.unsplash.com/400x300/?decor,clock",
                "details": {
                    "Size": "30cm",
                    "Material": "Wooden Frame",
                    "Type": "Quartz Movement",
                    "Features": "Silent Operation"
                },
                "discount": 0
            },
            {
                "id": 96, "name": "Artificial Plants Set", "price": 1500,
                "image_url": "https://source.unsplash.com/400x300/?decor,plants",
                "details": {
                    "Quantity": "3 Plants",
                    "Material": "High Quality Plastic",
                    "Height": "30-45cm",
                    "Features": "UV Resistant, Realistic"
                },
                "discount": 18,
                "occasion": "Home Makeover"
            }
        ]
    },
    {
        "name": "Beauty & Personal Care",
        "varieties": [
            {
                "id": 103, "name": "Hair Dryer Professional", "price": 2800,
                "image_url": "https://source.unsplash.com/400x300/?beauty,hairdryer",
                "details": {
                    "Power": "2000W",
                    "Speed": "2 Speed + Cool Shot",
                    "Attachments": "3 Nozzles",
                    "Features": "Ionic Technology, Foldable"
                },
                "discount": 18,
                "occasion": "Beauty Week"
            },
            {
                "id": 104, "name": "Electric Toothbrush", "price": 1500,
                "image_url": "https://source.unsplash.com/400x300/?beauty,toothbrush",
                "details": {
                    "Battery": "30 days",
                    "Modes": "3 Cleaning Modes",
                    "Timer": "2-minute Timer",
                    "Features": "Waterproof, Travel Case"
                },
                "discount": 0
            },
            {
                "id": 105, "name": "Facial Cleansing Brush", "price": 1200,
                "image_url": "https://source.unsplash.com/400x300/?beauty,cleansing",
                "details": {
                    "Brushes": "4 Different Heads",
                    "Speed": "2 Speed Settings",
                    "Battery": "USB Rechargeable",
                    "Features": "Waterproof, Gentle Exfoliation"
                },
                "discount": 22,
                "occasion": "Skincare Month"
            }
        ]
    }
]
users = {}
orders = []

@app.route('/')
def root():
    return redirect(url_for('cover'))

@app.route('/cover')
def cover():
    return render_template('landing.html')

@app.route('/home')
def home():
    query = request.args.get('q', '').lower()
    filtered_products = []
    for product in products:
        filtered_varieties = []
        for v in product['varieties']:
            # Search in product name, variety name, and details
            matches = False
            if not query:
                matches = True
            else:
                # Search in product category name
                if query in product['name'].lower():
                    matches = True
                # Search in variety name
                elif query in v['name'].lower():
                    matches = True
                # Search in product details if they exist
                elif 'details' in v:
                    for detail_key, detail_value in v['details'].items():
                        if query in str(detail_value).lower():
                            matches = True
                            break
                # Search in occasion if it exists
                elif 'occasion' in v and query in v['occasion'].lower():
                    matches = True
            
            if matches:
                filtered_varieties.append(v)
        
        if filtered_varieties:
            filtered_products.append({
                'name': product['name'],
                'varieties': filtered_varieties
            })
    return render_template('home.html', products=filtered_products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.')
        else:
            users[username] = password
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            flash('Login successful.')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out.')
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please log in first.'}), 401
    
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    
    return jsonify({'success': True, 'message': 'Added to cart.'})

def get_variety_by_id(pid):
    for p in products:
        for v in p['varieties']:
            if v['id'] == pid:
                return {"product": p["name"], **v}
    return None

@app.route('/cart')
def view_cart():
    cart_ids = session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        item = get_variety_by_id(pid)
        if item:
            # Calculate discounted price
            original_price = item['price']
            discount_percent = item.get('discount', 0)
            discounted_price = original_price * (1 - discount_percent / 100)
            
            # Add calculated fields to item
            item['original_price'] = original_price
            item['discounted_price'] = discounted_price
            item['discount_amount'] = original_price - discounted_price
            
            cart_items.append(item)
            total += discounted_price
    return render_template('cart.html', cart=cart_items, total=total)

# NOTE: The place_order route is redundant since checkout handles order placement, 
# but is left here for completeness if other parts of your code rely on it.
@app.route('/place_order')
def place_order():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    if not cart:
        flash('Cart is empty.')
        return redirect(url_for('home'))
    orders.append({'user': session['user'], 'items': cart.copy()})
    session['cart'] = []
    flash('Order placed successfully!')
    return redirect(url_for('view_cart'))

# =================================================================================
# FIX APPLIED: Corrected logic for fetching and structuring order data for the template
# =================================================================================
@app.route('/orders')
def my_orders():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_orders = [o for o in orders if o['user'] == session['user']]
    return render_template('orders.html', user_orders=user_orders)

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart_ids = session.get('cart', [])
    cart_items = []
    total = 0
    for pid in cart_ids:
        item = get_variety_by_id(pid)
        if item:
            # Calculate discounted price
            original_price = item['price']
            discount_percent = item.get('discount', 0)
            discounted_price = original_price * (1 - discount_percent / 100)
            
            # Add calculated fields to item
            item['original_price'] = original_price
            item['discounted_price'] = discounted_price
            item['discount_amount'] = original_price - discounted_price
            
            cart_items.append(item)
            total += discounted_price
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        method = request.form.get('method')
        if not name or not address or not method:
            flash('Please fill all checkout details.')
            return render_template('checkout.html', cart=cart_items, total=total)
        # Save order (add name, address, method to order)
        orders.append({
            'id': len(orders) + 1,
            'user': session['user'],
            'order_items': cart_items,  # Save full item details
            'name': name,
            'address': address,
            'method': method,
            'total': total
        })
        session['cart'] = []
        flash('Order placed successfully!')
        return redirect(url_for('my_orders'))
    return render_template('checkout.html', cart=cart_items, total=total)

@app.route('/product/<int:pid>')
def product_detail(pid):
    variety = None
    for product in products:
        for v in product['varieties']:
            if v['id'] == pid:
                variety = v.copy()
                variety['product'] = product['name']
                break
    if not variety:
        flash("Product not found.")
        return redirect(url_for('home'))
    return render_template('product_detail.html', variety=variety)

if __name__ == '__main__':
    app.run(debug=True)