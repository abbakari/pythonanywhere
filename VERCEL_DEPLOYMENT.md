# 🚀 Django IT Helpdesk - Vercel Deployment Guide

This guide will help you deploy your Django IT Helpdesk application to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Cloud Database**: Set up a cloud MySQL database (see options below)
4. **Git Repository**: Your code should be in a Git repository

## 🗄️ Database Setup (Required)

Since Vercel is serverless, you need a cloud database. Choose one:

### Option 1: PlanetScale (Recommended)
```bash
# 1. Sign up at planetscale.com
# 2. Create a new database
# 3. Get connection details from the dashboard
# 4. Use the connection string in your environment variables
```

### Option 2: Railway
```bash
# 1. Sign up at railway.app
# 2. Create a MySQL database
# 3. Get connection details
# 4. Use in your Vercel environment variables
```

### Option 3: AWS RDS
```bash
# 1. Create an RDS MySQL instance
# 2. Configure security groups
# 3. Get connection details
# 4. Use in your Vercel environment variables
```

## 🔧 Configuration Files Created

The following files have been configured for Vercel:

- `helpdesk/settings_vercel.py` - Vercel-specific Django settings
- `vercel.json` - Vercel deployment configuration
- `build_files.sh` - Build script for static files
- `requirements.txt` - Updated dependencies
- `.env.vercel` - Environment variables template
- `deploy_vercel.py` - Deployment preparation script

## 🚀 Deployment Steps

### 1. Prepare Your Project
```bash
# Run the deployment preparation script
python deploy_vercel.py
```

### 2. Set Up Environment Variables
In your Vercel dashboard, add these environment variables:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=helpdesk.settings_vercel
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=3306
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_domain@example.com
```

### 3. Deploy to Vercel
```bash
# Login to Vercel
vercel login

# Deploy to production
vercel --prod

# Or deploy for preview
vercel
```

### 4. Set Up Custom Domain (Optional)
```bash
# Add your custom domain
vercel domains add superdoll.co.tz

# Configure DNS records as instructed by Vercel
```

## 🔍 Important Notes

### Limitations on Vercel
- **No WebSocket Support**: Django Channels won't work on Vercel serverless
- **No Background Tasks**: Use external services like Celery with Redis/RabbitMQ
- **Cold Starts**: First request may be slower due to serverless nature
- **File Storage**: Use cloud storage (AWS S3, Cloudinary) for media files

### Database Migrations
```bash
# Run migrations manually after deployment
vercel env pull .env.local
python manage.py migrate --settings=helpdesk.settings_vercel
```

### Static Files
- Handled automatically by `build_files.sh`
- Served through Vercel's CDN
- Compressed with WhiteNoise

## 🛠️ Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify your cloud database credentials
   - Check if the database server allows connections from Vercel IPs

2. **Static Files Not Loading**
   - Ensure `build_files.sh` runs successfully
   - Check `vercel.json` routing configuration

3. **Module Import Errors**
   - Verify all dependencies are in `requirements.txt`
   - Check Python version compatibility (3.11 recommended)

4. **Environment Variables**
   - Double-check all required variables are set in Vercel dashboard
   - Ensure no typos in variable names

### Debugging
```bash
# View deployment logs
vercel logs your-deployment-url

# Check function logs
vercel logs --follow
```

## 📊 Performance Optimization

1. **Database Connection Pooling**
   - Use connection pooling in your cloud database
   - Consider using `django-db-pool` for better performance

2. **Caching**
   - Database caching is configured
   - Consider Redis cache for better performance

3. **Static File Optimization**
   - Files are automatically compressed
   - Served through Vercel's global CDN

## 🔒 Security Considerations

- SSL/HTTPS is automatically handled by Vercel
- Environment variables are encrypted
- CORS is configured for your domain
- Security headers are enabled

## 💰 Cost Estimation

**Vercel Pro Plan** (~$20/month):
- Unlimited deployments
- Custom domains
- Analytics
- Team collaboration

**Database Costs** (varies by provider):
- PlanetScale: $29/month for production
- Railway: $5-20/month depending on usage
- AWS RDS: $15-50/month depending on instance

## 🎯 Next Steps After Deployment

1. **Create Superuser**
   ```bash
   python manage.py createsuperuser --settings=helpdesk.settings_vercel
   ```

2. **Test All Features**
   - Admin panel access
   - Ticket creation/management
   - Email notifications
   - File uploads

3. **Set Up Monitoring**
   - Use Vercel Analytics
   - Configure error tracking with Sentry
   - Set up uptime monitoring

4. **Backup Strategy**
   - Regular database backups
   - Export important data periodically

## 📞 Support

If you encounter issues:
1. Check Vercel documentation
2. Review deployment logs
3. Verify environment variables
4. Test database connectivity

Your Django IT Helpdesk is now ready for Vercel deployment! 🎉
