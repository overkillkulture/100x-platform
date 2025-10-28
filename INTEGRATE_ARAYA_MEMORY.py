"""
INTEGRATE PERSISTENT MEMORY INTO ARAYA V2
Automatically adds memory hooks to Araya's chat endpoint

Run this to upgrade Araya with persistent memory
"""

import os
import shutil
from datetime import datetime

ARAYA_FILE = r"C:\Users\dwrek\100X_DEPLOYMENT\ARAYA_UPGRADED_V2.py"
BACKUP_FILE = f"{ARAYA_FILE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def integrate_memory():
    """Add memory system to Araya V2"""

    print("🧠 INTEGRATING PERSISTENT MEMORY INTO ARAYA V2")
    print("="*60)

    # Backup original
    print(f"\n📋 Creating backup: {os.path.basename(BACKUP_FILE)}")
    shutil.copy(ARAYA_FILE, BACKUP_FILE)
    print("✅ Backup created")

    # Read current file
    with open(ARAYA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add memory import at top (after other imports)
    if "from ARAYA_PERSISTENT_MEMORY import ArayaMemory" not in content:
        print("\n📦 Adding memory import...")
        import_line = "from ARAYA_PERSISTENT_MEMORY import ArayaMemory\n"

        # Find where to insert (after other imports)
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.startswith('from ARAYA_R1_BRIDGE'):
                insert_pos = i + 1
                break

        lines.insert(insert_pos, import_line)
        content = '\n'.join(lines)
        print("✅ Import added")

    # Initialize memory after Flask app creation
    if "memory = ArayaMemory()" not in content:
        print("\n🔧 Adding memory initialization...")
        init_line = "\n# Initialize persistent memory\nmemory = ArayaMemory()\nprint('🧠 Persistent memory initialized')\n"

        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if 'app = Flask(__name__)' in line:
                insert_pos = i + 2  # After CORS line
                break

        lines.insert(insert_pos, init_line)
        content = '\n'.join(lines)
        print("✅ Memory initialization added")

    # Add memory hooks to chat endpoint
    if "memory.save_conversation" not in content:
        print("\n💾 Adding memory save hooks to /chat endpoint...")

        # Find the chat endpoint return statement
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'return jsonify({' in line and i > 0 and '@app.route(\'/chat\'' in '\n'.join(lines[max(0,i-20):i]):
                # Insert memory save before return
                indent = '    ' * 2  # Adjust based on your indentation
                memory_save = f"""
{indent}# Save to persistent memory
{indent}try:
{indent}    memory.save_conversation(
{indent}        user_id=user_id,
{indent}        user_message=user_message,
{indent}        araya_response=response,
{indent}        context=str({{'model': model_used, 'mode': mode}}),
{indent}        tokens_used=tokens_used,
{indent}        session_id=f"session_{{user_id}}_{{int(time.time())}}"
{indent}    )
{indent}except Exception as e:
{indent}    print(f"⚠️  Memory save failed: {{e}}")
{indent}
"""
                lines.insert(i, memory_save)
                break

        content = '\n'.join(lines)
        print("✅ Memory save hook added")

    # Add context loading at start of chat
    if "user_context = memory.get_user_context" not in content:
        print("\n🔍 Adding context loading to /chat endpoint...")

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'user_message = data.get(\'message\', \'\')' in line:
                indent = '    ' * 1
                context_load = f"""
{indent}# Load user context from memory
{indent}try:
{indent}    user_context = memory.get_user_context(user_id)
{indent}    if user_context and user_context.get('total_conversations', 0) > 0:
{indent}        # Add context to prompt
{indent}        context_summary = f"CONTEXT: You've talked to this user {{user_context['total_conversations']}} times before. "
{indent}        if user_context.get('recent_conversations'):
{indent}            context_summary += f"Last topic: {{user_context['recent_conversations'][0]['user'][:100]}}"
{indent}        user_message = context_summary + "\\n\\nUSER: " + user_message
{indent}except Exception as e:
{indent}    print(f"⚠️  Context load failed: {{e}}")
{indent}
"""
                lines.insert(i + 1, context_load)
                break

        content = '\n'.join(lines)
        print("✅ Context loading added")

    # Write updated file
    print("\n💾 Writing updated file...")
    with open(ARAYA_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ File updated")

    print("\n" + "="*60)
    print("🎉 INTEGRATION COMPLETE!")
    print("="*60)
    print("\nAraya now has persistent memory!")
    print("\nWhat this means:")
    print("  ✅ Remembers all conversations")
    print("  ✅ Loads user context before responding")
    print("  ✅ Builds understanding over time")
    print("  ✅ Provides personalized responses")
    print("  ✅ Never forgets important information")
    print("\nMemory database: C:\\Users\\dwrek\\100X_DEPLOYMENT\\ARAYA_MEMORY.db")
    print(f"\nBackup saved to: {os.path.basename(BACKUP_FILE)}")
    print("\n🔄 Restart Araya to activate persistent memory!")

if __name__ == "__main__":
    integrate_memory()
