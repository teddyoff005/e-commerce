from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

# Sample data
products = [
    {
        "name": "Laptop",
        "varieties": [
            {
                "id": 1, "name": "Dell Inspiron 15", "price": 50000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Dell+Inspiron+15",
                "details": {
                    "RAM": "8GB DDR4",
                    "CPU": "Intel Core i5 11th Gen",
                    "GPU": "Intel Iris Xe",
                    "Storage": "512GB SSD",
                    "Display": "15.6\" FHD"
                },
                "discount": 20,
                "occasion": "Diwali Sale"
            },
            {
                "id": 2, "name": "HP Pavilion x360", "price": 62000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=HP+Pavilion+x360",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Apple+MacBook+Air",
                "details": {
                    "RAM": "8GB Unified",
                    "CPU": "Apple M1",
                    "GPU": "Integrated 7-core",
                    "Storage": "256GB SSD",
                    "Display": "13.3\" Retina"
                },
                "discount": 10,
                "occasion": "New Year Bonanza"
            }
        ]
    },
    {
        "name": "Smartphone",
        "varieties": [
            {
                "id": 4, "name": "Samsung Galaxy S23", "price": 70000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Samsung+Galaxy+S23",
                "details": {
                    "RAM": "8GB",
                    "CPU": "Snapdragon 8 Gen 2",
                    "Storage": "256GB",
                    "Camera": "50MP Triple",
                    "Display": "6.1\" FHD+ AMOLED"
                },
                "discount": 25,
                "occasion": "Holi Festival Offer"
            },
            {
                "id": 5, "name": "iPhone 14", "price": 80000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=iPhone+14",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=OnePlus+11",
                "details": {
                    "RAM": "8GB",
                    "CPU": "Snapdragon 8 Gen 2",
                    "Storage": "128GB",
                    "Camera": "50MP Triple",
                    "Display": "6.7\" QHD+ AMOLED"
                },
                "discount": 15,
                "occasion": "Summer Sale"
            }
        ]
    },
    {
        "name": "Headphones",
        "varieties": [
            {
                "id": 7, "name": "Sony WH-1000XM4", "price": 25000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Sony+WH-1000XM4",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Boat+Rockerz+450",
                "details": {
                    "Type": "Over-ear Wireless",
                    "Battery": "15 hours",
                    "Driver": "50mm",
                    "Connectivity": "Bluetooth 5.0",
                    "Color": "Black/Red",
                    "Features": "Bass Boost, Voice Assistant"
                },
                "discount": 30,
                "occasion": "Monsoon Mania"
            },
            {
                "id": 9, "name": "JBL Tune 510BT", "price": 3500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=JBL+Tune+510BT",
                "details": {
                    "Type": "Over-ear Wireless",
                    "Battery": "40 hours",
                    "Driver": "32mm",
                    "Connectivity": "Bluetooth 5.0",
                    "Color": "Blue/White/Black",
                    "Features": "JBL Pure Bass, Multi-point Connect"
                },
                "discount": 10,
                "occasion": "Winter Fest"
            }
        ]
    },
    {
        "name": "Book",
        "varieties": [
            {
                "id": 10, "name": "Atomic Habits", "price": 500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Atomic+Habits",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=The+Alchemist",
                "details": {
                    "Author": "Paulo Coelho",
                    "Pages": "208 pages",
                    "Language": "English",
                    "Format": "Paperback",
                    "Genre": "Fiction/Philosophy",
                    "Publisher": "HarperOne"
                },
                "discount": 15,
                "occasion": "Book Lovers Day"
            },
            {
                "id": 12, "name": "Rich Dad Poor Dad", "price": 450,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Rich+Dad+Poor+Dad",
                "details": {
                    "Author": "Robert Kiyosaki",
                    "Pages": "336 pages",
                    "Language": "English",
                    "Format": "Paperback",
                    "Genre": "Personal Finance",
                    "Publisher": "Warner Books"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Smartwatch",
        "varieties": [
            {
                "id": 13, "name": "Apple Watch SE", "price": 32000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Apple+Watch+SE",
                "details": {
                    "Display": "40mm/44mm Retina",
                    "Battery": "18 hours",
                    "Connectivity": "GPS + Cellular",
                    "Sensors": "Heart Rate, ECG, Blood Oxygen",
                    "Color": "Space Gray/Silver/Gold",
                    "Features": "Water Resistant, Sleep Tracking"
                },
                "discount": 5,
                "occasion": "Valentine's Special"
            },
            {
                "id": 14, "name": "Samsung Galaxy Watch 5", "price": 28000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Samsung+Galaxy+Watch+5",
                "details": {
                    "Display": "1.4\" AMOLED",
                    "Battery": "50 hours",
                    "Connectivity": "Bluetooth, Wi-Fi",
                    "Sensors": "Heart Rate, SpO2, GPS",
                    "Color": "Black/Silver/Pink Gold",
                    "Features": "Samsung Pay, Bixby Voice"
                },
                "discount": 0
            },
            {
                "id": 15, "name": "Noise ColorFit Pro", "price": 3500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Noise+ColorFit+Pro",
                "details": {
                    "Display": "1.55\" HD Color",
                    "Battery": "10 days",
                    "Connectivity": "Bluetooth 5.0",
                    "Sensors": "Heart Rate, SpO2",
                    "Color": "Black/Blue/Pink",
                    "Features": "IP68 Water Resistant, 150+ Watch Faces"
                },
                "discount": 20,
                "occasion": "Independence Day Sale"
            }
        ]
    },
    {
        "name": "Bluetooth Speaker",
        "varieties": [
            {
                "id": 16, "name": "JBL Flip 5", "price": 8000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=JBL+Flip+5",
                "details": {
                    "Power": "20W",
                    "Battery": "12 hours",
                    "Connectivity": "Bluetooth 4.2",
                    "Waterproof": "IPX7",
                    "Color": "Black/Blue/Red/Pink",
                    "Features": "JBL Connect+, Voice Assistant"
                },
                "discount": 10,
                "occasion": "Ganesh Chaturthi Offer"
            },
            {
                "id": 17, "name": "Boat Stone 650", "price": 1800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Boat+Stone+650",
                "details": {
                    "Power": "10W",
                    "Battery": "8 hours",
                    "Connectivity": "Bluetooth 5.0",
                    "Waterproof": "IPX5",
                    "Color": "Black/Blue/Red",
                    "Features": "Bass Boost, TWS Connect"
                },
                "discount": 0
            },
            {
                "id": 18, "name": "Sony SRS-XB13", "price": 3500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Sony+SRS-XB13",
                "details": {
                    "Power": "16W",
                    "Battery": "16 hours",
                    "Connectivity": "Bluetooth 5.0",
                    "Waterproof": "IP67",
                    "Color": "Black/Blue/Pink/Orange",
                    "Features": "Extra Bass, Party Connect"
                },
                "discount": 15,
                "occasion": "Christmas Sale"
            }
        ]
    },
    {
        "name": "Backpack",
        "varieties": [
            {
                "id": 19, "name": "Wildcraft 35L", "price": 1200,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Wildcraft+35L",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Skybags+Brat",
                "details": {
                    "Capacity": "30L",
                    "Material": "Polyester",
                    "Compartments": "Main + 2 Pockets",
                    "Color": "Black/Red/Blue",
                    "Features": "Anti-theft, USB Charging Port",
                    "Weight": "1.0kg"
                },
                "discount": 10,
                "occasion": "Back to College"
            },
            {
                "id": 21, "name": "American Tourister", "price": 1800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=American+Tourister",
                "details": {
                    "Capacity": "40L",
                    "Material": "Nylon + PVC",
                    "Compartments": "Main + 4 Pockets",
                    "Color": "Black/Navy/Red",
                    "Features": "TSA Lock, Expandable",
                    "Weight": "1.5kg"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Desk Lamp",
        "varieties": [
            {
                "id": 22, "name": "Philips LED Desk Lamp", "price": 900,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Philips+LED+Desk+Lamp",
                "details": {
                    "Power": "5W LED",
                    "Brightness": "400 Lumens",
                    "Color Temperature": "3000K-6500K",
                    "Color": "White/Silver",
                    "Features": "Touch Control, USB Charging Port",
                    "Warranty": "2 years"
                },
                "discount": 10,
                "occasion": "Work from Home Essentials"
            },
            {
                "id": 23, "name": "Wipro Garnet", "price": 1100,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Wipro+Garnet",
                "details": {
                    "Power": "8W LED",
                    "Brightness": "600 Lumens",
                    "Color Temperature": "2700K-6500K",
                    "Color": "Black/White",
                    "Features": "Dimmable, Memory Function",
                    "Warranty": "3 years"
                },
                "discount": 0
            },
            {
                "id": 24, "name": "Syska Table Lamp", "price": 850,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Syska+Table+Lamp",
                "details": {
                    "Power": "6W LED",
                    "Brightness": "500 Lumens",
                    "Color Temperature": "3000K-6000K",
                    "Color": "Black/Silver",
                    "Features": "3-Level Dimming, Flexible Arm",
                    "Warranty": "1 year"
                },
                "discount": 15,
                "occasion": "Student Offer"
            }
        ]
    },
    {
        "name": "Wireless Mouse",
        "varieties": [
            {
                "id": 25, "name": "Logitech M235", "price": 700,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Logitech+M235",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=HP+X200",
                "details": {
                    "Connectivity": "Wireless 2.4GHz",
                    "Battery": "15 months",
                    "DPI": "1200",
                    "Color": "Black/Silver",
                    "Features": "Plug & Play, Energy Saving",
                    "Compatibility": "Windows, Mac"
                },
                "discount": 0
            },
            {
                "id": 27, "name": "Dell WM126", "price": 800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Dell+WM126",
                "details": {
                    "Connectivity": "Wireless 2.4GHz",
                    "Battery": "18 months",
                    "DPI": "1000",
                    "Color": "Black/White",
                    "Features": "Nano Receiver, Scroll Wheel",
                    "Compatibility": "Universal"
                },
                "discount": 10,
                "occasion": "Gaming Week"
            }
        ]
    },
    {
        "name": "Water Bottle",
        "varieties": [
            {
                "id": 28, "name": "Milton Thermosteel", "price": 900,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Milton+Thermosteel",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Cello+Puro",
                "details": {
                    "Capacity": "750ml",
                    "Material": "BPA Free Plastic",
                    "Insulation": "Basic",
                    "Color": "Blue/Green/Pink",
                    "Features": "Leak-proof, Lightweight",
                    "Weight": "150g"
                },
                "discount": 0
            },
            {
                "id": 30, "name": "Borosil Hydra", "price": 650,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Borosil+Hydra",
                "details": {
                    "Capacity": "1L",
                    "Material": "Borosilicate Glass",
                    "Insulation": "Silicone Sleeve",
                    "Color": "Clear/Blue/Green",
                    "Features": "Heat Resistant, Easy Grip",
                    "Weight": "400g"
                },
                "discount": 5,
                "occasion": "Stay Hydrated Sale"
            }
        ]
    },
    {
        "name": "Dress (Men)",
        "varieties": [
            {
                "id": 31, "name": "Formal Shirt", "price": 1200,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Formal+Shirt",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Casual+T-Shirt",
                "details": {
                    "Material": "Cotton Blend",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/White/Blue/Red/Green",
                    "Fit": "Regular Fit",
                    "Features": "Pre-shrunk, Machine Washable",
                    "Occasion": "Casual, Daily Wear"
                },
                "discount": 20,
                "occasion": "Clearance Sale"
            },
            {
                "id": 33, "name": "Jeans", "price": 1500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Jeans",
                "details": {
                    "Material": "Denim",
                    "Size": "28, 30, 32, 34, 36, 38",
                    "Color": "Blue/Black/Dark Blue",
                    "Fit": "Slim/Regular/Relaxed",
                    "Features": "Stretch Denim, Fade Resistant",
                    "Occasion": "Casual, Party"
                },
                "discount": 0
            },
            {
                "id": 34, "name": "Kurta", "price": 900,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Kurta",
                "details": {
                    "Material": "Cotton",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "White/Beige/Blue/Maroon",
                    "Fit": "Regular Fit",
                    "Features": "Handcrafted, Traditional Design",
                    "Occasion": "Festival, Traditional Events"
                },
                "discount": 25,
                "occasion": "Dussehra Special"
            }
        ]
    },
    {
        "name": "Dress (Women)",
        "varieties": [
            {
                "id": 35, "name": "Saree", "price": 2000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Saree",
                "details": {
                    "Material": "Silk/Cotton/Georgette",
                    "Size": "5.5 meters length",
                    "Color": "Red/Blue/Green/Pink/Maroon",
                    "Design": "Printed/Embroidered/Plain",
                    "Features": "Blouse Piece Included, Ready to Wear",
                    "Occasion": "Wedding, Festival, Party"
                },
                "discount": 30,
                "occasion": "Karwa Chauth Offer"
            },
            {
                "id": 36, "name": "Kurti", "price": 800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Kurti",
                "details": {
                    "Material": "Cotton/Rayon",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Blue/Green/Pink/Orange/Black",
                    "Length": "Knee Length/Ankle Length",
                    "Features": "Comfortable Fit, Easy Care",
                    "Occasion": "Casual, Office, Festival"
                },
                "discount": 0
            },
            {
                "id": 37, "name": "Western Dress", "price": 1800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Western+Dress",
                "details": {
                    "Material": "Polyester/Cotton Blend",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/Red/Blue/Green/White",
                    "Style": "A-line/Fit & Flare/Shift",
                    "Features": "Machine Washable, Wrinkle Free",
                    "Occasion": "Party, Office, Date"
                },
                "discount": 15,
                "occasion": "End of Season Sale"
            },
            {
                "id": 38, "name": "Leggings", "price": 400,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Leggings",
                "details": {
                    "Material": "Cotton Lycra",
                    "Size": "S, M, L, XL, XXL",
                    "Color": "Black/Navy/Blue/Green/Pink",
                    "Fit": "High Waist, Stretchy",
                    "Features": "Opaque, Comfortable",
                    "Occasion": "Casual, Gym, Daily Wear"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Shoes",
        "varieties": [
            {
                "id": 46, "name": "Nike Running Shoes", "price": 3500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Nike+Running+Shoes",
                "details": {
                    "Type": "Running Shoes",
                    "Size": "6, 7, 8, 9, 10, 11, 12",
                    "Color": "Black/White/Blue/Red",
                    "Material": "Mesh Upper, Rubber Sole",
                    "Features": "Air Cushioning, Breathable",
                    "Occasion": "Running, Gym, Casual"
                },
                "discount": 10,
                "occasion": "Fitness Challenge"
            },
            {
                "id": 47, "name": "Adidas Sneakers", "price": 4000,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Adidas+Sneakers",
                "details": {
                    "Type": "Casual Sneakers",
                    "Size": "6, 7, 8, 9, 10, 11, 12",
                    "Color": "White/Black/Blue/Green",
                    "Material": "Leather/Synthetic Upper",
                    "Features": "Boost Technology, Comfortable",
                    "Occasion": "Casual, Daily Wear, Sports"
                },
                "discount": 0
            },
            {
                "id": 48, "name": "Bata Formal Shoes", "price": 1800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Bata+Formal+Shoes",
                "details": {
                    "Type": "Formal Leather Shoes",
                    "Size": "6, 7, 8, 9, 10, 11, 12",
                    "Color": "Black/Brown",
                    "Material": "Genuine Leather",
                    "Features": "Polished Finish, Comfortable",
                    "Occasion": "Office, Formal Events, Business"
                },
                "discount": 5,
                "occasion": "Corporate Deal"
            }
        ]
    },
    {
        "name": "Sunglasses",
        "varieties": [
            {
                "id": 49, "name": "Ray-Ban Aviator", "price": 6500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Ray-Ban+Aviator",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Fastrack+Wayfarer",
                "details": {
                    "Style": "Wayfarer",
                    "Lens Color": "Black/Brown/Blue",
                    "Frame Color": "Black/Brown/Tortoise",
                    "Lens Material": "Polycarbonate",
                    "Features": "UV Protection, Lightweight",
                    "Occasion": "Casual, Fashion, Daily Wear"
                },
                "discount": 40,
                "occasion": "Flash Sale"
            },
            {
                "id": 51, "name": "Vincent Chase Round", "price": 900,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Vincent+Chase+Round",
                "details": {
                    "Style": "Round",
                    "Lens Color": "Black/Brown/Green",
                    "Frame Color": "Black/Brown/Gold",
                    "Lens Material": "CR-39",
                    "Features": "UV Protection, Scratch Resistant",
                    "Occasion": "Fashion, Vintage Style, Casual"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Kitchen Appliances",
        "varieties": [
            {
                "id": 91, "name": "Mixer Grinder 750W", "price": 4500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Mixer+Grinder+750W",
                "details": {
                    "Power": "750W",
                    "Jars": "3 Stainless Steel",
                    "Speed": "3 Speed Control",
                    "Features": "Overload Protection"
                },
                "discount": 10,
                "occasion": "Navratri Special"
            },
            {
                "id": 92, "name": "Electric Kettle 1.5L", "price": 1800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Electric+Kettle+1.5L",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Air+Fryer+4.2L",
                "details": {
                    "Capacity": "4.2L",
                    "Power": "1500W",
                    "Temperature": "80-200°C",
                    "Features": "Digital Display, Timer"
                },
                "discount": 20,
                "occasion": "Dhanteras Dhamaka"
            }
        ]
    },
    {
        "name": "Home Decor",
        "varieties": [
            {
                "id": 94, "name": "LED Strip Lights 5m", "price": 800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=LED+Strip+Lights+5m",
                "details": {
                    "Length": "5 meters",
                    "Color": "RGB",
                    "Control": "Remote + App",
                    "Features": "Waterproof, Adhesive"
                },
                "discount": 50,
                "occasion": "Diwali Lighting Deal"
            },
            {
                "id": 95, "name": "Wall Clock Modern", "price": 1200,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Wall+Clock+Modern",
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
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Artificial+Plants+Set",
                "details": {
                    "Quantity": "3 Plants",
                    "Material": "High Quality Plastic",
                    "Height": "30-45cm",
                    "Features": "UV Resistant, Realistic"
                },
                "discount": 0
            }
        ]
    },
    {
        "name": "Beauty & Personal Care",
        "varieties": [
            {
                "id": 97, "name": "Hair Dryer Professional", "price": 2800,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Hair+Dryer+Professional",
                "details": {
                    "Power": "2000W",
                    "Speed": "2 Speed + Cool Shot",
                    "Attachments": "3 Nozzles",
                    "Features": "Ionic Technology, Foldable"
                },
                "discount": 0
            },
            {
                "id": 98, "name": "Electric Toothbrush", "price": 1500,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Electric+Toothbrush",
                "details": {
                    "Battery": "30 days",
                    "Modes": "3 Cleaning Modes",
                    "Timer": "2-minute Timer",
                    "Features": "Waterproof, Travel Case"
                },
                "discount": 10,
                "occasion": "Personal Care Week"
            },
            {
                "id": 99, "name": "Facial Cleansing Brush", "price": 1200,
                "image_url": "https://placehold.co/400x300/0a0e27/e8e8ff?text=Facial+Cleansing+Brush",
                "details": {
                    "Brushes": "4 Different Heads",
                    "Speed": "2 Speed Settings",
                    "Battery": "USB Rechargeable",
                    "Features": "Waterproof, Gentle Exfoliation"
                },
                "discount": 0
            }
        ]
    }
]
users = {}
orders = []
wishlists = {}

@app.route('/')
def root():
    return render_template('animation.html')

@app.route('/get-landing-content')
def get_landing_content():
    all_varieties = []
    for p in products:
        for v in p['varieties']:
            all_varieties.append(v)
    # Manually select new arrivals by ID
    new_arrival_ids = [2, 5, 9, 14, 21]
    new_arrivals = [v for v in all_varieties if v['id'] in new_arrival_ids]
    return render_template('landing.html', new_arrivals=new_arrivals)

@app.route('/landing')
def landing():
    return render_template('animation.html')

@app.route('/add_to_wishlist/<int:pid>')
def add_to_wishlist(pid):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please log in first.'}), 401

    user = session['user']
    if user not in wishlists:
        wishlists[user] = []

    if pid not in wishlists[user]:
        wishlists[user].append(pid)
        message = 'Added to wishlist.'
    else:
        message = 'Item already in wishlist.'

    return jsonify({'success': True, 'message': message, 'wishlist_count': len(wishlists[user])})

@app.route('/home')
def home():
    query = request.args.get('q', '').lower()
    category_filter = request.args.get('category', '').lower()

    filtered_products = []
    trending_products = []
    deals = []

    all_varieties = []
    all_product_categories = []
    for p in products:
        all_product_categories.append(p['name'])
        for v in p['varieties']:
            all_varieties.append(v)

    # Manually select trending products by ID
    trending_ids = [3, 4, 7, 46, 49]
    trending_products = [v for v in all_varieties if v['id'] in trending_ids]

    # Filter for deals (e.g., discount >= 20%)
    deals = [v for v in all_varieties if v.get('discount', 0) >= 20]

    # Apply filters
    for product_category_data in products:
        if category_filter and product_category_data['name'].lower() != category_filter:
            continue

        filtered_varieties_for_category = []
        for v in product_category_data['varieties']:
            current_price = v['price'] - (v['price'] * v.get('discount', 0) // 100)

            # No price filtering

            matches = False
            if not query:
                matches = True
            else:
                # Search in product category name
                if query in product_category_data['name'].lower():
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
                filtered_varieties_for_category.append(v)

        if filtered_varieties_for_category:
            # Apply sorting to varieties within each category
            # No sorting applied

            filtered_products.append({
                'name': product_category_data['name'],
                'varieties': filtered_varieties_for_category
            })

    return render_template('home.html', products=filtered_products, trending_products=trending_products, deals=deals, all_product_categories=sorted(list(set(all_product_categories))))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists.')
        else:
            users[username] = generate_password_hash(password)
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users.get(username), password):
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

@app.route('/set_location/<location>')
def set_location(location):
    session['location'] = location
    return redirect(url_for('home'))

@app.route('/add_to_cart/<int:pid>')
def add_to_cart(pid):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please log in first.'}), 401

    cart = session.get('cart', {})
    if isinstance(cart, list):
        cart_dict = {}
        for item_id in cart:
            cart_dict[str(item_id)] = cart_dict.get(str(item_id), 0) + 1
        cart = cart_dict

    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session['cart'] = cart

    return jsonify({'success': True, 'message': 'Added to cart.', 'cart_count': len(cart)})

@app.route('/remove_from_cart/<int:pid>')
def remove_from_cart(pid):
    if 'user' not in session:
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    if str(pid) in cart:
        del cart[str(pid)]
    session['cart'] = cart

    return redirect(url_for('view_cart'))

@app.route('/update_cart/<int:pid>', methods=['POST'])
def update_cart(pid):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please log in first.'}), 401

    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})

    if quantity > 0:
        cart[str(pid)] = quantity
    else:
        if str(pid) in cart:
            del cart[str(pid)]
    
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/increase_quantity/<int:pid>')
def increase_quantity(pid):
    if 'user' not in session:
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session['cart'] = cart

    return redirect(url_for('view_cart'))

@app.route('/decrease_quantity/<int:pid>')
def decrease_quantity(pid):
    if 'user' not in session:
        return redirect(url_for('login'))

    cart = session.get('cart', {})
    if cart.get(str(pid), 0) > 1:
        cart[str(pid)] -= 1
    else:
        if str(pid) in cart:
            del cart[str(pid)]
    session['cart'] = cart

    return redirect(url_for('view_cart'))

def get_variety_by_id(pid):
    for p in products:
        for v in p['varieties']:
            if v['id'] == pid:
                return {"product": p["name"], **v}
    return None

@app.context_processor
def cart_item_count():
    return {'cart_count': len(session.get('cart', {}))}

@app.context_processor
def wishlist_item_count():
    user = session.get('user')
    if user and user in wishlists:
        return {'wishlist_count': len(wishlists[user])}
    return {'wishlist_count': 0}

@app.route('/remove_from_wishlist/<int:pid>')
def remove_from_wishlist(pid):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Please log in first.'}), 401

    user = session['user']
    if user in wishlists and pid in wishlists[user]:
        wishlists[user].remove(pid)
        message = 'Removed from wishlist.'
    else:
        message = 'Item not found in wishlist.'

    return jsonify({'success': True, 'message': message, 'wishlist_count': len(wishlists.get(user, []))})

@app.route('/cart')
def view_cart():
    cart_data = session.get('cart', {})
    if isinstance(cart_data, list):
        cart_dict = {}
        for item_id in cart_data:
            cart_dict[str(item_id)] = cart_dict.get(str(item_id), 0) + 1
        cart_data = cart_dict
        session['cart'] = cart_data

    cart_items = []
    total = 0
    for pid, quantity in cart_data.items():
        item = get_variety_by_id(int(pid))
        if item:
            original_price = item['price']
            discount_percent = item.get('discount', 0)
            discounted_price = original_price * (1 - discount_percent / 100)

            item['original_price'] = original_price
            item['discounted_price'] = discounted_price
            item['discount_amount'] = original_price - discounted_price
            item['quantity'] = quantity

            cart_items.append(item)
            total += discounted_price * quantity

    return render_template('cart.html', cart=cart_items, total=total)

# NOTE: The place_order route is redundant since checkout handles order placement,
# but is left here for completeness if other parts of your code rely on it.
@app.route('/place_order')
def place_order():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart = session.get('cart', {})
    if isinstance(cart, list):
        cart_dict = {}
        for item_id in cart:
            cart_dict[item_id] = cart_dict.get(item_id, 0) + 1
        cart = cart_dict
        session['cart'] = cart

    if not cart:
        flash('Cart is empty.')
        return redirect(url_for('home'))
    orders.append({'user': session['user'], 'items': cart.copy()})
    session['cart'] = {}
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
    if 'user' not in session:
        flash('Please log in to view your wishlist.')
        return redirect(url_for('login'))

    user = session['user']
    user_wishlist_ids = wishlists.get(user, [])
    wishlist_items = []
    for pid in user_wishlist_ids:
        item = get_variety_by_id(pid)
        if item:
            wishlist_items.append(item)

    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please log in to view your profile.')
        return redirect(url_for('login'))
    user_orders = [o for o in orders if o['user'] == session['user']]
    return render_template('profile.html', user_orders=user_orders)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    cart_data = session.get('cart', {})
    if isinstance(cart_data, list):
        cart_dict = {}
        for item_id in cart_data:
            cart_dict[str(item_id)] = cart_dict.get(str(item_id), 0) + 1
        cart_data = cart_dict
        session['cart'] = cart_data

    cart_items = []
    total = 0
    for pid, quantity in cart_data.items():
        item = get_variety_by_id(int(pid))
        if item:
            original_price = item['price']
            discount_percent = item.get('discount', 0)
            discounted_price = original_price * (1 - discount_percent / 100)

            item['original_price'] = original_price
            item['discounted_price'] = discounted_price
            item['discount_amount'] = original_price - discounted_price
            item['quantity'] = quantity

            cart_items.append(item)
            total += discounted_price * quantity

    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        pincode = request.form.get('pincode')
        country = request.form.get('country')
        method = request.form.get('method')
        if not all([name, address, city, pincode, country, method]):
            flash('Please fill all checkout details.')
            return render_template('checkout.html', cart=cart_items, total=total)

        delivery_days = random.randint(3, 10)
        delivery_date = datetime.now() + timedelta(days=delivery_days)

        orders.append({
            'id': len(orders) + 1,
            'user': session['user'],
            'order_items': cart_items,
            'name': name,
            'address': address,
            'city': city,
            'pincode': pincode,
            'country': country,
            'method': method,
            'total': total,
            'delivery_date': delivery_date.strftime('%A, %B %d, %Y')
        })
        session['cart'] = {}
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

@app.route('/order_details/<int:order_id>')
def order_details(order_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    order = next((o for o in orders if o['id'] == order_id and o['user'] == session['user']), None)

    if order:
        return render_template('order_detail.html', order=order)
    else:
        flash('Order not found.')
        return redirect(url_for('my_orders'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']

        if not new_username:
            flash('Username cannot be empty.')
            return render_template('edit_profile.html')

        # In a real application, you would also update the email and other fields in the database.
        # For this example, we'll just update the username and email in the session.

        # Check if the new username is already taken
        if new_username != session['user'] and new_username in users:
            flash('Username already exists.')
            return render_template('edit_profile.html')

        # Update the username in the users dictionary if the user exists
        if session['user'] in users:
            users[new_username] = users.pop(session['user'])

        session['user'] = new_username
        session['email'] = new_email

        flash('Profile updated successfully.')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html')

@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        pincode = request.form['pincode']
        country = request.form['country']

        if 'addresses' not in session:
            session['addresses'] = []

        session['addresses'].append({
            'name': name,
            'address': address,
            'city': city,
            'pincode': pincode,
            'country': country
        })

        flash('Address added successfully.')
        return redirect(url_for('profile', _anchor='addresses'))

    return render_template('add_address.html')

@app.route('/delete_address/<int:address_index>')
def delete_address(address_index):
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'addresses' in session and len(session['addresses']) > address_index:
        session['addresses'].pop(address_index)
        flash('Address deleted successfully.')
    return redirect(url_for('profile', _anchor='addresses'))

if __name__ == '__main__':
    app.run(debug=True)