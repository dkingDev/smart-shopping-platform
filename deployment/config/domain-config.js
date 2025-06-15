/**
 * Smart Shopping Platform - Multi-Domain Configuration
 * Copyright (c) 2025 Spirit of the Immortals Ltd
 * Company Registration: 13434726 (England & Wales)
 *  * Domain Strategy:
 * - thesmartshoppingsite.com (primary platform - global)
 * - thesmartshoppingsite.co.uk (UK platform)
 * - spiritoftheimmortals.co.uk (company site - UK)
 * - spiritoftheimmortalsltd.co.uk (company site - global)
 */

const DOMAIN_CONFIG = {
    // Production domains
    production: {
        platform: {
            primary: 'thesmartshoppingsite.com',
            uk: 'thesmartshoppingsite.co.uk'
        },        company: {
            primary: 'spiritoftheimmortalsltd.co.uk',
            uk: 'spiritoftheimmortals.co.uk'
        }
    },
      // API endpoints for each domain
    api: {
        'thesmartshoppingsite.com': 'https://api.thesmartshoppingsite.com',
        'thesmartshoppingsite.co.uk': 'https://api.thesmartshoppingsite.co.uk',
        'spiritoftheimmortalsltd.co.uk': 'https://api.spiritoftheimmortalsltd.co.uk',
        'spiritoftheimmortals.co.uk': 'https://api.spiritoftheimmortals.co.uk'
    },
    
    // SSL/TLS configuration
    ssl: {
        certificates: [
            '*.thesmartshoppingsite.com',
            '*.thesmartshoppingsite.co.uk',
            '*.spiritoftheimmortalsltd.co.uk',
            '*.spiritoftheimmortals.co.uk'
        ]
    },
    
    // Redirect rules
    redirects: {
        // UK visitors prefer .co.uk        geoRedirects: {
            'GB': {
                'thesmartshoppingsite.com': 'thesmartshoppingsite.co.uk',
                'spiritoftheimmortalsltd.co.uk': 'spiritoftheimmortals.co.uk'
            }
        },
        
        // www redirects        www: {
            'www.thesmartshoppingsite.com': 'thesmartshoppingsite.com',
            'www.thesmartshoppingsite.co.uk': 'thesmartshoppingsite.co.uk',
            'www.spiritoftheimmortalsltd.co.uk': 'spiritoftheimmortalsltd.co.uk',
            'www.spiritoftheimmortals.co.uk': 'spiritoftheimmortals.co.uk'
        }
    },
    
    // Email configuration
    email: {
        'spiritoftheimmortals.co.uk': {
            mx: 'mail.spiritoftheimmortals.co.uk',
            addresses: [
                'derek@spiritoftheimmortals.co.uk',
                'info@spiritoftheimmortals.co.uk',
                'support@spiritoftheimmortals.co.uk',
                'admin@spiritoftheimmortals.co.uk'
            ]        },
        'spiritoftheimmortalsltd.co.uk': {
            mx: 'mail.spiritoftheimmortalsltd.co.uk',
            addresses: [
                'derek@spiritoftheimmortalsltd.co.uk',
                'info@spiritoftheimmortalsltd.co.uk',
                'support@spiritoftheimmortalsltd.co.uk'
            ]
        },
        'thesmartshoppingsite.com': {
            mx: 'mail.thesmartshoppingsite.com',
            addresses: [
                'support@thesmartshoppingsite.com',
                'hello@thesmartshoppingsite.com'
            ]
        },
        'thesmartshoppingsite.co.uk': {
            mx: 'mail.thesmartshoppingsite.co.uk',
            addresses: [
                'support@thesmartshoppingsite.co.uk',
                'hello@thesmartshoppingsite.co.uk'
            ]
        }
    }
};

// Function to get the appropriate API URL based on current domain
function getApiBaseUrl() {
    const hostname = window.location.hostname;
    
    // Development environment
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:9999';
    }
    
    // Production environments
    if (hostname === 'thesmartshoppingsite.com') {
        return 'https://api.thesmartshoppingsite.com';
    }
    if (hostname === 'thesmartshoppingsite.co.uk') {
        return 'https://api.thesmartshoppingsite.co.uk';
    }    if (hostname === 'spiritoftheimmortalsltd.co.uk') {
        return 'https://api.spiritoftheimmortalsltd.co.uk';
    }
    if (hostname === 'spiritoftheimmortals.co.uk') {
        return 'https://api.spiritoftheimmortals.co.uk';
    }
    
    // GitHub Pages or other hosting
    if (hostname.includes('github.io')) {
        return 'https://your-backend-api.herokuapp.com';
    }
    
    // Default fallback
    return 'https://api.thesmartshoppingsite.com';
}

// Export for use in applications
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DOMAIN_CONFIG, getApiBaseUrl };
}
