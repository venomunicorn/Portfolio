// ============================================
// LUXE E-COMMERCE PLATFORM
// ============================================

// --- PRODUCT DATA ---
const products = [
    // Bags
    {
        id: 1, name: "Canvas Tote Bag", price: 45.00, category: "Bags",
        desc: "Handcrafted organic cotton canvas tote with leather handles. Perfect for everyday use.",
        img: "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400&h=500&fit=crop"
    },
    {
        id: 2, name: "Leather Crossbody", price: 125.00, category: "Bags",
        desc: "Minimalist crossbody bag in genuine Italian leather. Adjustable strap.",
        img: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=500&fit=crop"
    },
    {
        id: 3, name: "Weekend Duffle", price: 195.00, category: "Bags",
        desc: "Spacious duffle bag in water-resistant waxed canvas. Ideal for short trips.",
        img: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=500&fit=crop"
    },

    // Clothing
    {
        id: 4, name: "Linen Summer Shirt", price: 89.00, category: "Clothing",
        desc: "Breathable 100% linen shirt. Relaxed fit, perfect for warm days.",
        img: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=500&fit=crop"
    },
    {
        id: 5, name: "Organic Cotton Tee", price: 35.00, category: "Clothing",
        desc: "Essential crew neck tee made from GOTS certified organic cotton.",
        img: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop"
    },
    {
        id: 6, name: "Merino Wool Sweater", price: 145.00, category: "Clothing",
        desc: "Lightweight merino wool sweater. Temperature regulating and odor resistant.",
        img: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=500&fit=crop"
    },
    {
        id: 7, name: "Tailored Linen Pants", price: 120.00, category: "Clothing",
        desc: "Relaxed tailored pants in premium European linen. Comfortable elegance.",
        img: "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&h=500&fit=crop"
    },

    // Accessories
    {
        id: 8, name: "Leather Minimal Watch", price: 150.00, category: "Accessories",
        desc: "Swiss movement watch with Italian leather strap. Sapphire crystal glass.",
        img: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=500&fit=crop"
    },
    {
        id: 9, name: "Silk Scarf", price: 95.00, category: "Accessories",
        desc: "Hand-rolled silk twill scarf. Original print, made in Italy.",
        img: "https://images.unsplash.com/photo-1601370690183-1c7796ecec61?w=400&h=500&fit=crop"
    },
    {
        id: 10, name: "Leather Belt", price: 75.00, category: "Accessories",
        desc: "Full-grain leather belt with brushed brass buckle. Built to last.",
        img: "https://images.unsplash.com/photo-1553062407-98eeb64c6a45?w=400&h=500&fit=crop"
    },

    // Footwear
    {
        id: 11, name: "Suede Loafers", price: 210.00, category: "Footwear",
        desc: "Handcrafted suede loafers with leather sole. Classic Italian design.",
        img: "https://images.unsplash.com/photo-1614252369475-531eba835eb1?w=400&h=500&fit=crop"
    },
    {
        id: 12, name: "Canvas Sneakers", price: 85.00, category: "Footwear",
        desc: "Minimalist canvas sneakers with rubber sole. Comfortable all-day wear.",
        img: "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=500&fit=crop"
    }
];

// --- STATE ---
let cart = [];
let activeCategory = 'all';

// --- DOM ELEMENTS ---
const productGrid = document.getElementById('product-grid');
const cartSidebar = document.getElementById('cart-sidebar');
const overlay = document.getElementById('overlay');
const cartItemsContainer = document.getElementById('cart-items');
const cartTotalElement = document.getElementById('cart-total');
const cartCountElement = document.getElementById('cart-count');
const quickViewModal = document.getElementById('quickViewModal');
const checkoutModal = document.getElementById('checkoutModal');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    loadCart();
    renderProducts();
    setupEventListeners();
});

function setupEventListeners() {
    // Category filters
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeCategory = btn.dataset.category;
            renderProducts();
        });
    });

    // Checkout form
    document.getElementById('checkout-form').addEventListener('submit', (e) => {
        e.preventDefault();
        processCheckout();
    });

    // Close modals on overlay click
    quickViewModal.addEventListener('click', (e) => {
        if (e.target === quickViewModal) closeQuickView();
    });
    checkoutModal.addEventListener('click', (e) => {
        if (e.target === checkoutModal) closeCheckout();
    });
}

