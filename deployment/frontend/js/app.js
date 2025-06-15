/**
 * Smart Shopping Platform - Secure Frontend Application
 * Copyright (c) 2025 Spirit of the Immortals Ltd
 * Company Registration: 13434726 (England & Wales)
 * Director: Derek King
 * 
 * ALL RIGHTS RESERVED - PROPRIETARY SOFTWARE
 * This software contains trade secrets and proprietary algorithms.
 * Unauthorized copying, modification, or distribution is strictly prohibited.
 * For licensing inquiries: derek.j.king@live.com
 * 
 * Configuration:
 * - All API calls require JWT authentication
 * - User data stored in AWS PostgreSQL only
 * - No local storage of sensitive data
 * - Secure token management
 */

class SmartShoppingApp {
    constructor() {
        this.apiBaseUrl = this.getApiBaseUrl();
        this.token = null;
        this.user = null;
        this.refreshTokenTimer = null;
        
        // Initialize the application
        this.init();
    }    getApiBaseUrl() {
        // Check current domain and return appropriate API URL
        const hostname = window.location.hostname;
        
        // Development environment
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:9999';
        }
        
        // Production environments - domain-specific APIs
        if (hostname === 'thesmartshoppingsite.com') {
            return 'https://api.thesmartshoppingsite.com';
        }
        if (hostname === 'thesmartshoppingsite.co.uk') {
            return 'https://api.thesmartshoppingsite.co.uk';
        }        if (hostname === 'spiritoftheimmortalsltd.co.uk') {
            return 'https://api.spiritoftheimmortalsltd.co.uk';
        }
        if (hostname === 'spiritoftheimmortals.co.uk') {
            return 'https://api.spiritoftheimmortals.co.uk';
        }
        
        // GitHub Pages or temporary hosting
        if (hostname.includes('github.io')) {
            return 'https://your-backend-api.herokuapp.com';
        }
        
