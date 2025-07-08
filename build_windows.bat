@echo off
REM Build script for Windows
streamlit-desktop-app build binary_classification_review.py --name AudioClipReviewer --pyinstaller-options --onefile --noconfirm --recursive-copy-metadata streamlit-extras --recursive-copy-metadata plotly --collect-data plotly