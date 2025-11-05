# Virtual Studio Node - Complete System Documentation
**Production-Ready Discord + OBS Recording System**

## 🎯 System Overview

Virtual Studio Node is a comprehensive, headless Ubuntu 24.04 server that automates Discord voice recording with OBS Studio, featuring:

- **🎙️ Discord Integration**: Automated voice channel detection and recording
- **📹 OBS Studio**: Headless video/audio recording with dual-track support  
- **🎬 YouTube Integration**: Automatic uploads with metadata
- **📁 GitHub Integration**: Repository commits for transcripts and metadata
- **☁️ Cloud Storage**: S3 and rclone upload support
- **🌐 Browser Extension**: Chrome extension for real-time Discord control
- **🤖 Enhanced Bot**: Discord commands for recording management
- **💚 Health Monitoring**: Auto-restart and system health checks

## 🚀 Quick Installation

```bash
# Download and run installer
wget https://your-server/install-complete-virtualstudio.sh
chmod +x install-complete-virtualstudio.sh
sudo ./install-complete-virtualstudio.sh

# Configure credentials
sudo nano /opt/virtualstudio/config/.env

# Start services
virtualstudio start

# Check status
virtualstudio status
```

## 📋 System Architecture

### Core Components

#### 1. **OBS Studio Service** (`virtualstudio-obs.service`)
- Headless operation with Xvfb virtual display
- Dual audio tracks (Discord + System audio)
- WebSocket API for remote control
- Automatic recording with timestamped filenames

#### 2. **Enhanced Discord Bot** (`virtualstudio-bot.service`)
- `/record start [minutes]` - Start recording
- `/record stop` - Stop recording  
- `/record status` - Check recording status
- `/record upload` - Manual upload management
- YouTube, GitHub, and cloud integration
- Real-time processing pipeline

#### 3. **YouTube Processor** (`virtualstudio-youtube.service`)
- Automatic video upload processing
- OAuth2 authentication support
- Metadata generation and privacy controls
- Retry logic with error handling

#### 4. **GitHub Integration Service** (`virtualstudio-github.service`)
- Automatic transcript commits
- Metadata JSON storage
- Organized repository structure
- Branch and release management

#### 5. **Cloud Upload Service** (`virtualstudio-upload.service`)
- S3 multipart uploads
- rclone remote sync
- File watching with automatic processing
- Progress tracking and retry logic

#### 6. **Health Monitor** (`virtualstudio-health.service`)
- Process monitoring and auto-restart
- Disk space management
- Memory usage tracking
- System health reporting

### Directory Structure

```
/opt/virtualstudio/
├── config/
│   ├── .env              # Environment variables
│   ├── prompts.json      # Discord bot messages
│   └── obs-websocket.json # OBS WebSocket config
├── scripts/
│   ├── enhanced-bot.py   # Main Discord bot
│   ├── youtube-processor.py # YouTube integration
│   ├── github-service.py # GitHub integration
│   ├── upload-service.py # Cloud uploads
│   ├── health-monitor.py # System monitoring
│   └── system-test.py    # Health testing
├── browser-extension/    # Chrome extension files
├── recordings/          # Video recordings
├── transcripts/         # AI-generated transcripts
├── exports/            # Processed exports
├── profiles/           # OBS profiles
├── scenes/            # OBS scene collections
└── logs/              # System logs
```

## 🎮 Discord Bot Commands

### Recording Control
```bash
/record start [minutes]    # Start recording (optional duration)
/record stop              # Stop current recording
/record status            # Check recording status
/record upload            # Manual upload management
```

### Features
- **Voice Channel Detection**: Automatically detects Discord voice activity
- **Dual Audio Tracks**: Separate Discord and system audio
- **Automatic Processing**: Post-recording pipeline (transcription → YouTube → GitHub)
- **Real-time Status**: Live updates and notifications

## 🌐 Browser Extension Features

### Chrome Extension Installation
1. Open Chrome → Settings → Extensions
2. Enable "Developer mode"  
3. Click "Load unpacked"
4. Select `/opt/virtualstudio/browser-extension/`

### Extension Features
- **Discord UI Integration**: Controls embedded in Discord interface
- **Real-time Status**: Live recording status display
- **Quick Controls**: One-click start/stop from Discord
- **System Monitoring**: Resource usage and health indicators
- **Professional Styling**: Matches Discord's native design

## ☁️ Cloud Storage Integration

### AWS S3 Configuration
```bash
# Configure AWS credentials
aws configure

# Set S3 bucket in .env
S3_BUCKET=your-recordings-bucket
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### rclone Configuration
```bash
# Configure rclone remotes
rclone config

