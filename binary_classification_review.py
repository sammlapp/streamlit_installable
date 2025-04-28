from pathlib import Path
import streamlit as st
import filedialpy
from opensoundscape import Audio, Spectrogram
import numpy as np
import pandas as pd
import streamlit as st
from pagination import paginator

import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_shortcuts import button

st.set_page_config(layout="wide")


# TODO: click img to play, instead of separate audio widget
# TODO: comment  field for each image
# TODO: field for multi-select of species: user picks species list file, field updates 'labels' column
# TODO: summary stats
# TODO: filter by label

ss = st.session_state
if not "annotation_df" in ss:
    ss.annotation_df = None

if not "active_idx" in ss:
    ss.active_idx = 0  # index of the currently selected clip

if not "n_columns" in ss:
    ss.n_columns = 4

if not "n_samples_per_page" in ss:
    ss.n_samples_per_page = 12

if not "clip_duration" in ss:
    ss.clip_duration = 3  # seconds

if not "pre_look_time" in ss:
    ss.pre_look_time = 0  # seconds

if not "annotation_save_path" in ss:
    ss.annotation_save_path = None

if not "labels_are_up_to_date" in ss:
    ss.labels_are_up_to_date = True

if not "original_annotation_path" in ss:
    ss.original_annotation_path = None

if not "audio_dir" in ss:
    ss.audio_dir = None

if not "bandpass_range" in ss:
    ss.bandpass_range = [0, 10000]

if not "spec_window_size" in ss:
    ss.spec_window_size = 512  # samples

if not "use_bandpass" in ss:
    ss.use_bandpass = None

if "page_number" not in ss:
    ss.page_number = 0

if "full_page_annotation" not in ss:
    ss.full_page_annotation = None

if "image_width" not in ss:
    ss.image_width = 400
if "image_height" not in ss:
    ss.image_height = 200
if "resize_images" not in ss:
    ss.resize_images = False

if "visible_labels" not in ss:
    # only show clips with these annotations
    ss.visible_labels = ["yes", "no", "unknown", None]

option_map = {
    0: ":material/check_circle:",
    1: ":material/cancel:",
    2: ":material/question_mark:",
}

option_map_w_none = {
    0: ":material/check_circle:",
    1: ":material/cancel:",
    2: ":material/question_mark:",
    3: "No selection",
}

option_labels = {
    0: "yes",
    1: "no",
    2: "unknown",
    # 3: "no-selection",
    None: None,
}
label_to_index = {v: k for k, v in option_labels.items()}

option_colormap = {
    "yes": "#c7f0c2",  # green
    "no": "#f0c6c2",  # red
    "unknown": "#f8ee81",  # amber
    None: "#cccccc",  # grey
}


@st.dialog("unsaved changes")
def unsaved_changes():
    st.write("You have unsaved changes to annotations. Save or discard them.")


def load_annotation_df(f=None, discard_changes=False):
    if not ss.labels_are_up_to_date and not discard_changes:
        unsaved_changes()
        return
    if f is None:
        f = filedialpy.openFile()
    if f:
        ss.annotation_df = pd.read_csv(f)
        ss.original_annotation_path = f
        assert (
            "file" in ss.annotation_df.columns
            and "start_time" in ss.annotation_df.columns
        )
        if not "annotation" in ss.annotation_df.columns:
            ss.annotation_df["annotation"] = None

    # change 'nan' to None in annotation column
    ss.annotation_df["annotation"] = ss.annotation_df["annotation"].replace(
        {np.nan: None}
    )
    ss.page_number = 0
    ss.labels_are_up_to_date = True


def save_annotation_df(saveas=False):
    if ss.annotation_df is None:
        st.write("No output scores to save")
        return
    if ss.annotation_save_path is None or saveas:
        ss.annotation_save_path = filedialpy.saveFile()
    if ss.annotation_save_path:
        ss.annotation_df.to_csv(ss.annotation_save_path, index=False)
    ss.labels_are_up_to_date = True


