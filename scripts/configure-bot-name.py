#!/usr/bin/env python3
"""
Easy Bot Name Configuration Script
Configure your Discord bot name easily without manual .env editing
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    """Main configuration function"""
    print("🎙️  Virtual Studio Node - Bot Name Configuration")
    print("=" * 50)
    
    # Find the .env file
    script_dir = Path(__file__).parent
    env_file = script_dir.parent / "config" / ".env"
    
    if not env_file.exists():
        print("❌ Configuration file not found!")
        print(f"Expected location: {env_file}")
        return 1
    
    # Load current configuration
    load_dotenv(env_file)
    current_name = os.getenv('DISCORD_BOT_NAME', 'VirtualStudioRecorder')
    
    print(f"Current bot name: {current_name}")
    print()
    
    # Get new bot name
    print("🤖 Choose your Discord bot name:")
    print("   - Keep it short (under 32 characters)")
    print("   - Use letters, numbers, underscores")
    print("   - Make it memorable and unique")
    print()
    
    suggestions = [
        "VirtualStudioRecorder",
        "DiscordRecorderBot", 
        "StudioBot",
        "RecordMaster",
        "VoiceRecorder",
        "StreamRecorder"
    ]
    
    print("💡 Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion}")
    print("   7. Custom name")
    print()
    
    try:
        choice = input("Select option (1-7) or enter custom name: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= 7:
            if choice == "7":
                new_name = input("Enter your custom bot name: ").strip()
            else:
                new_name = suggestions[int(choice) - 1]
        else:
            new_name = choice
        
        if not new_name:
            print("❌ Bot name cannot be empty!")
            return 1
        
        if len(new_name) > 32:
            print("❌ Bot name too long! Maximum 32 characters.")
            return 1
        
        # Validate characters
        if not all(c.isalnum() or c in ['_', '-', ' '] for c in new_name):
            print("❌ Bot name contains invalid characters!")
            print("   Use only letters, numbers, spaces, underscores, and hyphens.")
            return 1
        
        # Update .env file
        print(f"\n🔧 Updating bot name to: {new_name}")
        update_env_file(env_file, new_name)
        
        print("\n✅ Configuration updated successfully!")
        print("\n🚀 Next steps:")
        print("   1. Restart the Discord bot service")
        print("   2. Test the bot to see your new name")
        print("   3. The bot will show your custom name in:")
        print("      - Discord server member list")
        print("      - Bot status messages")
        print("      - Log files")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration cancelled.")
        return 1
    except Exception as e:
        print(f"\n❌ Error updating configuration: {e}")
        return 1

def update_env_file(env_file: Path, new_bot_name: str):
    """Update the bot name in the .env file"""
    
    # Read current content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Find and replace the DISCORD_BOT_NAME line
    lines = content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith('DISCORD_BOT_NAME='):
            lines[i] = f'DISCORD_BOT_NAME={new_bot_name}  # ✨ EASY TO CUSTOMIZE: Change this to name your bot'
            updated = True
            break
    
    # If not found, add it to Discord Bot Configuration section
    if not updated:
        discord_section_found = False
        for i, line in enumerate(lines):
            if line.strip() == '# Discord Bot Configuration':
                discord_section_found = True
                lines.insert(i + 1, f'DISCORD_BOT_NAME={new_bot_name}  # ✨ EASY TO CUSTOMIZE: Change this to name your bot')
                break
    
    # Write back
    with open(env_file, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    sys.exit(main())