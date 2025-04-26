### Inference and annotation guis with Streamlit

this is a work in progress

You can run the annotation gui with
```
pip install -r ./requirements.txt
streamlit run binary_classification_review.py
```
opens a web browser where you can annotate audio clips

To use the tool, create a .csv where `file` column contains (relative) path to audio file, `start_time` contains the amount of time from the beginning of the audio file until the clip you want to load, and `annotation` will contain the annotations "yes", "no", "unknown", or empty for un-annotated. 

Then, select the root audio path from which relative paths are defined. 

Annotate each clip by moving through the pages. Remember to click "save". Adjust view settings as needed. 

Post bugs and feature requests to the Issues page on this repo
