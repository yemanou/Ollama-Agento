# Ollama Agent for ComfyUI

> **Voice-Controlled AI Screen Analysis for ComfyUI**

A powerful ComfyUI custom node plugin that creates a multimodal AI assistant capable of analyzing screen content through voice commands. Combines screen capture, speech recognition, and local AI vision models via Ollama.

## 🎯 What It Does

This plugin enables you to:
- **Capture your screen** automatically within ComfyUI workflows
- **Ask questions using your voice** about what's displayed
- **Get AI-powered analysis** of screen content using local Ollama models
- **Chain operations** flexibly in ComfyUI's node-based interface

Perfect for accessibility, workflow automation, content analysis, and hands-free computer interaction.

## 🧩 Nodes

### Screen Capture
- Captures the primary monitor's screen in real-time
- Outputs ComfyUI-compatible image tensors
- Cross-platform support (Windows, macOS, Linux)

### Ollama Vision  
- Sends images and text prompts to local Ollama models
- Supports multimodal models like LLaVA for vision analysis
- Returns detailed text analysis of visual content
- Handles errors gracefully with informative feedback

### Voice Control
- Converts speech to text using Google Speech Recognition
- Triggered by boolean input for controlled activation
- Handles ambient noise adjustment automatically
- Provides clear error messages for audio issues

## 📋 Prerequisites

1. **ComfyUI** installed and running
2. **Ollama** installed with a vision model (e.g., `ollama pull llava`)
3. **Microphone** access for voice control
4. **Internet connection** for speech recognition (uses Google's API)

## 🚀 Installation

### Method 1: Standard Installation

1. Navigate to your ComfyUI custom nodes directory:
   ```bash
   cd /path/to/ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```bash
   git clone <repository_url> ollama_agento
   ```

3. Install dependencies in your ComfyUI environment:
   ```bash
   # If using ComfyUI's venv
   /path/to/ComfyUI/venv/bin/pip install -r ollama_agento/requirements.txt
   
   # Or if using system Python
   pip install -r ollama_agento/requirements.txt
   ```

4. Restart ComfyUI

### Method 2: Manual Dependency Installation

If you encounter dependency issues, install packages individually:

```bash
pip install mss>=10.0.0
pip install ollama>=0.6.0
pip install SpeechRecognition>=3.8.0
pip install PyAudio>=0.2.11
```

## 🔧 Setup & Configuration

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)

2. **Pull a vision model**:
   ```bash
   ollama pull llava
   ```

3. **Test Ollama** (optional):
   ```bash
   ollama run llava "Describe this image" --image /path/to/test-image.jpg
   ```

4. **Verify microphone access** and ensure your system can record audio

## 💡 Usage Examples

### Basic Workflow: Voice-Controlled Screen Analysis

1. Add a **Screen Capture** node to capture your display
2. Add a **Voice Control** node with a boolean trigger
3. Add an **Ollama Vision** node for AI analysis
4. Connect the nodes:
   - `Screen Capture` → `IMAGE` → `Ollama Vision`
   - `Voice Control` → `STRING` → `Ollama Vision` (prompt input)

### Advanced Workflows

- **Automated Documentation**: Capture code screens and generate documentation
- **Accessibility Helper**: Voice-describe screen content for visually impaired users  
- **Content Moderation**: Analyze screenshots for inappropriate content
- **UI Testing**: Describe interface elements and identify issues

## 🐛 Troubleshooting

### Common Issues

**Ollama Connection Failed:**
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Verify model supports vision: `ollama show llava`

**Voice Recognition Not Working:**
- Check microphone permissions
- Test with: `python -c "import speech_recognition as sr; print('OK')"`
- Ensure internet connection (uses Google Speech API)

**Dependencies Missing:**
- Reinstall with: `pip install --force-reinstall -r requirements.txt`
- Check Python environment matches ComfyUI's

### Dependency Issues

If you see `ModuleNotFoundError` or version conflicts:

1. **Update requirements.txt** with compatible versions
2. **Use virtual environment** matching ComfyUI's Python version
3. **Check for conflicting packages** in your environment

## 🔬 Technical Details

- **Screen Capture**: Uses `mss` library for fast, cross-platform screenshots
- **AI Integration**: Leverages Ollama's Python client for local model inference  
- **Speech Processing**: Google Speech Recognition with ambient noise handling
- **Image Processing**: Proper tensor conversions for ComfyUI compatibility
- **Error Handling**: Comprehensive exception handling with user feedback

## 🤝 Contributing

Issues and improvements welcome! This plugin bridges multiple technologies and benefits from community testing across different setups.

## 📄 License

[Add your license here]

---

**Note**: This plugin requires external services (Ollama, Google Speech API) and hardware access (microphone, screen). Ensure proper permissions and privacy considerations for your use case.
