import socket
import threading
import time
import webview
import speech_recognition as sr
import pyttsx3
import json
from pathlib import Path
from app import app

HOST = "127.0.0.1"

class JOATVoiceAPI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.listen_lock = threading.Lock()
        self.speak_lock = threading.Lock()
        self.speaking = False

    def listen(self):
        try:
            with self.listen_lock:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=15)
                text = self.recognizer.recognize_google(audio, language="en-NG")
                return {"ok": True, "text": text}
        except sr.WaitTimeoutError:
            return {"ok": False, "error": "I didn't hear anything."}
        except sr.UnknownValueError:
            return {"ok": False, "error": "I couldn't understand that. Try again."}
        except sr.RequestError:
            return {"ok": False, "error": "Speech recognition needs an internet connection."}
        except Exception as e:
            return {"ok": False, "error": f"Microphone error: {e}"}

    def _speak_worker(self, text, voice_id):
        with self.speak_lock:
            engine = None
            try:
                engine = pyttsx3.init()
                voices = engine.getProperty("voices") or []
                if voice_id is not None and str(voice_id).isdigit():
                    i = int(voice_id)
                    if 0 <= i < len(voices):
                        engine.setProperty("voice", voices[i].id)
                engine.setProperty("rate", 175)
                engine.say(str(text))
                engine.runAndWait()
            except Exception:
                pass
            finally:
                try:
                    if engine is not None:
                        engine.stop()
                except Exception:
                    pass
                self.speaking = False

    def speak(self, text, voice_id=None):
        try:
            if not str(text).strip():
                return {"ok": False, "error": "Nothing to speak."}
            self.speaking = True
            threading.Thread(target=self._speak_worker, args=(str(text), voice_id), daemon=True).start()
            return {"ok": True, "started": True}
        except Exception as e:
            self.speaking = False
            return {"ok": False, "error": str(e)}

    def open_model_file(self):
        try:
            result=webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=('GGUF model (*.gguf)', 'All files (*.*)'))
            if result:
                return {"ok":True,"path":result[0]}
            return {"ok":False,"cancelled":True}
        except Exception as e:
            return {"ok":False,"error":str(e)}

    def voices(self):
        try:
            return [{"id": str(i), "name": v.name or f"Voice {i}", "languages": str(v.languages)} for i, v in enumerate(self.engine.getProperty("voices"))]
        except Exception:
            return []


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, 0))
        return s.getsockname()[1]

def run_server(port):
    app.run(host=HOST, port=port, debug=False, use_reloader=False, threaded=True)

def wait_for_server(port, timeout=10):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((HOST, port), timeout=0.25):
                return True
        except OSError:
            time.sleep(0.1)
    return False

def main():
    port = get_free_port()
    server = threading.Thread(target=run_server, args=(port,), daemon=True)
    server.start()
    if not wait_for_server(port):
        raise RuntimeError("J.O.A.T. server could not start.")
    api = JOATVoiceAPI()
    webview.create_window("J.O.A.T. — Jack Of All Trades", f"http://{HOST}:{port}/", width=1280, height=820, min_size=(900, 620), resizable=True, text_select=True, js_api=api)
    webview.start(gui="edgechromium", debug=False)

if __name__ == "__main__":
    main()
