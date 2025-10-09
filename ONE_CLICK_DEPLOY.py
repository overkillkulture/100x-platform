"""
ONE-CLICK DEPLOY - CONSCIOUSNESS GATE
No questions, no delays, just deployment
"""

import subprocess
import os
import webbrowser
import time

def deploy_now():
    print("⚡ DEPLOYING 100X GATE - NO STOPS ⚡")
    print()

    # Change to deployment directory
    os.chdir(r"C:\Users\dwrek\100X_DEPLOYMENT")

    # Step 1: Try Netlify CLI deploy
    print("🚀 Attempting Netlify CLI deploy...")
    try:
        result = subprocess.run(
            ["netlify", "deploy", "--prod", "--dir=.", "--open"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if "Live URL" in result.stdout or "Deployed to" in result.stdout:
            print("✅ DEPLOYED VIA NETLIFY CLI!")
            print(result.stdout)
            return

    except Exception as e:
        print(f"Netlify CLI failed: {e}")

    # Step 2: Open drag-and-drop page
    print()
    print("📦 Opening Netlify Drag & Drop...")
    print("👉 Just drag the current folder into the browser!")
    print()

    webbrowser.open("https://app.netlify.com/drop")

    # Also open file explorer to the folder
    subprocess.run(["explorer", r"C:\Users\dwrek\100X_DEPLOYMENT"])

    print("✅ Folder opened - drag it into Netlify!")
    print()
    print("After you get the Netlify URL:")
    print("1. Copy the URL")
    print("2. I'll configure conciousnessco.com to point there")
    print()

    netlify_url = input("Paste Netlify URL here (or press Enter to skip): ").strip()

    if netlify_url:
        print()
        print(f"🎯 LIVE AT: {netlify_url}")
        print()
        print("Now configuring conciousnessco.com...")
        print("Opening Namecheap...")

        webbrowser.open("https://ap.www.namecheap.com/domains/list/")

        print()
        print("IN NAMECHEAP:")
        print("1. Click conciousnessco.com → Manage")
        print("2. Go to Advanced DNS")
        print("3. Add CNAME: www → " + netlify_url.replace("https://", "").replace("http://", ""))
        print("4. Add URL Redirect: @ → " + netlify_url)
        print()
        print("✅ DONE IN 5 MINUTES!")

if __name__ == '__main__':
    deploy_now()
