from tempfile import template
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime, timedelta
from jinja2 import BaseLoader, TemplateNotFound

class DictLoader(BaseLoader):
    def __init__(self, templates):
        self.templates = templates

    def get_source(self, environment, template):
        if template in self.templates:
            source = self.templates[template]
            return source, None, lambda: True
        raise TemplateNotFound(template)

templates = {
    "add_address.html": """{% extends "base.html" %}

{% block title %}Add New Address - My E-Commerce{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <h3>Add New Address</h3>
            <div class="card">
                <div class="card-body">
                    <form method="POST" action="{{ url_for('add_address') }}">
                        <div class="mb-3">
                            <label for="name" class="form-label">Full Name</label>
                            <input type="text" class="form-control" id="name" name="name" required>
                        </div>
                        <div class="mb-3">
                            <label for="address" class="form-label">Address</label>
                            <input type="text" class="form-control" id="address" name="address" required>
                        </div>
                        <div class="mb-3">
                            <label for="city" class="form-label">City</label>
                            <input type="text" class="form-control" id="city" name="city" required>
                        </div>
                        <div class="mb-3">
                            <label for="pincode" class="form-label">Pincode</label>
                            <input type="text" class="form-control" id="pincode" name="pincode" required>
                        </div>
                        <div class="mb-3">
                            <label for="country" class="form-label">Country</label>
                            <input type="text" class="form-control" id="country" name="country" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Address</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",
    "animation.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #0a0e27;
        }

        #bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .animation-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .welcome-message {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 4rem;
            font-weight: 800;
            color: #fff;
            animation: wave 2s ease-in-out forwards;
        }

        .landing-page-container {
            display: none;
            width: 100%;
            height: 100%;
        }

        @keyframes wave {
            0% {
                transform: scale(0);
            }
            100% {
                transform: scale(1);
            }
        }
    </style>
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    <div class="animation-container" style="flex-direction: column;">
        <h1 class="welcome-message">Welcome to One Stop Store</h1>
        <h2 class="welcome-message" style="font-size: 2rem; margin-top: 20px;">Thank you for connecting with us</h2>
    </div>
    <div class="landing-page-container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('bg-canvas'), antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setClearColor(0x0a0e27, 1);
        camera.position.z = 5;

        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 8000;
        const posArray = new Float32Array(particlesCount * 3);
        for (let i = 0; i < particlesCount * 3; i += 3) {
            posArray[i] = (Math.random() - 0.5) * 50;
            posArray[i + 1] = (Math.random() - 0.5) * 50;
            posArray[i + 2] = (Math.random() - 0.5) * 50;
        }
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particlesMaterial = new THREE.PointsMaterial({ size: 0.02, color: 0x6080ff, transparent: true, opacity: 0.6, sizeAttenuation: true, blending: THREE.AdditiveBlending });
        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particles);

        let mouseX = 0, mouseY = 0;
        document.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
        });

        const clock = new THREE.Clock();
        const animate = () => {
            requestAnimationFrame(animate);
            const elapsed = clock.getElapsedTime();
            particles.rotation.y = elapsed * 0.02;
            particles.rotation.x = elapsed * 0.01;

            let targetCameraX = mouseX * 0.3;
            let targetCameraY = mouseY * 0.3;
            camera.position.x += (targetCameraX - camera.position.x) * 0.05;
            camera.position.y += (targetCameraY - camera.position.y) * 0.05;
            camera.lookAt(scene.position);

            renderer.render(scene, camera);
        };
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        setTimeout(() => {
            document.querySelector('.animation-container').style.display = 'none';
            const landingPageContainer = document.querySelector('.landing-page-container');
            landingPageContainer.style.display = 'block';
            fetch('{{ url_for("get_landing_content") }}')
                .then(response => response.text())
                .then(html => {
                    landingPageContainer.innerHTML = html;
                });
        }, 2000);
    </script>
</body>
</html>
""",
    "base.html": """<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}One Stop Store{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lato:wght@400;700&family=Montserrat:wght@400;700&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <style>
        body {
            padding-top: 70px;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            background-color: #0a0e27;
            color: #e8e8ff;
            font-family: 'Inter', sans-serif;
        }
        main {
            flex: 1;
        }
        .navbar {
            background-color: rgba(10, 14, 39, 0.7) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(100, 100, 255, 0.15);
        }
        .navbar-brand {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1.5rem;
        }
        .footer {
            background-color: #0a0e27;
            border-top: 1px solid rgba(100, 100, 255, 0.15);
            padding: 40px 0;
            color: #a0a0c0;
        }
        .footer h5 {
            color: #00d9ff;
            font-family: 'Space Grotesk', sans-serif;
        }
        .footer a {
            color: #a0a0c0;
            text-decoration: none;
            transition: color 0.3s;
        }
        .footer a:hover {
            color: #00d9ff;
        }

        .theme-button {
            padding: 10px 20px;
            background: linear-gradient(135deg, #00d9ff 0%, #9d4edd 100%);
            border: none;
            border-radius: 8px;
            color: #fff;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 217, 255, 0.2);
            text-decoration: none;
            display: inline-block;
        }

        .theme-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 217, 255, 0.4);
        }

        .navbar-nav.mx-auto {
            flex: 1;
            justify-content: center;
        }
        .navbar-nav .nav-link {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    {% block head %}{% endblock %}
</head>
<body>
    <header>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top shadow-sm">
            <div class="container-fluid">
                <a class="navbar-brand" href="{{ url_for('home') }}">◆ One Stop Store</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav mx-auto">
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('home') }}">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('view_cart') }}"><i class="fas fa-shopping-cart"></i> Cart <span id="cart-badge" class="badge bg-info rounded-pill ms-1" {% if cart_count == 0 %}style="display: none;"{% endif %}>{{ cart_count }}</span></a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('my_orders') }}"><i class="fas fa-box"></i> My Orders</a></li>
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('wishlist') }}"><i class="fas fa-heart"></i> Wishlist <span id="wishlist-badge" class="badge bg-info rounded-pill ms-1" {% if wishlist_count == 0 %}style="display: none;"{% endif %}>{{ wishlist_count }}</span></a></li>
                    </ul>
                    <div class="d-flex align-items-center">
                        <form class="d-flex me-1" action="{{ url_for('home') }}" method="get">
                            <input class="form-control form-control-sm" type="search" name="q" placeholder="Search" aria-label="Search" value="{{ request.args.get('q', '') }}">
                            <button class="btn btn-outline-info btn-sm" type="submit">Search</button>
                        </form>
                        {% block nav_form %}{% endblock %}
                    </div>
                    <ul class="navbar-nav ms-2">
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="locationDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="fas fa-map-marker-alt"></i> {% if session.location %}{{ session.location }}{% else %}Select Location{% endif %}
                            </a>
                            <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="locationDropdown">
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='USA') }}">USA</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='UK') }}">UK</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='Japan') }}">Japan</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='Australia') }}">Australia</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='India') }}">India</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='UAE') }}">UAE</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='Singapore') }}">Singapore</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='Canada') }}">Canada</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='Germany') }}">Germany</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('set_location', location='France') }}">France</a></li>
                            </ul>
                        </li>
                        {% if session.user %}
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    Hello, <b>{{ session.user }}</b>
                                </a>
                                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDropdown">
                                    <li><a class="dropdown-item" href="{{ url_for('profile') }}">Profile</a></li>
                                    <li><a class="dropdown-item" href="{{ url_for('logout') }}">Logout</a></li>
                                </ul>
                            </li>
                        {% else %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('register') }}">Register</a></li>
                        {% endif %}
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <main class="container my-5">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>

    <footer class="footer mt-auto py-3">
        <div class="container">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <h5>About Us</h5>
                    <p>Your one-stop destination for the best products, curated with passion and delivered with care.</p>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Quick Links</h5>
                    <ul class="list-unstyled">
                        <li><a href="{{ url_for('home') }}">Home</a></li>
                        <li><a href="#">About</a></li>
                        <li><a href="#">Contact</a></li>
                    </ul>
                </div>
                <div class="col-md-4 mb-3">
                    <h5>Contact</h5>
                    <ul class="list-unstyled">
                        <li><i class="fas fa-map-marker-alt me-2"></i> 123 Tech Lane, Future City</li>
                        <li><i class="fas fa-phone me-2"></i> (123) 456-7890</li>
                        <li><i class="fas fa-envelope me-2"></i> contact@onestopstore.com</li>
                    </ul>
                </div>
            </div>
            <hr style="border-color: rgba(100, 100, 255, 0.15);"/>
            <div class="text-center pt-3">
                <p>&copy; 2025 One Stop Store. All Rights Reserved.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const cartCountBadge = document.getElementById('cart-badge');
            const wishlistCountBadge = document.getElementById('wishlist-badge');
            const flashContainer = document.querySelector('main .container');

            // Function to display flash messages
            function displayFlashMessage(message, category) {
                const alertDiv = `<div class="alert alert-${category} alert-dismissible fade show" role="alert">
                                    ${message}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>`;
                flashContainer.insertAdjacentHTML('afterbegin', alertDiv);
            }

            // Handle Add to Cart
            document.querySelectorAll('.add-to-cart-btn').forEach(button => {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    const productId = this.dataset.productId;
                    const url = `/add_to_cart/${productId}`;
                    const currentButton = this; // Keep a reference to the button

                    fetch(url, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            if (cartCountBadge) {
                                cartCountBadge.textContent = data.cart_count;
                                cartCountBadge.style.display = data.cart_count > 0 ? 'inline-block' : 'none';
                            }
                            displayFlashMessage(data.message, 'success');

                            // Add the animation and change the button text
                            currentButton.classList.add('clicked', 'pop');
                            currentButton.textContent = 'Added!';

                            // Revert the button after a delay
                            setTimeout(() => {
                                currentButton.classList.remove('clicked', 'pop');
                                currentButton.textContent = 'Add to Cart';
                            }, 2000);
                        } else {
                            displayFlashMessage(data.message, 'danger');
                            if (data.message === 'Please log in first.') {
                                window.location.href = "{{ url_for('login') }}";
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        displayFlashMessage('An error occurred while adding to cart.', 'danger');
                    });
                });
            });

            // Handle Add to Wishlist
            document.querySelectorAll('.add-to-wishlist-btn').forEach(button => {
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    const productId = this.dataset.productId;

                    fetch('/add_to_wishlist/' + productId, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            if (wishlistCountBadge) {
                                wishlistCountBadge.textContent = data.wishlist_count;
                                wishlistCountBadge.style.display = data.wishlist_count > 0 ? 'inline-block' : 'none';
                            }
                            displayFlashMessage(data.message, 'success');
                        } else {
                            displayFlashMessage(data.message, 'danger');
                            if (data.message === 'Please log in first.') {
                                window.location.href = '{{ url_for('login') }}';
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        displayFlashMessage('An error occurred while adding to wishlist.', 'danger');
                    });
                });
            });

            // This script is a direct copy from the new login page design
            // It creates the animated background effect.
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('bg-canvas'), antialias: true, alpha: true });
            if (renderer.domElement) {
                renderer.setSize(window.innerWidth, window.innerHeight);
                renderer.setPixelRatio(window.devicePixelRatio);
                renderer.setClearColor(0x0a0e27, 1);
                camera.position.z = 5;

                const ambientLight = new THREE.AmbientLight(0x5050ff, 0.5);
                scene.add(ambientLight);
                const cyanLight = new THREE.PointLight(0x00d9ff, 1.5, 200); cyanLight.position.set(5, 3, 2); scene.add(cyanLight);
                const purpleLight = new THREE.PointLight(0x9d4edd, 1.5, 200); purpleLight.position.set(-5, -3, 2); scene.add(purpleLight);

                const particlesGeometry = new THREE.BufferGeometry();
                const particlesCount = 5000;
                const posArray = new Float32Array(particlesCount * 3);
                for (let i = 0; i < particlesCount * 3; i++) {
                    posArray[i] = (Math.random() - 0.5) * (Math.random() * 5) * 10;
                }
                particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
                const particlesMaterial = new THREE.PointsMaterial({ size: 0.015, color: 0x6080ff, blending: THREE.AdditiveBlending, transparent: true, opacity: 0.8 });
                const particles = new THREE.Points(particlesGeometry, particlesMaterial);
                scene.add(particles);

                let scrollY = window.scrollY;
                window.addEventListener('scroll', () => {
                    scrollY = window.scrollY;
                });

                const clock = new THREE.Clock();
                const animate = () => {
                    requestAnimationFrame(animate);
                    const elapsed = clock.getElapsedTime();
                    particles.rotation.y = elapsed * 0.05;
                    particles.position.y = -scrollY * 0.01; // Move particles as user scrolls
                    renderer.render(scene, camera);
                };
                animate();

                window.addEventListener('resize', () => {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                });
            }
        });
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
""",
    "cart.html": """{% extends "base.html" %}

{% block head %}
<style>
    .content-wrapper {
        max-width: 600px;
        margin: 40px auto;
        backdrop-filter: blur(10px);
        background: rgba(20, 25, 50, 0.4);
        border: 1px solid rgba(100, 100, 255, 0.15);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00d9ff, #9d4edd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
    }

    .cart-list {
        list-style: none;
        padding: 0;
        margin-bottom: 30px;
    }

    .cart-list li {
        background: rgba(30, 35, 70, 0.6);
        border: 1.5px solid rgba(100, 120, 255, 0.25);
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 15px;
        font-size: 1.1rem;
        color: #e0e0ff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px; /* Add gap between items */
        transition: all 0.3s ease;
    }

    .item-details {
        flex-grow: 1; /* Allow item details to take up available space */
    }

    .cart-list li:hover {
        border-color: rgba(0, 217, 255, 0.5);
        background: rgba(30, 40, 80, 0.8);
    }

    .item-details .discount-info {
        display: block;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    .item-details .original-price {
        text-decoration: line-through;
        color: #ff4d6d;
        margin-right: 8px;
    }

    .item-details .discounted-price {
        color: #50fa7b;
        font-weight: 600;
    }

    .total-section {
        text-align: right;
        font-size: 1.4rem;
        font-weight: 600;
        color: #50fa7b; /* Green for total */
        margin-bottom: 30px;
        padding-top: 20px;
        border-top: 1px solid rgba(100, 100, 255, 0.15);
    }

    .cart-actions {
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }

    .empty-cart-message {
        text-align: center;
        font-size: 1.2rem;
        color: #a0a0c0;
        padding: 40px 0;
    }

</style>
{% endblock %}

{% block content %}
<div class="content-wrapper">
    <h1 class="page-title">Your Shopping Cart</h1>

    {% if cart %}
        <ul class="cart-list">
    {% for item in cart %}
        <li>
            <div class="item-details">
                                    <span>{{ item.name }} - Rs.{{ "%.0f"|format(item.discounted_price) if item.get('discount', 0) > 0 else item.price }}</span>
                                    {% if item.get('discount', 0) > 0 %}
                                        <div class="discount-info">
                                            <span class="original-price">Rs.{{ item.original_price }}</span>
                                            <span class="discounted-price">Rs.{{ "%.0f"|format(item.discounted_price) }}</span>
                                            <span style="color: #ffb86c; font-size: 0.9em;"> ({{ item.discount }}% off)</span>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="item-quantity">
                                    <form action="{{ url_for('update_cart', pid=item.id) }}" method="post" style="display: flex; align-items: center; gap: 5px;">
                                        <a href="{{ url_for('decrease_quantity', pid=item.id) }}" class="theme-button" style="background: none; border: none;">-</a>
                                        <input type="number" name="quantity" value="{{ item.quantity }}" min="1" style="width: 60px; text-align: center;" onchange="this.form.submit()">
                                        <a href="{{ url_for('increase_quantity', pid=item.id) }}" class="theme-button" style="background: none; border: none;">+</a>
                                    </form>
                                </div>                                                    <div class="item-remove">
                                                        <a href="{{ url_for('remove_from_cart', pid=item.id) }}" class="theme-button" style="background: #ff4d6d;">Remove</a>
                                                    </div>        </li>
    {% endfor %}
</ul>

        <div class="total-section">
            Total: Rs.{{ total }}
        </div>

        <div class="cart-actions">
            <a href="{{ url_for('home') }}" class="theme-button" style="background: rgba(100, 120, 255, 0.3); flex-grow: 1; text-align: center;">Back to Shopping</a>
            <a href="{{ url_for('checkout') }}" class="theme-button" style="flex-grow: 1; text-align: center;">Proceed to Checkout</a>
        </div>

    {% else %}
        <div class="empty-cart-message">
            <p>Your cart is currently empty.</p>
        </div>
        <div class="cart-actions" style="justify-content: center;">
            <a href="{{ url_for('home') }}" class="theme-button">Start Shopping</a>
        </div>
    {% endif %}
</div>
{% endblock %}
""",
    "checkout.html": """{% extends "base.html" %}

{% block head %}
<style>
    .content-wrapper {
        max-width: 600px;
        margin: 40px auto;
        backdrop-filter: blur(10px);
        background: rgba(20, 25, 50, 0.4);
        border: 1px solid rgba(100, 100, 255, 0.15);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00d9ff, #9d4edd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
    }

    .order-summary-title {
        font-size: 1.2rem;
        color: #c0c0e0;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(100, 100, 255, 0.15);
    }

    .cart-list li {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-size: 1rem;
        color: #c0c0e0;
    }

    .total-section {
        text-align: right;
        font-size: 1.4rem;
        font-weight: 600;
        color: #50fa7b;
        margin: 20px 0 30px 0;
        padding-top: 20px;
        border-top: 1px solid rgba(100, 100, 255, 0.15);
    }

    .checkout-form .input-group {
        margin-bottom: 20px;
    }

    .checkout-form .form-input {
        width: 100%;
        padding: 14px 16px;
        background: rgba(30, 35, 70, 0.6);
        border: 1.5px solid rgba(100, 120, 255, 0.25);
        border-radius: 12px;
        color: #e8e8ff;
        font-size: 1rem;
        outline: none;
        transition: all 0.3s ease;
    }

    .checkout-form .form-input:focus {
        border-color: rgba(0, 217, 255, 0.6);
        background: rgba(30, 40, 80, 0.8);
    }

    .checkout-form textarea.form-input {
        min-height: 100px;
        resize: vertical;
    }

    .form-actions {
        display: flex;
        gap: 20px;
        margin-top: 30px;
    }

</style>
{% endblock %}

{% block content %}
<div class="content-wrapper">
    <h1 class="page-title">Checkout</h1>

    {% if cart %}
        <h2 class="order-summary-title">Order Summary</h2>
        <ul class="cart-list">
            {% for item in cart %}
                <li>
                    <span>{{ item.product }} - {{ item.name }} x {{ item.quantity }}</span>
                    <span>Rs.{{ "%.0f"|format(item.discounted_price) if item.get('discount', 0) > 0 else item.price }}</span>
                </li>
            {% endfor %}
        </ul>

        <div class="total-section">
            Amount to Pay: Rs.{{ total }}
        </div>

        <form class="checkout-form" method="post" action="{{ url_for('checkout') }}">
            <div class="input-group">
                <input type="text" name="name" placeholder="Full Name" class="form-input" required>
            </div>
            <div class="input-group">
                <textarea name="address" placeholder="Street Address" class="form-input" required></textarea>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="input-group">
                        <input type="text" name="city" placeholder="City" class="form-input" required>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="input-group">
                        <input type="text" name="pincode" placeholder="Pin Code" class="form-input" required>
                    </div>
                </div>
            </div>
            <div class="input-group">
                <input type="text" name="country" placeholder="Country" class="form-input" value="{% if session.location %}{{ session.location }}{% endif %}" required>
            </div>
            <div class="input-group">
                <select name="method" class="form-input" required>
                    <option value="" disabled selected>Select Payment Method</option>
                    <option value="Cash on Delivery">Cash on Delivery</option>
                    <option value="UPI">UPI</option>
                    <option value="Credit/Debit Card">Credit/Debit Card</option>
                </select>
            </div>
            <div class="form-actions">
                <a href="{{ url_for('view_cart') }}" class="theme-button" style="background: rgba(100, 120, 255, 0.3); text-align: center; flex-grow: 1;">Back to Cart</a>
                <button type="submit" class="theme-button" style="text-align: center; flex-grow: 1;">Confirm Order</button>
            </div>
        </form>

    {% else %}
        <div style="text-align: center; font-size: 1.2rem; color: #a0a0c0; padding: 40px 0;">
            <p>Your cart is empty. Nothing to check out.</p>
        </div>
        <div style="display: flex; justify-content: center;">
            <a href="{{ url_for('home') }}" class="theme-button">Start Shopping</a>
        </div>
    {% endif %}
</div>
{% endblock %}
""",
    "edit_profile.html": """{% extends "base.html" %}

{% block title %}Edit Profile - My E-Commerce{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <h3>Edit Profile</h3>
            <div class="card">
                <div class="card-body">
                    <form method="POST" action="{{ url_for('edit_profile') }}">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" class="form-control" id="username" name="username" value="{{ session['user'] }}">
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email address</label>
                            <input type="email" class="form-control" id="email" name="email" value="{{ session.get('email', session['user'] + '@example.com') }}">
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",
    "home.html": """{% extends "base.html" %}

{% block head %}
<style>
    /* Add canvas to the background */
    #bg-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1; /* Behind all content */
    }

    .page-header {
        text-align: center;
        margin-bottom: 40px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        gap: 20px;
    }

    .promo-text {
        font-size: 1.1rem;
        font-weight: 500;
        color: #a0a0c0;
        max-width: 250px;
        text-align: center;
        font-style: italic;
        border-left: 3px solid #00d9ff;
        padding-left: 15px;
    }

    .promo-text.right {
        border-left: none;
        border-right: 3px solid #9d4edd;
        padding-left: 0;
        padding-right: 15px;
    }

    .page-title {
        font-size: 3rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #e8e8ff 0%, #9d4edd 50%, #00d9ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }

    .category-section-title {
        font-size: 1.8rem;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
        color: #00d9ff;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(0, 217, 255, 0.2);
    }

    .products-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 30px;
    }

    .product-card {
        background-color: #1c1e3e; /* Solid dark color */
        border: 1px solid rgba(100, 100, 255, 0.1);
        border-radius: 8px; /* Slightly sharper corners */
        overflow: hidden;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 217, 255, 0.2);
        border-color: rgba(0, 217, 255, 0.3);
    }

    .product-card a {
        text-decoration: none;
        color: inherit;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }

    .product-image {
        width: 100%;
        height: 220px;
        object-fit: cover;
        /* Opacity removed for a sharper look */
    }

    .product-card:hover .product-image {
        opacity: 1;
    }

    .product-info {
        padding: 20px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    .product-variety {
        font-family: 'Lato', sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        color: #e0e0ff;
        margin-bottom: 8px;
    }

    .product-price {
        font-size: 1rem;
        margin-bottom: 15px;
    }

    .product-price .original-price {
        text-decoration: line-through;
        color: #ff4d6d;
        margin-right: 10px;
    }

    .product-price .discounted-price {
        color: #50fa7b;
        font-weight: 600;
    }

    .product-price .discount-tag {
        color: #ffb86c;
        font-size: 0.9em;
        margin-left: 8px;
        font-weight: 500;
    }

    .details-link {
        color: #00d9ff;
        font-size: 0.9rem;
        text-decoration: underline;
        margin-top: auto; /* Pushes to the bottom */
    }

    .card-actions {
        padding: 0 20px 20px 20px;
        display: flex;
        gap: 10px;
        margin-top: auto; /* Pushes to the bottom */
    }

    .add-to-cart-btn.clicked {
        background: linear-gradient(135deg, #50fa7b 0%, #32b562 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(80, 250, 123, 0.4);
    }

    @keyframes pop {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }

    .add-to-cart-btn.pop {
        animation: pop 0.3s ease-out;
    }

    .add-to-wishlist-btn {
        background: rgba(100, 120, 255, 0.2);
        color: #c0c0e0;
        border: 1px solid rgba(100, 120, 255, 0.3);
        padding: 10px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .add-to-wishlist-btn:hover {
        background: rgba(255, 77, 109, 0.3);
        color: #ff79c6;
        border-color: #ff79c6;
    }
    .horizontal-scroll-section {
        overflow-x: auto;
        white-space: nowrap;
        padding-bottom: 15px;
        margin-bottom: 30px;
    }
    .horizontal-scroll-section .product-card-horizontal {
        display: inline-block;
        width: 180px;
        margin-right: 15px;
        vertical-align: top;
        white-space: normal;
    }
    .product-card-horizontal .product-image-horizontal {
        width: 100%;
        height: 150px;
        object-fit: cover;
    }
    .product-card-horizontal .product-info-horizontal {
        padding: 10px;
    }
    .product-card-horizontal .product-variety-horizontal {
        font-size: 0.9rem;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .product-card-horizontal .card-actions {
        padding: 0 10px 10px 10px;
    }

    .product-card-horizontal .add-to-cart-btn {
        font-size: 0.8rem;
        padding: 8px 12px;
    }

    .product-card-horizontal .original-price {
        text-decoration: line-through;
        color: #ff4d6d;
        margin-right: 10px;
    }

</style>
{% endblock %}

{% block nav_form %}
<form class="d-flex align-items-center" action="{{ url_for('home') }}" method="get">
    <select name="category" class="form-select form-select-sm">
        <option value="">All Categories</option>
        {% for product_category in all_product_categories %}
            <option value="{{ product_category }}" {% if request.args.get('category') == product_category %}selected{% endif %}>{{ product_category }}</option>
        {% endfor %}
    </select>
    <button class="btn btn-outline-info btn-sm ms-1" type="submit">Apply</button>
</form>
{% endblock %}

{% block content %}
<canvas id="bg-canvas"></canvas>

<div class="page-header">
    <div class="promo-text">
        <p><strong>Curated Collections:</strong> Discover the latest trends and top brands, all in one place.</p>
    </div>
    <h1 class="page-title">Explore Our Products</h1>
    <div class="promo-text right">
        <p><strong>Seamless Shopping:</strong> Unbeatable prices and a smooth checkout experience, just for you.</p>
    </div>
</div>

<!-- Trending Products -->
<h2 class="category-section-title">Trending Products</h2>
<div class="horizontal-scroll-section">
    {% for product in trending_products %}
    <div class="product-card product-card-horizontal">
        <a href="{{ url_for('product_detail', pid=product.id) }}">
            <img src="{{ product.image_url }}" alt="{{ product.name }}" class="product-image-horizontal">
            <div class="product-info-horizontal">
                <div class="product-variety-horizontal">{{ product.name }}</div>
                <div class="product-price-horizontal">
                    {% if product.discount and product.discount > 0 %}
                        <span class="original-price">Rs.{{ product.price }}</span>
                        <span class="discounted-price">Rs.{{ product.price - (product.price * product.discount // 100) }}</span>
                        <span class="discount-tag">({{ product.discount }}% OFF)</span>
                    {% else %}
                        <span class="discounted-price">Rs.{{ product.price }}</span>
                    {% endif %}
                </div>
            </div>
        </a>
        {% if session.user %}
            <div class="card-actions">
                <button class="theme-button add-to-cart-btn" data-product-id="{{ product.id }}" style="flex-grow: 1; text-align: center;">Add to Cart</button>
                <button class="add-to-wishlist-btn" data-product-id="{{ product.id }}" data-product-name="{{ product.name }}" data-product-price="{{ product.price - (product.price * product.discount // 100) if product.discount and product.discount > 0 else product.price }}"><i class="fas fa-heart"></i></button>
            </div>
        {% endif %}
    </div>
    {% endfor %}
</div>

<!-- Latest Deals -->
<h2 class="category-section-title">Latest Deals</h2>
<div class="horizontal-scroll-section">
    {% for deal in deals %}
    <div class="product-card product-card-horizontal">
        <a href="{{ url_for('product_detail', pid=deal.id) }}">
            <img src="{{ deal.image_url }}" alt="{{ deal.name }}" class="product-image-horizontal">
            <div class="product-info-horizontal">
                <div class="product-variety-horizontal">{{ deal.name }}</div>
                <div class="product-price-horizontal">
                    <span class="original-price">Rs.{{ deal.price }}</span>
                    <span class="discounted-price">Rs.{{ deal.price - (deal.price * deal.discount // 100) }}</span>
                    <span class="discount-tag">({{ deal.discount }}% OFF)</span>
                </div>
            </div>
        </a>
        {% if session.user %}
            <div class="card-actions">
                <button class="theme-button add-to-cart-btn" data-product-id="{{ deal.id }}" style="flex-grow: 1; text-align: center;">Add to Cart</button>
                <button class="add-to-wishlist-btn" data-product-id="{{ deal.id }}" data-product-name="{{ deal.name }}" data-product-price="{{ deal.price - (deal.price * deal.discount // 100) if deal.discount and deal.discount > 0 else deal.price }}"><i class="fas fa-heart"></i></button>
            </div>
        {% endif %}
    </div>
    {% endfor %}
</div>

{% set categories = products | map(attribute='name') | unique | list %}

{% for category in categories %}
    {% set cat_products = products | selectattr('name', 'equalto', category) | list %}
    {% if cat_products and cat_products[0].varieties %}
        <section class="product-category-section" style="margin-bottom:40px;">
            <h2 class="category-section-title">{{ category }}</h2>
            <div class="products-list">
                {% for variety in cat_products[0].varieties %}
                <div class="product-card" data-name="{{ category }}" data-variety="{{ variety.name }}" data-price="{{ variety.price - (variety.price * variety.discount // 100) if variety.discount and variety.discount > 0 else variety.price }}">
                    <a href="{{ url_for('product_detail', pid=variety.id) }}">
                        <img src="{{ variety.image_url }}" alt="{{ variety.name }}" class="product-image">
                        <div class="product-info">
                            <span class="product-variety">{{ variety.name }}</span>
                            <div class="product-price">
                                {% if variety.discount and variety.discount > 0 %}
                                    <span class="original-price">Rs.{{ variety.price }}</span>
                                    <span class="discounted-price">Rs.{{ variety.price - (variety.price * variety.discount // 100) }}</span>
                                    <span class="discount-tag">({{ variety.discount }}% OFF)</span>
                                {% else %}
                                    <span class="discounted-price">Rs.{{ variety.price }}</span>
                                {% endif %}
                            </div>
                            <span class="details-link">View Details</span>
                        </div>
                    </a>
                    {% if session.user %}
                        <div class="card-actions">
                            <button class="theme-button add-to-cart-btn" data-product-id="{{ variety.id }}" style="flex-grow: 1; text-align: center;">Add to Cart</button>
                            <button class="add-to-wishlist-btn" data-product-id="{{ variety.id }}" data-product-name="{{ variety.name }}" data-product-price="{{ variety.price - (variety.price * variety.discount // 100) if variety.discount and variety.discount > 0 else variety.price }}"><i class="fas fa-heart"></i></button>
                        </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </section>
    {% endif %}
{% endfor %}

{% endblock %}
""",
    "landing.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>One Stop Store | Welcome</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: #0a0e27;
            color: #e8e8ff;
            overflow: hidden;
            line-height: 1.6;
        }

        #bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .wrapper {
            width: 100%;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }

        .content-container {
            max-width: 900px;
            animation: slideUp 1s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .logo {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
            margin-bottom: 20px;
            letter-spacing: -2px;
            text-shadow: 0 0 40px rgba(0, 217, 255, 0.4);
        }

        .main-subtitle {
            font-size: 1.3rem;
            color: #b0b0d0;
            font-weight: 300;
            line-height: 1.8;
            margin-bottom: 20px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        .philosophy-text {
            font-size: 1rem;
            color: #a0a0c0;
            margin-bottom: 40px;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        .cta-button {
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(135deg, #00d9ff 0%, #9d4edd 100%);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 1.1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(0, 217, 255, 0.3);
            text-transform: uppercase;
            text-decoration: none;
            position: relative;
            overflow: hidden;
            font-family: 'Inter', sans-serif;
        }

        .cta-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .cta-button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 30px rgba(0, 217, 255, 0.5);
        }

        .cta-button:hover::before {
            left: 100%;
        }

        @media (max-width: 768px) {
            body { overflow-y: auto; }
            .wrapper { position: relative; height: auto; padding: 60px 20px; }
            .logo { font-size: 3rem; }
            .main-subtitle { font-size: 1.1rem; }
        }
    </style>
</head>
<body>

    <div class="wrapper">
        <canvas id="bg-canvas"></canvas>
        <div class="content-container">
            <h1 class="logo">◆ One Stop Store</h1>
            <p class="main-subtitle">
                Engineered for speed, curated for excellence.
            </p>
            <p class="philosophy-text">
                Inspired by the high-stakes world of performance racing, our name comes from the legendary "One-Stop" strategy &mdash; a commitment to winning with a single, perfectly executed stop. We bring you a curated selection of elite products, so you can skip the endless searching and get everything you need in one perfect stop. This is shopping, engineered for the win.
            </p>
            <a href="{{ url_for('home') }}" class="cta-button">Enter the Fast Lane</a>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('bg-canvas'), antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setClearColor(0x0a0e27, 1);
        camera.position.z = 5;

        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 8000;
        const posArray = new Float32Array(particlesCount * 3);
        for (let i = 0; i < particlesCount * 3; i += 3) {
            posArray[i] = (Math.random() - 0.5) * 50;
            posArray[i + 1] = (Math.random() - 0.5) * 50;
            posArray[i + 2] = (Math.random() - 0.5) * 50;
        }
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particlesMaterial = new THREE.PointsMaterial({ size: 0.02, color: 0x6080ff, transparent: true, opacity: 0.6, sizeAttenuation: true, blending: THREE.AdditiveBlending });
        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particles);

        let mouseX = 0, mouseY = 0;
        document.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
        });

        const clock = new THREE.Clock();
        const animate = () => {
            requestAnimationFrame(animate);
            const elapsed = clock.getElapsedTime();
            particles.rotation.y = elapsed * 0.02;
            particles.rotation.x = elapsed * 0.01;

            let targetCameraX = mouseX * 0.3;
            let targetCameraY = mouseY * 0.3;
            camera.position.x += (targetCameraX - camera.position.x) * 0.05;
            camera.position.y += (targetCameraY - camera.position.y) * 0.05;
            camera.lookAt(scene.position);

            renderer.render(scene, camera);
        };
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
""",
    "login.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>One Stop Store | Login</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <style>
        /* ======================================= */
        /* === COPIED CSS FROM NEW DESIGN START === */
        /* ======================================= */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: #0a0e27;
            color: #e8e8ff;
            overflow: hidden;
            line-height: 1.6;
        }

        /* Canvas background */
        #bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            display: block;
        }

        /* Main container */
        .wrapper {
            position: fixed;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2;
            pointer-events: none;
        }

        /* Left side - Branding (Adjusted for simpler E-commerce use) */
        .landing-left {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            padding-left: 8%;
            pointer-events: all;
            max-width: 50%;
        }

        .brand-section {
            margin-bottom: 60px;
        }

        .logo {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
            margin-bottom: 15px;
            letter-spacing: -2px;
            text-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
        }

        .tagline {
            font-size: 1.1rem;
            color: #a0a0ff;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .hero-text {
            margin-top: 40px;
            max-width: 500px;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #e8e8ff 0%, #9d4edd 50%, #00d9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
        }

        .hero-subtitle {
            font-size: 1.2rem;
            color: #b0b0d0;
            font-weight: 300;
            line-height: 1.8;
            margin-bottom: 40px;
        }

        .features-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 30px;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.95rem;
            color: #c0c0e0;
            opacity: 0.9;
            transition: all 0.3s ease;
        }

        .feature-item:hover {
            color: #00d9ff;
            transform: translateX(5px);
        }

        .feature-icon {
            width: 6px;
            height: 6px;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            border-radius: 50%;
        }

        /* Right side - Form */
        .landing-right {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            pointer-events: all;
        }

        .form-container {
            width: 100%;
            max-width: 420px;
            backdrop-filter: blur(10px);
            background: rgba(20, 25, 50, 0.4);
            border: 1px solid rgba(100, 100, 255, 0.15);
            border-radius: 20px;
            padding: 50px 40px;
            box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1),
                        inset 0 1px 1px rgba(255, 255, 255, 0.1);
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .form-header {
            text-align: center;
            margin-bottom: 45px;
        }

        .form-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
        }

        .form-subtitle {
            font-size: 0.9rem;
            color: #a0a0c0;
            font-weight: 300;
        }

        /* FLASK MESSAGE STYLE */
        .flask-messages {
            margin-bottom: 20px;
            text-align: center;
            font-size: 1rem;
            color: #ff3366; /* Error color for general flash messages */
            background: rgba(255, 51, 102, 0.15);
            border: 1px solid rgba(255, 51, 102, 0.3);
            padding: 10px;
            border-radius: 8px;
        }

        .input-group {
            position: relative;
            margin-bottom: 20px;
        }

        .input-label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: #a0a0ff;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-icon {
            position: absolute;
            left: 16px;
            color: #6080c0;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            pointer-events: none;
        }

        .form-input {
            width: 100%;
            padding: 14px 16px 14px 48px;
            background: rgba(30, 35, 70, 0.6);
            border: 1.5px solid rgba(100, 120, 255, 0.25);
            border-radius: 12px;
            color: #e8e8ff;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(4px);
        }

        .form-input::placeholder {
            color: #7080b0;
        }

        .form-input:focus {
            border-color: rgba(0, 217, 255, 0.6);
            background: rgba(30, 40, 80, 0.8);
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.25),
                        inset 0 0 10px rgba(0, 217, 255, 0.1);
        }

        .form-input:focus + .input-icon {
            color: #00d9ff;
            transform: scale(1.2);
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.6);
        }

        .options-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            font-size: 0.9rem;
        }

        .remember-me {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            color: #a0a0c0;
            transition: color 0.3s ease;
        }

        .remember-me input {
            cursor: pointer;
            width: 20px; /* Increased width */
            height: 20px; /* Increased height */
            accent-color: #00d9ff;
            vertical-align: middle; /* Improved alignment */
        }

        .remember-me:hover {
            color: #00d9ff;
        }

        .forgot-password {
            color: #00d9ff;
            text-decoration: none;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .forgot-password:hover {
            color: #9d4edd;
            text-decoration: underline;
        }

        .login-button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #00d9ff 0%, #9d4edd 100%);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(0, 217, 255, 0.3);
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
            font-family: 'Inter', sans-serif;
        }

        .login-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .login-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 217, 255, 0.5);
        }

        .login-button:hover::before {
            left: 100%;
        }

        .login-button:active {
            transform: translateY(0);
        }

        .signup-text {
            text-align: center;
            margin-top: 25px;
            font-size: 0.9rem;
            color: #a0a0c0;
        }

        .signup-link {
            color: #00d9ff;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .signup-link:hover {
            color: #9d4edd;
        }

        /* Gradient orb effect */
        .gradient-orb {
            position: fixed;
            pointer-events: none;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.3;
            z-index: 0;
        }

        .orb-1 {
            width: 400px;
            height: 400px;
            background: linear-gradient(135deg, #00d9ff, transparent);
            top: -100px;
            right: -100px;
            animation: float 20s ease-in-out infinite;
        }

        .orb-2 {
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #9d4edd, transparent);
            bottom: -50px;
            left: -50px;
            animation: float 25s ease-in-out infinite reverse;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(30px, 30px); }
        }

        .show-password-checkbox {
            width: 20px;
            height: 20px;
            accent-color: #00d9ff;
            vertical-align: middle; /* Improved alignment */
        }

        /* Responsive design */
        @media (max-width: 1024px) {
            .landing-left {
                max-width: 60%;
                padding-left: 5%;
            }

            .hero-title {
                font-size: 2.8rem;
            }

            .landing-right {
                max-width: 40%;
            }
        }

        @media (max-width: 768px) {
            .wrapper {
                flex-direction: column;
                padding: 40px 20px;
                position: relative; /* Allow content to scroll if needed */
                overflow-y: auto;
                height: auto;
            }

            .landing-left {
                max-width: 100%;
                padding-left: 0;
                text-align: center;
                margin-bottom: 40px;
            }
            .brand-section {
                align-items: center;
                text-align: center;
            }
            .landing-left .logo, .landing-left .tagline {
                margin: 0 auto 15px auto;
                background: linear-gradient(135deg, #00d9ff, #9d4edd);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hero-title {
                font-size: 2.2rem;
            }

            .hero-subtitle {
                font-size: 1rem;
            }

            .landing-right {
                max-width: 100%;
                margin-bottom: 40px;
            }

            .form-container {
                max-width: 100%;
            }
            /* Re-enable scrolling for body on small screens */
            body {
                overflow-y: auto;
                overflow-x: hidden;
            }
        }
        /* ===================================== */
        /* === COPIED CSS FROM NEW DESIGN END === */
        /* ===================================== */
    </style>
</head>
<body>

    <div class="gradient-orb orb-1"></div>
    <div class="gradient-orb orb-2"></div>

    <canvas id="bg-canvas"></canvas>

    <div class="wrapper">
        <div class="landing-left">
            <div class="brand-section">
                <a href="{{ url_for('landing') }}" class="logo">◆ One Stop Store</a>
                <div class="tagline">The Future of E-commerce Access</div>
            </div>

            <div class="hero-text">
                <h1 class="hero-title">Discover Your Next Great Purchase Securely</h1>
                <p class="hero-subtitle">Access your account now for seamless shopping, personalized offers, and secure order tracking.</p>

                <div class="features-list">
                    <div class="feature-item">
                        <div class="feature-icon"></div>
                        <span>Exclusive user deals and flash sales</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon"></div>
                        <span>Personalized product recommendations</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon"></div>
                        <span>Fast, secure checkout experience</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="landing-right">
            <div class="form-container">
                <div class="form-header">
                    <h2 class="form-title">Account Access</h2>
                    <p class="form-subtitle">Enter your credentials to start shopping</p>
                </div>

                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        <div class="flask-messages">
                            {% for message in messages %}
                                {{ message }}<br>
                            {% endfor %}
                        </div>
                    {% endif %}
                {% endwith %}

                <form method="post"> 
                    <div class="input-group">
                        <label class="input-label" for="username">Username</label>
                        <div class="input-wrapper">
                            <input type="text" class="form-input" id="username" name="username" placeholder="Your username" required autocomplete="username">
                            <i class="fas fa-user input-icon"></i> 
                        </div>
                    </div>

                    <div class="input-group">
                        <label class="input-label" for="password">Password</label>
                        <div class="input-wrapper">
                            <input type="password" class="form-input" id="password" name="password" placeholder="••••••••" required autocomplete="current-password">
                            <i class="fas fa-lock input-icon"></i>
                        </div>
                        <div style="margin-top: 10px;">
                            <input type="checkbox" class.show-password-checkbox" onclick="showPassword()"> Show Password
                        </div>
                    </div>

                    <div class="options-row">
                        <label class="remember-me">
                            <input type="checkbox">
                            <span>Remember me</span>
                        </label>
                        <a href="#" class="forgot-password">Forgot Password?</a>
                    </div>

                    <button type="submit" class="login-button">Log In</button>
                </form>

                <div class="signup-text">
                    Don't have an account? <a href="{{ url_for('register') }}" class="signup-link">Create one now</a>
                </div>
                <div class="signup-text" style="margin-top: 10px;">
                    <a href="{{ url_for('landing') }}" class="signup-link">Back to Welcome</a>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script>
        // ========== SCENE SETUP ==========
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({
            canvas: document.getElementById('bg-canvas'),
            antialias: true,
            alpha: true
        });

        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setClearColor(0x0a0e27, 1);
        camera.position.z = 5;

        // ========== LIGHTING ==========
        const ambientLight = new THREE.AmbientLight(0x5050ff, 0.5);
        scene.add(ambientLight);

        // Cyan light
        const cyanLight = new THREE.PointLight(0x00d9ff, 2, 150);
        cyanLight.position.set(8, 5, 3);
        scene.add(cyanLight);

        // Purple light
        const purpleLight = new THREE.PointLight(0x9d4edd, 2, 150);
        purpleLight.position.set(-8, -5, 3);
        scene.add(purpleLight);

        // ========== BACKGROUND PARTICLES ==========
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 8000;
        const posArray = new Float32Array(particlesCount * 3);

        for (let i = 0; i < particlesCount * 3; i += 3) {
            posArray[i] = (Math.random() - 0.5) * 50;
            posArray[i + 1] = (Math.random() - 0.5) * 50;
            posArray[i + 2] = (Math.random() - 0.5) * 50;
        }

        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

        const particlesMaterial = new THREE.PointsMaterial({
            size: 0.02,
            color: 0x6080ff,
            transparent: true,
            opacity: 0.6,
            sizeAttenuation: true,
            blending: THREE.AdditiveBlending
        });

        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particles);

        // ========== FLOATING GEOMETRIC OBJECTS ==========
        const geometries = [
            new THREE.IcosahedronGeometry(0.8, 4),
            new THREE.TetrahedronGeometry(1),
            new THREE.OctahedronGeometry(0.7)
        ];

        const objects = [];

        geometries.forEach((geom, idx) => {
            const material = new THREE.MeshPhysicalMaterial({
                color: idx % 2 === 0 ? 0x00d9ff : 0x9d4edd,
                wireframe: true,
                transparent: true,
                opacity: 0.2,
                emissive: idx % 2 === 0 ? 0x00d9ff : 0x9d4edd,
                emissiveIntensity: 0.3
            });

            const obj = new THREE.Mesh(geom, material);
            obj.position.set(
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 15 - 10
            );
            obj.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
            obj.scale.set(1.5, 1.5, 1.5);

            scene.add(obj);
            objects.push({
                mesh: obj,
                speed: Math.random() * 0.002 + 0.001,
                rotationSpeed: Math.random() * 0.005 + 0.001
            });
        });

        // ========== GLOWING TORUS ==========
        const torusGeometry = new THREE.TorusGeometry(3, 0.3, 16, 64);
        const torusMaterial = new THREE.MeshPhysicalMaterial({
            color: 0x00d9ff,
            emissive: 0x00d9ff,
            emissiveIntensity: 0.5,
            wireframe: false,
            transparent: true,
            opacity: 0.3,
            metalness: 0.8,
            roughness: 0.2
        });

        const torus = new THREE.Mesh(torusGeometry, torusMaterial);
        torus.position.set(-8, 3, -8);
        torus.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
        scene.add(torus);

        // ========== MOUSE INTERACTION ==========
        let mouseX = 0, mouseY = 0;
        let targetCameraX = 0, targetCameraY = 0;

        document.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
        });

        // ========== ANIMATION LOOP ==========
        const clock = new THREE.Clock();

        const animate = () => {
            requestAnimationFrame(animate);
            const elapsed = clock.getElapsedTime();

            // Particle rotation
            particles.rotation.y = elapsed * 0.02;
            particles.rotation.x = elapsed * 0.01;

            // Animate objects
            objects.forEach((obj) => {
                obj.mesh.rotation.x += obj.rotationSpeed;
                obj.mesh.rotation.y += obj.rotationSpeed * 0.7;
                obj.mesh.position.y += Math.sin(elapsed * obj.speed) * 0.01;
            });

            // Torus animation
            torus.rotation.x += 0.003;
            torus.rotation.z += 0.002;

            // Lights orbiting
            cyanLight.position.x = Math.sin(elapsed * 0.3) * 12;
            cyanLight.position.z = Math.cos(elapsed * 0.3) * 12;

            purpleLight.position.x = Math.cos(elapsed * 0.4) * 12;
            purpleLight.position.z = Math.sin(elapsed * 0.4) * 12;

            // Smooth camera follow
            targetCameraX = mouseX * 0.3;
            targetCameraY = mouseY * 0.3;

            camera.position.x += (targetCameraX - camera.position.x) * 0.05;
            camera.position.y += (targetCameraY - camera.position.y) * 0.05;
            camera.lookAt(scene.position);

            renderer.render(scene, camera);
        };

        animate();

        // ========== RESIZE HANDLER ==========
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        function showPassword() {
            var password = document.getElementById("password");
            if (password.type === "password") {
                password.type = "text";
            } else {
                password.type = "password";
            }
        }

        // NOTE: Removed the original alert('Authentication initiated!') JavaScript form handler
        // to allow the Flask form submission to work correctly.
    </script>
</body>
</html>
""",
    "order_detail.html": """{% extends "base.html" %}

{% block title %}Order Details - My E-Commerce{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="card">
        <div class="card-header">
            <h2>Order #{{ order.id }}</h2>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <h4>Shipping Address</h4>
                    <p><strong>Name:</strong> {{ order.name }}</p>
                    <p><strong>Address:</strong> {{ order.address }}</p>
                    <p><strong>City:</strong> {{ order.city }}</p>
                    <p><strong>Pincode:</strong> {{ order.pincode }}</p>
                    <p><strong>Country:</strong> {{ order.country }}</p>
                </div>
                <div class="col-md-6">
                    <h4>Payment Method</h4>
                    <p><strong>Method:</strong> {{ order.method }}</p>
                    <p><strong>Estimated Delivery:</strong> {{ order.delivery_date }}</p>
                </div>
            </div>
            <hr>
            <h4>Items</h4>
            <ul class="list-group">
                {% for item in order.order_items %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="my-0">{{ item.name }} x {{ item.quantity }}</h6>
                            <small class="text-muted">{{ item.product }}</small>
                        </div>
                        <span>₹{{ "%.2f"|format(item.discounted_price) }}</span>
                    </li>
                {% endfor %}
            </ul>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
            <h4>Total: ₹{{ "%.2f"|format(order.total) }}</h4>
            <a href="{{ url_for('profile') }}" class="btn btn-primary">Back to Profile</a>
        </div>
    </div>
</div>
{% endblock %}
""",
    "orders.html": """{% extends "base.html" %}

{% block head %}
<style>
    .content-wrapper {
        max-width: 800px;
        margin: 40px auto;
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00d9ff, #9d4edd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 40px;
    }

    .order-block {
        backdrop-filter: blur(10px);
        background: rgba(20, 25, 50, 0.4);
        border: 1px solid rgba(100, 100, 255, 0.15);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
    }

    .order-header h2 {
        font-size: 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        color: #00d9ff;
        margin: 0 0 20px 0;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(100, 100, 255, 0.15);
    }

    .order-details p {
        margin: 0 0 10px 0;
        color: #c0c0e0;
        font-size: 1rem;
    }

    .order-details p strong {
        color: #e0e0ff;
        font-weight: 600;
    }

    .products-title {
        font-size: 1.2rem;
        color: #c0c0e0;
        margin-top: 25px;
        margin-bottom: 15px;
        padding-top: 15px;
        border-top: 1px solid rgba(100, 100, 255, 0.15);
    }

    .product-list {
        list-style: none;
        padding: 0;
    }

    .product-list li {
        background: rgba(30, 35, 70, 0.6);
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
    }

    .order-total {
        text-align: right;
        font-size: 1.4rem;
        font-weight: 600;
        color: #50fa7b;
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(100, 100, 255, 0.15);
    }

    .no-orders-message, .back-action {
        text-align: center;
        margin-top: 20px;
    }

    .no-orders-message p {
        font-size: 1.2rem;
        color: #a0a0c0;
    }

</style>
{% endblock %}

{% block content %}
<div class="content-wrapper">
    <h1 class="page-title">My Order History</h1>

    {% if user_orders %}
        {% for order in user_orders %}
            <div class="order-block">
                <div class="order-header">
                    <h2>Order #{{ order.id }}</h2>
                </div>
                <div class="order-details">
                    <p><strong>Shipping To:</strong> {{ order.name }}</p>
                    <p><strong>Address:</strong> {{ order.address }}, {{ order.city }}, {{ order.pincode }}, {{ order.country }}</p>
                    <p><strong>Payment Method:</strong> {{ order.method }}</p>
                    <p><strong>Estimated Delivery:</strong> {{ order.delivery_date }}</p>
                </div>

                <h3 class="products-title">Products Ordered:</h3>
                <ul class="product-list">
                    {% for item in order.order_items %}
                        <li>
                            <span>{{ item.name }} ({{ item.product }}) x {{ item.quantity }}</span>
                            <span>Rs.{{ "%.0f"|format(item.discounted_price) if item.get('discount', 0) > 0 else item.price }}</span>
                        </li>
                    {% endfor %}
                </ul>

                <div class="order-total">
                    Order Total: Rs.{{ "%.2f"|format(order.total) }}
                </div>
            </div>
        {% endfor %}
    {% else %}
        <div class="no-orders-message">
            <p>You haven't placed any orders yet.</p>
        </div>
    {% endif %}

    <div class="back-action">
        <a href="{{ url_for('home') }}" class="theme-button">Back to Home</a>
    </div>
</div>
{% endblock %}
""",
    "product_detail.html": """{% extends "base.html" %}

{% block head %}
<style>
    .product-detail-wrapper {
        max-width: 1000px;
        margin: 40px auto;
        display: flex;
        gap: 40px;
        backdrop-filter: blur(10px);
        background: rgba(20, 25, 50, 0.4);
        border: 1px solid rgba(100, 100, 255, 0.15);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
    }

    .product-image-container {
        flex: 1;
    }

    .product-image-large {
        width: 100%;
        border-radius: 16px;
        object-fit: cover;
    }

    .product-info-container {
        flex: 1.2;
    }

    .product-title {
        font-size: 2.2rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        color: #e0e0ff;
        margin: 0 0 15px 0;
    }

    .product-price-details {
        font-size: 1.5rem;
        margin-bottom: 25px;
    }

    .product-price-details .original-price {
        text-decoration: line-through;
        color: #ff4d6d;
        font-size: 1.2rem;
        margin-right: 10px;
    }

    .product-price-details .discounted-price {
        color: #50fa7b;
        font-weight: 600;
    }

    .product-price-details .discount-tag {
        color: #ffb86c;
        font-size: 1rem;
        margin-left: 8px;
        font-weight: 500;
    }

    .details-title {
        font-size: 1.3rem;
        color: #00d9ff;
        font-family: 'Space Grotesk', sans-serif;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(0, 217, 255, 0.2);
    }

    .product-details-list {
        list-style: none;
        padding: 0;
        color: #c0c0e0;
    }

    .product-details-list li {
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(100, 120, 255, 0.1);
        padding-bottom: 10px;
    }

    .product-details-list li b {
        color: #e0e0ff;
        font-weight: 600;
        min-width: 120px;
        display: inline-block;
    }

    .page-actions {
        margin-top: 30px;
        display: flex;
        gap: 15px;
        align-items: center;
    }

</style>
{% endblock %}

{% block content %}
<div class="product-detail-wrapper">
    <div class="product-image-container">
        <img src="{{ variety.image_url.replace('400x300', '500x500') if variety.image_url else 'https://source.unsplash.com/500x500/?' + variety.name.replace(' ', '+') }}" alt="{{ variety.name }}" class="product-image-large">
    </div>

    <div class="product-info-container">
        <h1 class="product-title">{{ variety.product }} - {{ variety.name }}</h1>
        
        <div class="product-price-details">
            {% if variety.discount and variety.discount > 0 %}
                <span class="original-price">Rs.{{ variety.price }}</span>
                <span class="discounted-price">Rs.{{ variety.price - (variety.price * variety.discount // 100) }}</span>
                <span class="discount-tag">({{ variety.discount }}% OFF{% if variety.occasion %} - {{ variety.occasion }}{% endif %})</span>
            {% else %}
                <span class="discounted-price">Rs.{{ variety.price }}</span>
            {% endif %}
        </div>

        <div class="page-actions">
            {% if session.user %}
                <button class="theme-button add-to-cart-btn" data-product-id="{{ variety.id }}">Add to Cart</button>
            {% endif %}
            <button class="add-to-wishlist-btn theme-button" data-product-id="{{ variety.id }}" data-product-name="{{ variety.name }}" data-product-price="{{ variety.price - (variety.price * variety.discount // 100) if variety.discount and variety.discount > 0 else variety.price }}" style="background: rgba(100, 120, 255, 0.3);"><i class="fas fa-heart"></i> Add to Wishlist</button>
            <a href="{{ url_for('home') }}" class="theme-button" style="background: transparent; border: 1px solid rgba(100, 120, 255, 0.3);">Back to Products</a>
        </div>

        <h2 class="details-title">Product Details</h2>
        <ul class="product-details-list">
            {% for key, value in variety.details.items() %}
                <li><b>{{ key }}:</b> {{ value }}</li>
            {% endfor %}
        </ul>
    </div>
</div>
{% endblock %}
""",
    "profile.html": """{% extends "base.html" %}

{% block title %}User Profile - My E-Commerce{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ session['user'] }}</h5>
                    <p class="card-text text-muted">Welcome to your profile</p>
                </div>
                <div class="list-group list-group-flush">
                    <a href="#profile" class="list-group-item list-group-item-action active" data-bs-toggle="tab">Profile</a>
                    <a href="#orders" class="list-group-item list-group-item-action" data-bs-toggle="tab">Orders</a>
                    <a href="#addresses" class="list-group-item list-group-item-action" data-bs-toggle="tab">Saved Addresses</a>
                </div>
            </div>
        </div>
        <div class="col-md-9">
            <div class="tab-content">
                <div class="tab-pane fade show active" id="profile">
                    <h3>Profile Information</h3>
                    <div class="card">
                        <div class="card-body">
                            <p><strong>Username:</strong> {{ session['user'] }}</p>
                            <p><strong>Email:</strong> {{ session.get('email', session['user'] + '@example.com') }}</p>
                            <a href="{{ url_for('edit_profile') }}" class="btn btn-primary">Edit Profile</a>
                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="orders">
                    <h3>My Order History</h3>
                    {% if user_orders %}
                        {% for order in user_orders %}
                            <div class="card mb-3">
                                <div class="card-header d-flex justify-content-between">
                                    <span>Order #{{ order.id }}</span>
                                    <span>Total: ₹{{ "%.2f"|format(order.total) }}</span>
                                </div>
                                <div class="card-body">
                                    <p><strong>Shipping to:</strong> {{ order.name }} at {{ order.address }}, {{ order.city }}</p>
                                    <p><strong>Estimated Delivery:</strong> {{ order.delivery_date }}</p>
                                    <h6>Items:</h6>
                                    <ul class="list-group">
                                        {% for item in order.order_items %}
                                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                                {{ item.name }} x {{ item.quantity }}
                                                <span>₹{{ "%.2f"|format(item.discounted_price) }}</span>
                                            </li>
                                        {% endfor %}
                                    </ul>
                                </div>
                                <div class="card-footer">
                                    <a href="{{ url_for('order_details', order_id=order.id) }}" class="btn btn-primary btn-sm">View Details</a>
                                </div>
                            </div>
                        {% endfor %}
                    {% else %}
                        <p>You have no past orders.</p>.
                    {% endif %}
                </div>
                <div class="tab-pane fade" id="addresses">
                    <h3>Saved Addresses</h3>
                    <div class="card">
                        <div class="card-body">
                            {% if session['addresses'] %}
                                {% for address in session['addresses'] %}
                                    <div class="mb-3 d-flex justify-content-between align-items-start">
                                        <div>
                                            <strong>{{ address.name }}</strong><br>
                                            {{ address.address }}<br>
                                            {{ address.city }}, {{ address.pincode }}<br>
                                            {{ address.country }}
                                        </div>
                                        <a href="{{ url_for('delete_address', address_index=loop.index0) }}" class="btn btn-danger btn-sm">Delete</a>
                                    </div>
                                    <hr>
                                {% endfor %}
                            {% else %}
                                <p>You have no saved addresses.</p>
                            {% endif %}
                            <a href="{{ url_for('add_address') }}" class="btn btn-primary">Add New Address</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",
    "register.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>One Stop Store | Register</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <style>
        /* ======================================= */
        /* === COPIED CSS FROM NEW DESIGN START === */
        /* ======================================= */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: #0a0e27;
            color: #e8e8ff;
            overflow: hidden;
            line-height: 1.6;
        }

        /* Canvas background */
        #bg-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            display: block;
        }

        /* Main container */
        .wrapper {
            position: fixed;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2;
            pointer-events: none;
        }

        /* Left side - Branding (Adjusted for simpler E-commerce use) */
        .landing-left {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
            padding-left: 8%;
            pointer-events: all;
            max-width: 50%;
        }

        .brand-section {
            margin-bottom: 60px;
        }

        .logo {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
            margin-bottom: 15px;
            letter-spacing: -2px;
            text-shadow: 0 0 30px rgba(0, 217, 255, 0.3);
        }

        .tagline {
            font-size: 1.1rem;
            color: #a0a0ff;
            font-weight: 300;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .hero-text {
            margin-top: 40px;
            max-width: 500px;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #e8e8ff 0%, #9d4edd 50%, #00d9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
        }

        .hero-subtitle {
            font-size: 1.2rem;
            color: #b0b0d0;
            font-weight: 300;
            line-height: 1.8;
            margin-bottom: 40px;
        }

        .features-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-top: 30px;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.95rem;
            color: #c0c0e0;
            opacity: 0.9;
            transition: all 0.3s ease;
        }

        .feature-item:hover {
            color: #00d9ff;
            transform: translateX(5px);
        }

        .feature-icon {
            width: 6px;
            height: 6px;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            border-radius: 50%;
        }

        /* Right side - Form */
        .landing-right {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            pointer-events: all;
        }

        .form-container {
            width: 100%;
            max-width: 420px;
            backdrop-filter: blur(10px);
            background: rgba(20, 25, 50, 0.4);
            border: 1px solid rgba(100, 100, 255, 0.15);
            border-radius: 20px;
            padding: 50px 40px;
            box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1),
                        inset 0 1px 1px rgba(255, 255, 255, 0.1);
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .form-header {
            text-align: center;
            margin-bottom: 45px;
        }

        .form-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #00d9ff, #9d4edd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-family: 'Space Grotesk', sans-serif;
        }

        .form-subtitle {
            font-size: 0.9rem;
            color: #a0a0c0;
            font-weight: 300;
        }

        /* FLASK MESSAGE STYLE */
        .flask-messages {
            margin-bottom: 20px;
            text-align: center;
            font-size: 1rem;
            color: #ff3366; /* Error color for general flash messages */
            background: rgba(255, 51, 102, 0.15);
            border: 1px solid rgba(255, 51, 102, 0.3);
            padding: 10px;
            border-radius: 8px;
        }

        .input-group {
            position: relative;
            margin-bottom: 20px;
        }

        .input-label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: #a0a0ff;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-icon {
            position: absolute;
            left: 16px;
            color: #6080c0;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            pointer-events: none;
        }

        .form-input {
            width: 100%;
            padding: 14px 16px 14px 48px;
            background: rgba(30, 35, 70, 0.6);
            border: 1.5px solid rgba(100, 120, 255, 0.25);
            border-radius: 12px;
            color: #e8e8ff;
            font-size: 1rem;
            font-family: 'Inter', sans-serif;
            outline: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(4px);
        }

        .form-input::placeholder {
            color: #7080b0;
        }

        .form-input:focus {
            border-color: rgba(0, 217, 255, 0.6);
            background: rgba(30, 40, 80, 0.8);
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.25),
                        inset 0 0 10px rgba(0, 217, 255, 0.1);
        }

        .form-input:focus + .input-icon {
            color: #00d9ff;
            transform: scale(1.2);
            text-shadow: 0 0 10px rgba(0, 217, 255, 0.6);
        }

        .register-button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #00d9ff 0%, #9d4edd 100%);
            border: none;
            border-radius: 12px;
            color: #fff;
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 20px rgba(0, 217, 255, 0.3);
            text-transform: uppercase;
            position: relative;
            overflow: hidden;
            font-family: 'Inter', sans-serif;
            margin-top: 10px; /* Added margin for spacing */
        }

        .register-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s ease;
        }

        .register-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 217, 255, 0.5);
        }

        .register-button:hover::before {
            left: 100%;
        }

        .register-button:active {
            transform: translateY(0);
        }

        .login-text {
            text-align: center;
            margin-top: 25px;
            font-size: 0.9rem;
            color: #a0a0c0;
        }

        .login-link {
            color: #00d9ff;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .login-link:hover {
            color: #9d4edd;
        }

        /* Gradient orb effect */
        .gradient-orb {
            position: fixed;
            pointer-events: none;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.3;
            z-index: 0;
        }

        .orb-1 {
            width: 400px;
            height: 400px;
            background: linear-gradient(135deg, #00d9ff, transparent);
            top: -100px;
            right: -100px;
            animation: float 20s ease-in-out infinite;
        }

        .orb-2 {
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #9d4edd, transparent);
            bottom: -50px;
            left: -50px;
            animation: float 25s ease-in-out infinite reverse;
        }

        @keyframes float {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(30px, 30px); }
        }

        .show-password-checkbox {
            width: 20px;
            height: 20px;
            accent-color: #00d9ff;
            vertical-align: middle; /* Improved alignment */
        }

        /* Responsive design */
        @media (max-width: 1024px) {
            .landing-left {
                max-width: 60%;
                padding-left: 5%;
            }

            .hero-title {
                font-size: 2.8rem;
            }

            .landing-right {
                max-width: 40%;
            }
        }

        @media (max-width: 768px) {
            .wrapper {
                flex-direction: column;
                padding: 40px 20px;
                position: relative; /* Allow content to scroll if needed */
                overflow-y: auto;
                height: auto;
            }

            .landing-left {
                max-width: 100%;
                padding-left: 0;
                text-align: center;
                margin-bottom: 40px;
            }
            .brand-section {
                align-items: center;
                text-align: center;
            }
            .landing-left .logo, .landing-left .tagline {
                margin: 0 auto 15px auto;
                background: linear-gradient(135deg, #00d9ff, #9d4edd);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hero-title {
                font-size: 2.2rem;
            }

            .hero-subtitle {
                font-size: 1rem;
            }

            .landing-right {
                max-width: 100%;
                margin-bottom: 40px;
            }

            .form-container {
                max-width: 100%;
            }
            /* Re-enable scrolling for body on small screens */
            body {
                overflow-y: auto;
                overflow-x: hidden;
            }
        }
        /* ===================================== */
        /* === COPIED CSS FROM NEW DESIGN END === */
        /* ===================================== */
    </style>
</head>
<body>

    <div class="gradient-orb orb-1"></div>
    <div class="gradient-orb orb-2"></div>

    <canvas id="bg-canvas"></canvas>

    <div class="wrapper">
        <div class="landing-left">
            <div class="brand-section">
                <a href="{{ url_for('landing') }}" class="logo">◆ One Stop Store</a>
                <div class="tagline">Join the Future of Shopping</div>
            </div>

            <div class="hero-text">
                <h1 class="hero-title">Create Your Account to Begin</h1>
                <p class="hero-subtitle">Join our community to unlock exclusive deals, manage your orders with ease, and enjoy a shopping experience tailored just for you.</p>

                <div class="features-list">
                    <div class="feature-item">
                        <div class="feature-icon"></div>
                        <span>Save your favorite items to a wishlist</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon"></div>
                        <span>Track your order status in real-time</span>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon"></div>
                        <span>Receive members-only discounts</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="landing-right">
            <div class="form-container">
                <div class="form-header">
                    <h2 class="form-title">Register Account</h2>
                    <p class="form-subtitle">Fill in your details to get started</p>
                </div>

                {% with messages = get_flashed_messages(with_categories=true) %}
                    {% if messages %}
                        <div class="flask-messages">
                            {% for category, message in messages %}
                                <div class="alert alert-{{ category }}">{{ message }}</div>
                            {% endfor %}
                        </div>
                    {% endif %}
                {% endwith %}

                <form method="post"> 
                    <div class="input-group">
                        <label class="input-label" for="username">Username</label>
                        <div class="input-wrapper">
                            <input type="text" class="form-input" id="username" name="username" placeholder="Choose a unique username" required autocomplete="username">
                            <i class="fas fa-user input-icon"></i> 
                        </div>
                    </div>

                    <div class="input-group">
                        <label class="input-label" for="password">Password</label>
                        <div class="input-wrapper">
                            <input type="password" class="form-input" id="password" name="password" placeholder="Create a strong password" required autocomplete="new-password">
                            <i class="fas fa-lock input-icon"></i>
                        </div>
                        <div style="margin-top: 10px;">
                            <input type="checkbox" class="show-password-checkbox" onclick="showPassword()"> Show Password
                        </div>
                    </div>

                    <div class="input-group">
                        <label class="input-label" for="confirm_password">Confirm Password</label>
                        <div class="input-wrapper">
                            <input type="password" class="form-input" id="confirm_password" name="confirm_password" placeholder="Confirm your password" required autocomplete="new-password">
                            <i class="fas fa-lock input-icon"></i>
                        </div>
                    </div>

                    <button type="submit" class="register-button">Create Account</button>
                </form>

                <div class="login-text">
                    Already have an account? <a href="{{ url_for('login') }}" class="login-link">Log in here</a>
                </div>
                 <div class="login-text" style="margin-top: 10px;">
                    <a href="{{ url_for('landing') }}" class="login-link">Back to Welcome</a>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <script>
        // This script is a direct copy from the new login page design
        // It creates the animated background effect.
        
        // ========== SCENE SETUP ==========
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({
            canvas: document.getElementById('bg-canvas'),
            antialias: true,
            alpha: true
        });

        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setClearColor(0x0a0e27, 1);
        camera.position.z = 5;

        // ========== LIGHTING ==========
        const ambientLight = new THREE.AmbientLight(0x5050ff, 0.5);
        scene.add(ambientLight);

        const cyanLight = new THREE.PointLight(0x00d9ff, 2, 150);
        cyanLight.position.set(8, 5, 3);
        scene.add(cyanLight);

        const purpleLight = new THREE.PointLight(0x9d4edd, 2, 150);
        purpleLight.position.set(-8, -5, 3);
        scene.add(purpleLight);

        // ========== BACKGROUND PARTICLES ==========
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesCount = 8000;
        const posArray = new Float32Array(particlesCount * 3);

        for (let i = 0; i < particlesCount * 3; i += 3) {
            posArray[i] = (Math.random() - 0.5) * 50;
            posArray[i + 1] = (Math.random() - 0.5) * 50;
            posArray[i + 2] = (Math.random() - 0.5) * 50;
        }

        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

        const particlesMaterial = new THREE.PointsMaterial({
            size: 0.02,
            color: 0x6080ff,
            transparent: true,
            opacity: 0.6,
            sizeAttenuation: true,
            blending: THREE.AdditiveBlending
        });

        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        scene.add(particles);

        // ========== FLOATING GEOMETRIC OBJECTS ==========
        const geometries = [
            new THREE.IcosahedronGeometry(0.8, 4),
            new THREE.TetrahedronGeometry(1),
            new THREE.OctahedronGeometry(0.7)
        ];

        const objects = [];

        geometries.forEach((geom, idx) => {
            const material = new THREE.MeshPhysicalMaterial({
                color: idx % 2 === 0 ? 0x00d9ff : 0x9d4edd,
                wireframe: true,
                transparent: true,
                opacity: 0.2,
                emissive: idx % 2 === 0 ? 0x00d9ff : 0x9d4edd,
                emissiveIntensity: 0.3
            });

            const obj = new THREE.Mesh(geom, material);
            obj.position.set(
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 20,
                (Math.random() - 0.5) * 15 - 10
            );
            obj.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
            obj.scale.set(1.5, 1.5, 1.5);

            scene.add(obj);
            objects.push({
                mesh: obj,
                speed: Math.random() * 0.002 + 0.001,
                rotationSpeed: Math.random() * 0.005 + 0.001
            });
        });

        // ========== GLOWING TORUS ==========
        const torusGeometry = new THREE.TorusGeometry(3, 0.3, 16, 64);
        const torusMaterial = new THREE.MeshPhysicalMaterial({
            color: 0x00d9ff,
            emissive: 0x00d9ff,
            emissiveIntensity: 0.5,
            wireframe: false,
            transparent: true,
            opacity: 0.3,
            metalness: 0.8,
            roughness: 0.2
        });

        const torus = new THREE.Mesh(torusGeometry, torusMaterial);
        torus.position.set(-8, 3, -8);
        torus.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
        scene.add(torus);

        // ========== MOUSE INTERACTION ==========
        let mouseX = 0, mouseY = 0;
        let targetCameraX = 0, targetCameraY = 0;

        document.addEventListener('mousemove', (event) => {
            mouseX = (event.clientX / window.innerWidth) * 2 - 1;
            mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
        });

        // ========== ANIMATION LOOP ==========
        const clock = new THREE.Clock();

        const animate = () => {
            requestAnimationFrame(animate);
            const elapsed = clock.getElapsedTime();

            particles.rotation.y = elapsed * 0.02;
            particles.rotation.x = elapsed * 0.01;

            objects.forEach((obj) => {
                obj.mesh.rotation.x += obj.rotationSpeed;
                obj.mesh.rotation.y += obj.rotationSpeed * 0.7;
                obj.mesh.position.y += Math.sin(elapsed * obj.speed) * 0.01;
            });

            torus.rotation.x += 0.003;
            torus.rotation.z += 0.002;

            cyanLight.position.x = Math.sin(elapsed * 0.3) * 12;
            cyanLight.position.z = Math.cos(elapsed * 0.3) * 12;

            purpleLight.position.x = Math.cos(elapsed * 0.4) * 12;
            purpleLight.position.z = Math.sin(elapsed * 0.4) * 12;

            targetCameraX = mouseX * 0.3;
            targetCameraY = mouseY * 0.3;

            camera.position.x += (targetCameraX - camera.position.x) * 0.05;
            camera.position.y += (targetCameraY - camera.position.y) * 0.05;
            camera.lookAt(scene.position);

            renderer.render(scene, camera);
        };

        animate();

        // ========== RESIZE HANDLER ==========
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        function showPassword() {
            var password = document.getElementById("password");
            var confirm_password = document.getElementById("confirm_password");
            if (password.type === "password") {
                password.type = "text";
                confirm_password.type = "text";
            } else {
                password.type = "password";
                confirm_password.type = "password";
            }
        }
    </script>
</body>
</html>
""",
    "wishlist.html": """{% extends "base.html" %}

{% block head %}
<style>
    .content-wrapper {
        max-width: 700px;
        margin: 40px auto;
        backdrop-filter: blur(10px);
        background: rgba(20, 25, 50, 0.4);
        border: 1px solid rgba(100, 100, 255, 0.15);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, #00d9ff, #9d4edd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 30px;
    }

    #wishlist-items .wishlist-list {
        list-style: none;
        padding: 0;
    }

    #wishlist-items .wishlist-list li {
        background: rgba(30, 35, 70, 0.6);
        border: 1.5px solid rgba(100, 120, 255, 0.25);
        border-radius: 12px;
        padding: 15px 20px;
        margin-bottom: 15px;
        font-size: 1.1rem;
        color: #e0e0ff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.3s ease;
    }

    #wishlist-items .wishlist-list li:hover {
        border-color: rgba(0, 217, 255, 0.5);
        background: rgba(30, 40, 80, 0.8);
    }

    .remove-btn {
        background: rgba(255, 77, 109, 0.2);
        color: #ff79c6;
        border: 1px solid rgba(255, 77, 109, 0.4);
        padding: 8px 15px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .remove-btn:hover {
        background: rgba(255, 77, 109, 0.4);
        color: #fff;
        box-shadow: 0 0 10px rgba(255, 77, 109, 0.5);
    }

    .empty-wishlist-message, .back-action {
        text-align: center;
        margin-top: 20px;
    }

    .empty-wishlist-message p {
        font-size: 1.2rem;
        color: #a0a0c0;
    }

</style>
{% endblock %}

{% block content %}
<div class="content-wrapper">
    <h1 class="page-title">Your Wishlist</h1>

    <div id="wishlist-items">
        {% if wishlist_items %}
            <ul class="wishlist-list">
                {% for item in wishlist_items %}
                    <li id="wishlist-item-{{ item.id }}">
                        <span>{{ item.name }} - Rs. {{ item.price }}</span>
                        <button class="remove-btn" data-product-id="{{ item.id }}">Remove</button>
                    </li>
                {% endfor %}
            </ul>
        {% else %}
            <div class="empty-wishlist-message"><p>Your wishlist is empty.</p></div>
        {% endif %}
    </div>

    <div class="back-action">
        <a href="{{ url_for('home') }}" class="theme-button">Back to Home</a>
    </div>
</div>

{% endblock %}

{% block scripts %}
<script>
    document.addEventListener('DOMContentLoaded', function() {
        const wishlistContainer = document.getElementById('wishlist-items');
        const wishlistCountBadge = document.getElementById('wishlist-badge');

        wishlistContainer.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-btn')) {
                e.preventDefault();
                const productId = e.target.dataset.productId;
                
                fetch('/remove_from_wishlist/' + productId, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove item from DOM
                        const listItem = document.getElementById('wishlist-item-' + productId);
                        if (listItem) {
                            listItem.remove();
                        }

                        // Update wishlist count in navbar
                        if (wishlistCountBadge) {
                            wishlistCountBadge.textContent = data.wishlist_count;
                            wishlistCountBadge.style.display = data.wishlist_count > 0 ? 'inline-block' : 'none';
                        }

                        // If wishlist becomes empty, display message
                        if (data.wishlist_count === 0) {
                            wishlistContainer.innerHTML = '<div class="empty-wishlist-message"><p>Your wishlist is empty.</p></div>';
                        }
                    } else {
                        // Handle error, e.g., display a flash message
                        console.error('Error removing from wishlist:', data.message);
                    }
                })
                .catch(error => {
                    console.error('Network error:', error);
                });
            }
        });
    });
</script>
{% endblock %}
"""
}

app = Flask(__name__)

app.jinja_loader = DictLoader(templates)
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