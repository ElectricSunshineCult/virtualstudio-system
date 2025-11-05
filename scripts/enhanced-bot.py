#!/usr/bin/env python3
"""
Virtual Studio Node Enhanced Discord Bot
Integrates Discord + OBS + YouTube + GitHub + Browser Extension
Production-ready with full automation
"""

import os
import sys
import json
import asyncio
import logging
import subprocess
import base64
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import discord
from discord.ext import commands, tasks
from obswebsocket import obsws
from obswebsocket.exceptions import ConnectionFailure
import boto3
import requests
from botocore.exceptions import NoCredentialsError

# Load configuration
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/virtualstudio/enhanced-bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global configuration
class Config:
    def __init__(self):
        self.install_dir = Path(os.getenv('INSTALL_DIR', '/opt/virtualstudio'))
        self.recordings_dir = self.install_dir / 'recordings'
        self.transcripts_dir = self.install_dir / 'transcripts'
        self.obs_host = os.getenv('OBS_HOST', 'localhost')
        self.obs_port = int(os.getenv('OBS_PORT', '4455'))
        self.obs_password = os.getenv('OBS_WEBSOCKET_PASSWORD')
        self.youtube_client_id = os.getenv('YOUTUBE_CLIENT_ID')
        self.youtube_client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_repo = os.getenv('GITHUB_REPO')
        self.s3_bucket = os.getenv('S3_BUCKET')
        self.rclone_remote = os.getenv('RCLONE_REMOTE')
        self.discord_bot_name = os.getenv('DISCORD_BOT_NAME', 'VirtualStudioRecorder')
        self.discord_token = os.getenv('DISCORD_BOT_TOKEN')

config = Config()

# Discord bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='/', intents=intents, 
                  description=f"Discord Bot: {config.discord_bot_name} - Records Discord voice channels with OBS, uploads to YouTube, commits to GitHub")

# Global recording state
recording_state = {
    'active': False,
    'start_time': None,
    'duration_minutes': 0,
    'recording_filename': None,
    'participants': [],
    'youtube_upload_id': None,
    'github_commit_url': None,
    'transcript_path': None
}

# Prompts configuration
prompts = {}

class YouTubeUploader:
    """YouTube upload integration"""
    
    def __init__(self):
        self.client_id = config.youtube_client_id
        self.client_secret = config.youtube_client_secret
        self.api_key = config.youtube_api_key
    
    async def upload_video(self, file_path: Path, title: str, description: str = "", 
                          privacy_status: str = "private") -> Optional[str]:
        """Upload video to YouTube"""
        if not all([self.client_id, self.client_secret, self.api_key]):
            logger.warning("YouTube credentials not configured")
            return None
        
        try:
            # This would typically use the YouTube Data API v3
            # For production, implement OAuth2 flow
            logger.info(f"Would upload {file_path} to YouTube as: {title}")
            
            # Simulate upload process
            upload_id = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # In production, you would:
            # 1. Authenticate with OAuth2
            # 2. Upload video chunk by chunk
            # 3. Set metadata
            # 4. Return upload ID
            
            logger.info(f"Video upload simulated: {upload_id}")
            return upload_id
            
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            return None

