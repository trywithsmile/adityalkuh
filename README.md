# Telegram Image Caption Link Bot

A powerful Telegram bot that automatically adds channel links to image captions in private channels.

## 🚀 Features

- **Auto Caption Linking**: Automatically adds channel links to all images
- **Caption Preservation**: Keeps original captions intact
- **Multi-format Support**: Works with photos and image documents
- **Admin Controls**: Full command-based management
- **Error Handling**: Robust error handling and logging
- **Statistics**: Track bot performance
- **Railway Deployment Ready**: Optimized for Railway.app deployment

## 📋 Commands

### User Commands
- `/start` - Start the bot and see welcome message
- `/help` - Get detailed help and usage instructions
- `/status` - Check bot status and statistics

### Admin Commands
- `/set_channel @username link` - Add/update channel configuration
- `/remove_channel @username` - Remove channel from bot
- `/list_channels` - List all configured channels
- `/clear_stats` - Clear bot statistics

## 🛠️ Setup Instructions

### 1. Create Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Save your bot token

### 2. Deploy on Railway.app

#### Option A: Direct GitHub Deploy
1. Fork this repository
2. Connect your GitHub account to Railway
3. Create new project from GitHub repo
4. Add environment variable: `TELEGRAM_BOT_TOKEN=your_bot_token`
5. Deploy!

#### Option B: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variable
railway variables set TELEGRAM_BOT_TOKEN=your_bot_token

# Deploy
railway up
```

### 3. Configure Bot
1. Add bot to your private channel as admin
2. Give bot "Edit Messages" permission
3. Use `/set_channel @yourchannel https://t.me/yourchannel`
4. Bot will start working automatically!

## 🔧 Configuration

### Environment Variables
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required)

### Channel Setup
```bash
/set_channel @mychannel https://t.me/mychannel
```

## 📁 File Structure
```
.
├── main.py              # Main bot code
├── requirements.txt     # Python dependencies
├── railway.json         # Railway configuration
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## 🔍 How It Works

1. **Channel Monitoring**: Bot monitors configured channels for new images
2. **Caption Processing**: When an image is posted, bot adds channel link to caption
3. **Link Generation**: Creates direct message links using channel URL + message ID
4. **Caption Update**: Updates the image caption while preserving original text

## 🛡️ Error Handling

- **Duplicate Prevention**: Avoids processing same message multiple times
- **Permission Checks**: Validates bot permissions before editing
- **Graceful Failures**: Logs errors without crashing
- **Retry Logic**: Built-in retry mechanisms for failed operations

## 📊 Features Included

✅ **Multi-language Support** (Hindi/English)  
✅ **Interactive Keyboard Navigation**  
✅ **Statistics Tracking**  
✅ **Admin Panel**  
✅ **Error Logging**  
✅ **Railway Deployment Ready**  
✅ **Docker Support**  
✅ **Auto-restart on Failure**  

## 🆘 Troubleshooting

### Common Issues

**Bot not responding?**
- Check if bot token is correctly set
- Ensure bot is admin in the channel
- Verify "Edit Messages" permission is enabled

**Links not being added?**
- Run `/set_channel @yourchannel https://t.me/yourchannel`
- Check channel username is correct
- Ensure channel is public or bot has access

**Deployment issues?**
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure requirements.txt is up to date

## 📝 Example Usage

```bash
# Start bot
/start

# Configure channel
/set_channel @mychannel https://t.me/mychannel

# Check status
/status

# List all channels
/list_channels
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆕 Updates & Support

For updates and support:
- Create issues on GitHub
- Check Railway deployment logs
- Monitor bot using `/status` command

---

**Happy Botting! 🤖**
