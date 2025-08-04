# SSL Certificate Setup for Windows

## Option A: Let's Encrypt with win-acme (Free SSL)

### 1. Download win-acme
1. Go to https://www.win-acme.com/
2. Download the latest release
3. Extract to `C:\win-acme`

### 2. Generate SSL Certificate
1. Open Command Prompt as Administrator
2. Navigate to `C:\win-acme`
3. Run the certificate wizard:
   ```cmd
   wacs.exe
   ```
4. Select option **N** (Create certificate with advanced options)
5. Select **2** (Manual input)
6. Enter domains: `superdoll.co.tz,www.superdoll.co.tz`
7. Select **2** (Http validation)
8. Select **1** (Self-hosting)
9. Select **3** (IIS Central Certificate Store) or **1** (IIS bindings)
10. Follow the prompts to complete setup

### 3. Configure IIS for HTTPS
1. Open IIS Manager
2. Select your website
3. Click **Bindings** in Actions panel
4. Click **Add**
5. Type: **https**
6. Port: **443**
7. Host name: **superdoll.co.tz**
8. SSL certificate: Select your Let's Encrypt certificate
9. Repeat for **www.superdoll.co.tz**

## Option B: Cloudflare SSL (Recommended for Simplicity)

### 1. Sign up for Cloudflare
1. Go to https://cloudflare.com
2. Create free account
3. Add your domain `superdoll.co.tz`

### 2. Update DNS to Cloudflare
1. Change nameservers at your domain registrar to Cloudflare's nameservers
2. Wait for DNS propagation (24-48 hours)

### 3. Enable SSL in Cloudflare
1. Go to **SSL/TLS** tab in Cloudflare dashboard
2. Set encryption mode to **Full (strict)**
3. Enable **Always Use HTTPS**
4. Enable **HTTP Strict Transport Security (HSTS)**

### 4. Configure Origin Certificate
1. In Cloudflare, go to **SSL/TLS** → **Origin Certificates**
2. Click **Create Certificate**
3. Download the certificate and private key
4. Install in IIS:
   - Convert to PFX format if needed
   - Import in IIS Manager → Server Certificates

## Option C: Commercial SSL Certificate

### 1. Purchase SSL Certificate
- From providers like GoDaddy, Namecheap, or DigiCert
- Choose Domain Validated (DV) certificate for basic needs

### 2. Generate Certificate Signing Request (CSR)
1. In IIS Manager, go to **Server Certificates**
2. Click **Create Certificate Request**
3. Fill in organization details
4. Save CSR file

### 3. Submit CSR to Certificate Authority
1. Upload CSR to your SSL provider
2. Complete domain validation
3. Download issued certificate

### 4. Complete Certificate Request
1. In IIS Manager → **Server Certificates**
2. Click **Complete Certificate Request**
3. Select downloaded certificate file
4. Assign to your website bindings
