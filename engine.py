import asyncio
import sqlite3
import random
import discord
from discord.ext import tasks

class CustomWorkerBot(discord.Client):
    def __init__(self, token, bot_type, guild_id, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_token = token
        self.bot_type = bot_type
        self.target_guild_id = int(guild_id) if guild_id else None
        self.target_channel_id = int(channel_id) if channel_id else None

    async def on_ready(self):
        print(f"🤖 [{self.user.name}] Deployed as {self.bot_type.upper()} status.")
        
        # Handle Chat Bot behavior loop
        if self.bot_type == "chat" and self.target_channel_id:
            self.chat_loop.start()
            
        # Handle Voice Chat (VC) Bot behavior
        if self.bot_type == "vc" and self.target_channel_id:
            try:
                channel = self.get_channel(self.target_channel_id)
                if channel and isinstance(channel, discord.VoiceChannel):
                    vc = await channel.connect()
                    # Stay completely muted and deafened in voice channel
                    await vc.main_ws.voice_state(self.target_guild_id, channel.id, self_mute=True, self_deaf=True)
                    print(f"🎙️ [{self.user.name}] Successfully joined VC: {channel.name}")
            except Exception as e:
                print(f"❌ [{self.user.name}] VC Join Failed: {e}")

    @tasks.loop(seconds=45)
    async def chat_loop(self):
        # Conversational phrases loop for Chat bots
        channel = self.get_channel(self.target_channel_id)
        if channel:
            phrases = [
                "This server looks awesome!",
                "Hello everyone! What's going on?",
                "Glad to be hanging out here. 🔥",
                "Chatting away smoothly!",
                "Wow, incredible vibes in this channel."
            ]
            try:
                await channel.send(random.choice(phrases))
            except Exception as e:
                print(f"❌ [{self.user.name}] Failed to send message: {e}")

async def run_all_active_bots():
    conn = sqlite3.connect("bot_stock.db")
    cursor = conn.cursor()
    
    # Retrieve all active bots that need deployment from database
    cursor.execute("SELECT token, bot_type, assigned_guild, target_channel FROM bots WHERE status = 'active'")
    active_rows = cursor.fetchall()
    conn.close()
    
    if not active_rows:
        print("📭 No active bot deployments found in your database right now.")
        return

    print(f"⚙️ Initializing {len(active_rows)} worker bot connection instances...")
    
    tasks_list = []
    for token, b_type, guild_id, channel_id in active_rows:
        # Configure Intents
        intents = discord.Intents.default()
        intents.guilds = True
        intents.messages = True
        
        # Configure Status/Presence parameters based on configuration type
        status_setting = discord.Status.online
        if b_type == "offline":
            status_setting = discord.Status.offline
            
        bot_instance = CustomWorkerBot(
            token=token,
            bot_type=b_type,
            guild_id=guild_id,
            channel_id=channel_id,
            intents=intents,
            status=status_setting
        )
        
        tasks_list.append(bot_instance.start(token))
        
    # Execute all bot client network loops concurrently
    await asyncio.gather(*tasks_list)

if __name__ == "__main__":
    try:
        asyncio.run(run_all_active_bots())
    except KeyboardInterrupt:
        print("\n🛑 Master Bot Execution Engine shutting down smoothly.")
