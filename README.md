# 💬 ChatGPT to Gemini Migration Tool

A beautiful, easy-to-use tool to export, convert, and browse your ChatGPT conversation history. Perfect for users migrating to Gemini or anyone who wants to preserve their ChatGPT conversations in a searchable, accessible format.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 🔍 **Interactive Viewer** - Beautiful web interface to browse all conversations
- 📝 **Markdown Export** - Each conversation as a clean, readable `.md` file
- 📊 **CSV Summary** - Analyze your data in Excel or Google Sheets
- 💾 **JSON Export** - Structured data for developers
- 🎨 **Modern UI** - Responsive, gradient design with smooth scrolling
- 🔒 **100% Local** - All processing happens on your computer
- 🚀 **Easy Setup** - Just 2 commands to get started

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher ([Download here](https://www.python.org/downloads/))
- Your ChatGPT data export

### Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/yourusername/chatgpt-to-gemini.git
   cd chatgpt-to-gemini
   ```

2. **Export your ChatGPT data**
   - Go to ChatGPT → Settings → Data Controls → Export Data
   - Download the ZIP file you receive via email
   - Extract it and copy `conversations.json` to this folder

3. **Run the migration**
   ```bash
   python migrate_to_gemini.py
   ```

4. **View your conversations**
   ```bash
   python view_conversations.py
   ```
   Your browser will automatically open at `http://localhost:8000`

## 📖 Full Documentation

Open `index.html` in your browser for the complete guide with:
- Step-by-step instructions
- Troubleshooting tips
- Best practices
- Feature showcase

Or simply run:
```bash
python -m http.server 8080
```
Then open `http://localhost:8080/index.html`

## 📂 What Gets Created

After migration, you'll have a `migrated_conversations` folder with:

```
migrated_conversations/
├── html/
│   └── conversation_viewer_v2.html    # Interactive viewer
├── markdown/
│   ├── 0001_First_Conversation.md
│   ├── 0002_Second_Conversation.md
│   └── ... (one per conversation)
├── json/
│   └── all_conversations.json         # All data in JSON
└── csv/
    └── conversation_summary.csv        # Metadata spreadsheet
```

## 🎯 Using with Gemini

Since Gemini doesn't have direct import:

1. Browse conversations in the viewer
2. Copy relevant context
3. Start a new Gemini chat and paste:
   ```
   I'm migrating from ChatGPT. Here's context from a previous conversation:
   
   [paste conversation]
   
   Can you help me continue this?
   ```

## 🛠️ Scripts Overview

| Script | Purpose |
|--------|---------|
| `migrate_to_gemini.py` | Main conversion script - exports to all formats |
| `view_conversations.py` | Starts local web server for the viewer |
| `analyze_structure.py` | Analyzes your JSON structure (optional) |
| `index.html` | Complete user guide and documentation |

## 💡 Tips

- **Backup**: Keep your original `conversations.json` safe
- **Search**: Use the viewer's search to find specific topics
- **Archive**: Markdown files are perfect for long-term storage
- **Analysis**: Use the CSV for conversation statistics
- **Developers**: JSON format is ideal for custom integrations

## ❓ Troubleshooting

### Python not found
Install Python from [python.org](https://www.python.org/downloads/) and ensure "Add to PATH" is checked

### File not found
Make sure `conversations.json` is in the same folder as the scripts

### Browser doesn't open
Manually navigate to `http://localhost:8000` after running the viewer

### Port already in use
Edit `view_conversations.py` and change `PORT = 8000` to another number

## 🔒 Privacy & Security

- ✅ **100% Local Processing** - Everything runs on your computer
- ✅ **No Data Upload** - Your conversations never leave your device
- ✅ **No Tracking** - No analytics or telemetry
- ✅ **Open Source** - Inspect the code yourself

## 📊 Statistics

The tool will show you:
- Total conversations
- Total messages (user + assistant)
- Date range of your conversations
- Message counts per conversation

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📝 License

MIT License - feel free to use, modify, and distribute

## 🙏 Acknowledgments

Built for the ChatGPT community migrating to Gemini and anyone who wants to preserve their AI conversation history.

---

**Made with ❤️ for ChatGPT users**

*Questions? Issues? Open an issue on GitHub or check the full guide in `index.html`*
