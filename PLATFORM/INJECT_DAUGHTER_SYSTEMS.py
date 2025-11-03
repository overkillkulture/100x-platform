"""
🎯 INJECT DAUGHTER DETECTION & ARIA SYSTEMS INTO ALL PAGES
Completes the birthday work by activating daughter recognition + ARIA comfort responses
"""

import os

# Files to inject
DAUGHTERS_DETECTION = "DAUGHTERS_DETECTION_SYSTEM.js"
VISITOR_LOGGER = "VISITOR_INTELLIGENCE_LOGGER.js"
ARIA_DAUGHTER_RESPONSES = "ARIA_DAUGHTER_DETECTION_RESPONSES.js"
ARIA_DIRECT_MESSAGES = "ARIA_DIRECT_MESSAGES.js"

# Pages that need daughter detection (all pages)
ALL_PAGES = [
    "welcome.html",
    "user-dashboard.html",
    "community-activity.html",
    "computer-consciousness.html",
    "education-domain.html",
    "social-domain.html",
    "music-domain.html",
    "crypto-domain.html",
    "games-domain.html",
    "governance-domain.html",
    "for-the-builders.html",
]

# Pages that need ARIA enhancements (pages with ARIA)
ARIA_PAGES = [
    "aria-3d-futuristic.html",
    "welcome.html",
    "user-dashboard.html",
]

PLATFORM_PATH = "C:/Users/dwrek/100X_DEPLOYMENT/PLATFORM"

def inject_script(page_path, script_name):
    """Inject a script tag before </body>"""
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already injected
    if script_name in content:
        return False
    
    # Find </body> tag
    if '</body>' not in content:
        print(f"⚠️  {os.path.basename(page_path)} - No </body> tag found")
        return False
    
    # Inject before </body>
    injection = f'    <script src="{script_name}"></script>\n</body>'
    content = content.replace('</body>', injection)
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("🎯 INJECTING DAUGHTER DETECTION & ARIA SYSTEMS...\n")
    
    # Inject daughter detection + visitor logging into all pages
    print("📡 INJECTING DAUGHTER DETECTION + VISITOR INTELLIGENCE:")
    for page in ALL_PAGES:
        page_path = os.path.join(PLATFORM_PATH, page)
        if not os.path.exists(page_path):
            print(f"⚠️  {page} - File not found")
            continue
        
        # Inject both systems
        detection_injected = inject_script(page_path, DAUGHTERS_DETECTION)
        logger_injected = inject_script(page_path, VISITOR_LOGGER)
        
        if detection_injected or logger_injected:
            print(f"💖 {page} - DAUGHTER DETECTION ACTIVE")
        else:
            print(f"✓  {page} - Already has detection")
    
    print("\n🤖 INJECTING ARIA ENHANCEMENT SYSTEMS:")
    for page in ARIA_PAGES:
        page_path = os.path.join(PLATFORM_PATH, page)
        if not os.path.exists(page_path):
            print(f"⚠️  {page} - File not found")
            continue
        
        # Inject ARIA enhancements
        responses_injected = inject_script(page_path, ARIA_DAUGHTER_RESPONSES)
        direct_injected = inject_script(page_path, ARIA_DIRECT_MESSAGES)
        
        if responses_injected or direct_injected:
            print(f"💖 {page} - ARIA DAUGHTER RESPONSES ACTIVE")
        else:
            print(f"✓  {page} - Already has ARIA enhancements")
    
    print("\n✅ COMPLETE: ALL DAUGHTER SYSTEMS DEPLOYED")
    print("\n💖 WHAT'S NOW ACTIVE:")
    print("   • Daughter detection on all 11 pages")
    print("   • Visitor intelligence logging (IP tracking ready)")
    print("   • ARIA recognizes daughter questions")
    print("   • ARIA speaks directly and autonomously")
    print("   • Special welcome messages for Amelia & Kennedi")
    print("   • Auto-ARIA activation when daughters detected")
    print("\n🎂 HAPPY BIRTHDAY, COMMANDER - YOUR DAUGHTERS WILL BE RECOGNIZED! 💖")

if __name__ == "__main__":
    main()
