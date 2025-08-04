# Windows Production Monitoring and Backup Setup

## 1. 📊 System Monitoring

### Task Manager Enhanced Monitoring:
1. Open **Task Manager** (Ctrl+Shift+Esc)
2. Go to **Performance** tab
3. Monitor CPU, Memory, Disk, Network usage
4. Keep an eye on your Django processes

### Windows Performance Monitor:
1. Press **Win+R** → type `perfmon`
2. Create custom performance counters for:
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

### Event Viewer for Logs:
1. Press **Win+R** → type `eventvwr`
2. Monitor **Windows Logs** → **Application** for errors
3. Check **Windows Logs** → **System** for system issues

## 2. 🔄 Windows Services Setup

### Create Windows Service for Django:

1. **Install NSSM (Non-Sucking Service Manager):**
   - Download from https://nssm.cc/download
   - Extract to `C:\nssm`
   - Add to PATH environment variable

2. **Create Django Service:**
   ```cmd
   # Open Command Prompt as Administrator
   cd C:\nssm\win64
   
   # Create service
   nssm install "Django IT Helpdesk"
   ```

3. **Configure Service in NSSM GUI:**
   - **Application Path:** `C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main\venv\Scripts\python.exe`
   - **Startup Directory:** `C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main`
   - **Arguments:** `manage.py runserver 127.0.0.1:8000 --settings=helpdesk.settings_production`
   - **Service Name:** `Django IT Helpdesk`

4. **Set Environment Variables:**
   - Go to **Environment** tab in NSSM
   - Add: `DJANGO_SETTINGS_MODULE=helpdesk.settings_production`

5. **Start Service:**
   ```cmd
   net start "Django IT Helpdesk"
   ```

## 3. 💾 Automated Backup System

### Create Backup Script:

Create `C:\Scripts\django_backup.bat`:

```batch
@echo off
REM Django IT Helpdesk Backup Script for Windows

set BACKUP_DIR=C:\Backups\Django_Helpdesk
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATE=%DATE: =0%
set PROJECT_DIR=C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main

REM Create backup directory
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo Starting backup at %DATE%

REM Database backup using mysqldump
echo Backing up database...
"C:\xampp\mysql\bin\mysqldump.exe" -u root django_it_help > "%BACKUP_DIR%\database_%DATE%.sql"

REM Media files backup
echo Backing up media files...
powershell Compress-Archive -Path "%PROJECT_DIR%\media" -DestinationPath "%BACKUP_DIR%\media_%DATE%.zip" -Force

REM Application backup (excluding venv and logs)
echo Backing up application files...
powershell Compress-Archive -Path "%PROJECT_DIR%\helpdesk", "%PROJECT_DIR%\tickets", "%PROJECT_DIR%\static", "%PROJECT_DIR%\templates", "%PROJECT_DIR%\*.py", "%PROJECT_DIR%\*.txt", "%PROJECT_DIR%\*.md" -DestinationPath "%BACKUP_DIR%\app_%DATE%.zip" -Force

REM Environment file backup
copy "%PROJECT_DIR%\.env" "%BACKUP_DIR%\.env_%DATE%.backup"

REM Clean old backups (keep last 7 days)
forfiles /p "%BACKUP_DIR%" /s /m *.sql /d -7 /c "cmd /c del @path" 2>nul
forfiles /p "%BACKUP_DIR%" /s /m *.zip /d -7 /c "cmd /c del @path" 2>nul
forfiles /p "%BACKUP_DIR%" /s /m *.backup /d -7 /c "cmd /c del @path" 2>nul

echo Backup completed successfully at %DATE%
echo Backup location: %BACKUP_DIR%
```

### Schedule Daily Backups:

1. **Open Task Scheduler:**
   - Press **Win+R** → type `taskschd.msc`

2. **Create Basic Task:**
   - Click **Create Basic Task**
   - **Name:** `Django IT Helpdesk Daily Backup`
   - **Description:** `Daily backup of Django application and database`

3. **Configure Trigger:**
   - **Trigger:** Daily
   - **Start:** 2:00 AM
   - **Recur every:** 1 days

4. **Configure Action:**
   - **Action:** Start a program
   - **Program:** `C:\Scripts\django_backup.bat`
   - **Start in:** `C:\Scripts`

5. **Configure Settings:**
   - Check **Run with highest privileges**
   - **Configure for:** Windows 10/Windows Server 2016

## 4. 🔍 Application Monitoring

### Create Health Check Script:

