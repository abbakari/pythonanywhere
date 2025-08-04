# Apache Setup for Django IT Helpdesk on Windows

## 1. Download and Install Apache

1. Download **Apache 2.4** from https://www.apachelounge.com/download/
2. Extract to `C:\Apache24`
3. Open Command Prompt as Administrator
4. Navigate to `C:\Apache24\bin`
5. Install Apache as Windows service:
   ```cmd
   httpd.exe -k install
   ```

## 2. Install mod_wsgi

1. Install mod_wsgi for your Python version:
   ```cmd
   pip install mod_wsgi
   ```
2. Get mod_wsgi module location:
   ```cmd
   mod_wsgi-express module-config
   ```
3. Copy the output to Apache's `httpd.conf`

## 3. Configure Apache

Edit `C:\Apache24\conf\httpd.conf`:

```apache
# Add at the end of the file
<VirtualHost *:80>
    ServerName superdoll.co.tz
    ServerAlias www.superdoll.co.tz
    DocumentRoot "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main"
    
    WSGIDaemonProcess django python-path="C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main" python-home="C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/venv"
    WSGIProcessGroup django
    WSGIScriptAlias / "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/helpdesk/wsgi.py"
    
    <Directory "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/helpdesk">
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    Alias /static "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/staticfiles"
    <Directory "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/staticfiles">
        Require all granted
    </Directory>
    
    Alias /media "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/media"
    <Directory "C:/Users/abbak/Desktop/superIT/atarIT-main/atarIT-main/media">
        Require all granted
    </Directory>
</VirtualHost>
```

## 4. Start Apache

```cmd
# Start Apache service
net start Apache2.4

# Or restart if already running
net stop Apache2.4
net start Apache2.4
```