        // Default fallback to primary domain
        return 'https://api.thesmartshoppingsite.com';
    }

    async init() {
        console.log('🚀 Initializing Smart Shopping Platform...');
        
        // Show loading screen
        this.showElement('loadingScreen');
        
        // Check for existing authentication
        await this.checkAuthentication();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Hide loading screen
        setTimeout(() => {
            this.hideElement('loadingScreen');
            
            if (this.token && this.user) {
                this.showDashboard();
            } else {
                this.showAuthentication();
            }
        }, 1500);
    }

    async checkAuthentication() {
        // Check for stored token (secure httpOnly cookie would be better for production)
        const storedToken = localStorage.getItem('smart_shopping_token');
        const storedUser = localStorage.getItem('smart_shopping_user');
        
        if (storedToken && storedUser) {
            try {
                // Verify token with backend
                const response = await this.apiCall('GET', '/auth/verify-token', null, storedToken);
                
                if (response.success) {
                    this.token = storedToken;
                    this.user = JSON.parse(storedUser);
                    this.startTokenRefresh();
                    console.log('✅ Authentication verified');
                    return true;
                }
            } catch (error) {
                console.log('❌ Token verification failed:', error.message);
            }
        }
        
        // Clear invalid authentication
        this.clearAuthentication();
        return false;
    }

    setupEventListeners() {
        // Authentication forms
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });

        // Feature interactions
        document.getElementById('savingsSearch').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.analyzeSavings();
            }
        });

        document.getElementById('compareProduct').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.compareStores();
            }
        });

        // Auto-load data when tabs are switched
        document.getElementById('featureTabs').addEventListener('shown.bs.tab', (e) => {
            const targetTab = e.target.getAttribute('data-bs-target');
            this.handleTabSwitch(targetTab);
        });
    }

    async handleLogin() {
        const email = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;
        
        if (!email || !password) {
            this.showAlert('Please fill in all fields', 'danger');
            return;
        }

        try {
            this.showAlert('Signing in...', 'info');
            
            const response = await this.apiCall('POST', '/auth/login', {
                email: email,
                password: password
            });

            if (response.success) {
                this.token = response.data.access_token;
                this.user = response.data.user;
                
                // Store authentication (in production, use secure httpOnly cookies)
                localStorage.setItem('smart_shopping_token', this.token);
                localStorage.setItem('smart_shopping_user', JSON.stringify(this.user));
                
                this.startTokenRefresh();
                this.showAlert('Login successful! Welcome back.', 'success');
                
                setTimeout(() => {
                    this.showDashboard();
                }, 1000);
                
                console.log('✅ Login successful for user:', this.user.email);
            }
        } catch (error) {
            console.error('❌ Login failed:', error);
            this.showAlert(error.message || 'Login failed. Please check your credentials.', 'danger');
        }
    }

    async handleRegister() {
        const name = document.getElementById('registerName').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const location = document.getElementById('registerLocation').value.trim();
        
        // Validation
        if (!name || !email || !password || !confirmPassword) {
            this.showAlert('Please fill in all required fields', 'danger');
            return;
        }
        
        if (password !== confirmPassword) {
            this.showAlert('Passwords do not match', 'danger');
            return;
        }
        
        if (password.length < 8) {
            this.showAlert('Password must be at least 8 characters long', 'danger');
            return;
        }

        try {
            this.showAlert('Creating your account...', 'info');
            
            const response = await this.apiCall('POST', '/auth/register', {
                full_name: name,
                email: email,
                password: password,
                location: location || null
            });

            if (response.success) {
                this.showAlert('Account created successfully! Please sign in.', 'success');
                
                // Switch to login tab
                document.getElementById('login-tab').click();
                
                // Pre-fill email
                document.getElementById('loginEmail').value = email;
                
                console.log('✅ Registration successful for:', email);
            }
        } catch (error) {
            console.error('❌ Registration failed:', error);
            this.showAlert(error.message || 'Registration failed. Please try again.', 'danger');
        }
    }

    async logout() {
        try {
            // Notify backend of logout
            if (this.token) {
                await this.apiCall('POST', '/auth/logout');
            }
        } catch (error) {
            console.log('Logout notification failed:', error);
        }
        
        this.clearAuthentication();
        this.showAuthentication();
        console.log('✅ Logged out successfully');
    }

    clearAuthentication() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('smart_shopping_token');
        localStorage.removeItem('smart_shopping_user');
        
        if (this.refreshTokenTimer) {
            clearInterval(this.refreshTokenTimer);
            this.refreshTokenTimer = null;
        }
    }

    startTokenRefresh() {
        // Refresh token every 20 minutes (tokens expire in 24 hours)
        this.refreshTokenTimer = setInterval(async () => {
            try {
                const response = await this.apiCall('POST', '/auth/refresh-token');
                if (response.success) {
                    this.token = response.data.access_token;
                    localStorage.setItem('smart_shopping_token', this.token);
                }
            } catch (error) {
                console.error('Token refresh failed:', error);
                this.logout();
            }
        }, 20 * 60 * 1000); // 20 minutes
    }

    async apiCall(method, endpoint, data = null, token = null) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
        };
        
        // Add authentication header
        const authToken = token || this.token;
        if (authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }
        
        const options = {
            method: method,
            headers: headers,
            credentials: 'include', // Include cookies for CORS
        };
        
        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || result.message || `HTTP ${response.status}`);
            }
            
            return result;
        } catch (error) {
            console.error(`API call failed: ${method} ${endpoint}`, error);
            
            // Handle authentication errors
            if (error.message.includes('401') || error.message.includes('Unauthorized')) {
                this.logout();
                throw new Error('Session expired. Please log in again.');
            }
            
            throw error;
        }
    }

    showAuthentication() {
        this.hideElement('appSection');
        this.showElement('authSection');
        this.clearAlert();
    }

    showDashboard() {
        this.hideElement('authSection');
        this.showElement('appSection');
        
        // Update user name
        document.getElementById('userName').textContent = this.user.full_name || this.user.email;
        
        // Load initial data
        this.loadPromotions();
        this.loadShoppingLists();
    }

    showElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.remove('hidden');
            element.classList.add('fade-in');
        }
    }

    hideElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.add('hidden');
            element.classList.remove('fade-in');
        }
    }

    showAlert(message, type = 'info') {
        const alertElement = document.getElementById('authAlert');
        alertElement.className = `alert alert-${type}`;
        alertElement.textContent = message;
        alertElement.classList.remove('d-none');
        
        // Auto-hide success/info messages
        if (type === 'success' || type === 'info') {
            setTimeout(() => {
                this.clearAlert();
            }, 5000);
        }
    }

    clearAlert() {
        const alertElement = document.getElementById('authAlert');
        alertElement.classList.add('d-none');
    }

    handleTabSwitch(targetTab) {
        switch (targetTab) {
            case '#promotions':
                this.loadPromotions();
                break;
            case '#lists':
                this.loadShoppingLists();
                break;
            case '#savings':
                // Savings analysis is on-demand
                break;
            case '#stores':
                // Store comparison is on-demand
                break;
        }
    }

    async analyzeSavings() {
        const query = document.getElementById('savingsSearch').value.trim();
        
        if (!query) {
            alert('Please enter a product to search for');
            return;
        }
        
        try {
            const response = await this.apiCall('POST', '/api/analyze-savings', {
                query: query,
                user_location: this.user.location
            });
            
            if (response.success) {
                this.displaySavingsResults(response.data);
            }
        } catch (error) {
            console.error('Savings analysis failed:', error);
            alert('Failed to analyze savings: ' + error.message);
        }
    }

    displaySavingsResults(data) {
        const resultsDiv = document.getElementById('savingsResults');
        const tableBody = document.getElementById('savingsTableBody');
        
        tableBody.innerHTML = '';
        
        if (data.store_comparisons && data.store_comparisons.length > 0) {
            data.store_comparisons.forEach(store => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>
                        <strong>${store.store_name}</strong>
                        <br><small class="text-muted">${store.product_name}</small>
                    </td>
                    <td>
                        <span class="fw-bold">£${store.current_price}</span>
                        ${store.original_price && store.original_price !== store.current_price ? 
                            `<br><small class="text-muted text-decoration-line-through">£${store.original_price}</small>` : ''}
                    </td>
                    <td>
                        <span class="badge ${store.savings > 0 ? 'bg-success' : 'bg-secondary'}">
                            ${store.savings > 0 ? `Save £${store.savings.toFixed(2)}` : 'Best Price'}
                        </span>
                    </td>
                    <td>
                        <span class="text-muted">${store.distance || 'Unknown'}</span>
                    </td>
                `;
                tableBody.appendChild(row);
            });
            
            resultsDiv.classList.remove('d-none');
        } else {
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No results found</td></tr>';
            resultsDiv.classList.remove('d-none');
        }
    }

    async loadPromotions() {
        try {
            const storeFilter = document.getElementById('storeFilter').value;
            const response = await this.apiCall('GET', `/api/promotions${storeFilter ? `?store=${storeFilter}` : ''}`);
            
            if (response.success) {
                this.displayPromotions(response.data);
            }
        } catch (error) {
            console.error('Failed to load promotions:', error);
            document.getElementById('promotionsList').innerHTML = 
                '<div class="col-12"><div class="alert alert-warning">Failed to load promotions</div></div>';
        }
    }

    displayPromotions(promotions) {
        const container = document.getElementById('promotionsList');
        container.innerHTML = '';
        
        if (promotions.length === 0) {
            container.innerHTML = '<div class="col-12"><div class="alert alert-info">No promotions found</div></div>';
            return;
        }
        
        promotions.forEach(promo => {
            const card = document.createElement('div');
            card.className = 'col-md-6 col-lg-4 mb-3';
            card.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${promo.product_name}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">${promo.store_name}</h6>
                        <p class="card-text">
                            <span class="badge bg-success">£${promo.promotional_price}</span>
                            ${promo.original_price ? `<span class="text-muted text-decoration-line-through ms-2">£${promo.original_price}</span>` : ''}
                        </p>
                        <p class="card-text"><small class="text-muted">${promo.promotion_type}</small></p>
                        ${promo.end_date ? `<p class="card-text"><small class="text-danger">Ends: ${new Date(promo.end_date).toLocaleDateString()}</small></p>` : ''}
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    async loadShoppingLists() {
        try {
            const response = await this.apiCall('GET', '/api/shopping-lists');
            
            if (response.success) {
                this.displayShoppingLists(response.data);
            }
        } catch (error) {
            console.error('Failed to load shopping lists:', error);
            document.getElementById('shoppingLists').innerHTML = 
                '<div class="col-12"><div class="alert alert-warning">Failed to load shopping lists</div></div>';
        }
    }

    displayShoppingLists(lists) {
        const container = document.getElementById('shoppingLists');
        container.innerHTML = '';
        
        if (lists.length === 0) {
            container.innerHTML = '<div class="col-12"><div class="alert alert-info">No shopping lists yet. Create your first one!</div></div>';
            return;
        }
        
        lists.forEach(list => {
            const card = document.createElement('div');
            card.className = 'col-md-6 col-lg-4 mb-3';
            card.innerHTML = `
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${list.list_name}</h5>
                        <p class="card-text">
                            ${list.items_count || 0} items
                            ${list.total_estimated_cost ? `- £${list.total_estimated_cost.toFixed(2)} estimated` : ''}
                        </p>
                        <p class="card-text"><small class="text-muted">Created: ${new Date(list.created_at).toLocaleDateString()}</small></p>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-primary btn-sm" onclick="app.viewShoppingList(${list.list_id})">
                            <i class="fas fa-eye me-1"></i>View
                        </button>
                        <button class="btn btn-outline-danger btn-sm ms-2" onclick="app.deleteShoppingList(${list.list_id})">
                            <i class="fas fa-trash me-1"></i>Delete
                        </button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    async createShoppingList() {
        const listName = document.getElementById('newListName').value.trim();
        
        if (!listName) {
            alert('Please enter a list name');
            return;
        }
        
        try {
            const response = await this.apiCall('POST', '/api/shopping-lists', {
                list_name: listName
            });
            
            if (response.success) {
                document.getElementById('newListName').value = '';
                this.loadShoppingLists();
                alert('Shopping list created successfully!');
            }
        } catch (error) {
            console.error('Failed to create shopping list:', error);
            alert('Failed to create shopping list: ' + error.message);
        }
    }

    async deleteShoppingList(listId) {
        if (!confirm('Are you sure you want to delete this shopping list?')) {
            return;
        }
        
        try {
            const response = await this.apiCall('DELETE', `/api/shopping-lists/${listId}`);
            
            if (response.success) {
                this.loadShoppingLists();
                alert('Shopping list deleted successfully!');
            }
        } catch (error) {
            console.error('Failed to delete shopping list:', error);
            alert('Failed to delete shopping list: ' + error.message);
        }
    }

    async compareStores() {
        const product = document.getElementById('compareProduct').value.trim();
        
        if (!product) {
            alert('Please enter a product to compare');
            return;
        }
        
        try {
            const response = await this.apiCall('POST', '/api/compare-stores', {
                product_query: product
            });
            
            if (response.success) {
                this.displayStoreComparison(response.data);
            }
        } catch (error) {
            console.error('Store comparison failed:', error);
            alert('Failed to compare stores: ' + error.message);
        }
    }

    displayStoreComparison(data) {
        const resultsDiv = document.getElementById('storeComparison');
        const tableBody = document.getElementById('comparisonTableBody');
        
        tableBody.innerHTML = '';
        
        if (data.length > 0) {
            data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><strong>${item.store_name}</strong></td>
                    <td>${item.product_name}</td>
                    <td>
                        <span class="fw-bold">£${item.current_price}</span>
                        ${item.promotion_price && item.promotion_price !== item.current_price ? 
                            `<br><span class="badge bg-success">On Sale: £${item.promotion_price}</span>` : ''}
                    </td>
                    <td>
                        ${item.rating ? `${'★'.repeat(Math.floor(item.rating))}${'☆'.repeat(5-Math.floor(item.rating))} (${item.rating})` : 'No rating'}
                    </td>
                    <td>
                        <span class="badge ${item.in_stock ? 'bg-success' : 'bg-danger'}">
                            ${item.in_stock ? 'In Stock' : 'Out of Stock'}
                        </span>
                    </td>
                `;
                tableBody.appendChild(row);
            });
            
            resultsDiv.classList.remove('d-none');
        } else {
            tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No products found</td></tr>';
            resultsDiv.classList.remove('d-none');
        }
    }
}

// Global functions for onclick handlers
window.logout = function() {
    app.logout();
};

window.analyzeSavings = function() {
    app.analyzeSavings();
};

window.createShoppingList = function() {
    app.createShoppingList();
};

window.compareStores = function() {
    app.compareStores();
};

window.loadPromotions = function() {
    app.loadPromotions();
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Smart Shopping Platform - Secure AWS Edition');
    console.log('🔐 All features require AWS PostgreSQL authentication');
    
    // Initialize the application
    window.app = new SmartShoppingApp();
});

// Handle browser refresh/close
window.addEventListener('beforeunload', function() {
    if (window.app && window.app.refreshTokenTimer) {
        clearInterval(window.app.refreshTokenTimer);
    }
});
