#!/usr/bin/env python3
"""Fix the broken regex line in ARAYA_UPGRADED_V2.py"""

# Read the broken file
with open('ARAYA_UPGRADED_V2.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the broken line (around line 33)
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # If we find the broken regex line
    if "code_blocks = re.findall(r'```(?:python" in line and line.strip().endswith("?"):
        # This is the broken line - combine it with the next line
        next_line = lines[i+1] if i+1 < len(lines) else ""
        fixed_line = "    code_blocks = re.findall(r'```(?:python|javascript|html|css|json)?\\n(.*?)```', araya_response, re.DOTALL)\n"
        fixed_lines.append(fixed_line)
        i += 2  # Skip the next line since we combined them
    else:
        fixed_lines.append(line)
        i += 1

# Write the fixed version
with open('ARAYA_UPGRADED_V2.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("✅ Fixed syntax error in ARAYA_UPGRADED_V2.py")