// --- LOCAL STORAGE ---
function loadCart() {
    const saved = localStorage.getItem('luxe_cart');
    cart = saved ? JSON.parse(saved) : [];
    updateCartUI();
}

function saveCart() {
    localStorage.setItem('luxe_cart', JSON.stringify(cart));
}

// --- PRODUCT RENDERING ---
function renderProducts() {
    const filtered = activeCategory === 'all'
        ? products
        : products.filter(p => p.category === activeCategory);

    productGrid.innerHTML = filtered.map(product => `
        <div class="product-card" onclick="openQuickView(${product.id})">
            <div class="img-container">
                <img src="${product.img}" alt="${product.name}" class="product-img">
                <button class="btn-add" onclick="event.stopPropagation(); addToCart(${product.id})">Add to Bag</button>
            </div>
            <div class="product-info">
                <span class="product-category">${product.category}</span>
                <h3>${product.name}</h3>
                <span class="price">$${product.price.toFixed(2)}</span>
            </div>
        </div>
    `).join('');
}

// --- CART FUNCTIONS ---
function toggleCart() {
    cartSidebar.classList.toggle('open');
    overlay.classList.toggle('open');
}

function addToCart(id) {
    const product = products.find(p => p.id === id);
    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    saveCart();
    updateCartUI();
    toggleCart();
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    updateCartUI();
}

function updateQuantity(id, delta) {
    const item = cart.find(i => i.id === id);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        removeFromCart(id);
    } else {
        saveCart();
        updateCartUI();
    }
}

function updateCartUI() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    cartCountElement.textContent = totalItems;
    cartTotalElement.textContent = `$${totalPrice.toFixed(2)}`;

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p class="empty-msg">Your bag is empty.</p>';
        return;
    }

    cartItemsContainer.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-img">
                <img src="${item.img}" alt="${item.name}">
            </div>
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <span class="item-price">$${(item.price * item.quantity).toFixed(2)}</span>
                <div class="quantity-controls">
                    <button onclick="updateQuantity(${item.id}, -1)">−</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateQuantity(${item.id}, 1)">+</button>
                </div>
                <span class="remove-item" onclick="removeFromCart(${item.id})">Remove</span>
            </div>
        </div>
    `).join('');
}

// --- QUICK VIEW MODAL ---
function openQuickView(id) {
    const product = products.find(p => p.id === id);
    if (!product) return;

    const qvImage = document.getElementById('qv-image');
    qvImage.style.backgroundImage = `url(${product.img})`;
    qvImage.style.backgroundSize = 'cover';
    qvImage.style.backgroundPosition = 'center';
    document.getElementById('qv-category').textContent = product.category;
    document.getElementById('qv-name').textContent = product.name;
    document.getElementById('qv-price').textContent = `$${product.price.toFixed(2)}`;
    document.getElementById('qv-desc').textContent = product.desc;
    document.getElementById('qv-add-btn').onclick = () => {
        addToCart(id);
        closeQuickView();
    };

    quickViewModal.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeQuickView() {
    quickViewModal.classList.remove('open');
    document.body.style.overflow = '';
}

// --- CHECKOUT ---
function openCheckout() {
    if (cart.length === 0) return;

    toggleCart();

    const totalPrice = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    document.getElementById('checkout-items').innerHTML = cart.map(item => `
        <div class="checkout-item">
            <span>${item.name} × ${item.quantity}</span>
            <span>$${(item.price * item.quantity).toFixed(2)}</span>
        </div>
    `).join('');

    document.getElementById('checkout-total-price').textContent = `$${totalPrice.toFixed(2)}`;

    document.getElementById('checkout-form-view').classList.remove('hidden');
    document.getElementById('checkout-success-view').classList.add('hidden');

    checkoutModal.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeCheckout() {
    checkoutModal.classList.remove('open');
    document.body.style.overflow = '';
}

function processCheckout() {
    // Simulate order processing
    document.getElementById('checkout-form-view').classList.add('hidden');
    document.getElementById('checkout-success-view').classList.remove('hidden');

    // Clear cart
    cart = [];
    saveCart();
    updateCartUI();
}

// --- UTILITIES ---
function scrollToProducts() {
    document.getElementById('products-section').scrollIntoView({ behavior: 'smooth' });
}