def update_annotation(review_id):
    df_idx = int(review_id.replace("review_clip_", ""))
    ss.annotation_df.at[df_idx, "annotation"] = option_labels[ss[review_id]]
    #     ss[review_id]
    ss.labels_are_up_to_date = False


def show_audio(file, start, end, review_buttons=False, review_id=None, active=False):
    if review_id is not None:
        df_idx = int(review_id.replace("review_clip_", ""))
        label = ss.annotation_df.at[df_idx, "annotation"]
        if label != label:
            label = None  # could use 'no-annotations' and just return label I think
        initial_value = label_to_index[label]

    else:
        initial_value = None
        label = None

    with stylable_container(
        key="c" + review_id,
        css_styles=f"""
            {{
                border: 3px solid {option_colormap[label]}; 
                border-radius: .3rem;
                padding: calc(1em - 1px)
            }}
            """,  # //{"4px" if active else "1px"}
    ):
        with st.container():
            # st.markdown("This is a container with a border.")
            # (border=border, key="c" + review_id):
            a = Audio.from_file(file, offset=start, duration=end - start)
            st.audio(
                a.samples,
                sample_rate=a.sample_rate,
                format="audio/wav",
                start_time=0,
            )
            spec = Spectrogram.from_audio(a, window_samples=ss.spec_window_size)
            if ss.use_bandpass:
                spec = spec.bandpass(*ss.bandpass_range)
            img = spec.to_image(range=[-80, -20], invert=True)

            if ss.resize_images:
                img = img.resize((ss.image_width, ss.image_height))
            st.image(img)

            if review_buttons:
                st.segmented_control(
                    "Annotation",
                    options=option_map.keys(),
                    format_func=lambda option: option_map[option],
                    selection_mode="single",
                    key=review_id,
                    on_change=update_annotation,
                    args=(review_id,),
                    default=initial_value,
                )


# from streamlit_option_menu import option_menu

# if not review_id in ss:
#     ss[review_id] = label  # option_labels[initial_value]
# color = option_colormap[ss[review_id]]
# color
# option_menu(
#     menu_title=None,  # No title
#     options=["yes", "no", "unknown", "no-selection"],
#     icons=[
#         "check2-circle",
#         "x-circle",
#         "question-circle",
#         # no selection:
#         "arrow-counterclockwise",
#     ],  # Bootstrap icons https://www.tutorialrepublic.com/bootstrap-icons-classes.php
#     menu_icon="cast",
#     default_index=initial_value if initial_value is not None else 3,
#     orientation="horizontal",
#     styles={
#         "container": {
#             "padding": "0!important",
#             "background-color": "#fafafa",
#         },
#         "icon": {"color": "black", "font-size": "14px"},
#         "nav-link": {
#             "font-size": "8px",
#             "text-align": "center",
#             "margin": "2px",
#             "--hover-color": "#eee",
#         },
#         "nav-link-selected": {
#             "background-color": color,
#             "color": "black",
#         },
#     },
#     key=review_id,
#     on_change=update_annotation,
# )
# st.rerun()
# ss[review_id] = val


def update_page_annotations(indices):
    indices = list(indices)
    val = (
        None if ss.full_page_annotation == 3 else st.session_state.full_page_annotation
    )
    for idx in indices:
        ss.annotation_df.at[idx, "annotation"] = option_labels[val]
        key = f"review_clip_{idx}"
        ss[key] = val
        ss.labels_are_up_to_date = False
    ss.full_page_annotation = None


def select_audio_dir():
    ss.audio_dir = filedialpy.openDir()


def clear_audio_dir():
    ss.audio_dir = None


def set_label(idx, label):
    """Set the label for the current active index."""
    ss.annotation_df.at[idx, "annotation"] = label
    ss.labels_are_up_to_date = False
    # ss["active_idx"] = idx  # update active index to ensure correct display


from streamlit_shortcuts import button, add_keyboard_shortcuts