# Set remote in .env  
RCLONE_REMOTE=your_remote_name
```

## 🔧 Configuration Guide

### Environment Variables (`/opt/virtualstudio/config/.env`)

#### Core Configuration
```bash
# System
HOSTNAME=virtual-studio-node
INSTALL_DIR=/opt/virtualstudio
USER=virtualstudio

# OBS
OBS_WEBSOCKET_PASSWORD=secure_random_password
OBS_HOST=localhost
OBS_PORT=4455

# Discord
DISCORD_BOT_NAME=VirtualStudioRecorder  # ✨ Easy to customize
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_server_id
DISCORD_VOICE_CHANNEL_ID=target_voice_channel
```

#### YouTube Integration
```bash
# Get from Google Cloud Console
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret  
YOUTUBE_API_KEY=your_api_key
YOUTUBE_UPLOAD_PRIVACY=unlisted
```

#### GitHub Integration
```bash
# Personal Access Token with repo permissions
GITHUB_TOKEN=ghp_your_token_here
GITHUB_REPO=username/repository
```

#### Cloud Storage
```bash
# AWS S3
S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# rclone
RCLONE_REMOTE=your_remote_name
```

### Discord Bot Setup

1. **Create Discord Application**
   - Go to https://discord.com/developers/applications
   - Create new application
   - Go to "Bot" section
   - Create bot and copy token

2. **Configure Bot Permissions**
   - Send Messages
   - Use Slash Commands  
   - Connect to Voice
   - View Channels

3. **Invite Bot to Server**
   - Use OAuth2 URL Generator
   - Select bot permissions
   - Copy invitation URL

4. **🤖 Easy Bot Name Configuration**

   **Quick Name Change (Recommended):**
   ```bash
   cd /opt/virtualstudio/scripts
   ./quick-name-change.sh "YourBotName"
   ```
   
   **Interactive Configuration:**
   ```bash
   cd /opt/virtualstudio/scripts  
   python3 configure-bot-name.py
   ```
   
   **Manual Editing:**
   ```bash
   sudo nano /opt/virtualstudio/config/.env
   # Edit: DISCORD_BOT_NAME=YourBotName
   sudo systemctl restart virtualstudio-enhanced-bot
   ```
   
   **Naming Guidelines:**
   - Maximum 32 characters
   - Letters, numbers, spaces, underscores, hyphens
   - Keep it memorable and unique
   - Examples: `StudioRecorder`, `DiscordBot`, `VoiceRecorder`

### YouTube API Setup

1. **Google Cloud Console**
   - Create project or select existing
   - Enable YouTube Data API v3

2. **OAuth2 Credentials**
   - Create OAuth2 Client ID
   - Download credentials JSON
   - Extract client ID and secret

3. **API Key**
   - Create API key for basic operations

### GitHub Integration

1. **Personal Access Token**
   - Go to GitHub Settings → Developer settings
   - Create "Personal access tokens (classic)"
   - Select scopes: `repo`, `user:email`

2. **Repository Setup**
   - Create dedicated repository
   - Add folders: `transcripts/`, `metadata/`

## 🛡️ Security Best Practices

### Network Security
```bash
# Firewall is automatically configured
# Only allows:
# - SSH (22/tcp)
# - OBS WebSocket (4455/tcp)  
# - HTTPS (443/tcp)
# - DNS (53/tcp)
```

### Credential Security
```bash
# Environment file permissions (already set)
chmod 600 /opt/virtualstudio/config/.env

# Never commit .env to version control
echo ".env" >> /opt/virtualstudio/.gitignore

# Rotate tokens regularly
# Use least-privilege permissions
# Monitor access logs
```

### System Hardening
- **fail2ban**: SSH brute force protection
- **Firewall**: Restrict network access
- **User Isolation**: Dedicated user for services
- **Log Monitoring**: Regular log review
- **Updates**: Keep system packages updated

## 📊 System Management

### Service Control
```bash
# Start all services
virtualstudio start

# Stop all services  
virtualstudio stop

# Restart services
virtualstudio restart

# Check status
virtualstudio status

# View logs
virtualstudio logs
```

### Health Monitoring
```bash
# Run system test
virtualstudio test

# Check disk usage
df -h /opt/virtualstudio

# Monitor services
systemctl status virtualstudio-*

# View specific logs
journalctl -u virtualstudio-bot.service -f
```

### Maintenance Tasks
```bash
# Manual disk cleanup
python3 /opt/virtualstudio/scripts/disk-cleanup.py

# Restart health monitor
systemctl restart virtualstudio-health.service

