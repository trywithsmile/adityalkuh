import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ParseMode
import asyncio
from datetime import datetime

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramImageBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.channel_links = {}  # Store channel username -> link mapping
        self.processed_messages = set()  # Track processed messages to avoid duplicates
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_text = """
🤖 **Image Caption Link Bot**

**मुख्य विशेषताएं:**
• Private channels में images के captions में channel link add करता है
• Original caption को preserve करता है  
• Duplicate processing से बचता है
• Admin controls के साथ

**Commands:**
/start - Bot को शुरू करें
/help - Help देखें
/set_channel - Channel link set करें
/status - Bot status देखें
/stats - Statistics देखें

**Setup करने के लिए:**
1. Bot को channel में admin बनाएं
2. /set_channel command use करें
3. Bot automatically काम करना शुरू कर देगा!
        """
        
        keyboard = [
            [InlineKeyboardButton("📚 Help", callback_data="help"),
             InlineKeyboardButton("⚙️ Setup", callback_data="setup")],
            [InlineKeyboardButton("📊 Stats", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_text = """
📖 **Bot का उपयोग कैसे करें:**

**1. Channel Setup:**
• Bot को अपने channel में admin बनाएं
• "Edit Messages" permission दें

**2. Channel Link Set करें:**
• `/set_channel @yourchannel https://t.me/yourchannel`

**3. Bot Features:**
✅ Images के captions में automatic link add
✅ Original caption preserve करता है
✅ Error handling के साथ
✅ Statistics tracking

**4. Admin Commands:**
• `/set_channel <username> <link>` - Channel link set करें  
• `/remove_channel <username>` - Channel remove करें
• `/list_channels` - सभी channels देखें
• `/clear_stats` - Statistics clear करें

**Example:**
`/set_channel @mychannel https://t.me/mychannel`
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

    async def set_channel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set channel link command"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ **Usage:** `/set_channel @channel_username channel_link`\n\n"
                    "**Example:** `/set_channel @mychannel https://t.me/mychannel`",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            channel_username = context.args[0].replace('@', '')
            channel_link = context.args[1]
            
            # Validate link format
            if not channel_link.startswith(('https://t.me/', 'http://t.me/')):
                await update.message.reply_text(
                    "❌ **Invalid link format!**\n"
                    "Link should start with https://t.me/ or http://t.me/"
                )
                return
            
            self.channel_links[channel_username] = channel_link
            
            await update.message.reply_text(
                f"✅ **Channel successfully added!**\n\n"
                f"**Channel:** @{channel_username}\n"
                f"**Link:** {channel_link}\n\n"
                f"Bot will now automatically add links to images in this channel!",
                parse_mode=ParseMode.MARKDOWN
            )
            
            logger.info(f"Channel set: @{channel_username} -> {channel_link}")
            
        except Exception as e:
            logger.error(f"Error in set_channel_command: {e}")
            await update.message.reply_text("❌ Error setting channel. Please try again.")

    async def remove_channel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Remove channel command"""
        try:
            if len(context.args) < 1:
                await update.message.reply_text(
                    "❌ **Usage:** `/remove_channel @channel_username`"
                )
                return
            
            channel_username = context.args[0].replace('@', '')
            
            if channel_username in self.channel_links:
                del self.channel_links[channel_username]
                await update.message.reply_text(
                    f"✅ **Channel @{channel_username} removed successfully!**"
                )
            else:
                await update.message.reply_text(
                    f"❌ **Channel @{channel_username} not found!**"
                )
                
        except Exception as e:
            logger.error(f"Error in remove_channel_command: {e}")
            await update.message.reply_text("❌ Error removing channel.")

    async def list_channels_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all configured channels"""
        if not self.channel_links:
            await update.message.reply_text("❌ **No channels configured yet!**")
            return
        
        channels_text = "📋 **Configured Channels:**\n\n"
        for username, link in self.channel_links.items():
            channels_text += f"• @{username} → {link}\n"
        
        await update.message.reply_text(channels_text, parse_mode=ParseMode.MARKDOWN)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot status"""
        status_text = f"""
🤖 **Bot Status**

**Status:** ✅ Online
**Configured Channels:** {len(self.channel_links)}
**Processed Messages:** {len(self.processed_messages)}
**Uptime:** Running smoothly!

**Bot Info:**
• Version: 1.0
• Features: Auto Caption Linking
• Deployment: Railway Ready
        """
        await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)

    async def clear_stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear statistics"""
        self.processed_messages.clear()
        await update.message.reply_text("✅ **Statistics cleared successfully!**")

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "help":
            await self.help_command(update, context)
        elif query.data == "setup":
            setup_text = """
⚙️ **Quick Setup Guide:**

1. **Add bot to channel as admin**
2. **Give "Edit Messages" permission**
3. **Set channel link:**
   `/set_channel @yourchannel https://t.me/yourchannel`
4. **Done! Bot will start working automatically**

**Need help?** Use /help command for detailed guide.
            """
            await query.edit_message_text(setup_text, parse_mode=ParseMode.MARKDOWN)
        elif query.data == "stats":
            await self.status_command(update, context)

    async def handle_photo_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages and add channel links to captions"""
        try:
            message = update.message
            chat = message.chat
            
            # Skip if not a channel or if already processed
            if chat.type != 'channel' or message.message_id in self.processed_messages:
                return
            
            # Get channel username (without @)
            channel_username = chat.username
            if not channel_username or channel_username not in self.channel_links:
                return
            
            # Get channel link
            channel_link = self.channel_links[channel_username]
            
            # Get original caption
            original_caption = message.caption or ""
            
            # Create message link
            message_link = f"{channel_link}/{message.message_id}"
            
            # Prepare new caption
            if original_caption:
                new_caption = f"{original_caption}\n\n📎 [Message Link]({message_link})"
            else:
                new_caption = f"📎 [View Original]({message_link})"
            
            # Add to processed messages
            self.processed_messages.add(message.message_id)
            
            # Edit the message caption
            await context.bot.edit_message_caption(
                chat_id=chat.id,
                message_id=message.message_id,
                caption=new_caption,
                parse_mode=ParseMode.MARKDOWN
            )
            
            logger.info(f"Updated caption for message {message.message_id} in @{channel_username}")
            
        except Exception as e:
            logger.error(f"Error handling photo message: {e}")

    async def handle_document_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document/file messages (including images sent as files)"""
        try:
            message = update.message
            chat = message.chat
            
            # Skip if not a channel or if already processed
            if chat.type != 'channel' or message.message_id in self.processed_messages:
                return
            
            # Check if document is an image
            if message.document and message.document.mime_type and message.document.mime_type.startswith('image/'):
                channel_username = chat.username
                if not channel_username or channel_username not in self.channel_links:
                    return
                
                channel_link = self.channel_links[channel_username]
                original_caption = message.caption or ""
                message_link = f"{channel_link}/{message.message_id}"
                
                if original_caption:
                    new_caption = f"{original_caption}\n\n📎 [Message Link]({message_link})"
                else:
                    new_caption = f"📎 [View Original]({message_link})"
                
                self.processed_messages.add(message.message_id)
                
                await context.bot.edit_message_caption(
                    chat_id=chat.id,
                    message_id=message.message_id,
                    caption=new_caption,
                    parse_mode=ParseMode.MARKDOWN
                )
                
                logger.info(f"Updated document caption for message {message.message_id} in @{channel_username}")
                
        except Exception as e:
            logger.error(f"Error handling document message: {e}")

    def run(self):
        """Run the bot"""
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("set_channel", self.set_channel_command))
        self.application.add_handler(CommandHandler("remove_channel", self.remove_channel_command))
        self.application.add_handler(CommandHandler("list_channels", self.list_channels_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("clear_stats", self.clear_stats_command))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo_message))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document_message))
        
        # Start the bot
        logger.info("Starting Telegram Image Bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return
    
    # Create and run bot
    bot = TelegramImageBot(token)
    bot.run()

if __name__ == '__main__':
    main()
