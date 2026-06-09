"""
Parse Claude Code session transcripts to extract tool call patterns
for permission allowlisting.
"""
import json, re, os, glob
from collections import Counter

bash_cmds = Counter()
other_tools = Counter()

projects_dir = r"C:\Users\Administrator\.claude\projects"

# Collect jsonl files
jsonl_files = []
for root, dirs, files in os.walk(projects_dir):
    for f in files:
        if f.endswith('.jsonl'):
            path = os.path.join(root, f)
            mtime = os.path.getmtime(path)
            jsonl_files.append((mtime, path))

jsonl_files.sort(reverse=True)
recent = jsonl_files[:50]

for mtime, path in recent:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()

        # Find tool_use blocks (they may span multiple lines, but let's try line by line first)
        for line in content.split('\n'):
            try:
                record = json.loads(line.strip())
            except:
                continue

            # Only process assistant-type records
            if record.get('type') != 'assistant':
                continue

            msg = record.get('message', {})
            if isinstance(msg, str):
                continue
            blocks = msg.get('content', [])
            if isinstance(blocks, str):
                continue

            for block in blocks:
                if not isinstance(block, dict):
                    continue
                if block.get('type') != 'tool_use':
                    continue

                tool_name = block.get('name', '')
                t_input = block.get('input', {})

                if tool_name == 'Bash':
                    cmd = t_input.get('command', '').strip()
                    if not cmd:
                        continue

                    parts = cmd.split()

                    # Find first real command (skip env vars, export, sudo)
                    i = 0
                    while i < len(parts):
                        p = parts[i]
                        if p in ('export', 'sudo'):
                            i += 1
                            continue
                        if '=' in p:
                            i += 1
                            continue
                        break

                    if i >= len(parts):
                        continue

                    cmd_name = parts[i]

                    # Special: cd -> Bash(cd)
                    if cmd_name == 'cd':
                        bash_cmds['cd'] += 1
                        continue

                    # Get subcommand if available
                    i += 1
                    if i < len(parts) and parts[i] not in (
                        '|', '&&', '||', ';', '2>&1', '2>/dev/null',
                        '1>/dev/null', '>/dev/null'
                    ):
                        bash_cmds[f'{cmd_name} {parts[i]}'] += 1
                    else:
                        bash_cmds[cmd_name] += 1

                elif tool_name.startswith('mcp__'):
                    other_tools[tool_name] += 1
                elif tool_name == 'Skill':
                    skill_name = t_input.get('skill', '')
                    other_tools[f'Skill({skill_name})'] += 1
                else:
                    other_tools[tool_name] += 1

    except Exception as e:
        pass

print("=== Bash commands (frequency) ===")
for cmd, count in bash_cmds.most_common(50):
    print(f"  {count:>4}  {cmd}")

print("\n=== Other tools (frequency) ===")
for name, count in other_tools.most_common(30):
    print(f"  {count:>4}  {name}")
