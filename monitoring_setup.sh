#!/bin/bash
# Production Monitoring and Backup Setup for Django IT Helpdesk

echo "🔧 Setting up production monitoring and backups..."

# 1. Install system monitoring tools
echo "📊 Installing monitoring tools..."
sudo apt update
sudo apt install -y htop iotop nethogs fail2ban ufw

# 2. Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# 3. Configure fail2ban for security
echo "🛡️ Configuring fail2ban..."
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Create Django-specific fail2ban filter
sudo tee /etc/fail2ban/filter.d/django.conf > /dev/null <<EOF
[Definition]
failregex = ^.* "POST /login/" 401 .*$
            ^.* "POST /admin/login/" 401 .*$
ignoreregex =
EOF

# Add Django jail to fail2ban
sudo tee -a /etc/fail2ban/jail.local > /dev/null <<EOF

[django]
enabled = true
port = http,https
filter = django
logpath = /path/to/your/project/logs/django.log
maxretry = 5
bantime = 3600
EOF

# 4. Create backup script
echo "💾 Creating backup script..."
sudo tee /usr/local/bin/django_backup.sh > /dev/null <<'EOF'
#!/bin/bash
# Django IT Helpdesk Backup Script

BACKUP_DIR="/backups/django_helpdesk"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/path/to/your/project"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
echo "Backing up database..."
mysqldump -u root -p django_it_help > $BACKUP_DIR/database_$DATE.sql

# Media files backup
echo "Backing up media files..."
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $PROJECT_DIR media/

# Application backup (excluding venv and logs)
echo "Backing up application..."
tar --exclude='venv' --exclude='logs' --exclude='*.pyc' --exclude='__pycache__' \
    -czf $BACKUP_DIR/app_$DATE.tar.gz -C $PROJECT_DIR .

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

# Make backup script executable
sudo chmod +x /usr/local/bin/django_backup.sh

# 5. Setup cron job for daily backups
echo "⏰ Setting up daily backups..."
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/django_backup.sh >> /var/log/django_backup.log 2>&1") | crontab -

# 6. Create log rotation
echo "📋 Setting up log rotation..."
sudo tee /etc/logrotate.d/django-helpdesk > /dev/null <<EOF
/path/to/your/project/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload gunicorn
    endscript
}
EOF

# 7. Create systemd service for Django
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/django-helpdesk.service > /dev/null <<EOF
[Unit]
Description=Django IT Helpdesk
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment=PATH=/path/to/your/project/venv/bin
Environment=DJANGO_SETTINGS_MODULE=helpdesk.settings_production
ExecStart=/path/to/your/project/venv/bin/gunicorn helpdesk.wsgi:application -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable django-helpdesk
sudo systemctl start django-helpdesk

echo "✅ Monitoring and backup setup completed!"
echo ""
echo "📋 What was configured:"
echo "- Firewall (UFW) with proper ports"
echo "- Fail2ban for security"
echo "- Daily database and file backups"
echo "- Log rotation"
echo "- Systemd service for Django"
echo ""
echo "🔧 Manual steps needed:"
echo "1. Update paths in the scripts to match your server"
echo "2. Configure database backup password"
echo "3. Test backup script: sudo /usr/local/bin/django_backup.sh"
echo "4. Monitor logs: tail -f /var/log/django_backup.log"
