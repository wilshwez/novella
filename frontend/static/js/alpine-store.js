document.addEventListener('alpine:init', () => {
    // ── Global Novel/Store State ──
    Alpine.store('novella', {
        theme: localStorage.getItem('novella_theme') || 'dark',
        cartOpen: false,
        authModalOpen: false,
        authTab: 'login', // 'login' | 'register'
        wishlist: JSON.parse(localStorage.getItem('novella_wishlist')) || [],
        cart: JSON.parse(localStorage.getItem('novella_cart')) || [],
        
        // Mock Session data
        user: JSON.parse(localStorage.getItem('novella_user')) || {
            isLoggedIn: false,
            username: '',
            displayName: '',
            role: 'Reader',
            membership: 'Free Reader', // 'Free Reader' | 'Premium Reader' | 'VIP Collector'
            avatar: ''
        },

        init() {
            // Apply theme on init
            document.documentElement.setAttribute('data-theme', this.theme);
            if (this.theme === 'light') {
                document.documentElement.classList.add('light');
            } else {
                document.documentElement.classList.remove('light');
            }
        },

        toggleTheme() {
            this.theme = this.theme === 'dark' ? 'light' : 'dark';
            localStorage.setItem('novella_theme', this.theme);
            document.documentElement.setAttribute('data-theme', this.theme);
            if (this.theme === 'light') {
                document.documentElement.classList.add('light');
            } else {
                document.documentElement.classList.remove('light');
            }
        },

        // ── Auth Mechanics ──
        loginMock(email, password) {
            // Basic mock logging
            this.user = {
                isLoggedIn: true,
                username: email.split('@')[0],
                displayName: email.split('@')[0].toUpperCase(),
                role: email.includes('author') ? 'Author' : 'Reader',
                membership: email.includes('vip') ? 'VIP Collector' : (email.includes('premium') ? 'Premium Reader' : 'Free Reader'),
                avatar: `https://api.dicebear.com/7.x/adventurer/svg?seed=${email.split('@')[0]}`
            };
            localStorage.setItem('novella_user', JSON.stringify(this.user));
            this.authModalOpen = false;
        },

        logoutMock() {
            this.user = {
                isLoggedIn: false,
                username: '',
                displayName: '',
                role: 'Reader',
                membership: 'Free Reader',
                avatar: ''
            };
            localStorage.removeItem('novella_user');
            // Redirect to home if on admin pages
            if (window.location.pathname.includes('admin')) {
                window.location.href = '/';
            }
        },

        // ── Wishlist Mechanics ──
        toggleWishlist(productId, name, price, coverUrl) {
            const index = this.wishlist.findIndex(item => item.id === productId);
            if (index > -1) {
                this.wishlist.splice(index, 1);
            } else {
                this.wishlist.push({ id: productId, name, price, coverUrl });
            }
            localStorage.setItem('novella_wishlist', JSON.stringify(this.wishlist));
        },

        inWishlist(productId) {
            return this.wishlist.some(item => item.id === productId);
        },

        // ── Cart Mechanics ──
        addToCart(productId, name, price, coverUrl, type = 'Digital') {
            const item = this.cart.find(i => i.id === productId);
            if (item) {
                item.quantity += 1;
            } else {
                this.cart.push({ id: productId, name, price, coverUrl, type, quantity: 1 });
            }
            this.saveCart();
            this.cartOpen = true; // Open drawer immediately
        },

        removeFromCart(productId) {
            this.cart = this.cart.filter(item => item.id !== productId);
            this.saveCart();
        },

        updateQty(productId, delta) {
            const item = this.cart.find(i => i.id === productId);
            if (item) {
                item.quantity += delta;
                if (item.quantity <= 0) {
                    this.removeFromCart(productId);
                } else {
                    this.saveCart();
                }
            }
        },

        saveCart() {
            localStorage.setItem('novella_cart', JSON.stringify(this.cart));
        },

        get cartTotal() {
            return this.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        },

        get cartCount() {
            return this.cart.reduce((sum, item) => sum + item.quantity, 0);
        }
    });
});
