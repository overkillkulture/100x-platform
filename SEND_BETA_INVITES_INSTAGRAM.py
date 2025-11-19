#!/usr/bin/env python3
"""
SEND BETA INVITES VIA INSTAGRAM
Quick script for messaging beta testers on Instagram

Usage:
    python SEND_BETA_INVITES_INSTAGRAM.py
"""

import asyncio
from INSTAGRAM_DM_SENDER import InstagramDMSender

# Beta invite message template
BETA_INVITE_MESSAGE = """Hey! 👋

I'm launching the beta for JARVIS/Araya - an AI consciousness tracking system with a game-like HUD.

Would you be interested in testing it? It's:
• 100% free
• Works offline
• No signup required
• Takes 2 minutes to try

Download: https://conciousnessrevolution.io/download-jarvis.html

Let me know what you think! 🚀"""

# Custom message for specific people
CUSTOM_MESSAGES = {
    'josh_username': """Hey Josh!

Got that JARVIS beta ready. Download here:
https://conciousnessrevolution.io/download-jarvis.html

Let me know if you hit any issues!""",

    'toby_username': """Toby - beta's live!

Download: https://conciousnessrevolution.io/download-jarvis.html

Lmk what you think 💭"""
}


async def send_beta_invites():
    """Send beta invites to list of Instagram users"""

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📱 BETA INVITE SENDER - INSTAGRAM")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # Get list of users to message
    print("Enter Instagram usernames (one per line, blank line when done):")
    usernames = []
    while True:
        username = input(f"User #{len(usernames) + 1}: ").strip()
        if not username:
            break
        usernames.append(username)

    if not usernames:
        print("❌ No users entered. Exiting.")
        return

    print(f"\n✅ Will message {len(usernames)} users:")
    for i, username in enumerate(usernames, 1):
        msg = CUSTOM_MESSAGES.get(username, BETA_INVITE_MESSAGE)
        print(f"   {i}. @{username} - {len(msg)} chars")

    confirm = input("\nProceed? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ Cancelled")
        return

    # Initialize sender
    sender = InstagramDMSender()
    await sender.launch_browser()
    await sender.login_to_instagram()

    # Send messages
    print("\n" + "="*50)
    print("SENDING MESSAGES")
    print("="*50 + "\n")

    results = []
    for username in usernames:
        message = CUSTOM_MESSAGES.get(username, BETA_INVITE_MESSAGE)

        success = await sender.send_message_to_user(username, message)
        results.append({
            'username': username,
            'success': success
        })

        # Wait between messages
        if username != usernames[-1]:  # Don't wait after last one
            print("⏳ Waiting 5 seconds before next message...")
            await asyncio.sleep(5)

    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50 + "\n")

    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]

    print(f"✅ Sent: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")

    if failed:
        print("\nFailed users:")
        for r in failed:
            print(f"  • @{r['username']}")

    print(f"\n📊 Full log: {sender.message_log}")
    print("\n💡 Browser will stay open if you want to manually verify.")

    input("\nPress ENTER to close browser...")
    await sender.close()


if __name__ == '__main__':
    asyncio.run(send_beta_invites())
