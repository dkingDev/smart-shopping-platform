/**
 * Cloudflare Worker - Multi-Domain Security Router
 * Spirit of the Immortals Ltd
 * Handles secure routing for all domains with secret store integration
 */

// Define domain routing configuration
const DOMAIN_ROUTES = {
  'thesmartshoppingsite.com': {
    type: 'platform',
    region: 'global',
    backend: 'https://your-backend.herokuapp.com'
  },
  'thesmartshoppingsite.co.uk': {
    type: 'platform', 
    region: 'uk',
    backend: 'https://your-backend.herokuapp.com'
  },
  'spiritoftheimmortalsltd.co.uk': {
    type: 'company',
    region: 'global', 
    backend: 'https://company-site.pages.dev'
  },
  'spiritoftheimmortals.co.uk': {
    type: 'company',
    region: 'uk',
    backend: 'https://company-site.pages.dev'
  }
};

// Security headers configuration
const SECURITY_HEADERS = {
  'Strict-Transport-Security': 'max-age=15768000; includeSubDomains; preload',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '1; mode=block',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
  'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; img-src 'self' data: https:; connect-src 'self' https://api.*"
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const hostname = url.hostname;
    
    // Get domain configuration
    const domainConfig = DOMAIN_ROUTES[hostname];
    if (!domainConfig) {
      return new Response('Domain not configured', { status: 404 });
    }

    try {
      // Access secrets based on request type
      const secrets = await getSecretsForDomain(env, domainConfig);
      
      // Apply security checks
      const securityCheck = await performSecurityChecks(request, env, secrets);
      if (securityCheck.blocked) {
        return new Response('Access Denied', { 
          status: 403,
          headers: { 'X-Block-Reason': securityCheck.reason }
        });
      }

      // Handle different request types
      let response;
      
      if (url.pathname.startsWith('/api/')) {
        // API requests - proxy to backend with authentication
        response = await handleApiRequest(request, env, domainConfig, secrets);
      } else if (url.pathname.startsWith('/admin/')) {
        // Admin requests - require authentication
        response = await handleAdminRequest(request, env, secrets);
      } else {
        // Static content - serve from appropriate source
        response = await handleStaticRequest(request, domainConfig);
      }

      // Add security headers to all responses
      return addSecurityHeaders(response, domainConfig);
      
    } catch (error) {
      console.error('Worker error:', error);
      return new Response('Internal Server Error', { status: 500 });
    }
  }
};

/**
 * Get appropriate secrets for domain
 */
async function getSecretsForDomain(env, domainConfig) {
  const secrets = {};
  
  // Always get domain configuration
  secrets.primaryDomain = await env.spirit_immortals_domains.get("PRIMARY_DOMAIN");
  secrets.adminEmail = await env.spirit_immortals_domains.get("ADMIN_EMAIL");
  
  // Get authentication secrets for API requests
  secrets.jwtSecret = await env.spirit_immortals_auth.get("JWT_SECRET_KEY");
  
  // Get database credentials if needed
  if (domainConfig.type === 'platform') {
    secrets.dbHost = await env.spirit_immortals_database.get("AWS_DB_HOST");
    secrets.dbUser = await env.spirit_immortals_database.get("AWS_DB_USER");
  }
  
  return secrets;
}

/**
 * Perform security checks on incoming requests
 */
async function performSecurityChecks(request, env, secrets) {
  const url = new URL(request.url);
  const clientIP = request.headers.get('CF-Connecting-IP');
  const userAgent = request.headers.get('User-Agent') || '';
  
  // Check for suspicious patterns
  const suspiciousPatterns = [
    /union\s+select/i,
    /<script/i,
    /\.\.\/\.\.\//,
    /eval\s*\(/i,
    /javascript:/i
  ];
  
  const fullUrl = url.toString();
  for (const pattern of suspiciousPatterns) {
    if (pattern.test(fullUrl)) {
      return { blocked: true, reason: 'Suspicious URL pattern detected' };
    }
  }
  
  // Check user agent
  if (!userAgent || userAgent.length < 10) {
    return { blocked: true, reason: 'Invalid or missing User-Agent' };
  }
  
  // Rate limiting check (simplified - use KV storage for production)
  const rateLimitKey = `rate_limit:${clientIP}`;
  const rateLimitThreshold = await env.spirit_immortals_security.get("RATE_LIMIT_THRESHOLD") || "100";
  
  // Additional checks can be added here
  
  return { blocked: false };
}

/**
 * Handle API requests with authentication
 */
async function handleApiRequest(request, env, domainConfig, secrets) {
  const authHeader = request.headers.get('Authorization');
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return new Response('Authentication required', { 
      status: 401,
      headers: { 'WWW-Authenticate': 'Bearer' }
    });
  }
  
  // Verify JWT token (simplified - implement full verification)
  const token = authHeader.substring(7);
  // TODO: Implement JWT verification using secrets.jwtSecret
  
  // Proxy to backend
  const backendUrl = new URL(request.url);
  backendUrl.hostname = new URL(domainConfig.backend).hostname;
  
  const backendRequest = new Request(backendUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body
  });
  
  return await fetch(backendRequest);
}

/**
 * Handle admin requests with additional security
 */
async function handleAdminRequest(request, env, secrets) {
  // Additional admin authentication logic
  const clientIP = request.headers.get('CF-Connecting-IP');
  
  // Check if IP is in allowed admin IPs (store in secrets)
  // For now, require authentication
  
  return new Response('Admin access requires additional authentication', {
    status: 401
  });
}

/**
 * Handle static content requests
 */
async function handleStaticRequest(request, domainConfig) {
  if (domainConfig.type === 'company') {
    // Serve company website
    return await fetch(`${domainConfig.backend}${new URL(request.url).pathname}`);
  } else {
    // Serve platform frontend
    return await fetch(`${domainConfig.backend}${new URL(request.url).pathname}`);
  }
}

/**
 * Add security headers to response
 */
function addSecurityHeaders(response, domainConfig) {
  const newResponse = new Response(response.body, response);
  
  // Add all security headers
  Object.entries(SECURITY_HEADERS).forEach(([key, value]) => {
    newResponse.headers.set(key, value);
  });
  
  // Add domain-specific headers
  newResponse.headers.set('X-Domain-Type', domainConfig.type);
  newResponse.headers.set('X-Region', domainConfig.region);
  newResponse.headers.set('X-Powered-By', 'Spirit of the Immortals Ltd');
  
  return newResponse;
}

/**
 * Scheduled tasks for maintenance
 */
export async function scheduled(controller, env, ctx) {
  // Clean up rate limiting data
  // Update security configurations
  // Monitor domain health
  
  console.log('Scheduled maintenance completed');
}
