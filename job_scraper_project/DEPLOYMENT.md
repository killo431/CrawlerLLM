# Production Deployment Guide

This guide covers deploying the Job Scraper project to production environments.

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Docker and Docker Compose installed
- Python 3.11+ (if deploying without Docker)
- At least 2GB RAM
- 10GB disk space

## Deployment Options

### Option 1: Docker Deployment (Recommended)

#### 1. Clone the Repository

```bash
git clone https://github.com/killo431/CrawlerLLM.git
cd CrawlerLLM/job_scraper_project
```

#### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your production settings
nano .env
```

#### 3. Build and Start Services

```bash
# Build the image
docker-compose build

# Start services in detached mode
docker-compose up -d

# Check logs
docker-compose logs -f
```

#### 4. Access the Application

- Dashboard: `http://your-server:8501`
- CLI: `docker-compose --profile cli up job-scraper-cli`

#### 5. Monitoring

```bash
# View logs
docker-compose logs -f job-scraper

# Check container status
docker-compose ps

# Restart services
docker-compose restart

# Stop services
docker-compose down
```

### Option 2: Direct Python Deployment

#### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install system dependencies for Playwright
sudo apt install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2
```

#### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/killo431/CrawlerLLM.git
cd CrawlerLLM/job_scraper_project

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure environment
cp .env.example .env
nano .env
```

#### 3. Create Systemd Service

Create `/etc/systemd/system/job-scraper.service`:

```ini
[Unit]
Description=Job Scraper Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/CrawlerLLM/job_scraper_project
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 4. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable job-scraper
sudo systemctl start job-scraper
sudo systemctl status job-scraper
```

### Option 3: Cloud Deployment

#### AWS EC2

1. Launch EC2 instance (t3.medium or larger)
2. Configure security group:
   - Allow port 8501 (Streamlit)
   - Allow port 22 (SSH)
3. Follow "Direct Python Deployment" steps
4. Consider using Elastic Load Balancer
5. Set up CloudWatch for monitoring

#### Google Cloud Platform

```bash
# Deploy to Cloud Run
gcloud run deploy job-scraper \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### DigitalOcean

1. Create Droplet (2GB RAM minimum)
2. Follow "Docker Deployment" steps
3. Configure firewall
4. Set up monitoring and alerts

## Production Configuration

### Environment Variables

Critical production settings in `.env`:

```bash
# Logging
LOG_LEVEL=WARNING

# Performance
MAX_RETRIES=5
TIMEOUT=60

# Security
# Add API keys here (never commit to git)
```

### Nginx Reverse Proxy

Install and configure Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable HTTPS with Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Security Hardening

### 1. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Secure Secrets

- Use environment variables for secrets
- Never commit `.env` files
- Rotate API keys regularly
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)

### 3. User Permissions

```bash
# Create dedicated user
sudo useradd -m -s /bin/bash scraper
sudo chown -R scraper:scraper /path/to/project
```

### 4. Rate Limiting

Configure rate limiting in your reverse proxy or application.

## Monitoring and Logging

### Application Logs

```bash
# View logs
tail -f logs/*.log

# With Docker
docker-compose logs -f
```

### Health Checks

Access health endpoint (implement in dashboard):

```bash
curl http://localhost:8501/health
```

### Monitoring Stack

Consider setting up:

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Alertmanager**: Alerting
- **ELK Stack**: Log aggregation

### Uptime Monitoring

Use services like:
- UptimeRobot
- Pingdom
- StatusCake

## Backup Strategy

### Database Backups

```bash
# Backup output data
tar -czf backup-$(date +%Y%m%d).tar.gz data/output/

# Upload to cloud storage
aws s3 cp backup-*.tar.gz s3://your-bucket/backups/
```

### Automated Backups

Create cron job:

```bash
0 2 * * * /path/to/backup-script.sh
```

## Scaling

### Horizontal Scaling

```bash
# Scale with Docker Compose
docker-compose up --scale job-scraper-cli=3
```

### Load Balancing

Use Nginx or cloud load balancer to distribute traffic across multiple instances.

### Database

For high volume:
- Migrate from file storage to PostgreSQL
- Implement connection pooling
- Use read replicas

## Performance Optimization

### 1. Caching

- Implement Redis for caching
- Cache API responses
- Use CDN for static assets

### 2. Async Processing

- Use Celery for background tasks
- Implement job queues
- Process scraping asynchronously

### 3. Resource Limits

Docker resource limits:

```yaml
services:
  job-scraper:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Troubleshooting

### Common Issues

1. **Out of Memory**
   - Increase container/server memory
   - Optimize scraping batch size
   - Implement pagination

2. **Browser Crashes**
   - Increase shared memory in Docker
   - Update Playwright browsers
   - Add retry logic

3. **Slow Performance**
   - Enable caching
   - Optimize database queries
   - Use connection pooling

### Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=DEBUG python main.py
```

## Maintenance

### Regular Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart services
sudo systemctl restart job-scraper
# OR
docker-compose restart
```

### Database Maintenance

```bash
# Clean old data
find data/output -type f -mtime +30 -delete

# Vacuum database (if using PostgreSQL)
psql -c "VACUUM ANALYZE;"
```

## Disaster Recovery

### Backup Recovery

```bash
# Restore from backup
tar -xzf backup-20251106.tar.gz -C /path/to/project/
```

### High Availability

- Use multi-region deployment
- Implement automatic failover
- Maintain hot standby servers

## Cost Optimization

### Cloud Resources

- Use spot instances for batch jobs
- Implement auto-scaling
- Schedule downtime for dev environments
- Use reserved instances for production

### Storage

- Compress old data
- Archive to cold storage
- Implement data retention policies

## Compliance

### Data Protection

- Implement GDPR compliance
- Add data anonymization
- Provide data export/deletion
- Maintain audit logs

### Legal

- Respect robots.txt
- Follow rate limits
- Obtain necessary permissions
- Review terms of service

## Support

For production support:
- GitHub Issues: Technical problems
- Email: Production emergencies
- Documentation: Setup questions

## Checklist

Before going to production:

- [ ] Environment variables configured
- [ ] Secrets secured
- [ ] Firewall configured
- [ ] HTTPS enabled
- [ ] Backups configured
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] Health checks working
- [ ] Documentation updated
- [ ] Load testing completed
- [ ] Security audit performed
- [ ] Disaster recovery tested

---

**Last Updated**: November 6, 2025