# Test Discord connectivity
python3 /opt/virtualstudio/scripts/system-test.py

# Check OBS WebSocket
curl -X GET http://localhost:4455 -H "password: your_password"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. OBS Won't Start
```bash
# Check Xvfb display
systemctl status virtualstudio-obs.service
journalctl -u virtualstudio-obs.service

# Verify OBS profile
ls -la /opt/virtualstudio/profiles/
```

#### 2. Discord Bot Offline
```bash
# Check bot token validity
python3 -c "import discord; print('Discord.py installed')"

# Verify network access
curl -I https://discord.com/api/v10/applications

# Check service logs
journalctl -u virtualstudio-bot.service
```

#### 3. YouTube Upload Failures
```bash
# Verify API credentials
python3 -c "
from googleapiclient.discovery import build
# Test API connection
"

# Check quota limits
# Verify OAuth flow
```

#### 4. GitHub Integration Issues
```bash
# Test token validity
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Check repository permissions
# Verify branch protection
```

#### 5. Browser Extension Not Loading
```bash
# Check extension files
ls -la /opt/virtualstudio/browser-extension/

# Verify Chrome permissions
# Clear extension cache
```

### Log Locations
```
/var/log/virtualstudio/
├── enhanced-bot.log         # Discord bot logs
├── youtube-processor.log    # YouTube processing logs  
├── github-service.log      # GitHub integration logs
├── upload-service.log       # Cloud upload logs
├── health-monitor.log       # System health logs
├── cleanup.log             # Disk cleanup logs
└── obs-service.log         # OBS Studio logs
```

## 🔄 Automated Workflow

### Recording Pipeline
1. **Voice Detection** → Bot detects Discord voice activity
2. **OBS Recording** → Automatic start with dual audio tracks
3. **Post-Processing** → Transcription, YouTube upload, GitHub commit
4. **Cloud Upload** → S3/rclone backup storage
5. **Cleanup** → Automatic old file removal

### Daily Maintenance
- **Health Checks** → Every 5 minutes via timer
- **Disk Cleanup** → Weekly via timer  
- **Log Rotation** → Automatic via logrotate
- **System Updates** → Manual or automated

## 📈 Performance Optimization

### Resource Usage
- **CPU**: OBS encoding (variable based on quality settings)
- **Memory**: ~2-4GB for OBS + Discord + services
- **Disk**: Varies by recording length and quality
- **Network**: Upload bandwidth requirements

### Tuning Recommendations
```bash
# OBS encoding settings in profile
RecordingVBitrate=3500    # Adjust based on bandwidth
RecordingABitrate=192     # Good quality audio
UseStreamEncoder=true     # Hardware acceleration

# Health monitor settings
HEALTH_CHECK_INTERVAL=30  # Check frequency
DISK_SPACE_THRESHOLD=80   # Cleanup trigger
```

## 🎯 Production Deployment

### Cloud Deployment Options
1. **AWS EC2** - c5.large or larger
2. **Google Cloud** - n1-standard-2 or larger  
3. **DigitalOcean** - Basic droplets (not recommended)
4. **Dedicated Server** - Minimum 4GB RAM

### Scalability Considerations
- **Multi-Recording**: Support for multiple simultaneous sessions
- **Load Balancing**: Multiple OBS instances for high traffic
- **Database Integration**: Optional PostgreSQL for metadata
- **Caching**: Redis for session management
- **Monitoring**: Prometheus + Grafana for metrics

## 📞 Support

### Getting Help
1. **Check logs**: `virtualstudio logs`
2. **Run tests**: `virtualstudio test`  
3. **Review configuration**: Check `.env` file
4. **Community support**: GitHub issues
5. **Professional support**: Available upon request

### Contributing
- **Fork repository** and create feature branch
- **Follow coding standards** (PEP 8)
- **Add tests** for new functionality  
- **Update documentation**
- **Submit pull request**

---

## 🏆 Features Summary

✅ **Headless Operation** - No GUI required  
✅ **Discord Integration** - Automated voice recording  
✅ **OBS Studio** - Professional video recording  
✅ **YouTube Uploads** - Automatic video publishing  
✅ **GitHub Integration** - Transcript repository commits  
✅ **Cloud Storage** - S3 and rclone support  
✅ **Browser Extension** - Real-time Discord controls  
✅ **Health Monitoring** - Auto-restart and diagnostics  
✅ **Security Hardened** - Firewall and fail2ban  
✅ **Production Ready** - Comprehensive logging and testing  

**Virtual Studio Node** - The complete Discord recording solution! 🎉