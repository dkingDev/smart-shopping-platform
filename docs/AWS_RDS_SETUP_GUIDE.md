# AWS RDS PostgreSQL Setup Guide
# Complete production-ready configuration for smart shopping platform

## Step 1: Create AWS RDS Instance

### Option A: AWS Console (Recommended for beginners)
1. Go to AWS RDS Console: https://console.aws.amazon.com/rds/
2. Click "Create database"
3. Choose "PostgreSQL"
4. Select "Free tier" or "Production" template
5. Configure:
   - DB instance identifier: `smartshopping-db`
   - Master username: `admin`
   - Master password: [secure password]
   - DB instance class: `db.t3.micro` (free tier) or `db.t3.small`
   - Storage: 20 GB (can auto-scale)
   - VPC: Default or create new
   - Public access: Yes (for initial setup)
   - Security group: Create new or use existing

### Option B: AWS CLI Commands
```bash
# Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name smartshopping-subnet \
  --db-subnet-group-description "Smart Shopping DB Subnet Group" \
  --subnet-ids subnet-12345678 subnet-87654321

# Create security group
aws ec2 create-security-group \
  --group-name smartshopping-db-sg \
  --description "Smart Shopping Database Security Group"

# Add PostgreSQL port rule
aws ec2 authorize-security-group-ingress \
  --group-name smartshopping-db-sg \
  --protocol tcp \
  --port 5432 \
  --cidr 0.0.0.0/0

# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier smartshopping-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username admin \
  --master-user-password YourSecurePassword123! \
  --allocated-storage 20 \
  --storage-type gp2 \
  --storage-encrypted \
  --vpc-security-group-ids sg-your-security-group-id \
  --db-subnet-group-name smartshopping-subnet \
  --backup-retention-period 7 \
  --publicly-accessible
```

### Option C: Terraform Configuration
```hcl
# terraform/rds.tf
resource "aws_db_instance" "smartshopping" {
  identifier = "smartshopping-db"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type         = "gp2"
  storage_encrypted    = true
  
  db_name  = "smartshopping"
  username = "admin"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = true
  deletion_protection = false
  
  tags = {
    Name = "SmartShopping Database"
    Environment = "production"
  }
}

resource "aws_security_group" "rds" {
  name_prefix = "smartshopping-rds-"
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Step 2: Get Connection Details

After RDS instance is created, get these details:
- **Endpoint**: `smartshopping-db.c1234567890.us-east-1.rds.amazonaws.com`
- **Port**: `5432`
- **Database Name**: `postgres` (default) or your custom name
- **Username**: `admin`
- **Password**: [your password]

## Security Considerations

### Production Security Group Rules
```bash
# More restrictive for production
aws ec2 authorize-security-group-ingress \
  --group-name smartshopping-db-sg \
  --protocol tcp \
  --port 5432 \
  --source-group sg-app-servers-id  # Only allow app servers
```

### SSL/TLS Configuration
```python
# Ensure SSL in connection parameters
params = {
    "host": "your-endpoint.amazonaws.com",
    "port": "5432",
    "database": "smartshopping", 
    "user": "admin",
    "password": "your_password",
    "sslmode": "require",  # Force SSL
    "sslcert": "client-cert.pem",
    "sslkey": "client-key.pem",
    "sslrootcert": "ca-cert.pem"
}
```

## Monitoring Setup

### CloudWatch Alarms
```bash
# High CPU usage alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "RDS-HighCPU" \
  --alarm-description "RDS instance high CPU" \
  --metric-name CPUUtilization \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=DBInstanceIdentifier,Value=smartshopping-db \
  --evaluation-periods 2

# High connection count alarm  
aws cloudwatch put-metric-alarm \
  --alarm-name "RDS-HighConnections" \
  --alarm-description "RDS instance high connections" \
  --metric-name DatabaseConnections \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 15 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=DBInstanceIdentifier,Value=smartshopping-db \
  --evaluation-periods 2
```

## Cost Optimization

### For Development/Testing
- Use `db.t3.micro` (free tier eligible)
- 20 GB storage with auto-scaling
- Single AZ deployment
- Automated backups (7 days)

### For Production
- Use `db.t3.small` or larger
- Multi-AZ deployment for high availability
- Read replicas for analytics workloads
- 30-day backup retention

## Next Steps After RDS Creation

1. **Test Connection**: Use psql or pgAdmin to connect
2. **Configure Environment**: Update .env file with endpoint details  
3. **Run Database Setup**: Execute schema creation scripts
4. **Load Initial Data**: Import product catalogs and test data
5. **Setup Monitoring**: Configure CloudWatch alarms and dashboards

## Common Issues and Solutions

### Connection Timeout
- Check security group allows port 5432
- Verify VPC routing and internet gateway
- Ensure public accessibility is enabled

### SSL/TLS Errors
- Download RDS CA certificate bundle
- Configure SSL mode in connection string
- Update client certificates if using mutual TLS

### Performance Issues
- Monitor CPU and memory usage
- Analyze slow query logs
- Consider read replicas for analytics
- Optimize indexes and queries

Your AWS RDS PostgreSQL instance will be the robust, scalable foundation for your smart shopping platform!
