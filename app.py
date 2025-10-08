from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Sample data
products = [
    {
        "name": "Laptop",
        "varieties": [
            {
                "id": 1, "name": "Dell Inspiron 15", "price": 50000,
                "details": {
                    "RAM": "8GB DDR4",
                    "CPU": "Intel Core i5 11th Gen",
                    "GPU": "Intel Iris Xe",
                    "Storage": "512GB SSD",
                    "Display": "15.6\" FHD"
                },
                "discount": 10,  # 10% off
                "occasion": "Diwali"
            },
            {
                "id": 2, "name": "HP Pavilion x360", "price": 62000,
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
        "name": "Dress (Kids)",
        "varieties": [
            {
                "id": 39, "name": "Frock", "price": 700,
                "details": {
                    "Material": "Cotton",
                    "Size": "2-3Y, 3-4Y, 4-5Y, 5-6Y, 6-7Y",
                    "Color": "Pink/Blue/Red/Green/Yellow",
                    "Style": "Princess Cut, A-line",
                    "Features": "Comfortable, Easy to Wear",
                    "Occasion": "Party, Festival, Daily Wear"
                },
                "discount": 0
            },
            {
                "id": 40, "name": "Dungaree", "price": 900,
                "details": {
                    "Material": "Denim/Cotton",
                    "Size": "2-3Y, 3-4Y, 4-5Y, 5-6Y, 6-7Y",
                    "Color": "Blue/Black/Pink/Green",
                    "Style": "Overall Style",
                    "Features": "Adjustable Straps, Durable",
                    "Occasion": "Casual, Play, School"
                },
                "discount": 15,
                "occasion": "Kids Fashion Week"
            },
            {
                "id": 41, "name": "Kids T-Shirt", "price": 350,
                "details": {
                    "Material": "Cotton Blend",
                    "Size": "2-3Y, 3-4Y, 4-5Y, 5-6Y, 6-7Y",
                    "Color": "Blue/Red/Green/Yellow/Orange",
                    "Design": "Cartoon Prints, Solid Colors",
                    "Features": "Soft Fabric, Easy Care",
                    "Occasion": "Casual, Play, Daily Wear"
                },
                "discount": 20,
                "occasion": "Back to School"
            },
            {
                "id": 42, "name": "Shorts", "price": 400,
                "details": {
                    "Material": "Cotton",
                    "Size": "2-3Y, 3-4Y, 4-5Y, 5-6Y, 6-7Y",
                    "Color": "Blue/Black/Green/Red",
                    "Length": "Knee Length",
                    "Features": "Elastic Waist, Comfortable",
                    "Occasion": "Casual, Play, Summer Wear"
                },
                "discount": 18,
                "occasion": "Summer Collection"
            }
        ]
    },
    {
        "name": "Dress (Unisex)",
        "varieties": [
            {
                "id": 43, "name": "Hoodie", "price": 1200,
                "details": {
                    "Material": "Cotton Blend",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/Gray/Blue/Red/Green",
                    "Style": "Pullover with Hood",
                    "Features": "Kangaroo Pocket, Drawstring Hood",
                    "Occasion": "Casual, Gym, Winter Wear"
                },
                "discount": 0
            },
            {
                "id": 44, "name": "Track Pants", "price": 900,
                "details": {
                    "Material": "Polyester/Cotton",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/Gray/Blue/Red",
                    "Style": "Jogger Style",
                    "Features": "Elastic Waist, Side Pockets",
                    "Occasion": "Gym, Casual, Sports"
                },
                "discount": 15,
                "occasion": "Fitness Week"
            },
            {
                "id": 45, "name": "Raincoat", "price": 1100,
                "details": {
                    "Material": "PVC Waterproof",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Yellow/Blue/Red/Green",
                    "Style": "Full Length",
                    "Features": "Lightweight, Packable",
                    "Occasion": "Rainy Season, Outdoor"
                },
                "discount": 12,
                "occasion": "Monsoon Special"
            }
        ]
    },
    {
        "name": "Shoes",
        "varieties": [
            {
                "id": 46, "name": "Nike Running Shoes", "price": 3500,
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
        "name": "Cycle",
        "varieties": [
            {
                "id": 52, "name": "Hero Sprint Next 26T", "price": 8500,
                "details": {
                    "Type": "Mountain Bike",
                    "Wheel Size": "26 inches",
                    "Gears": "21 Speed",
                    "Color": "Red/Blue/Black/Green",
                    "Frame": "Steel Frame",
                    "Features": "Front Suspension, Disc Brakes"
                },
                "discount": 0
            },
            {
                "id": 53, "name": "Firefox Bad Attitude 8", "price": 12000,
                "details": {
                    "Type": "Mountain Bike",
                    "Wheel Size": "26 inches",
                    "Gears": "24 Speed",
                    "Color": "Black/Red/Blue",
                    "Frame": "Aluminum Frame",
                    "Features": "Dual Suspension, Hydraulic Brakes"
                },
                "discount": 12,
                "occasion": "Adventure Week"
            },
            {
                "id": 54, "name": "Btwin Rockrider ST 100", "price": 15000,
                "details": {
                    "Type": "Mountain Bike",
                    "Wheel Size": "27.5 inches",
                    "Gears": "21 Speed",
                    "Color": "Black/Red/Blue",
                    "Frame": "Aluminum Frame",
                    "Features": "Front Suspension, V-Brakes"
                },
                "discount": 8,
                "occasion": "Cycling Festival"
            }
        ]
    },
    {
        "name": "Bike",
        "varieties": [
            {
                "id": 55, "name": "Royal Enfield Classic 350", "price": 210000,
                "details": {
                    "Engine": "349cc Single Cylinder",
                    "Power": "20.2 bhp",
                    "Mileage": "35 kmpl",
                    "Color": "Black/Red/Blue/Green",
                    "Transmission": "5 Speed Manual",
                    "Features": "Electric Start, Disc Brakes"
                },
                "discount": 0
            },
            {
                "id": 56, "name": "Bajaj Pulsar 150", "price": 120000,
                "details": {
                    "Engine": "149.5cc Single Cylinder",
                    "Power": "14 bhp",
                    "Mileage": "45 kmpl",
                    "Color": "Black/Red/Blue/White",
                    "Transmission": "5 Speed Manual",
                    "Features": "Digital Console, LED Headlight"
                },
                "discount": 8,
                "occasion": "Bike Festival"
            },
            {
                "id": 57, "name": "Yamaha FZ-S V3", "price": 130000,
                "details": {
                    "Engine": "149cc Single Cylinder",
                    "Power": "12.4 bhp",
                    "Mileage": "50 kmpl",
                    "Color": "Black/Blue/Red/White",
                    "Transmission": "5 Speed Manual",
                    "Features": "LED Headlight, Digital Display"
                },
                "discount": 10,
                "occasion": "Sports Bike Week"
            }
        ]
    },
    {
        "name": "Car",
        "varieties": [
            {
                "id": 58, "name": "Maruti Suzuki Swift", "price": 600000,
                "details": {
                    "Engine": "1.2L Petrol",
                    "Power": "82 bhp",
                    "Mileage": "23.2 kmpl",
                    "Color": "White/Red/Blue/Black/Silver",
                    "Transmission": "5 Speed Manual",
                    "Features": "Airbags, ABS, Power Steering"
                },
                "discount": 0
            },
            {
                "id": 59, "name": "Hyundai Creta", "price": 1100000,
                "details": {
                    "Engine": "1.5L Diesel",
                    "Power": "113 bhp",
                    "Mileage": "21.4 kmpl",
                    "Color": "White/Black/Blue/Red/Silver",
                    "Transmission": "6 Speed Manual",
                    "Features": "Sunroof, Touchscreen, Cruise Control"
                },
                "discount": 5,
                "occasion": "Auto Expo"
            },
            {
                "id": 60, "name": "Tata Nexon", "price": 900000,
                "details": {
                    "Engine": "1.2L Turbo Petrol",
                    "Power": "118 bhp",
                    "Mileage": "17.4 kmpl",
                    "Color": "White/Black/Blue/Orange/Silver",
                    "Transmission": "6 Speed Manual",
                    "Features": "Touchscreen, Climate Control, Safety"
                },
                "discount": 8,
                "occasion": "Car Festival"
            }
        ]
    },
    {
        "name": "Tablet",
        "varieties": [
            {
                "id": 61, "name": "Apple iPad 9th Gen", "price": 32000,
                "details": {
                    "Display": "10.2\" Retina Display",
                    "Storage": "64GB/256GB",
                    "Processor": "A13 Bionic Chip",
                    "Color": "Space Gray/Silver",
                    "Battery": "10 hours",
                    "Features": "Touch ID, Apple Pencil Support"
                },
                "discount": 0
            },
            {
                "id": 62, "name": "Samsung Galaxy Tab A8", "price": 18000,
                "details": {
                    "Display": "10.5\" TFT Display",
                    "Storage": "32GB/64GB",
                    "Processor": "Unisoc T618",
                    "Color": "Gray/Silver/Gold",
                    "Battery": "7040mAh",
                    "Features": "Dolby Atmos, Kids Mode"
                },
                "discount": 12,
                "occasion": "Tech Week"
            },
            {
                "id": 63, "name": "Lenovo Tab M10", "price": 15000,
                "details": {
                    "Display": "10.1\" HD Display",
                    "Storage": "32GB/64GB",
                    "Processor": "MediaTek Helio P22T",
                    "Color": "Iron Gray/Platinum Gray",
                    "Battery": "5000mAh",
                    "Features": "Kids Mode, Eye Care"
                },
                "discount": 15,
                "occasion": "Education Week"
            }
        ]
    },
    {
        "name": "Camera",
        "varieties": [
            {
                "id": 64, "name": "Canon EOS 1500D", "price": 35000,
                "details": {
                    "Sensor": "24.1MP APS-C",
                    "Lens": "18-55mm Kit Lens",
                    "Video": "Full HD 1080p",
                    "Color": "Black",
                    "Display": "3\" LCD Screen",
                    "Features": "Wi-Fi, NFC, Auto Focus"
                },
                "discount": 0
            },
            {
                "id": 65, "name": "Nikon D3500", "price": 40000,
                "details": {
                    "Sensor": "24.2MP APS-C",
                    "Lens": "18-55mm Kit Lens",
                    "Video": "Full HD 1080p",
                    "Color": "Black",
                    "Display": "3\" LCD Screen",
                    "Features": "Bluetooth, Guide Mode"
                },
                "discount": 8,
                "occasion": "Photography Month"
            },
            {
                "id": 66, "name": "Sony Alpha ILCE-6100", "price": 65000,
                "details": {
                    "Sensor": "24.2MP APS-C",
                    "Lens": "16-50mm Kit Lens",
                    "Video": "4K Recording",
                    "Color": "Black/Silver",
                    "Display": "3\" Touchscreen",
                    "Features": "Real-time Eye AF, Wi-Fi"
                },
                "discount": 12,
                "occasion": "Camera Festival"
            }
        ]
    },
    {
        "name": "Gaming Console",
        "varieties": [
            {
                "id": 67, "name": "Sony PlayStation 5", "price": 49990,
                "details": {
                    "Storage": "825GB SSD",
                    "Resolution": "4K Gaming",
                    "Controller": "DualSense Wireless",
                    "Color": "White",
                    "Features": "3D Audio, Ray Tracing",
                    "Games": "Backward Compatible"
                },
                "discount": 0
            },
            {
                "id": 68, "name": "Microsoft Xbox Series S", "price": 34990,
                "details": {
                    "Storage": "512GB SSD",
                    "Resolution": "1440p Gaming",
                    "Controller": "Xbox Wireless Controller",
                    "Color": "White",
                    "Features": "Quick Resume, Game Pass",
                    "Games": "Backward Compatible"
                },
                "discount": 10,
                "occasion": "Gaming Festival"
            },
            {
                "id": 69, "name": "Nintendo Switch", "price": 29990,
                "details": {
                    "Storage": "32GB",
                    "Display": "6.2\" Touchscreen",
                    "Controller": "Joy-Con Controllers",
                    "Color": "Neon Blue/Red",
                    "Features": "Portable Gaming, Local Multiplayer",
                    "Games": "Nintendo Exclusives"
                },
                "discount": 15,
                "occasion": "Family Gaming Week"
            }
        ]
    },
    {
        "name": "Television",
        "varieties": [
            {
                "id": 70, "name": "Samsung 43\" 4K UHD", "price": 35000,
                "details": {
                    "Size": "43 inches",
                    "Resolution": "4K UHD (3840x2160)",
                    "Display": "LED",
                    "Color": "Black",
                    "Features": "Smart TV, HDR, Voice Control",
                    "Connectivity": "Wi-Fi, Bluetooth, 3 HDMI"
                },
                "discount": 0
            },
            {
                "id": 71, "name": "Sony Bravia 50\" 4K", "price": 55000,
                "details": {
                    "Size": "50 inches",
                    "Resolution": "4K UHD (3840x2160)",
                    "Display": "LED",
                    "Color": "Black",
                    "Features": "Android TV, Dolby Vision, X1 Processor",
                    "Connectivity": "Wi-Fi, Bluetooth, 4 HDMI"
                },
                "discount": 8,
                "occasion": "Entertainment Week"
            },
            {
                "id": 72, "name": "Mi 40\" Full HD", "price": 25000,
                "details": {
                    "Size": "40 inches",
                    "Resolution": "Full HD (1920x1080)",
                    "Display": "LED",
                    "Color": "Black",
                    "Features": "Android TV, PatchWall, Voice Remote",
                    "Connectivity": "Wi-Fi, Bluetooth, 3 HDMI"
                },
                "discount": 12,
                "occasion": "Tech Sale"
            }
        ]
    },
    {
        "name": "Refrigerator",
        "varieties": [
            {
                "id": 73, "name": "LG 260L Double Door", "price": 27000,
                "details": {
                    "Capacity": "260L",
                    "Type": "Double Door",
                    "Energy Rating": "3 Star",
                    "Color": "Silver/Black",
                    "Features": "Smart Inverter, Door Cooling",
                    "Compartments": "Freezer + Refrigerator"
                },
                "discount": 0
            },
            {
                "id": 74, "name": "Samsung 253L 3 Star", "price": 24000,
                "details": {
                    "Capacity": "253L",
                    "Type": "Double Door",
                    "Energy Rating": "3 Star",
                    "Color": "Silver/Black",
                    "Features": "Digital Inverter, All-around Cooling",
                    "Compartments": "Freezer + Refrigerator"
                },
                "discount": 10,
                "occasion": "Home Appliance Week"
            },
            {
                "id": 75, "name": "Whirlpool 190L Single Door", "price": 16000,
                "details": {
                    "Capacity": "190L",
                    "Type": "Single Door",
                    "Energy Rating": "2 Star",
                    "Color": "Silver/White",
                    "Features": "IntelliSense, Microblock Technology",
                    "Compartments": "Refrigerator with Small Freezer"
                },
                "discount": 15,
                "occasion": "Kitchen Upgrade"
            }
        ]
    },
    {
        "name": "Washing Machine",
        "varieties": [
            {
                "id": 76, "name": "Bosch 7kg Front Load", "price": 32000,
                "details": {
                    "Capacity": "7kg",
                    "Type": "Front Load",
                    "Energy Rating": "5 Star",
                    "Color": "White/Silver",
                    "Features": "VarioDrum, EcoSilence Drive",
                    "Programs": "15 Wash Programs"
                },
                "discount": 0
            },
            {
                "id": 77, "name": "LG 6.5kg Top Load", "price": 21000,
                "details": {
                    "Capacity": "6.5kg",
                    "Type": "Top Load",
                    "Energy Rating": "3 Star",
                    "Color": "White/Silver",
                    "Features": "Smart Inverter, Turbo Drum",
                    "Programs": "12 Wash Programs"
                },
                "discount": 12,
                "occasion": "Laundry Week"
            },
            {
                "id": 78, "name": "Samsung 7kg Top Load", "price": 22000,
                "details": {
                    "Capacity": "7kg",
                    "Type": "Top Load",
                    "Energy Rating": "4 Star",
                    "Color": "White/Silver",
                    "Features": "Digital Inverter, Magic Filter",
                    "Programs": "10 Wash Programs"
                },
                "discount": 8,
                "occasion": "Home Appliance Sale"
            }
        ]
    },
    {
        "name": "Microwave Oven",
        "varieties": [
            {
                "id": 79, "name": "IFB 20L Convection", "price": 9500,
                "details": {
                    "Capacity": "20L",
                    "Type": "Convection",
                    "Power": "1000W",
                    "Features": "Auto Cook, Grill, Defrost"
                },
                "discount": 12,
                "occasion": "New Year"
            },
            {
                "id": 80, "name": "Samsung 23L Solo", "price": 8000,
                "details": {
                    "Capacity": "23L",
                    "Type": "Solo",
                    "Power": "800W",
                    "Features": "Quick Start, Child Lock"
                },
                "discount": 0
            },
            {
                "id": 81, "name": "LG 28L Convection", "price": 14000,
                "details": {
                    "Capacity": "28L",
                    "Type": "Convection",
                    "Power": "1200W",
                    "Features": "Smart Inverter, Auto Cook"
                },
                "discount": 8,
                "occasion": "Festival Sale"
            }
        ]
    },
    {
        "name": "Air Conditioner",
        "varieties": [
            {
                "id": 82, "name": "LG 1.5 Ton 3 Star", "price": 35000,
                "details": {
                    "Capacity": "1.5 Ton",
                    "Energy Rating": "3 Star",
                    "Type": "Split AC",
                    "Features": "Smart Inverter, Wi-Fi Control"
                },
                "discount": 15,
                "occasion": "Summer Sale"
            },
            {
                "id": 83, "name": "Samsung 1 Ton 5 Star", "price": 32000,
                "details": {
                    "Capacity": "1 Ton",
                    "Energy Rating": "5 Star",
                    "Type": "Split AC",
                    "Features": "Digital Inverter, Auto Clean"
                },
                "discount": 10,
                "occasion": "Monsoon Special"
            },
            {
                "id": 84, "name": "Voltas 2 Ton 4 Star", "price": 45000,
                "details": {
                    "Capacity": "2 Ton",
                    "Energy Rating": "4 Star",
                    "Type": "Split AC",
                    "Features": "Turbo Cool, Sleep Mode"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Gaming Laptop",
        "varieties": [
            {
                "id": 85, "name": "ASUS ROG Strix G15", "price": 85000,
                "details": {
                    "RAM": "16GB DDR4",
                    "CPU": "AMD Ryzen 7 5800H",
                    "GPU": "NVIDIA RTX 3060",
                    "Storage": "512GB SSD",
                    "Display": "15.6\" FHD 144Hz"
                },
                "discount": 18,
                "occasion": "Gaming Festival"
            },
            {
                "id": 86, "name": "MSI GF63 Thin", "price": 65000,
                "details": {
                    "RAM": "8GB DDR4",
                    "CPU": "Intel Core i5 10th Gen",
                    "GPU": "NVIDIA GTX 1650",
                    "Storage": "256GB SSD",
                    "Display": "15.6\" FHD"
                },
                "discount": 12,
                "occasion": "Back to School"
            },
            {
                "id": 87, "name": "HP Omen 15", "price": 95000,
                "details": {
                    "RAM": "16GB DDR4",
                    "CPU": "Intel Core i7 11th Gen",
                    "GPU": "NVIDIA RTX 3070",
                    "Storage": "1TB SSD",
                    "Display": "15.6\" FHD 165Hz"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Fitness Equipment",
        "varieties": [
            {
                "id": 88, "name": "Treadmill Pro Max", "price": 25000,
                "details": {
                    "Motor": "2.5HP",
                    "Speed": "1-12 km/h",
                    "Display": "7\" Touch Screen",
                    "Features": "Bluetooth, Heart Rate Monitor"
                },
                "discount": 20,
                "occasion": "New Year Fitness"
            },
            {
                "id": 89, "name": "Dumbbell Set 20kg", "price": 3500,
                "details": {
                    "Weight": "20kg Total",
                    "Material": "Cast Iron",
                    "Type": "Adjustable",
                    "Features": "Non-slip Grip"
                },
                "discount": 15,
                "occasion": "Fitness Week"
            },
            {
                "id": 90, "name": "Yoga Mat Premium", "price": 1200,
                "details": {
                    "Material": "TPE",
                    "Thickness": "6mm",
                    "Size": "183cm x 61cm",
                    "Features": "Non-slip, Lightweight"
                },
                "discount": 25,
                "occasion": "International Yoga Day"
            }
        ]
    },
    {
        "name": "Kitchen Appliances",
        "varieties": [
            {
                "id": 91, "name": "Mixer Grinder 750W", "price": 4500,
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
        "name": "Pet Supplies",
        "varieties": [
            {
                "id": 97, "name": "Dog Food Premium 5kg", "price": 2500,
                "details": {
                    "Weight": "5kg",
                    "Type": "Adult Dog Food",
                    "Protein": "25%",
                    "Features": "Grain Free, Natural"
                },
                "discount": 12,
                "occasion": "Pet Care Week"
            },
            {
                "id": 98, "name": "Cat Litter 10L", "price": 800,
                "details": {
                    "Volume": "10L",
                    "Type": "Clumping",
                    "Material": "Bentonite Clay",
                    "Features": "Odor Control, Dust Free"
                },
                "discount": 0
            },
            {
                "id": 99, "name": "Pet Carrier Medium", "price": 1800,
                "details": {
                    "Size": "Medium",
                    "Material": "Hard Plastic",
                    "Weight Limit": "8kg",
                    "Features": "Ventilation, Easy Clean"
                },
                "discount": 20,
                "occasion": "Travel Season"
            }
        ]
    },
    {
        "name": "Office Supplies",
        "varieties": [
            {
                "id": 100, "name": "Wireless Mouse Logitech", "price": 1200,
                "details": {
                    "Connectivity": "Wireless 2.4GHz",
                    "Battery": "12 months",
                    "DPI": "1000",
                    "Features": "Ergonomic, Silent Click"
                },
                "discount": 15,
                "occasion": "Office Setup"
            },
            {
                "id": 101, "name": "Mechanical Keyboard", "price": 3500,
                "details": {
                    "Switch": "Blue Mechanical",
                    "Backlight": "RGB",
                    "Layout": "Full Size",
                    "Features": "Anti-ghosting, Wrist Rest"
                },
                "discount": 0
            },
            {
                "id": 102, "name": "Monitor Stand Adjustable", "price": 2200,
                "details": {
                    "Material": "Aluminum",
                    "Height": "Adjustable 8-20cm",
                    "Weight Limit": "10kg",
                    "Features": "Cable Management, Non-slip"
                },
                "discount": 25,
                "occasion": "Work from Home"
            }
        ]
    },
    {
        "name": "Beauty & Personal Care",
        "varieties": [
            {
                "id": 103, "name": "Hair Dryer Professional", "price": 2800,
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
    },
    {
        "name": "Sports & Outdoor",
        "varieties": [
            {
                "id": 106, "name": "Cricket Bat English Willow", "price": 4500,
                "details": {
                    "Material": "English Willow",
                    "Weight": "2.8-3.0 lbs",
                    "Size": "Size 6",
                    "Features": "Premium Grade, Hand Crafted"
                },
                "discount": 12,
                "occasion": "Cricket Season"
            },
            {
                "id": 107, "name": "Football Size 5", "price": 800,
                "details": {
                    "Size": "Size 5 (Official)",
                    "Material": "Synthetic Leather",
                    "Weight": "410-450g",
                    "Features": "FIFA Approved, Machine Stitched"
                },
                "discount": 0
            },
            {
                "id": 108, "name": "Badminton Racket Set", "price": 2200,
                "details": {
                    "Rackets": "2 Rackets",
                    "Material": "Carbon Fiber",
                    "Weight": "85g",
                    "Features": "Pre-strung, Grip Included"
                },
                "discount": 20,
                "occasion": "Sports Festival"
            }
        ]
    },
    {
        "name": "Travel & Luggage",
        "varieties": [
            {
                "id": 109, "name": "Hard Shell Suitcase 24\"", "price": 4500,
                "details": {
                    "Size": "24 inches",
                    "Material": "ABS Hard Shell",
                    "Wheels": "4 Spinner Wheels",
                    "Features": "TSA Lock, Expandable"
                },
                "discount": 15,
                "occasion": "Travel Season"
            },
            {
                "id": 110, "name": "Backpack 40L Travel", "price": 2800,
                "details": {
                    "Capacity": "40L",
                    "Material": "Nylon",
                    "Compartments": "Multiple Pockets",
                    "Features": "Laptop Compartment, Rain Cover"
                },
                "discount": 0
            },
            {
                "id": 111, "name": "Travel Adapter Universal", "price": 600,
                "details": {
                    "Compatibility": "150+ Countries",
                    "USB Ports": "2 USB-A + 1 USB-C",
                    "Power": "65W",
                    "Features": "Surge Protection, Compact"
                },
                "discount": 25,
                "occasion": "International Travel"
            }
        ]
    },
    {
        "name": "Health & Wellness",
        "varieties": [
            {
                "id": 112, "name": "Digital Blood Pressure Monitor", "price": 1800,
                "details": {
                    "Cuff Size": "22-42cm",
                    "Memory": "99 Readings",
                    "Display": "Large LCD",
                    "Features": "Irregular Heartbeat Detection"
                },
                "discount": 20,
                "occasion": "Health Awareness"
            },
            {
                "id": 113, "name": "Pulse Oximeter", "price": 1200,
                "details": {
                    "Measurement": "SpO2 & Heart Rate",
                    "Display": "OLED Screen",
                    "Battery": "30 hours",
                    "Features": "Finger Clip, Portable"
                },
                "discount": 0
            },
            {
                "id": 114, "name": "Digital Thermometer", "price": 400,
                "details": {
                    "Type": "Infrared",
                    "Range": "32-42.9°C",
                    "Response Time": "1 second",
                    "Features": "Memory Function, Fever Alert"
                },
                "discount": 18,
                "occasion": "Health Check"
            }
        ]
    },
    {
        "name": "Garden & Outdoor",
        "varieties": [
            {
                "id": 115, "name": "Garden Hose 50ft", "price": 1200,
                "details": {
                    "Length": "50 feet",
                    "Material": "Reinforced PVC",
                    "Diameter": "1/2 inch",
                    "Features": "Kink Resistant, UV Protected"
                },
                "discount": 15,
                "occasion": "Gardening Season"
            },
            {
                "id": 116, "name": "Plant Pot Set Ceramic", "price": 800,
                "details": {
                    "Quantity": "3 Pots",
                    "Sizes": "6\", 8\", 10\"",
                    "Material": "Ceramic",
                    "Features": "Drainage Holes, Saucers"
                },
                "discount": 0
            },
            {
                "id": 117, "name": "Garden Tools Set", "price": 1500,
                "details": {
                    "Tools": "5 Piece Set",
                    "Material": "Stainless Steel",
                    "Handle": "Ergonomic Grip",
                    "Features": "Rust Resistant, Durable"
                },
                "discount": 22,
                "occasion": "Spring Gardening"
            }
        ]
    },
    {
        "name": "Baby & Kids",
        "varieties": [
            {
                "id": 118, "name": "Baby Stroller 3-in-1", "price": 8500,
                "details": {
                    "Type": "3-in-1 Convertible",
                    "Weight": "12kg",
                    "Age": "0-3 years",
                    "Features": "Reversible Seat, 5-Point Harness"
                },
                "discount": 18,
                "occasion": "Baby Shower"
            },
            {
                "id": 119, "name": "Kids Learning Tablet", "price": 3500,
                "details": {
                    "Screen": "7\" Touch Screen",
                    "Storage": "32GB",
                    "Battery": "8 hours",
                    "Features": "Parental Control, Educational Apps"
                },
                "discount": 0
            },
            {
                "id": 120, "name": "Building Blocks Set", "price": 1200,
                "details": {
                    "Pieces": "100+ Blocks",
                    "Material": "Non-toxic Plastic",
                    "Age": "3+ years",
                    "Features": "Colorful, Creative Building"
                },
                "discount": 25,
                "occasion": "Children's Day"
            }
        ]
    },
    {
        "name": "Smart Home Devices",
        "varieties": [
            {
                "id": 121, "name": "Smart Speaker with Alexa", "price": 4500,
                "details": {
                    "Voice Assistant": "Amazon Alexa",
                    "Audio": "360° Sound",
                    "Connectivity": "Wi-Fi, Bluetooth",
                    "Features": "Voice Control, Music Streaming"
                },
                "discount": 20,
                "occasion": "Smart Home Week"
            },
            {
                "id": 122, "name": "Smart Doorbell Camera", "price": 6500,
                "details": {
                    "Resolution": "1080p HD",
                    "Night Vision": "Yes",
                    "Storage": "Cloud + Local",
                    "Features": "Motion Detection, Two-way Audio"
                },
                "discount": 15,
                "occasion": "Security Sale"
            },
            {
                "id": 123, "name": "Smart Light Bulbs Pack", "price": 1800,
                "details": {
                    "Quantity": "4 Bulbs",
                    "Color": "16 Million Colors",
                    "Control": "App + Voice",
                    "Features": "Dimmable, Timer, Scene Modes"
                },
                "discount": 25,
                "occasion": "Smart Lighting"
            }
        ]
    },
    {
        "name": "Automotive Accessories",
        "varieties": [
            {
                "id": 124, "name": "Car Dash Cam 4K", "price": 8500,
                "details": {
                    "Resolution": "4K Ultra HD",
                    "Storage": "128GB SD Card",
                    "Features": "GPS, Night Vision, Loop Recording",
                    "Display": "3\" LCD Screen"
                },
                "discount": 18,
                "occasion": "Road Safety Week"
            },
            {
                "id": 125, "name": "Car Phone Mount Magnetic", "price": 800,
                "details": {
                    "Type": "Magnetic Mount",
                    "Compatibility": "Universal",
                    "Material": "Aluminum + Rubber",
                    "Features": "360° Rotation, Strong Magnet"
                },
                "discount": 0
            },
            {
                "id": 126, "name": "Car Air Purifier", "price": 3200,
                "details": {
                    "Filter": "HEPA + Activated Carbon",
                    "Coverage": "Small Car",
                    "Power": "USB Powered",
                    "Features": "Auto Mode, LED Indicator"
                },
                "discount": 22,
                "occasion": "Clean Air Campaign"
            }
        ]
    },
    {
        "name": "Musical Instruments",
        "varieties": [
            {
                "id": 127, "name": "Acoustic Guitar 6-String", "price": 8500,
                "details": {
                    "Type": "Acoustic Guitar",
                    "Strings": "6 Steel Strings",
                    "Body": "Spruce Top, Mahogany Back",
                    "Features": "Cutaway Design, Built-in Tuner"
                },
                "discount": 12,
                "occasion": "Music Festival"
            },
            {
                "id": 128, "name": "Digital Piano 88 Keys", "price": 25000,
                "details": {
                    "Keys": "88 Weighted Keys",
                    "Sounds": "128 Voices",
                    "Connectivity": "USB, MIDI",
                    "Features": "Metronome, Recording, Headphone Jack"
                },
                "discount": 0
            },
            {
                "id": 129, "name": "Electronic Drum Kit", "price": 18000,
                "details": {
                    "Pads": "8 Drum Pads",
                    "Sounds": "200+ Drum Kits",
                    "Connectivity": "USB, Audio Out",
                    "Features": "Built-in Speaker, Headphone Jack"
                },
                "discount": 20,
                "occasion": "Drumming Workshop"
            }
        ]
    },
    {
        "name": "Photography Equipment",
        "varieties": [
            {
                "id": 130, "name": "DSLR Camera Kit", "price": 45000,
                "details": {
                    "Sensor": "24.2MP APS-C",
                    "Lens": "18-55mm Kit Lens",
                    "Video": "4K Recording",
                    "Features": "Wi-Fi, Touch Screen, Image Stabilization"
                },
                "discount": 15,
                "occasion": "Photography Month"
            },
            {
                "id": 131, "name": "Tripod Professional", "price": 3500,
                "details": {
                    "Height": "60-160cm Adjustable",
                    "Material": "Aluminum",
                    "Weight": "1.5kg",
                    "Features": "360° Pan, Quick Release Plate"
                },
                "discount": 0
            },
            {
                "id": 132, "name": "Camera Lens 50mm Prime", "price": 12000,
                "details": {
                    "Focal Length": "50mm",
                    "Aperture": "f/1.8",
                    "Type": "Prime Lens",
                    "Features": "Fast Autofocus, Low Light Performance"
                },
                "discount": 18,
                "occasion": "Lens Sale"
            }
        ]
    },
    {
        "name": "Jewelry & Watches",
        "varieties": [
            {
                "id": 133, "name": "Gold Chain 22K", "price": 25000,
                "details": {
                    "Material": "22K Gold",
                    "Weight": "8 grams",
                    "Length": "18 inches",
                    "Features": "Handcrafted, Hallmarked"
                },
                "discount": 8,
                "occasion": "Festival Season"
            },
            {
                "id": 134, "name": "Smart Watch Fitness", "price": 8500,
                "details": {
                    "Display": "1.4\" AMOLED",
                    "Battery": "7 days",
                    "Sensors": "Heart Rate, SpO2, GPS",
                    "Features": "Water Resistant, Sleep Tracking"
                },
                "discount": 0
            },
            {
                "id": 135, "name": "Diamond Earrings", "price": 18000,
                "details": {
                    "Diamonds": "0.5 carat total",
                    "Setting": "White Gold",
                    "Style": "Stud Earrings",
                    "Features": "Certified, Gift Box Included"
                },
                "discount": 12,
                "occasion": "Wedding Season"
            }
        ]
    },
    {
        "name": "Books & Stationery",
        "varieties": [
            {
                "id": 136, "name": "Programming Book Set", "price": 2500,
                "details": {
                    "Books": "5 Programming Books",
                    "Languages": "Python, JavaScript, Java",
                    "Format": "Paperback",
                    "Features": "Latest Editions, Code Examples"
                },
                "discount": 20,
                "occasion": "Education Week"
            },
            {
                "id": 137, "name": "Fountain Pen Set", "price": 1200,
                "details": {
                    "Quantity": "3 Pens",
                    "Nib": "Medium Point",
                    "Ink": "Blue, Black, Red",
                    "Features": "Gift Box, Refillable"
                },
                "discount": 0
            },
            {
                "id": 138, "name": "Notebook Set Premium", "price": 800,
                "details": {
                    "Quantity": "5 Notebooks",
                    "Pages": "200 pages each",
                    "Paper": "Premium Quality",
                    "Features": "Spiral Bound, Ruled"
                },
                "discount": 15,
                "occasion": "Back to School"
            }
        ]
    },
    {
        "name": "Food & Beverages",
        "varieties": [
            {
                "id": 139, "name": "Organic Green Tea Pack", "price": 600,
                "details": {
                    "Quantity": "100 Tea Bags",
                    "Type": "Organic Green Tea",
                    "Origin": "Assam, India",
                    "Features": "Antioxidant Rich, Caffeine Free"
                },
                "discount": 25,
                "occasion": "Health Month"
            },
            {
                "id": 140, "name": "Coffee Beans Premium", "price": 1200,
                "details": {
                    "Weight": "500g",
                    "Type": "Arabica Beans",
                    "Roast": "Medium Dark",
                    "Features": "Single Origin, Fresh Roasted"
                },
                "discount": 0
            },
            {
                "id": 141, "name": "Protein Powder 1kg", "price": 2800,
                "details": {
                    "Weight": "1kg",
                    "Type": "Whey Protein",
                    "Flavor": "Chocolate",
                    "Features": "25g Protein per serving, No Sugar"
                },
                "discount": 18,
                "occasion": "Fitness Challenge"
            }
        ]
    },
    {
        "name": "Art & Craft Supplies",
        "varieties": [
            {
                "id": 142, "name": "Oil Paint Set 24 Colors", "price": 1800,
                "details": {
                    "Colors": "24 Oil Paint Tubes",
                    "Size": "12ml each",
                    "Quality": "Artist Grade",
                    "Features": "Vibrant Colors, Long Lasting"
                },
                "discount": 22,
                "occasion": "Art Week"
            },
            {
                "id": 143, "name": "Sketching Pencils Set", "price": 600,
                "details": {
                    "Pencils": "12 Different Grades",
                    "Type": "Graphite Pencils",
                    "Range": "6H to 6B",
                    "Features": "Professional Quality, Sharpener Included"
                },
                "discount": 0
            },
            {
                "id": 144, "name": "Watercolor Paper Pad", "price": 800,
                "details": {
                    "Size": "A4",
                    "Sheets": "20 sheets",
                    "Weight": "300gsm",
                    "Features": "Cold Pressed, Acid Free"
                },
                "discount": 15,
                "occasion": "Creative Arts"
            }
        ]
    },
    {
        "name": "Tools & Hardware",
        "varieties": [
            {
                "id": 145, "name": "Drill Machine Cordless", "price": 4500,
                "details": {
                    "Power": "18V Lithium Battery",
                    "Torque": "50Nm",
                    "Chuck": "13mm Keyless",
                    "Features": "LED Light, 2 Speed Settings"
                },
                "discount": 20,
                "occasion": "DIY Workshop"
            },
            {
                "id": 146, "name": "Tool Kit 50 Pieces", "price": 2200,
                "details": {
                    "Pieces": "50 Tools",
                    "Case": "Hard Plastic Case",
                    "Tools": "Screwdrivers, Wrenches, Pliers",
                    "Features": "Professional Grade, Lifetime Warranty"
                },
                "discount": 0
            },
            {
                "id": 147, "name": "Measuring Tape 5m", "price": 300,
                "details": {
                    "Length": "5 meters",
                    "Width": "25mm",
                    "Material": "Steel Blade",
                    "Features": "Auto Lock, Magnetic Hook"
                },
                "discount": 18,
                "occasion": "Construction Week"
            }
        ]
    },
    {
        "name": "Seasonal Items",
        "varieties": [
            {
                "id": 148, "name": "Electric Blanket", "price": 3500,
                "details": {
                    "Size": "Double Bed",
                    "Material": "Fleece",
                    "Heat Settings": "3 Levels",
                    "Features": "Auto Shut-off, Machine Washable"
                },
                "discount": 25,
                "occasion": "Winter Sale"
            },
            {
                "id": 149, "name": "Portable Fan USB", "price": 800,
                "details": {
                    "Power": "USB Powered",
                    "Speed": "3 Speed Settings",
                    "Battery": "Built-in 2000mAh",
                    "Features": "Quiet Operation, Adjustable Angle"
                },
                "discount": 0
            },
            {
                "id": 150, "name": "Raincoat Adult", "price": 1200,
                "details": {
                    "Size": "Universal Fit",
                    "Material": "PVC Waterproof",
                    "Color": "Yellow",
                    "Features": "Lightweight, Packable"
                },
                "discount": 15,
                "occasion": "Monsoon Special"
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
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    flash('Added to cart.')
    return redirect(url_for('home'))

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

@app.route('/my_orders')
def my_orders():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    user_orders = []
    for o in orders:
        if o['user'] == session['user']:
            items = [get_variety_by_id(pid) for pid in o['items']]
            user_orders.append({'items': items})
    return render_template('orders.html', user_orders=user_orders)

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
            'user': session['user'],
            'items': cart_ids,
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