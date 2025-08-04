# DNS Configuration for superdoll.co.tz

## Step 1: Find Your Public IP Address

### If hosting from your Windows computer:
1. Go to https://whatismyipaddress.com/
2. Note your **IPv4 address** (e.g., 203.123.45.67)

### If using a hosting provider:
- Use the IP address provided by your hosting service

## Step 2: Configure DNS Records

Contact your domain registrar (where you bought superdoll.co.tz) and add these DNS records:

### Required DNS Records:
```
Type: A
Name: @
Value: YOUR_PUBLIC_IP_ADDRESS
TTL: 300 (5 minutes)

Type: A
Name: www
Value: YOUR_PUBLIC_IP_ADDRESS  
TTL: 300 (5 minutes)

Type: CNAME (optional)
Name: mail
Value: superdoll.co.tz
TTL: 300 (5 minutes)
```

## Step 3: Check DNS Propagation

### Online Tools:
- https://dnschecker.org/
- https://www.whatsmydns.net/

### Command Line (Windows):
```cmd
# Check A record
nslookup superdoll.co.tz

# Check with specific DNS server
nslookup superdoll.co.tz 8.8.8.8
```

## Step 4: Router Configuration (If Hosting from Home)

### Port Forwarding:
1. Access your router admin panel (usually 192.168.1.1)
2. Find **Port Forwarding** or **Virtual Server** settings
3. Add rules:
   - **Service Name:** HTTP
   - **External Port:** 80
   - **Internal IP:** Your computer's local IP
   - **Internal Port:** 80
   - **Protocol:** TCP
   
   - **Service Name:** HTTPS
   - **External Port:** 443
   - **Internal IP:** Your computer's local IP
   - **Internal Port:** 443
   - **Protocol:** TCP

### Find Your Local IP:
```cmd
ipconfig
```
Look for "IPv4 Address" under your active network adapter.

## Step 5: Firewall Configuration

### Windows Firewall:
1. Open **Windows Defender Firewall**
2. Click **Advanced settings**
3. **Inbound Rules** → **New Rule**
4. **Port** → **TCP** → **Specific Local Ports:** 80,443
5. **Allow the connection**
6. Apply to all profiles
7. Name: "Django IT Helpdesk HTTP/HTTPS"

## Step 6: Test Domain Access

1. Wait 15-30 minutes for DNS propagation
2. Open browser and test:
   - http://superdoll.co.tz
   - http://www.superdoll.co.tz
3. Should load your Django application

## Troubleshooting:

### Domain doesn't resolve:
- Check DNS records are correct
- Wait longer for propagation (up to 48 hours)
- Try different DNS servers (8.8.8.8, 1.1.1.1)

### Domain resolves but site doesn't load:
- Check firewall settings
- Verify port forwarding (if hosting from home)
- Ensure Django application is running
- Check IIS/Apache configuration