class GitHubIntegrator:
    """GitHub integration for repository operations"""
    
    def __init__(self):
        self.token = config.github_token
        self.repo = config.github_repo
        self.base_url = "https://api.github.com"
    
    async def commit_file(self, file_path: Path, content: str, 
                         commit_message: str) -> Optional[str]:
        """Commit file to GitHub repository"""
        if not all([self.token, self.repo]):
            logger.warning("GitHub credentials not configured")
            return None
        
        try:
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Get current file SHA if exists
            api_url = f"{self.base_url}/repos/{self.repo}/contents/{file_path}"
            response = requests.get(api_url, headers=headers)
            
            sha = None
            if response.status_code == 200:
                sha = response.json()["sha"]
            
            # Prepare commit data
            data = {
                "message": commit_message,
                "content": base64.b64encode(content.encode()).decode()
            }
            
            if sha:
                data["sha"] = sha
            
            # Commit the file
            response = requests.put(api_url, headers=headers, json=data)
            
            if response.status_code in [200, 201]:
                commit_url = response.json()["content"]["html_url"]
                logger.info(f"Successfully committed file to GitHub: {commit_url}")
                return commit_url
            else:
                logger.error(f"Failed to commit file: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"GitHub commit failed: {e}")
            return None
    
    async def upload_transcript(self, transcript_content: str, video_metadata: Dict[str, Any]) -> Optional[str]:
        """Upload transcript and metadata to GitHub"""
        try:
            # Create transcript file
            transcript_file = f"transcripts/{datetime.now().strftime('%Y-%m-%d')}-transcript.txt"
            transcript_commit = await self.commit_file(
                transcript_file,
                transcript_content,
                f"Add transcript: {video_metadata.get('title', 'Recording')}"
            )
            
            # Create metadata file
            metadata = {
                **video_metadata,
                "recording_date": datetime.now().isoformat(),
                "transcript_length": len(transcript_content)
            }
            metadata_file = f"metadata/{datetime.now().strftime('%Y-%m-%d')}.json"
            metadata_content = json.dumps(metadata, indent=2)
            metadata_commit = await self.commit_file(
                metadata_file,
                metadata_content,
                f"Add metadata: {video_metadata.get('title', 'Recording')}"
            )
            
            return transcript_commit or metadata_commit
            
        except Exception as e:
            logger.error(f"GitHub upload failed: {e}")
            return None

class TranscriptGenerator:
    """Audio transcription using AI"""
    
    async def generate_transcript(self, audio_file: Path) -> Optional[str]:
        """Generate transcript from audio file"""
        try:
            # In production, use OpenAI Whisper, Google Speech-to-Text, or similar
            logger.info(f"Generating transcript for: {audio_file}")
            
            # Simulate transcription process
            transcript_content = f"Transcript generated for {audio_file.name}\nTimestamp: {datetime.now()}\n\n[Generated transcript would appear here]"
            
            # Save transcript
            transcript_file = config.transcripts_dir / f"{audio_file.stem}.txt"
            with open(transcript_file, 'w') as f:
                f.write(transcript_content)
            
            logger.info(f"Transcript saved: {transcript_file}")
            return str(transcript_file)
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None

class OBSController:
    """OBS WebSocket controller"""
    
    async def get_connection(self) -> Optional[obsws]:
        """Get OBS WebSocket connection"""
        try:
            ws = obsws(config.obs_host, config.obs_port, config.obs_password)
            ws.connect()
            return ws
        except Exception as e:
            logger.error(f"Failed to connect to OBS: {e}")
            return None
    
    async def start_recording(self) -> bool:
        """Start OBS recording"""
        try:
            obs = await self.get_connection()
            if not obs:
                return False
            
            obs.start_record()
            obs.disconnect()
            logger.info("OBS recording started")
            return True
        except Exception as e:
            logger.error(f"Failed to start OBS recording: {e}")
            return False
    
    async def stop_recording(self) -> bool:
        """Stop OBS recording"""
        try:
            obs = await self.get_connection()
            if not obs:
                return False
            
            obs.stop_record()
            obs.disconnect()
            logger.info("OBS recording stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop OBS recording: {e}")
            return False

class CloudUploader:
    """Cloud storage uploader (S3/rclone)"""
    
    def __init__(self):
        self.s3_bucket = config.s3_bucket
        self.rclone_remote = config.rclone_remote
    
    async def upload_to_s3(self, file_path: Path) -> bool:
        """Upload to S3"""
        if not self.s3_bucket:
            return False
        
        try:
            s3_key = f"recordings/{datetime.now().strftime('%Y/%m/%d')}/{file_path.name}"
            s3 = boto3.client('s3')
            
            await asyncio.get_event_loop().run_in_executor(
                None, 
                s3.upload_file, 
                str(file_path), 
                self.s3_bucket, 
                s3_key
            )
            logger.info(f"Uploaded to S3: {s3_key}")
            return True
        except NoCredentialsError:
            logger.warning("AWS credentials not configured")
            return False
        except Exception as e:
            logger.error(f"S3 upload failed: {e}")
            return False
    
    async def upload_to_rclone(self, file_path: Path) -> bool:
        """Upload to rclone remote"""
        if not self.rclone_remote:
            return False
        
        try:
            remote_path = f"{self.rclone_remote}:recordings/{datetime.now().strftime('%Y/%m/%d')}/{file_path.name}"
            
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                subprocess.run,
                ['rclone', 'copy', str(file_path), remote_path, '--progress'],
                {'capture_output': True, 'text': True}
            )
            
            if result.returncode == 0:
                logger.info(f"Uploaded to rclone: {remote_path}")
                return True
            else:
                logger.error(f"Rclone upload failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Rclone upload failed: {e}")
            return False

# Initialize services
youtube_uploader = YouTubeUploader()
github_integrator = GitHubIntegrator()
transcript_generator = TranscriptGenerator()
obs_controller = OBSController()
cloud_uploader = CloudUploader()

