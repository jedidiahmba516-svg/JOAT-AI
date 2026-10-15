from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from PIL import Image
from core import respond
from engines.multimodal_engine import save_image_state, try_ocr
from engines.settings_engine import load as load_settings, update as update_settings
from engines.local_ai_engine import status as local_model_status, unload as unload_local_model
from config import VERSION, VERSION_WIN, APP_NAME, FULL_NAME

app=Flask(__name__)

@app.route("/")
def home(): return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data=request.get_json(silent=True) or {}
    message=str(data.get("message","")).strip()
    return jsonify({"reply":respond(message)})


@app.route("/version", methods=["GET"])
def version():
    return jsonify({"name":APP_NAME,"full_name":FULL_NAME,"version":VERSION,"windows_version":VERSION_WIN,"channel":"Beta"})

@app.route("/settings", methods=["GET","POST"])
def settings():
    if request.method == "GET":
        return jsonify({"ok":True,"settings":load_settings(),"model":local_model_status()})
    data=request.get_json(silent=True) or {}
    patch=data.get("settings",data)
    if not isinstance(patch,dict): return jsonify({"ok":False,"error":"Invalid settings."}),400
    saved=update_settings(patch)
    unload_local_model()
    return jsonify({"ok":True,"settings":saved,"model":local_model_status()})

@app.route("/health", methods=["GET"])
def health():
    from engines.ultimate_engine import _load, METRICS
    metrics=_load(METRICS,{})
    return jsonify({"ok":True,"status":"online","actions":sum(v for v in metrics.values() if isinstance(v,int))})

@app.route("/activity", methods=["GET"])
def activity():
    from engines.activity_engine import _load_log
    try:
        return jsonify({"ok":True,"activity":_load_log()[-25:]})
    except Exception:
        return jsonify({"ok":True,"activity":[]})

@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    upload=request.files.get("image")
    if not upload:return jsonify({"ok":False,"error":"No image was supplied."}),400
    os.makedirs("data/uploads",exist_ok=True)
    filename=secure_filename(upload.filename or "image.bin")
    path=os.path.join("data/uploads",filename)
    upload.save(path)
    try:
        with Image.open(path) as image:
            info={"filename":filename,"width":image.width,"height":image.height,"format":image.format,"mode":image.mode,"path":path}
        ocr=try_ocr(path)
        if ocr:info["ocr_text"]=ocr[:4000]
        save_image_state(info)
        message=f"Image received: {info['width']}×{info['height']} {info['format']}."
        if ocr:message += " I also extracted readable text from it."
        return jsonify({"ok":True,"image":info,"message":message})
    except Exception as exc:
        return jsonify({"ok":False,"error":f"I couldn't read that image: {exc}"}),400

if __name__=="__main__":app.run(debug=True)
