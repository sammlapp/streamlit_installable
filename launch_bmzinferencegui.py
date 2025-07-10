import os
import sys
from streamlit_desktop_app.core import start_desktop_app

## Launch BMZInferenceGUI in desktop window mode

icon = None  # Optional icon path, can be set to None if not needed
script_path = "./bmz_inference_gui.py"
streamlit_options = {}  # configure streamlit here

if not os.path.exists(script_path):
    sys.exit(f"Error: The script '{script_path}' does not exist.")

script_path = os.path.abspath(script_path)
if icon:
    icon = os.path.abspath(icon)

# To avoid font cache generation
if "MPLCONFIGDIR" in os.environ:
    del os.environ["MPLCONFIGDIR"]

if __name__ == "__main__":
    if "_PYI_SPLASH_IPC" in os.environ:
        import pyi_splash
        pyi_splash.close()
    start_desktop_app(script_path, title="BMZ Inference GUI", options=streamlit_options)