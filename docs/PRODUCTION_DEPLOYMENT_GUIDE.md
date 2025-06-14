# Production Deployment Guide for Smart Shopping Platform

## Railway Deployment (Recommended - Easy PostgreSQL integration)

### 1. Prepare for Railway
Create these files for Railway deployment:

#### railway.toml
```toml
[build]
builder = "NIXPACKS"

[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"

[env]
NODE_ENV = "production"
PYTHONPATH = "/app"
```

#### Procfile
```
web: uvicorn shopping_website_fastapi:app --host 0.0.0.0 --port $PORT
```

#### requirements.txt (production)
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
pandas==2.1.4
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
requests==2.31.0
sqlalchemy==2.0.23
alembic==1.13.1
```

### 2. Railway Deployment Steps
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add PostgreSQL database
railway add -d postgresql

# Set environment variables
railway variables set AWS_DB_HOST=${{PGHOST}}
railway variables set AWS_DB_PORT=${{PGPORT}}
railway variables set AWS_DB_NAME=${{PGDATABASE}}
railway variables set AWS_DB_USER=${{PGUSER}}
railway variables set AWS_DB_PASSWORD=${{PGPASSWORD}}
railway variables set JWT_SECRET_KEY="your-production-jwt-secret"

# Deploy
railway up
```

## Vercel Deployment (Serverless)

### 1. Prepare for Vercel
#### vercel.json
```json
{
  "builds": [
    {
      "src": "shopping_website_fastapi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "shopping_website_fastapi.py"
    }
  ],
  "env": {
    "PYTHONPATH": "/var/task"
  }
}
```

#### api/index.py (Vercel entry point)
```python
from shopping_website_fastapi import app

# Vercel expects a handler function
def handler(request):
    return app(request.environ, lambda *args: None)
```

### 2. Vercel Deployment Steps
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Set environment variables
vercel env add AWS_DB_HOST
vercel env add AWS_DB_PORT
vercel env add AWS_DB_NAME
vercel env add AWS_DB_USER
vercel env add AWS_DB_PASSWORD
vercel env add JWT_SECRET_KEY

# Deploy
vercel --prod
```

## AWS EC2 Deployment (Full Control)

### 1. Launch EC2 Instance
```bash
# Create key pair
aws ec2 create-key-pair --key-name smartshopping-key --query 'KeyMaterial' --output text > smartshopping-key.pem
chmod 400 smartshopping-key.pem

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.micro \
  --key-name smartshopping-key \
  --security-group-ids sg-your-security-group \
  --subnet-id subnet-your-subnet
```

### 2. Setup EC2 Instance
```bash
# Connect to instance
ssh -i smartshopping-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip git nginx -y

# Clone your repository
git clone https://github.com/yourusername/smart-shopping-platform.git
cd smart-shopping-platform

# Install Python dependencies
pip3 install -r requirements.txt

# Setup systemd service
sudo tee /etc/systemd/system/smartshopping.service > /dev/null <<EOF
[Unit]
Description=Smart Shopping FastAPI
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/smart-shopping-platform
Environment=PATH=/usr/local/bin
ExecStart=/usr/local/bin/uvicorn shopping_website_fastapi:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable smartshopping
sudo systemctl start smartshopping

# Configure Nginx
sudo tee /etc/nginx/conf.d/smartshopping.conf > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo systemctl restart nginx
```

## Docker Deployment

### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "shopping_website_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose with PostgreSQL
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AWS_DB_HOST=db
      - AWS_DB_PORT=5432
      - AWS_DB_NAME=smartshopping
      - AWS_DB_USER=postgres
      - AWS_DB_PASSWORD=password
      - JWT_SECRET_KEY=your-secret-key
    depends_on:
      - db
    volumes:
      - .:/app
    command: uvicorn shopping_website_fastapi:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=smartshopping
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## Load Balancer & SSL Setup

### 1. AWS Application Load Balancer
```bash
# Create load balancer
aws elbv2 create-load-balancer \
  --name smartshopping-alb \
  --subnets subnet-12345678 subnet-87654321 \
  --security-groups sg-your-alb-sg

# Create target group
aws elbv2 create-target-group \
  --name smartshopping-targets \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-your-vpc-id \
  --health-check-path /health

# Register targets
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/smartshopping-targets \
  --targets Id=i-your-instance-id,Port=8000
```

### 2. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo amazon-linux-extras install epel -y
sudo yum install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## Environment Variables for Production

### Complete Production .env
```bash
# Database
AWS_DB_HOST=smartshopping-db.c1a2b3c4d5e6.us-east-1.rds.amazonaws.com
AWS_DB_PORT=5432
AWS_DB_NAME=smartshopping
AWS_DB_USER=admin
AWS_DB_PASSWORD=YourProductionPassword123!

# Security
JWT_SECRET_KEY=your-32-character-production-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS for production
ALLOWED_ORIGINS=["https://yourdomain.com", "https://app.yourdomain.com"]

# Application
ENVIRONMENT=production
DEBUG=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Monetization
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Affiliate IDs
TESCO_AFFILIATE_ID=your_live_tesco_id
MORRISONS_AFFILIATE_ID=your_live_morrisons_id

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=your_app_password
```

## Monitoring and Logging

### 1. Application Monitoring
```python
# Add to shopping_website_fastapi.py
import logging
from fastapi import Request
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logging.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    return response
```

### 2. Health Check Endpoint
```python
@app.get("/health")
async def health_check():
    try:
        # Test database connection
        with get_database_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Unhealthy: {str(e)}")
```

## Performance Optimization

### 1. Database Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800
)
```

### 2. Redis Caching
```python
import redis
from functools import wraps

redis_client = redis.from_url(os.getenv("REDIS_URL"))

def cache_result(expiry=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Get fresh data
            result = await func(*args, **kwargs)
            
            # Cache the result
            redis_client.setex(
                cache_key, 
                expiry, 
                json.dumps(result, default=str)
            )
            
            return result
        return wrapper
    return decorator
```

Your FastAPI application is now ready for production deployment across multiple platforms with full monitoring, security, and performance optimizations!
