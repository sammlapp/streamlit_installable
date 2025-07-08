# build inference GUI app
# SITE_PACKAGES=$(python -c "import wandb, os; print(os.path.dirname(wandb.__file__))")
# streamlit-desktop-app build bmz_inference_gui.py --name BMZInferenceGUI --pyinstaller-options --onefile --noconfirm --add-data "${SITE_PACKAGES}/vendor:wandb/vendor"

# for building annotation app
# SITE_PACKAGES=$(python -c "import wandb, os; print(os.path.dirname(wandb.__file__))")
streamlit-desktop-app build binary_classification_review.py --name AudioClipReviewer --pyinstaller-options --onefile --noconfirm --recursive-copy-metadata streamlit-extras --recursive-copy-metadata plotly --collect-data plotly
# TODO: packaged app is not using theme from config.toml
# Error: 
#--add-data "${SITE_PACKAGES}/vendor:wandb/vendor"


# building dmg for mac: this helps user install in Applications folder with click-and-drag
# mkdir -p MyApp_DMG
# cp -R dist/MyApp.app MyApp_DMG/
# ln -s /Applications MyApp_DMG/Applications
# This creates a symbolic link to /Applications, so users can drag MyApp.app into Applications.

# Step 3: Create the .dmg with a Background and Custom Layout
# Create a temporary disk image:

# sh
# Copy
# Edit
# hdiutil create -size 100m -fs HFS+ -volname "MyApp" -srcfolder MyApp_DMG -ov MyApp_temp.dmg
# Convert it to a read-only compressed .dmg:

# sh
# Copy
# Edit
# hdiutil convert MyApp_temp.dmg -format UDZO -o MyApp.dmg