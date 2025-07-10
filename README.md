### Inference and annotation guis with Streamlit

this is a work in progress

### Installation and set up: running streamlit from a python enviornment (for developers)
We strongly recommend using python enviornments. For instance, install [mini-conda](https://www.anaconda.com/docs/getting-started/miniconda/main) if you don't have a Python environment manager, then create a new environment:

```
conda create -n streamlit python=3.10
conda activate streamlit
```

Then install the packages needed to use this tool
```
git clone https://github.com/sammlapp/streamlit_installable.git
cd streamlit_installable
pip install -r ./requirements.txt
```

You can now run the annotation gui with
```
streamlit run binary_classification_review.py
```
opens a web browser where you can annotate audio clips

### Installing desktop programs

**Desktop installers are available for Windows, macOS, and Linux:**

1. **Download the installer** for your platform from the [Releases](../../releases) page:
   - Windows: `AudioClipReviewer-1.0-Windows-x86_64.exe` or `BMZInferenceGUI-1.0-Windows-x86_64.exe`
   - macOS: `AudioClipReviewer-1.0-MacOSX-x86_64.pkg` or `BMZInferenceGUI-1.0-MacOSX-x86_64.pkg`
   - Linux: `AudioClipReviewer-1.0-Linux-x86_64.sh` or `BMZInferenceGUI-1.0-Linux-x86_64.sh`

2. **Run the installer**:
   - **Windows**: Double-click the `.exe` file and follow the installation wizard
   - **macOS**: Double-click the `.pkg` file and follow the installation wizard
   - **Linux**: Run `bash AudioClipReviewer-1.0-Linux-x86_64.sh` (or BMZ version) in terminal

3. **Launch the application**:
   - **Windows**: Find "AudioClipReviewer" or "BMZ Inference GUI" in your Start Menu
   - **macOS**: Find the app in your Applications folder
   - **Linux**: Launch from Applications menu or run `audioclipreviewer` / `bmzinferencegui` in terminal

**Note**: The installers are self-contained and include all necessary dependencies (Python, PyTorch, etc.). No additional setup is required.

### Usage
To use the tool, create a .csv where `file` column contains (relative) path to audio file, `start_time` contains the amount of time from the beginning of the audio file until the clip you want to load, and `annotation` will contain the annotations "yes", "no", "unknown", or empty for un-annotated. 

Then, select the root audio path from which relative paths are defined. 

Annotate each clip by moving through the pages. Remember to click "save". Adjust view settings as needed. 

Post bugs and feature requests to the Issues page on this repo
