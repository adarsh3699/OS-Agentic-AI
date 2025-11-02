# 🚀 Quick Start Guide - AI Desktop Assistant

## 🎯 What This Does

**Intelligent AI agent** that controls your computer, organizes files, and automates tasks using:

- **Groq** (fast, 30 req/min)
- **Gemini** (reliable, 200 req/day)
- **Llama 3.1 8B Local** (unlimited, offline)

**Auto-switches** providers on rate limits. **Smart file grouping**. **5x faster** than naive implementations.

---

## ⚡ Quick Setup (2 minutes)

### 1. Install Dependencies

```bash
source my-env/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp src/config.example.py src/config.py
# Edit src/config.py and add your API keys:
# GROQ_API_KEY = "your-key"
# GEMINI_API_KEY = "your-key"
```

### 3. Install Local Model (Optional)

```bash
# Already installed: llama3.1:8b (4.9 GB)
ollama list  # Verify
```

### 4. Run

```bash
python run.py
```

---

## 🧠 Key Features

### 1. **Auto-Switching Providers**

- Groq hits rate limit → Switches to Gemini automatically
- Gemini hits rate limit → Switches to Local (Llama 3.1)
- **No crashes, seamless failover**

### 2. **Smart File Grouping**

```bash
# OLD (Dumb):
JPG/, JPEG/, PNG/, GIF/, PDF/ folders

# NEW (Smart):
Images/ (jpg+jpeg+png+gif)
Documents/ (pdf+doc+txt)
Videos/ (mp4+mov+avi)
```

### 3. **Efficient Batching** (5x Faster)

```bash
# OLD: 25+ API calls
list → mkdir → verify → mv → verify (repeat for each type)

# NEW: 4-5 API calls
list → mkdir all → mv all with && → verify once
```

### 4. **20 Professional Tools**

- File operations (list, read, move, organize)
- Computer control (mouse, keyboard, screenshots)
- App management (open apps, URLs)
- Memory (save/recall across sessions)
- Debugging (error recovery, screenshots)

---

## 📖 Common Commands

### File Organization

```bash
🤖 Your command: Organize my Desktop by file type
# Creates: Images/, Documents/, Videos/, Audio/
# Groups intelligently: jpg+jpeg+png → Images/
# Completes in 4-5 API calls
```

### Manual Model Switching

```bash
switch to local   # Use Llama 3.1 (unlimited, offline)
switch to groq    # Use Groq (fast)
switch to gemini  # Use Gemini (reliable)
show model        # See current model
```

### File Operations

```bash
List files in my Downloads folder
Move all PDFs from Desktop to Documents
Find all Python files in this project
```

### Computer Control

```bash
Open Chrome browser
Take a screenshot
Check what apps are running
```

---

## 🎯 Smart Grouping Examples

### Images → `.jpg .jpeg .png .gif .bmp .svg .webp`

### Documents → `.pdf .doc .docx .txt .rtf .odt`

### Videos → `.mp4 .mov .avi .mkv .webm .flv`

### Audio → `.mp3 .wav .flac .aac .ogg .m4a`

### Archives → `.zip .rar .7z .tar .gz`

---

## ⚙️ Configuration

### Model Tiers (Auto-selected by task complexity)

```python
SMALL  - llama-3.1-8b-instant (Groq) | gemini-2.0-flash | llama3.1:8b
MEDIUM - llama-3.3-70b (Groq)        | gemini-2.0-flash | llama3.1:8b
LARGE  - llama-3.3-70b (Groq)        | gemini-2.0-flash | llama3.1:8b
```

### Rate Limits

- **Groq:** 30 requests/min, 14,400/day
- **Gemini:** 15 requests/min, 200/day
- **Local:** Unlimited (offline)

---

## 🔧 Troubleshooting

### Rate Limits

**System auto-switches!** If you see:

```
⚠️  Rate limit error detected!
🔄 Switching to backup provider...
```

This is **normal** - the system is handling it.

### Local Model Slow

First run loads model into RAM (~35s). Subsequent runs: ~10-15s.

### Tool Call Errors

Local models use simplified tools. Cloud models (Groq/Gemini) get all 20 tools.

---

## 📊 Performance

| Provider   | Speed             | Reliability | Cost                 |
| ---------- | ----------------- | ----------- | -------------------- |
| **Groq**   | ⚡⚡⚡⚡⚡ (1-2s) | Excellent   | FREE (30/min)        |
| **Gemini** | ⚡⚡⚡⚡ (2-4s)   | Excellent   | FREE (15/min)        |
| **Local**  | ⚡⚡⚡ (10-15s)   | Good        | **FREE (unlimited)** |

---

## 📚 Documentation

- **EFFICIENCY_OPTIMIZATION.md** - How batching works
- **INTELLIGENT_OPTIMIZATION.md** - Smart file grouping
- **MANUAL_SWITCHING.md** - Model switching commands
- **docs/** - Detailed architecture, cost optimization, setup

---

## 🎉 What's New

### Latest Updates:

✅ **Smart File Grouping** - jpg+jpeg+png → Images/ (not separate folders)  
✅ **Universal Optimization** - 5x faster for ALL tasks (not just file org)  
✅ **Local Model Fixed** - Llama 3.1 8B works with proper tool calling  
✅ **Format JSON** - Correct parameter names for local models  
✅ **Batch Operations** - Creates all folders at once, chains moves

---

## 🚀 Ready to Use!

```bash
python run.py
```

Then try:

```
Organize my Desktop by file type
```

Watch it:

- ✅ List files once
- ✅ Create Images/, Documents/, Videos/ (smart grouping!)
- ✅ Move all files with one chained command
- ✅ Verify once
- ✅ Complete in 4-5 API calls (not 25!)
- ✅ Auto-switch providers on rate limits

**Welcome to your intelligent AI assistant!** 🎊
