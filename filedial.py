import filedialpy

# great utility for opening files!
# use as callback function for Streamlit button

f = filedialpy.openFile()  # Open a single file (return a string)
f = filedialpy.openFiles()  # Open multiple files (return a list of strings)
f = filedialpy.openDir()  # Open a directory (return a string)