Create `C:\Scripts\health_check.bat`:

```batch
@echo off
REM Django IT Helpdesk Health Check

set LOG_FILE=C:\Logs\health_check.log
set PROJECT_DIR=C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main

echo %date% %time% - Starting health check >> "%LOG_FILE%"

REM Check if Django service is running
sc query "Django IT Helpdesk" | find "RUNNING" >nul
if %errorlevel% equ 0 (
    echo %date% %time% - Django service is running >> "%LOG_FILE%"
) else (
    echo %date% %time% - ERROR: Django service is not running >> "%LOG_FILE%"
    net start "Django IT Helpdesk" >> "%LOG_FILE%" 2>&1
)

REM Check if website responds
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -TimeoutSec 10; if ($response.StatusCode -eq 200) { Write-Output 'Website is responding' } } catch { Write-Output 'Website is not responding' }" >> "%LOG_FILE%"

REM Check database connection
cd /d "%PROJECT_DIR%"
call venv\Scripts\activate.bat
python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('Database connection OK')" >> "%LOG_FILE%" 2>&1

echo %date% %time% - Health check completed >> "%LOG_FILE%"
```

### Schedule Health Checks:

1. **Create Task in Task Scheduler:**
   - **Name:** `Django Health Check`
   - **Trigger:** Every 15 minutes
   - **Action:** Run `C:\Scripts\health_check.bat`

## 5. 📧 Email Alerts Setup

### Create Alert Script:

Create `C:\Scripts\send_alert.ps1`:

```powershell
# Email Alert Script for Django IT Helpdesk

param(
    [string]$Subject,
    [string]$Body
)

$SMTPServer = "smtp.gmail.com"
$SMTPPort = 587
$Username = "abbakariamali@gmail.com"
$Password = "fjikqzmjqcfqhhfc"  # Your app password
$To = "abbakariamali@gmail.com"
$From = "superdoll.co.tz"

$SMTPClient = New-Object Net.Mail.SmtpClient($SMTPServer, $SMTPPort)
$SMTPClient.EnableSsl = $true
$SMTPClient.Credentials = New-Object System.Net.NetworkCredential($Username, $Password)

$MailMessage = New-Object System.Net.Mail.MailMessage
$MailMessage.From = $From
$MailMessage.To.Add($To)
$MailMessage.Subject = $Subject
$MailMessage.Body = $Body

try {
    $SMTPClient.Send($MailMessage)
    Write-Output "Alert email sent successfully"
} catch {
    Write-Output "Failed to send alert email: $($_.Exception.Message)"
}

$MailMessage.Dispose()
$SMTPClient.Dispose()
```

## 6. 🛡️ Security Monitoring

### Windows Defender Configuration:
1. **Open Windows Security**
2. **Virus & threat protection** → **Manage settings**
3. **Add exclusions** for your Django project folder
4. **Enable Real-time protection**

### Firewall Monitoring:
1. **Windows Defender Firewall** → **Advanced settings**
2. **Monitoring** → **Firewall** to view active connections
3. **Logging** → Enable logging for dropped packets

## 7. 📈 Performance Monitoring

### Resource Monitor:
1. Press **Win+R** → type `resmon`
2. Monitor **CPU**, **Memory**, **Disk**, **Network** tabs
3. Look for your Python/Django processes

### Performance Counters:
- **Process(python)\% Processor Time**
- **Process(python)\Working Set**
- **Web Service(_Total)\Bytes Total/sec**
- **Web Service(_Total)\Current Connections**

## 8. 🔧 Maintenance Tasks

### Weekly Maintenance Script:

Create `C:\Scripts\weekly_maintenance.bat`:

```batch
@echo off
REM Weekly maintenance for Django IT Helpdesk

echo Starting weekly maintenance...

REM Clear Django cache
cd /d "C:\Users\abbak\Desktop\superIT\atarIT-main\atarIT-main"
call venv\Scripts\activate.bat
python manage.py clearsessions
python manage.py collectstatic --noinput

REM Clear temporary files
del /q /s "%TEMP%\*" 2>nul
del /q /s "C:\Windows\Temp\*" 2>nul

REM Restart Django service
net stop "Django IT Helpdesk"
timeout /t 5
net start "Django IT Helpdesk"

echo Weekly maintenance completed
```

Schedule this to run every Sunday at 3:00 AM using Task Scheduler.

This comprehensive Windows monitoring and backup setup will ensure your Django IT Helpdesk application runs reliably in production!
