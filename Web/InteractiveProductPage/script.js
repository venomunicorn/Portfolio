// ============================================
// INTERACTIVE PRODUCT PAGE
// ============================================

// --- STATE ---
let cart = { items: 0, total: 0 };
let currentColor = 'black';
let currentVariant = 'standard';
let currentPrice = 299;
let quantity = 1;
let isWishlisted = false;

// --- COLOR DEFINITIONS ---
const colors = {
    black: { name: 'Midnight Black', primary: '#1a1a1a', glow: 'rgba(26, 26, 26, 0.3)' },
    silver: { name: 'Silver', primary: '#c0c0c0', glow: 'rgba(192, 192, 192, 0.4)' },
    blue: { name: 'Ocean Blue', primary: '#0077b6', glow: 'rgba(0, 119, 182, 0.4)' },
    rose: { name: 'Rose Gold', primary: '#e8b4b8', glow: 'rgba(232, 180, 184, 0.4)' }
};

// --- VARIANT PRICES ---
const variants = {
    standard: { name: 'Standard', price: 299 },
    pro: { name: 'Pro', price: 399 },
    max: { name: 'Max', price: 499 }
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    setupColorSelection();
    setupVariantSelection();
    setupQuantityControls();
    setupCartButton();
    setupWishlist();
    setupTabs();
    setupGallery();
});

// --- COLOR SELECTION ---
function setupColorSelection() {
    const colorBtns = document.querySelectorAll('.color-btn');

    colorBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            colorBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            currentColor = btn.dataset.color;
            const colorData = colors[currentColor];

            // Update label
            document.getElementById('colorLabel').textContent = colorData.name;

            // Update glow background
            const glowBg = document.getElementById('glowBg');
            glowBg.style.background = `radial-gradient(circle at 70% 30%, ${colorData.glow} 0%, transparent 50%)`;

            // Update accent elements
            document.documentElement.style.setProperty('--accent', colorData.primary);
        });
    });
}

// --- VARIANT SELECTION ---
function setupVariantSelection() {
    const variantBtns = document.querySelectorAll('.variant-btn');

    variantBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            variantBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            currentVariant = btn.dataset.variant;
            currentPrice = parseInt(btn.dataset.price);

            updatePriceDisplay();
        });
    });
}

// --- QUANTITY CONTROLS ---
function setupQuantityControls() {
    const minusBtn = document.getElementById('qtyMinus');
    const plusBtn = document.getElementById('qtyPlus');
    const qtyDisplay = document.getElementById('qtyValue');

    minusBtn.addEventListener('click', () => {
        if (quantity > 1) {
            quantity--;
            qtyDisplay.textContent = quantity;
            updatePriceDisplay();
        }
    });

    plusBtn.addEventListener('click', () => {
        if (quantity < 10) {
            quantity++;
            qtyDisplay.textContent = quantity;
            updatePriceDisplay();
        }
    });
}

// --- PRICE DISPLAY ---
function updatePriceDisplay() {
    const priceEl = document.getElementById('currentPrice');
    const total = currentPrice * quantity;
    priceEl.textContent = `$${total}`;
}

// --- CART FUNCTIONALITY ---
function setupCartButton() {
    const addBtn = document.getElementById('addToCartBtn');
    const notification = document.getElementById('cartNotification');
    const cartCount = document.getElementById('cartCount');

    addBtn.addEventListener('click', () => {
        // Update cart
        cart.items += quantity;
        cart.total += currentPrice * quantity;

        // Update cart icon
        cartCount.textContent = cart.items;
        cartCount.classList.add('pulse');

        // Show notification
        notification.classList.add('show');

        // Button feedback
        addBtn.innerHTML = '<i class="fas fa-check"></i> Added!';
        addBtn.classList.add('added');

        // Reset after delay
        setTimeout(() => {
            notification.classList.remove('show');
            cartCount.classList.remove('pulse');
            addBtn.innerHTML = '<i class="fas fa-shopping-bag"></i> Add to Cart';
            addBtn.classList.remove('added');
        }, 2000);
    });
}

// --- WISHLIST ---
function setupWishlist() {
    const wishlistBtn = document.getElementById('wishlistBtn');

    wishlistBtn.addEventListener('click', () => {
        isWishlisted = !isWishlisted;

        if (isWishlisted) {
            wishlistBtn.innerHTML = '<i class="fas fa-heart"></i>';
            wishlistBtn.classList.add('active');
        } else {
            wishlistBtn.innerHTML = '<i class="far fa-heart"></i>';
            wishlistBtn.classList.remove('active');
        }
    });
}

// --- TABS ---
function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;

            // Update buttons
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `tab-${tab}`) {
                    content.classList.add('active');
                }
            });
        });
    });
}

// --- IMAGE GALLERY ---
function setupGallery() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('mainProductImage');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', () => {
            thumbnails.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');

            // Fade transition
            mainImage.style.opacity = 0;
            setTimeout(() => {
                mainImage.src = thumb.dataset.img;
                mainImage.style.opacity = 1;
            }, 200);
        });
    });
}
