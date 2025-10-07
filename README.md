# Gmail Email Alert Monitor
A Python script that monitors your Gmail inbox for new emails from a specific domain and plays an audible alarm when they arrive.

## Motivation
I created this script because I was anxiously waiting for an important email and didn't want to keep hitting refresh myself. I needed a tool that would check for me and provide a loud alert that I could hear even if I was in a different room or focused on another task.

## Features

- 🔔 Monitors Gmail for emails from any domain you specify (e.g., `@icloud.com`, `@work.com`)
- ⏰ Plays a continuous alarm sound when new emails are detected
- 📧 Shows sender and subject information for each new email
- ⚡ Checks every 30 minutes automatically
- 🎯 Only alerts on emails received after the program starts (ignores existing emails)
- 🔒 100% free using Google's Gmail API
- 🍎 macOS native text-to-speech and sound alerts

## Requirements

- macOS (uses native `say` and `afplay` commands)
- Python 3.7 or higher
- Gmail account
- Google Cloud project with Gmail API enabled

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gmail-alert-monitor.git
cd gmail-alert-monitor
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 4. Set Up Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the Gmail API:
   - Navigate to "APIs & Services" → "Enable APIs and Services"
   - Search for "Gmail API" and enable it
4. Create OAuth credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Configure OAuth consent screen if prompted (choose "External")
   - Select "Desktop app" as application type
   - Download the credentials JSON file
5. Rename the downloaded file to `credentials.json` and place it in the project directory
6. Add yourself as a test user:
   - Go to "APIs & Services" → "OAuth consent screen"
   - Scroll to "Test users" and add your Gmail address

## Usage

### Basic Usage

```bash
python gmail_checker.py
```

When prompted, enter the domain you want to monitor (e.g., `icloud.com`, `gmail.com`, `work-domain.com`)

### First Run

On the first run:
1. A browser window will open automatically
2. Sign in to your Gmail account
3. You'll see a warning "Google hasn't verified this app"
   - Click "Advanced"
   - Click "Go to [your app name] (unsafe)" (it's safe - it's your own app)
4. Click "Allow" to grant permissions
5. The script will start monitoring

### Stopping the Alarm

When the alarm sounds:
- Press **ENTER** to stop the alarm and continue monitoring
- Press **Ctrl+C** to stop the alarm and quit the program

### Stopping the Program

Press **Ctrl+C** at any time to quit

## Configuration

To change the check interval, edit the `CHECK_INTERVAL` variable in `gmail_checker.py`:

```python
CHECK_INTERVAL = 1800  # 30 minutes in seconds
```

Examples:
- 5 minutes: `300`
- 15 minutes: `900`
- 30 minutes: `1800`
- 1 hour: `3600`

## API Usage and Costs

This script uses Google's Gmail API, which is **completely free** for personal use:

- **Free quota**: 1 billion quota units per day
- **Typical usage**: ~2,000 quota units per day (checking every 30 minutes)
- **Cost**: $0.00

You would need to run this on approximately 500,000 computers simultaneously to exceed the free quota.

## File Structure

```
gmail-alert-monitor/
├── check_email.py      # Main script
├── credentials.json      # Your Google API credentials (DO NOT COMMIT)
├── token.pickle         # Generated after first login (DO NOT COMMIT)
├── README.md           # This file
└── .gitignore         # Git ignore file
```

## Security Notes

- Never commit `credentials.json` or `token.pickle` to version control
- The `.gitignore` file is configured to exclude these files
- Only share your repository without these credential files

## Troubleshooting

### "ModuleNotFoundError: No module named 'googleapiclient'"

Make sure you've activated your virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### "Access blocked: gmail checker has not completed the Google verification process"

Add yourself as a test user in the Google Cloud Console:
1. Go to "APIs & Services" → "OAuth consent screen"
2. Scroll to "Test users"
3. Click "Add users" and add your Gmail address

### Script not finding new emails

The script only monitors emails received **after** it starts. If you want to test it:
1. Start the script
2. Send yourself a test email from the domain you're monitoring
3. Wait for the next check cycle (up to 30 minutes)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project however you'd like.

## Author

Created by Amanda Hattaway

## Acknowledgments

- Uses Google's Gmail API
- Built for macOS using native system tools
