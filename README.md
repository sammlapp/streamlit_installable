### Grid-based Annotation GUI with Streamlit

this is a work in progress. The repo has some code for running machine learning models, but currently we focus the documentation on the clip annotation tool. 

Although we've experimented with creating desktop installable apps, for now we only support running the streamlit app via a python environment. 

### Installation and set up: running streamlit from a python enviornment 
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


# Usage instructions

Note: make sure you set "length" in the settings panel to match the duration of audio clips you wish to review. 

## 1. create csv to store annotations (`file`, `start_time`, `annotation` columns)
Create a .csv where `file` column contains (relative) path to audio file, `start_time` contains the amount of time from the beginning of the audio file until the clip you want to load, and `annotation` will contain the annotations "yes", "no", "unknown", or empty for un-annotated. 

2. Specify the location of your audio files, if needed
For the `file` column of the annotations csv, absolute (full) paths are allowed, and relative paths will be resolved relative to the "Audio Dir". "Audio Dir" is automatically set to the location of the annotation .csv file when one is loaded, but you can manually specify another location. For example, if your clip /full/path/to/folder/file.wav is listed in the `file` column of the annotation csv as "folder/file.wav", you should set "full/path/to/" as the Audio Dir. 

## 4. Adjust settings 
You'll need to click Apply settings for the selected settings to take effect! 

In the left panel, scroll down to Settings where you can choose to
- show or hide a "comments" text field for each clip. These are saved in a column called "comments" in the csv file.
- show or hide the file name of each clip
- enable/disable keyboard shortcuts (the green text in the left panel indicates the keyboard shortcuts; "meta" means ctrl key on Windows or Command key on Mac)
- enable/disable auto-save. When enabled, annotations are saved on each PAGE CHANGE (not each time you click an annotation button on a single clip)

Visual display settings:
- specify the number of rows and columns of clips to display in the grid layout (we find it is most efficient to set up a view where you can see all of the clips on a page without scrolling; the exact number depends on your monitor size and how large you want the visual displays to be; keep in mind that you can collapse the left panel to maximize display space)
- crop spectrograms to a desired frequency range
- change the contrast and brightness/darkness of spectrograms by adjusting the "dB limits": the range of decibel values, where the low value is white and the high value is black
- color scale of spectrograms
- optionally, resize spectrograms to a fixed pixel size
- change the duration of audio clips that are loaded
- optionally, load audio clips starting some number of seconds _before_ the `start_time` value to see extra audio using the "Pre-look" setting


## 5. Saving annotations
Then specify a new or existing .csv file in which to save the annotations.

If auto-save setting is checked, your annotations are saved to this file every time you change pages or use the "ctrl/cmd + S" shortcut. 

If auto-save setting is unchecked, your annotations are only saved when you use the Save or ctrl/cmd+S shortcut. 

Save As prompts you to specify a new .csv file in which to save the current annotations, then continues using this new file for future "Save" actions

The Discard button resets the annotations to the last-saved version. 

## 6. Annotate
Annotate each clip by moving through the pages. Remember to click "save". Adjust view settings as needed. 

There are two strategies for efficient annotation: keyboard and mouse (or some blend)
- For mouse-based annotation, click on the relevant button to annotate each clip. Use the dropdown menu or buttons in the left panel to go to the previous or next page. 
- for keyboard-based annotation, use j and k keys to change the "selected clip" (which is shown with a thicker border), use the a=Yes, b=No, d=Uncertain, f=unlabeled shortcuts to annotate the selected clip, and use the p=Previous page and n=Next page shortcuts to change pages.
- there is not currently a shortcut to play the audio of the selected clip in this rendition of the app
- you can use the Full-page annotation buttons in the left panel or the shortcuts (shift+A/S/D/F) to annotate all clips on the current page with the same label


## Filtering:
You can filter to only display clips with certain labels. For instance, filter to only the clips labeled positive, or clips labeled uncertain, or clips without labels (None), or some combination. Note that as soon as you annotate a clip, the label will change and the clip may "disappear" because it is filtered out of the display. 

## Summary
The annotation summary in the left panel shows a progress bar for the clips with annotations, and the count of each annotation type

## Shortcuts
- navigate between pages with p (previous) and n (next) (no modifier keys)
- activate the previous or next clip

## Bugs and feature requests
Post bugs and feature requests to the Issues page on this repo
