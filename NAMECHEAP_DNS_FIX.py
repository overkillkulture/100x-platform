#!/usr/bin/env python3
"""
NAMECHEAP DNS AUTOMATIC CONFIGURATION
Bypasses their terrible UI and configures DNS directly via API

NO MORE SEARCHING FOR "ADVANCED DNS" TAB
"""

import requests
import xml.etree.ElementTree as ET

# Namecheap API endpoint
API_URL = "https://api.namecheap.com/xml.response"

def configure_dns_for_netlify(domain, api_user, api_key, username, client_ip):
    """
    Configure DNS records for Netlify deployment

    Args:
        domain: Full domain (e.g., 'consciousnessrevolution.com')
        api_user: Namecheap API username
        api_key: Namecheap API key
        username: Namecheap account username
        client_ip: Your IP address (required by Namecheap)
    """

    # Split domain into SLD and TLD
    parts = domain.split('.')
    sld = parts[0]  # consciousnessrevolution
    tld = parts[1]  # com

    print(f"🌐 Configuring DNS for {domain}...")
    print(f"   SLD: {sld}")
    print(f"   TLD: {tld}")

    # DNS records for Netlify
    # A record: @ → 75.2.60.5 (Netlify load balancer)
    # CNAME: www → apex-loadbalancer.netlify.com

    params = {
        'ApiUser': api_user,
        'ApiKey': api_key,
        'UserName': username,
        'Command': 'namecheap.domains.dns.setHosts',
        'ClientIp': client_ip,
        'SLD': sld,
        'TLD': tld,

        # Record 1: A record for @ (root domain)
        'HostName1': '@',
        'RecordType1': 'A',
        'Address1': '75.2.60.5',
        'TTL1': '1800',  # 30 minutes

        # Record 2: CNAME for www
        'HostName2': 'www',
        'RecordType2': 'CNAME',
        'Address2': 'apex-loadbalancer.netlify.com',
        'TTL2': '1800',
    }

    print("\n📡 Sending DNS configuration to Namecheap API...")
    response = requests.get(API_URL, params=params)

    # Parse XML response
    root = ET.fromstring(response.text)

    # Check for errors
    errors = root.findall('.//{http://api.namecheap.com/xml.response}Error')
    if errors:
        print("\n❌ ERROR:")
        for error in errors:
            print(f"   {error.text}")
        return False

    # Check for success
    result = root.find('.//{http://api.namecheap.com/xml.response}DomainDNSSetHostsResult')
    if result is not None and result.get('IsSuccess') == 'true':
        print("\n✅ DNS CONFIGURED SUCCESSFULLY!")
        print(f"\n   A record:     consciousnessrevolution.com → 75.2.60.5")
        print(f"   CNAME record: www.consciousnessrevolution.com → apex-loadbalancer.netlify.com")
        print(f"\n⏰ DNS propagation: 5-30 minutes")
        print(f"   Check status: https://dnschecker.org/#A/consciousnessrevolution.com")
        return True
    else:
        print("\n❌ Unknown response from Namecheap:")
        print(response.text)
        return False


def get_current_ip():
    """Get your current public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json()['ip']
    except:
        print("⚠️  Could not auto-detect IP. You'll need to provide it manually.")
        return None


def enable_api_access_instructions():
    """
    Print instructions for enabling Namecheap API access
    """
    print("\n" + "="*60)
    print("HOW TO ENABLE NAMECHEAP API ACCESS")
    print("="*60)
    print("\n1. Login to Namecheap: https://www.namecheap.com/myaccount/login/")
    print("\n2. Go to Profile → Tools")
    print("   Direct link: https://ap.www.namecheap.com/settings/tools/apiaccess/")
    print("\n3. Enable API Access:")
    print("   - Toggle 'API Access' to ON")
    print("   - Whitelist your IP address (will show you your current IP)")
    print("\n4. Copy your API key")
    print("\n5. Come back here and run the configuration")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("\n🚀 NAMECHEAP DNS AUTOMATIC CONFIGURATION")
    print("="*60)

    # Check if API credentials are available
    # TODO: Store these securely in environment variables or .env file

    print("\n⚠️  API ACCESS REQUIRED")
    print("\nTo use this tool, you need:")
    print("  1. Namecheap API access enabled")
    print("  2. Your API key")
    print("  3. Your account username")
    print("  4. Your current IP address whitelisted")

    enable_api = input("\nDo you have Namecheap API access enabled? (y/n): ").lower()

    if enable_api != 'y':
        enable_api_access_instructions()
        print("\n💡 ALTERNATIVE: Manual DNS Configuration")
        print("="*60)
        print("\nIf you don't want to enable API access, here's the manual method:")
        print("\n1. Go to: https://ap.www.namecheap.com/domains/list/")
        print("\n2. Find: consciousnessrevolution.com")
        print("\n3. Click: MANAGE button (on the right)")
        print("\n4. Look for tabs at the top:")
        print("   - Domain")
        print("   - Nameservers")
        print("   - Advanced DNS  ← CLICK THIS ONE")
        print("\n5. In the 'HOST RECORDS' section, click 'ADD NEW RECORD'")
        print("\n6. Add these two records:")
        print("   ┌────────────────────────────────────────┐")
        print("   │ Record 1:                              │")
        print("   │   Type: A Record                       │")
        print("   │   Host: @                              │")
        print("   │   Value: 75.2.60.5                     │")
        print("   │   TTL: Automatic                       │")
        print("   └────────────────────────────────────────┘")
        print("   ┌────────────────────────────────────────┐")
        print("   │ Record 2:                              │")
        print("   │   Type: CNAME Record                   │")
        print("   │   Host: www                            │")
        print("   │   Value: apex-loadbalancer.netlify.com │")
        print("   │   TTL: Automatic                       │")
        print("   └────────────────────────────────────────┘")
        print("\n7. Click 'SAVE ALL CHANGES'")
        print("\n8. Wait 5-30 minutes for DNS propagation")
        print("\n9. Check if it worked: https://consciousnessrevolution.com")
        print("="*60)

    else:
        print("\n📝 Enter your Namecheap API credentials:")
        api_user = input("   API Username: ")
        api_key = input("   API Key: ")
        username = input("   Account Username: ")

        # Get current IP
        current_ip = get_current_ip()
        if current_ip:
            print(f"\n🌍 Your current IP: {current_ip}")
            use_ip = input(f"   Use this IP? (y/n): ").lower()
            if use_ip != 'y':
                current_ip = input("   Enter your IP address: ")
        else:
            current_ip = input("   Enter your IP address: ")

        # Configure DNS
        domain = "consciousnessrevolution.com"
        success = configure_dns_for_netlify(
            domain=domain,
            api_user=api_user,
            api_key=api_key,
            username=username,
            client_ip=current_ip
        )

        if success:
            print("\n🎉 ALL DONE!")
            print(f"\nYour site will be live at https://consciousnessrevolution.com")
            print(f"in about 5-30 minutes (DNS propagation time).")
        else:
            print("\n😞 Configuration failed. Try the manual method above.")
