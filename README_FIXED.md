J.O.A.T. — restored UI build

Run RUN_JOAT.bat or: python app.py

Python 3.13 compatible backend. Voice input uses Chrome/Edge speech recognition; voice output and voice selection use the browser speech synthesis voices.


DESKTOP APP MODE

1. Double-click INSTALL_JOAT.bat once.
2. Then double-click RUN_JOAT.bat.
3. J.O.A.T. opens in its own resizable/minimizable window. You do NOT need to copy or open the 127.0.0.1 address yourself.

The desktop window uses Microsoft Edge WebView2 on Windows. Windows 11 normally includes the WebView2 runtime. The local Flask server runs invisibly in the background and closes when the J.O.A.T. window closes.

## J.O.A.T. Four-Level Upgrade

This build adds four major layers without replacing the existing architecture:

1. Research Mode - combines Wikipedia and DuckDuckGo results when a request explicitly asks for research, sources, investigation, or comparison.
2. Tool System - exposes safe local tools for calculator, time, date, and system information.
3. Multimodal Image Intake - the camera button now opens an image picker and sends the image to J.O.A.T.; image metadata is stored as current multimodal context.
4. Agent Coordinator - `agent:` commands and selected combined requests can coordinate tools and research.

### Multimodal note
The image layer currently handles image intake and metadata. Full semantic image understanding requires a vision-capable model, so J.O.A.T. does not pretend to describe image contents it cannot actually inspect.

### Example commands
- `list tools`
- `system info`
- `agent: calculate 12 + 8`
- `research Microsoft with sources`


### Local AI runtime build note
The Windows builder uses the pre-built CPU wheel index for `llama-cpp-python` and refuses to compile it from source, so Visual Studio Build Tools are not required for the normal Beta 1 build.
