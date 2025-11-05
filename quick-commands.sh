#!/bin/bash
# Virtual Studio Node - Quick Commands Reference
# Generated: 2025-11-05

echo "🎙️ Virtual Studio Node - Quick Commands"
echo "======================================="

# System Status
echo "📊 System Status:"
echo "  cd virtualstudio-system && python3 test-system.py"

# GitHub Integration
echo "📁 GitHub Commands:"
echo "  # Test GitHub connection"
echo "  python3 scripts/github-integration.py YOUR_TOKEN owner/repo test"
echo "  # Commit transcript to repository"
echo "  python3 scripts/github-integration.py YOUR_TOKEN owner/repo commit transcript.txt \"Recording transcript\""

# YouTube Management
echo "🎬 YouTube Commands:"
echo "  # Check YouTube processor status"
echo "  bash scripts/youtube-management.sh status"
echo "  # Process pending recordings"
echo "  bash scripts/youtube-management.sh process"
echo "  # Configure YouTube authentication"
echo "  bash scripts/youtube-management.sh auth"

# Discord Bot
echo "🤖 Discord Bot:"
echo "  # Start enhanced Discord bot"
echo "  python3 scripts/enhanced-discord-bot.py"
echo "  # Stop all processes"
echo "  pkill -f discord-bot"

# Browser Extension
echo "🌐 Browser Extension:"
echo "  # Extension is ready in browser-extension/ folder"
echo "  # Install via Chrome: chrome://extensions/ (Developer Mode)"

echo ""
echo "🤖 Bot Name Configuration:"
echo "  # Quick name change (recommended)"
echo "  ./scripts/quick-name-change.sh \"YourBotName\""
echo "  # Interactive configuration"
echo "  python3 scripts/configure-bot-name.py"
echo "  # Manual editing"
echo "  nano config/.env  # Edit DISCORD_BOT_NAME"

echo ""
echo "🔧 General Configuration:"
echo "  # Edit environment variables"
echo "  nano config/.env"
echo "  # Edit bot prompts"
echo "  nano config/prompts.json"

echo ""
echo "📋 Next Steps:"
echo "  1. Configure YouTube API credentials in Google Cloud Console"
echo "  2. Update GITHUB_REPO in .env with your actual repository"
echo "  3. Install browser extension in Chrome"
echo "  4. Start testing the complete workflow"