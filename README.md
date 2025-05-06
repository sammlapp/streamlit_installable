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
Not available yet

### Usage
To use the tool, create a .csv where `file` column contains (relative) path to audio file, `start_time` contains the amount of time from the beginning of the audio file until the clip you want to load, and `annotation` will contain the annotations "yes", "no", "unknown", or empty for un-annotated. 

Then, select the root audio path from which relative paths are defined. 

Annotate each clip by moving through the pages. Remember to click "save". Adjust view settings as needed. 

Post bugs and feature requests to the Issues page on this repo
