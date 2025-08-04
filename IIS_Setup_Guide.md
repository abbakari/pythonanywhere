# IIS Setup for Django IT Helpdesk on Windows

## 1. Enable IIS on Windows

### Windows 10/11 Pro:
1. Open **Control Panel** → **Programs** → **Turn Windows features on or off**
2. Check **Internet Information Services (IIS)**
3. Expand IIS and check:
   - **Web Management Tools** → **IIS Management Console**
   - **World Wide Web Services** → **Application Development Features** → **CGI**
   - **World Wide Web Services** → **Common HTTP Features** (all items)
4. Click **OK** and restart if prompted

### Windows Server:
1. Open **Server Manager**
2. Click **Add roles and features**
3. Select **Web Server (IIS)** role
4. Add **CGI** feature under Application Development

## 2. Install URL Rewrite Module

1. Download **URL Rewrite Module 2.1** from Microsoft
2. Install the downloaded file
3. Restart IIS Manager

## 3. Configure IIS for Django

### Create Website:
1. Open **IIS Manager**
2. Right-click **Sites** → **Add Website**
3. **Site name:** `Django IT Helpdesk`
4. **Physical path:** `C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main`
5. **Binding:** 
   - Type: HTTP
   - Port: 80
   - Host name: `superdoll.co.tz`
6. Click **OK**

### Configure Reverse Proxy:
1. Select your website in IIS Manager
2. Double-click **URL Rewrite**
3. Click **Add Rule(s)** → **Reverse Proxy**
4. **Inbound Rules:**
   - Server name: `127.0.0.1:8000`
   - Enable SSL Offloading: ✓
5. Click **OK**

## 4. Static Files Configuration

1. In IIS Manager, select your website
2. Right-click → **Add Virtual Directory**
3. **Alias:** `static`
4. **Physical path:** `C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main\staticfiles`
5. Repeat for media files:
   - **Alias:** `media`
   - **Physical path:** `C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main\media`

## 5. Start Your Django Application

Before starting IIS, make sure your Django app is running:

```cmd
cd C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main
.\venv\Scripts\activate
set DJANGO_SETTINGS_MODULE=helpdesk.settings_production
gunicorn helpdesk.wsgi:application -c gunicorn.conf.py
```

## 6. Test Configuration

1. Open browser and go to `http://superdoll.co.tz`
2. Your Django application should load through IIS
