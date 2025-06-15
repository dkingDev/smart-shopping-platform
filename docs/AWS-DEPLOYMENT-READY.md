# 🚀 AWS EC2 + CLOUDFLARE DEPLOYMENT - READY TO LAUNCH

## ✅ EVERYTHING IS CONFIGURED AND READY

Your Smart Shopping Platform is now configured for production deployment with:
- **FastAPI + Uvicorn** (port 8000)
- **Nginx reverse proxy** (port 80) 
- **Systemd service** for auto-restart
- **Cloudflare SSL/CDN** integration
- **AWS EC2** hosting (51.21.152.177)

---

## 🎯 DEPLOYMENT STEPS

### **Step 1: Upload to EC2**
```bash
# Update the SSH key path in upload_to_ec2.sh first
bash upload_to_ec2.sh
```

### **Step 2: SSH to EC2 and Deploy**
```bash
ssh -i your-key.pem ubuntu@51.21.152.177
cd smart-shopping-platform
bash deploy_to_ec2_production.sh
```

### **Step 3: Configure Environment**
```bash
# Edit .env file with your real database credentials
nano .env
```

### **Step 4: Add Cloudflare DNS Records**
Use the records in `config/cloudflare-dns-records.txt`:
```
thesmartshoppingsite.com         A    51.21.152.177  (Proxied)
www.thesmartshoppingsite.com     A    51.21.152.177  (Proxied)
spiritoftheimmortalsltd.co.uk    A    51.21.152.177  (Proxied)
```

---

## 🔧 ARCHITECTURE OVERVIEW

```
Internet → Cloudflare CDN/SSL → EC2 (51.21.152.177)
                                  ↓
                               Nginx (Port 80) 
                                  ↓
                            FastAPI/Uvicorn (Port 8000)
                                  ↓
                            AWS PostgreSQL Database
```

---

## ✅ WHAT HAPPENS WHEN YOU DEPLOY

1. **System Setup**: Updates Ubuntu, installs Python/Nginx
2. **App Installation**: Creates virtual environment, installs requirements  
3. **Nginx Configuration**: Reverse proxy with security headers
4. **Systemd Service**: Auto-start FastAPI on boot
5. **Service Start**: Launches both Nginx and FastAPI
6. **Health Checks**: Verifies everything is running

---

## 🌐 YOUR LIVE DOMAINS

After deployment, these will work:
- **https://thesmartshoppingsite.com** - Shopping platform
- **https://thesmartshoppingsite.co.uk** - UK shopping 
- **https://spiritoftheimmortalsltd.co.uk** - Company website
- **https://spiritoftheimmortals.co.uk** - Company redirect

---

## 🔍 MONITORING & MANAGEMENT

```bash
# Check service status
sudo systemctl status smart-shopping

# View logs
sudo journalctl -u smart-shopping -f

# Restart services
sudo systemctl restart smart-shopping
sudo systemctl restart nginx

# Check what's running
sudo netstat -tlnp | grep -E ':(80|8000)'
```

---

## 🛠️ TROUBLESHOOTING

**If sites don't load:**
1. Check services: `sudo systemctl status smart-shopping nginx`
2. Check ports: `sudo netstat -tlnp | grep -E ':(80|8000)'`
3. Check DNS: `nslookup thesmartshoppingsite.com`
4. Check SSL: Cloudflare SSL/TLS tab

**If 502 errors:**
- FastAPI service down: `sudo systemctl restart smart-shopping`
- Database connection: Check `.env` credentials

---

## 🎉 SUCCESS METRICS

✅ FastAPI responds on port 8000
✅ Nginx proxies on port 80  
✅ Services auto-start on reboot
✅ Cloudflare SSL working
✅ All domains resolve correctly
✅ Database connections active

---

**🚀 YOU'RE READY TO LAUNCH! Run `bash upload_to_ec2.sh` to begin!**