with st.sidebar:

    button(
        ":material/folder_open: Load Annotation Table",
        "ctrl+o",
        key="load_annotation_table",
        on_click=load_annotation_df,
        help="CSV file with columns: 'file', 'start_time', 'annotation'",
    )
    st.caption(
        f"size of annotation df: {ss.annotation_df.shape if ss.annotation_df is not None else 'n/a'}"
    )

    cols = st.columns(2)
    with cols[0]:
        st.button(
            ":material/save: Save",
            # "meta+s",
            help="Save updates to the current annotation table",
            key="save_annotation_table",
            on_click=save_annotation_df,
            # hint=True,
        )
    with cols[1]:
        st.button(
            ":material/save_as: Save As",
            # "meta+shift+s",
            help="Save updates to a new file",
            key="save_annotation_table_as",
            on_click=save_annotation_df,
            args=(True,),
            # hint=True,
        )
    st.button(
        ":material/delete: Discard Unsaved Annotations",
        key="discard_annotation_table",
        on_click=load_annotation_df,
        args=(ss.original_annotation_path, True),
    )

    if ss.labels_are_up_to_date:
        st.success("All updates are saved")
    else:
        st.warning("Unsaved changes! use Save/Save As")

    cols = st.columns(2)
    with cols[0]:
        st.button(
            ":material/folder: Root Audio Directory",
            key="root_audio_directory",
            on_click=select_audio_dir,
            help=f"{ss.audio_dir if ss.audio_dir is not None else 'n/a'}",
        )
    with cols[1]:
        st.button(
            "Clear",
            key="clear_root_audio_directory",
            on_click=clear_audio_dir,
        )

    # add keyboard shortcuts for annotation
    # ss["active_idx"]
    # cols = st.columns(4)
    # with cols[0]:
    #     button(
    #         ":material/check_circle:",
    #         "ctrl+1",
    #         on_click=set_label,
    #         args=(ss["active_idx"], "yes"),
    #         help="Annotate current selection as 'yes'",
    #         hint=True,
    #     )
    # with cols[1]:
    #     button(
    #         ":material/cancel:",
    #         "w",
    #         on_click=set_label,
    #         args=(ss["active_idx"], "no"),
    #         help="Annotate current selection as 'no'",
    #         hint=True,
    #     )
    # with cols[2]:
    #     button(
    #         "none",
    #         "shift+f",
    #         on_click=set_label,
    #         args=(ss["active_idx"], None),
    #         help="clear annotation for current selection",
    #         hint=True,
    #     )


def check_first_path():
    # check that audio exists in expected location
    first_audio_path = ss.annotation_df.iloc[0]["file"]
    if ss.audio_dir is not None:
        first_audio_path = Path(ss.audio_dir) / first_audio_path
    return Path(first_audio_path).exists()


if ss.annotation_df is None:
    st.write("No annotation task loaded")
elif not check_first_path():
    st.warning(
        f"""Click Root Audio Directory to specify the location of audio files from which relative paths are specified.
        
        First audio file {ss.annotation_df.iloc[0]['file']} was not found relative to Root Audio Directory ({ss.audio_dir}). 
        
        Examples:
        
        If the first audio file in the annotation table is 'audio/clip1.wav', and 'audio' is a subdirectory in '/home/user/annotation_project',
        then set the Root Audio Directory to '/home/user/annotation_project'. 
        
        If the audio files are given just as the file path, eg `clip1.wav`, the 
        Root Audio Directory should be set to the directory where the audio files are located, eg `/home/user/annotation_project/audio`.
        
        If the audio files in the annotation table are absolute paths (eg /home/user/annotation_project/audio/clip1.wav`), use the `Clear` button to set the Root Audio Directory to None.
        """
    )