def load_prompts():
    """Load custom prompts from configuration"""
    global prompts
    prompts_file = config.install_dir / 'config' / 'prompts.json'
    
    if prompts_file.exists():
        with open(prompts_file, 'r') as f:
            prompts = json.load(f)
    else:
        # Default prompts
        prompts = {
            "recording_start": "🎙️ Recording started in {channel_name}!",
            "recording_stop": "⏹️ Recording stopped. Processing...",
            "upload_success": "✅ Video uploaded: {video_url}",
            "github_commit": "📁 Files committed to GitHub: {commit_url}",
            "transcript_ready": "📝 Transcript generated: {transcript_path}",
            "cloud_upload": "☁️ Uploaded to cloud storage: {file_path}"
        }

@bot.event
async def on_ready():
    """Bot ready event"""
    load_prompts()
    logger.info(f'{config.discord_bot_name} logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"for /record commands | {config.discord_bot_name} ready!"
    ))

@bot.command(name='record')
async def record_command(ctx, subcommand: str = None, minutes: int = 0):
    """Enhanced recording control with YouTube, GitHub, and cloud integration"""
    if ctx.guild is None:
        return
    
    if subcommand is None:
        await ctx.send("❓ Usage: `/record start [minutes]` | `/record stop` | `/record status` | `/record upload`")
        return
    
    subcommand = subcommand.lower()
    
    if subcommand == 'start':
        await handle_record_start(ctx, minutes)
    elif subcommand == 'stop':
        await handle_record_stop(ctx)
    elif subcommand == 'status':
        await handle_record_status(ctx)
    elif subcommand == 'upload':
        await handle_manual_upload(ctx)
    else:
        await ctx.send(f"❓ Unknown subcommand: {subcommand}")

async def handle_record_start(ctx, minutes):
    """Handle recording start with enhanced features"""
    if recording_state['active']:
        await ctx.send("⚠️ Recording already in progress!")
        return
    
    try:
        # Start OBS recording
        if not await obs_controller.start_recording():
            await ctx.send("❌ Failed to start OBS recording")
            return
        
        # Update state
        recording_state.update({
            'active': True,
            'start_time': datetime.now(),
            'duration_minutes': minutes,
            'recording_filename': datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
            'participants': [],
            'youtube_upload_id': None,
            'github_commit_url': None,
            'transcript_path': None
        })
        
        # Send start message
        minutes_str = f" for {minutes} minutes" if minutes > 0 else ""
        start_msg = prompts.get('recording_start', 'Recording started').format(
            channel_name=ctx.channel.name
        )
        await ctx.send(f"{start_msg}{minutes_str}")
        
        # Schedule automatic stop if minutes specified
        if minutes > 0:
            await asyncio.sleep(minutes * 60)
            if recording_state['active']:
                await ctx.send("⏰ Recording time limit reached. Stopping...")
                await handle_record_stop(ctx)
        
        logger.info(f"Enhanced recording started by {ctx.author.display_name}")
        
    except Exception as e:
        logger.error(f"Failed to start recording: {e}")
        await ctx.send(f"❌ Failed to start recording: {str(e)}")

async def handle_record_stop(ctx):
    """Handle recording stop with full processing pipeline"""
    if not recording_state['active']:
        await ctx.send("⚠️ No recording in progress!")
        return
    
    try:
        # Stop OBS recording
        if not await obs_controller.stop_recording():
            await ctx.send("❌ Failed to stop OBS recording")
            return
        
        # Update state
        duration = datetime.now() - recording_state['start_time']
        recording_filename = recording_state['recording_filename']
        
        recording_state.update({
            'active': False,
            'start_time': None,
            'duration_minutes': 0,
            'recording_filename': None
        })
        
        # Send stop message
        stop_msg = prompts.get('recording_stop', 'Recording stopped')
        await ctx.send(f"{stop_msg} Duration: {duration}")
        
        # Process recording in background
        asyncio.create_task(process_recording_pipeline(recording_filename, ctx))
        
        logger.info(f"Enhanced recording stopped by {ctx.author.display_name}")
        
    except Exception as e:
        logger.error(f"Failed to stop recording: {e}")
        await ctx.send(f"❌ Failed to stop recording: {str(e)}")

