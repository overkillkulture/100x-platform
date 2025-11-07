"""
CHATGPT CONVERSATION DATA EXPORTER
Helps export and structure ChatGPT conversation history
"""

import os
import json
import webbrowser
from datetime import datetime

def export_chatgpt_data():
    """
    Guide user through ChatGPT data export process
    """
    print("💬 CHATGPT DATA EXPORT TOOL")
    print("=" * 60)
    print()

    print("This tool will help you export all your ChatGPT conversations.")
    print()

    # Step 1: Request export
    print("STEP 1: Request Data Export")
    print("-" * 60)
    print("1. We'll open ChatGPT settings for you")
    print("2. Click 'Data controls' → 'Export data'")
    print("3. Confirm your email address")
    print("4. Wait for email (usually 5-30 minutes)")
    print()

    if input("Ready to open ChatGPT? (y/n): ").lower() == 'y':
        webbrowser.open('https://chat.openai.com/settings/data')
        print("✅ ChatGPT settings opened in browser")
    print()

    # Step 2: Wait for email
    print("STEP 2: Wait for Download Link")
    print("-" * 60)
    print("ChatGPT will email you a download link.")
    print("This usually takes 5-30 minutes.")
    print()

    email_received = input("Have you received the email? (y/n): ").lower()

    if email_received != 'y':
        print()
        print("⏳ Waiting for email...")
        print("   Come back and run this script when you get it!")
        print("   The email will be from OpenAI with subject:")
        print("   'Your ChatGPT data export is ready'")
        return

    # Step 3: Download and extract
    print()
    print("STEP 3: Download and Extract Data")
    print("-" * 60)
    print("1. Click the download link in the email")
    print("2. Save the ZIP file to your computer")
    print("3. Extract the ZIP file")
    print()

    downloads_path = os.path.expanduser('~/Downloads')
    print(f"💡 TIP: Look in {downloads_path}")
    print()

    zip_path = input("Enter path to extracted folder (or drag here): ").strip()

    if not os.path.exists(zip_path):
        print(f"❌ Path not found: {zip_path}")
        return

    # Step 4: Find conversations.json
    print()
    print("STEP 4: Locating conversations.json")
    print("-" * 60)

    conversations_file = None
    for root, dirs, files in os.walk(zip_path):
        for file in files:
            if file == 'conversations.json':
                conversations_file = os.path.join(root, file)
                break

    if not conversations_file:
        print("❌ Could not find conversations.json")
        print("   Expected structure: exported_data/conversations.json")
        return

    print(f"✅ Found: {conversations_file}")

    # Step 5: Load and analyze
    print()
    print("STEP 5: Analyzing Conversations")
    print("-" * 60)

    with open(conversations_file, 'r', encoding='utf-8') as f:
        conversations = json.load(f)

    print(f"📊 Total conversations: {len(conversations)}")

    # Count messages
    total_messages = 0
    code_blocks = 0
    for conv in conversations:
        for message in conv.get('mapping', {}).values():
            if message.get('message'):
                total_messages += 1
                content = str(message['message'].get('content', ''))
                code_blocks += content.count('```')

    print(f"📝 Total messages: {total_messages}")
    print(f"💻 Code blocks: {code_blocks // 2}")  # Divide by 2 (opening + closing)

    # Step 6: Save structured data
    print()
    print("STEP 6: Creating Unified Format")
    print("-" * 60)

    output_dir = 'AI_EXPORTS'
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, 'chatgpt_conversations.json')

    # Convert to unified format
    unified_conversations = []
    for conv in conversations:
        unified_conv = {
            'conversation_id': conv.get('id'),
            'platform': 'chatgpt',
            'title': conv.get('title', 'Untitled'),
            'created_at': datetime.fromtimestamp(conv.get('create_time', 0)).isoformat(),
            'messages': [],
            'tags': []
        }

        # Extract messages
        mapping = conv.get('mapping', {})
        for node_id, node in mapping.items():
            message = node.get('message')
            if message:
                unified_conv['messages'].append({
                    'role': message.get('author', {}).get('role', 'unknown'),
                    'content': message.get('content', {}).get('parts', [''])[0],
                    'timestamp': datetime.fromtimestamp(
                        message.get('create_time', 0)
                    ).isoformat()
                })

        unified_conversations.append(unified_conv)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unified_conversations, f, indent=2)

    print(f"✅ Saved to: {output_file}")

    # Step 7: Summary
    print()
    print("=" * 60)
    print("🎉 EXPORT COMPLETE!")
    print("=" * 60)
    print()
    print(f"📁 Exported data: {output_file}")
    print(f"📊 Conversations: {len(unified_conversations)}")
    print(f"📝 Messages: {total_messages}")
    print(f"💻 Code blocks: {code_blocks // 2}")
    print()
    print("NEXT STEPS:")
    print("1. This data can now be searched and analyzed")
    print("2. Use UNIFIED_AI_SEARCH.py to search across all AIs")
    print("3. Build knowledge graph with KNOWLEDGE_GRAPH_BUILDER.py")
    print()
    print("=" * 60)

if __name__ == '__main__':
    export_chatgpt_data()
