#!/usr/bin/env python3
"""
Test script for Ollama Agent ComfyUI nodes
Tests each component individually to verify functionality
"""

import sys
import traceback
from ollama_agento import ScreenCapture, OllamaVision, VoiceControl

def test_screen_capture():
    """Test the screen capture functionality"""
    print("🖥️  Testing Screen Capture...")
    try:
        screen_node = ScreenCapture()
        result = screen_node.capture()
        
        if result and len(result) > 0:
            image_tensor = result[0]
            print(f"   ✅ Screen captured successfully")
            print(f"   📏 Image shape: {image_tensor.shape}")
            print(f"   🎨 Image dtype: {image_tensor.dtype}")
            return True
        else:
            print("   ❌ Screen capture returned empty result")
            return False
            
    except Exception as e:
        print(f"   ❌ Screen capture failed: {e}")
        traceback.print_exc()
        return False

def test_ollama_connection():
    """Test Ollama connection and model availability"""
    print("🤖 Testing Ollama Connection...")
    try:
        import ollama
        
        # List available models
        models = ollama.list()
        model_names = []
        if 'models' in models:
            for m in models['models']:
                if hasattr(m, 'name'):
                    model_names.append(m.name)
                elif isinstance(m, dict) and 'name' in m:
                    model_names.append(m['name'])
                elif hasattr(m, 'model'):
                    model_names.append(m.model)
                else:
                    model_names.append(str(m))
        
        print(f"   📋 Available models: {model_names}")
        
        # Check if llava is available
        has_llava = any('llava' in str(name).lower() for name in model_names)
        if has_llava:
            print("   ✅ LLaVA model found")
            return True
        else:
            print("   ⚠️  LLaVA model not found - run 'ollama pull llava' first")
            return False
            
    except Exception as e:
        print(f"   ❌ Ollama connection failed: {e}")
        traceback.print_exc()
        return False

def test_voice_control():
    """Test voice control setup (without actually listening)"""
    print("🎤 Testing Voice Control Setup...")
    try:
        import speech_recognition as sr
        import pyaudio
        
        # Test microphone availability
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        print(f"   🎙️  Found {len(mic_list)} microphones")
        
        # Test default microphone
        with sr.Microphone() as source:
            print("   ✅ Default microphone accessible")
            
        print("   ⚠️  Voice recognition requires internet connection and audio input")
        return True
        
    except Exception as e:
        print(f"   ❌ Voice control setup failed: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between screen capture and ollama vision"""
    print("🔗 Testing Integration...")
    try:
        # Capture screen
        screen_node = ScreenCapture()
        screen_result = screen_node.capture()
        
        if not screen_result:
            print("   ❌ Screen capture failed")
            return False
            
        # Test with a simple prompt (if ollama is available)
        vision_node = OllamaVision() 
        test_prompt = "What do you see in this image? Describe it briefly."
        
        print("   🔄 Sending to Ollama for analysis...")
        analysis_result = vision_node.analyze(screen_result[0], test_prompt)
        
        if analysis_result and len(analysis_result) > 0:
            response = analysis_result[0]
            if response.startswith("Error"):
                print(f"   ❌ Ollama error: {response}")
                return False
            else:
                print(f"   ✅ Integration successful")
                print(f"   💬 AI Response: {response[:100]}...")
                return True
        else:
            print("   ❌ No response from Ollama")
            return False
            
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Ollama Agent ComfyUI Node Test Suite")
    print("=" * 50)
    
    tests = [
        ("Screen Capture", test_screen_capture),
        ("Ollama Connection", test_ollama_connection), 
        ("Voice Control Setup", test_voice_control),
        ("Integration", test_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print()
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The plugin should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("💡 Common fixes:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Install Ollama: https://ollama.ai")
        print("   - Pull LLaVA model: ollama pull llava")
        print("   - Check microphone permissions")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())