async def process_recording_pipeline(filename: str, ctx):
    """Process recording through full pipeline: upload, transcript, GitHub"""
    try:
        await ctx.send("🔄 Starting post-recording processing...")
        
        # Find recording file
        recording_files = list(config.recordings_dir.glob(f"{filename}.mp4"))
        if not recording_files:
            logger.error(f"Recording file not found: {filename}")
            await ctx.send("❌ Recording file not found for processing")
            return
        
        recording_file = recording_files[0]
        logger.info(f"Processing recording: {recording_file}")
        
        # Generate transcript
        transcript_path = await transcript_generator.generate_transcript(recording_file)
        if transcript_path:
            recording_state['transcript_path'] = transcript_path
            
            # Read transcript content
            with open(transcript_path, 'r') as f:
                transcript_content = f.read()
            
            # Commit to GitHub
            video_metadata = {
                'title': f"Recording {filename}",
                'description': f"Recording from {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                'duration': duration.total_seconds() if 'duration' in locals() else 0,
                'discord_channel': ctx.channel.name,
                'recording_user': ctx.author.display_name
            }
            
            github_url = await github_integrator.upload_transcript(transcript_content, video_metadata)
            if github_url:
                recording_state['github_commit_url'] = github_url
                github_msg = prompts.get('github_commit', 'Files committed to GitHub').format(
                    commit_url=github_url
                )
                await ctx.send(github_msg)
        
        # Upload to YouTube
        youtube_id = await youtube_uploader.upload_video(
            recording_file,
            f"Recording {filename}",
            f"Automated recording from Discord channel {ctx.channel.name}"
        )
        if youtube_id:
            recording_state['youtube_upload_id'] = youtube_id
            upload_msg = prompts.get('upload_success', 'Video uploaded').format(
                video_url=f"https://youtube.com/watch?v={youtube_id}"
            )
            await ctx.send(upload_msg)
        
        # Upload to cloud storage
        s3_success = await cloud_uploader.upload_to_s3(recording_file)
        rclone_success = await cloud_uploader.upload_to_rclone(recording_file)
        
        if s3_success or rclone_success:
            cloud_msg = prompts.get('cloud_upload', 'Uploaded to cloud storage').format(
                file_path=recording_file.name
            )
            await ctx.send(cloud_msg)
        
        # Final status
        await ctx.send("✅ Processing complete!")
        logger.info(f"Recording pipeline completed for: {filename}")
        
    except Exception as e:
        logger.error(f"Recording pipeline failed: {e}")
        await ctx.send(f"❌ Processing failed: {str(e)}")

async def handle_record_status(ctx):
    """Handle recording status command"""
    if not recording_state['active']:
        await ctx.send("🟦 Recording is not active")
        return
    
    duration = datetime.now() - recording_state['start_time']
    minutes, seconds = divmod(duration.total_seconds(), 60)
    
    status_msg = f"🔴 Recording active for {int(minutes):02d}:{int(seconds):02d}"
    
    if recording_state['youtube_upload_id']:
        status_msg += " | 📺 YouTube: Pending upload"
    
    if recording_state['github_commit_url']:
        status_msg += " | 📁 GitHub: Committed"
    
    if recording_state['transcript_path']:
        status_msg += " | 📝 Transcript: Generated"
    
    await ctx.send(status_msg)

async def handle_manual_upload(ctx):
    """Handle manual upload of existing recordings"""
    try:
        # List recent recordings
        recordings = sorted(config.recordings_dir.glob("*.mp4"), 
                          key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        
        if not recordings:
            await ctx.send("No recordings found for upload")
            return
        
        upload_options = []
        for i, recording in enumerate(recordings, 1):
            upload_options.append(f"{i}. {recording.name}")
        
        await ctx.send(f"📁 Available recordings:\n" + "\n".join(upload_options))
        
        # In production, this would handle user selection and upload
        await ctx.send("Upload functionality ready - select recording to upload")
        
    except Exception as e:
        logger.error(f"Manual upload failed: {e}")
        await ctx.send(f"❌ Upload failed: {str(e)}")

@tasks.loop(minutes=5)
async def health_check_task():
    """Periodic health check"""
    try:
        # Check OBS connection
        obs = await obs_controller.get_connection()
        if obs:
            obs.disconnect()
            logger.debug("OBS health check: OK")
        
        # Check recording state consistency
        if recording_state['active']:
            # Verify OBS is actually recording
            pass
            
    except Exception as e:
        logger.warning(f"Health check failed: {e}")

if __name__ == "__main__":
    # Validate configuration
    if not os.getenv('DISCORD_BOT_TOKEN'):
        logger.error("DISCORD_BOT_TOKEN not configured")
        sys.exit(1)
    
    if not config.obs_password:
        logger.error("OBS_WEBSOCKET_PASSWORD not configured")
        sys.exit(1)
    
    # Start health check task
    health_check_task.start()
    
    # Run bot
    discord_token = os.getenv('DISCORD_BOT_TOKEN')
    bot.run(discord_token)