else:
    ss.annotation_df["annotation"].unique()
    filtered_annotation_df = ss.annotation_df[
        ss.annotation_df["annotation"].isin(ss.visible_labels)
    ]

    if len(filtered_annotation_df) == 0:
        st.write("No annotations to display with the selected filters.")
    else:
        indices_one_page = paginator(
            "Select a page of model output scores",
            filtered_annotation_df.index,
            items_per_page=ss.n_samples_per_page,
        )
        if not ss["active_idx"] in indices_one_page:
            ss["active_idx"] = indices_one_page[0]

        # with st.sidebar:
        #     ss["active_idx"]

        # apply label to entire page
        cols = st.columns(2)
        with cols[0]:
            st.subheader("Annotation")
        with cols[1]:
            st.segmented_control(
                "Annotation: apply to all on this page",
                options=option_map_w_none.keys(),
                format_func=lambda option: option_map_w_none[option],
                selection_mode="single",
                key="full_page_annotation",
                on_change=update_page_annotations,
                args=(indices_one_page,),
                default=None,
            )

        st.divider()

        columns = st.columns(ss.n_columns)
        for ii, idx in enumerate(indices_one_page):
            row_to_display = ss.annotation_df.loc[idx]
            audio_path = row_to_display["file"]
            if ss.audio_dir is not None:
                audio_path = Path(ss.audio_dir) / audio_path
            with columns[ii % ss.n_columns]:
                start_t = row_to_display["start_time"] - ss.pre_look_time
                show_audio(
                    audio_path,
                    start_t,
                    start_t + ss.clip_duration,
                    review_buttons=True,
                    review_id=f"review_clip_{idx}",
                    active=idx == ss["active_idx"],
                )

# TODO: histograms of scores for selected species

with st.sidebar:
    with st.expander("Settings", expanded=True):
        with st.form("settings_form"):
            st.form_submit_button("Update")

            st.write("Spectrogram settings")
            ss.use_bandpass = st.checkbox(
                "Limit Spectrogram Frequency Range", value=ss.use_bandpass is not None
            )
            ss.bandpass_range = st.slider(
                "Bandpass filter range (Hz)",
                min_value=0,
                max_value=20000,
                value=(0, 20000),
                step=10,
                disabled=not ss.use_bandpass,
            )

            ss.spec_window_size = st.number_input(
                "Spectrogram window samples",
                value=ss.spec_window_size,
                min_value=16,
                max_value=4096,
            )

            ss.resize_images = st.checkbox("Resize images", value=ss.resize_images)
            ss.image_width = st.number_input(
                "Image width (px)", value=ss.image_width, min_value=10, max_value=1000
            )
            ss.image_height = st.number_input(
                "Image height (px)", value=ss.image_height, min_value=10, max_value=1000
            )

            st.write("Display settings")
            ss.n_columns = st.number_input(
                "number of columns", value=ss.n_columns, min_value=1, max_value=20
            )
            ss.n_samples_per_page = st.number_input(
                "number of samples per page",
                value=ss.n_samples_per_page,
                min_value=1,
                max_value=100,
            )
            ss.clip_duration = st.number_input(
                "Audio clip duration (seconds)",
                value=float(ss.clip_duration),
                min_value=0.1,
                max_value=60.0,
            )
            ss.pre_look_time = st.number_input(
                "Pre-look time (seconds)",
                value=float(ss.pre_look_time),
                min_value=0.0,
                max_value=60.0,
            )

    with st.expander("Annotation Summary", expanded=True):
        if ss.annotation_df is not None:
            st.progress(
                ss.annotation_df["annotation"].notna().sum() / len(ss.annotation_df)
            )
            st.write(
                f"Annotated:",
                ss.annotation_df["annotation"].notna().sum(),
                "/",
                len(ss.annotation_df),
            )
            text = []
            for label in option_labels.values():
                if label is None:
                    continue
                count = (ss.annotation_df["annotation"] == label).sum()
                text.extend([label, ": ", count, " "])
            st.write(*text)

        else:
            st.write("No annotations loaded.")

    with st.expander("Filter by Annotation", expanded=True):
        # filter by label
        with st.form("filter_form"):
            ss.visible_labels = st.multiselect(
                "Visible Labels",
                options=option_labels.values(),
                default=ss.visible_labels,
                help="Only show clips with these annotations",
            )
            st.form_submit_button("Apply Filter", type="primary")
