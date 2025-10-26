import torch
import numpy as np
from PIL import Image
import mss
import ollama
import io
import speech_recognition as sr

def capture_screen():
    with mss.mss() as sct:
        # Get information of monitor 1
        monitor_number = 1
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_number,
        }
        
        # Grab the data
        sct_img = sct.grab(monitor)
        
        # Convert to PIL Image
        return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

class ScreenCapture:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {}}

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "capture"
    CATEGORY = "OllamaAgent"

    def capture(self):
        captured_image = capture_screen()
        image_np = np.array(captured_image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]
        return (image_tensor,)

class OllamaVision:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "Analyze this image:"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "analyze"
    CATEGORY = "OllamaAgent"

    def analyze(self, image, prompt):
        # Convert tensor to PIL Image
        image_np = image.cpu().numpy().squeeze() * 255.0
        pil_image = Image.fromarray(image_np.astype(np.uint8))

        # Convert PIL image to bytes for Ollama
        byte_arr = io.BytesIO()
        pil_image.save(byte_arr, format='PNG')
        image_bytes = byte_arr.getvalue()

        # Interact with Ollama
        try:
            response = ollama.chat(
                model='llava:13b',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [image_bytes]
                    }
                ]
            )
            analysis_result = response['message']['content']
        except Exception as e:
            analysis_result = f"Error interacting with Ollama: {e}"

        return (analysis_result,)

class VoiceControl:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trigger": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "listen"

    CATEGORY = "OllamaAgent"

    def listen(self, trigger):
        if not trigger:
            return ("",)

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            return (text,)
        except sr.UnknownValueError:
            return ("Could not understand audio",)
        except sr.RequestError as e:
            return (f"Could not request results; {e}",)

NODE_CLASS_MAPPINGS = {
    "ScreenCapture": ScreenCapture,
    "OllamaVision": OllamaVision,
    "VoiceControl": VoiceControl
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ScreenCapture": "Screen Capture",
    "OllamaVision": "Ollama Vision",
    "VoiceControl": "Voice Control"
}
