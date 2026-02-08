# 📥 Input Folder - ChatGPT Export Files

This folder is where you place your ChatGPT conversation export files.

---

## 📋 Step-by-Step: How to Export from ChatGPT

### 1. **Open ChatGPT Settings**

- Go to [ChatGPT](https://chat.openai.com)
- Click on your **profile picture** (bottom left corner)
- Select **Settings**

### 2. **Navigate to Data Controls**

- In the Settings menu, find **Data controls**
- Click on it to expand the section

### 3. **Request Your Data Export**

- Look for **"Export data"** option
- Click the **"Export"** button
- Confirm the export request

### 4. **Wait for Email**

- OpenAI will process your request (usually takes a few minutes to a few hours)
- You'll receive an email at your registered email address
- Subject line: **"Your ChatGPT data export is ready"**

### 5. **Download the ZIP File**

- Open the email from OpenAI
- Click the **download link** in the email
- The link is valid for **24 hours** (download promptly!)
- Save the ZIP file to your computer

### 6. **Extract the ZIP File**

- Locate the downloaded ZIP file (usually in your Downloads folder)
- Right-click → **Extract All** (Windows) or double-click (Mac)
- Extract to a temporary location

### 7. **Find conversations.json**

- Inside the extracted folder, you'll find several files:
  - `conversations.json` ← **This is what you need!**
  - `chat.html` (optional HTML version)
  - `message_feedback.json`
  - `model_comparisons.json`
  - `user.json`
  - Other metadata files

### 8. **Copy to This Folder**

- Copy `conversations.json` from the extracted folder
- Paste it into **this folder** (`input/`)
- ✅ You're ready to run the migration!

---

## 📁 What Files to Place Here

### **Required:**

- ✅ **conversations.json** - Your complete ChatGPT conversation history

### **Optional:**

- 📄 **chat.html** - HTML version of your conversations (if you want to keep it)
- 📦 **[export].zip** - The original ZIP file (for backup)

---

## 🔒 Privacy & Security

- ✅ All files in this folder are **automatically ignored by git**
- ✅ Your conversations will **never be committed** to version control
- ✅ Everything is processed **locally on your computer**
- ✅ No data is sent to any external servers

---

## ⚠️ Troubleshooting

### "File not found" error?

- Make sure `conversations.json` is directly in the `input/` folder
- Check the filename is exactly `conversations.json` (case-sensitive on some systems)
- Verify the file isn't empty (should be several MB in size)

### Export link expired?

- Export links are valid for 24 hours only
- Request a new export from ChatGPT settings
- Download immediately when you receive the email

### Can't find the export option?

- Make sure you're logged into ChatGPT
- The export feature is available for all ChatGPT users (free and paid)
- Try using a desktop browser if you're on mobile

---

## 🚀 Next Steps

Once you've placed `conversations.json` here:

1. Go back to the main project folder
2. Run: `python migrate_to_gemini.py`
3. Wait for the migration to complete
4. View your conversations with: `python view_conversations.py`

---

**Need help?** Check the main `README.md` or `index.html` for more information!
