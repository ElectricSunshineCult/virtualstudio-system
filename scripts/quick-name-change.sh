#!/bin/bash
# Quick Bot Name Configuration Script
# Usage: ./quick-name-change.sh "YourBotName"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/config/.env"

# Check if bot name provided
if [ $# -eq 0 ]; then
    echo "🎙️  Virtual Studio Node - Quick Bot Name Change"
    echo "Usage: $0 \"YourBotName\""
    echo ""
    echo "Examples:"
    echo "   $0 \"StudioRecorder\""
    echo "   $0 \"DiscordRecorderBot\""
    echo "   $0 \"VoiceRecorder\""
    echo ""
    
    # Show current name if .env exists
    if [ -f "$ENV_FILE" ]; then
        current_name=$(grep "^DISCORD_BOT_NAME=" "$ENV_FILE" | cut -d'=' -f2 | cut -d'#' -f1 | tr -d ' ')
        if [ ! -z "$current_name" ]; then
            echo "Current bot name: $current_name"
        fi
    fi
    exit 0
fi

NEW_BOT_NAME="$1"

# Validate input
if [ -z "$NEW_BOT_NAME" ]; then
    echo "❌ Error: Bot name cannot be empty"
    exit 1
fi

if [ ${#NEW_BOT_NAME} -gt 32 ]; then
    echo "❌ Error: Bot name too long (max 32 characters)"
    exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: Configuration file not found at $ENV_FILE"
    exit 1
fi

# Create backup
cp "$ENV_FILE" "$ENV_FILE.backup.$(date +%Y%m%d_%H%M%S)"

# Update .env file
if grep -q "^DISCORD_BOT_NAME=" "$ENV_FILE"; then
    sed -i "s|^DISCORD_BOT_NAME=.*|DISCORD_BOT_NAME=$NEW_BOT_NAME  # ✨ EASY TO CUSTOMIZE: Change this to name your bot|" "$ENV_FILE"
else
    # Add if not found (append after Discord configuration section)
    sed -i "/# Discord Bot Configuration/a DISCORD_BOT_NAME=$NEW_BOT_NAME  # ✨ EASY TO CUSTOMIZE: Change this to name your bot" "$ENV_FILE"
fi

echo "✅ Bot name updated to: $NEW_BOT_NAME"
echo ""
echo "🚀 To apply the new name:"
echo "   sudo systemctl restart virtualstudio-enhanced-bot"
echo ""
echo "📝 To verify in logs:"
echo "   sudo journalctl -u virtualstudio-enhanced-bot -f"