import os
import shutil

# Define paths
root_dir = os.getcwd()
csv_folder = os.path.join(root_dir, "csvs")
pdf_folder = os.path.join(root_dir, "graphs")

# Create the csv folder if it doesn't exist
if not os.path.exists(csv_folder):
    os.mkdir(csv_folder)

# Iterate through files in the root directory
for file_name in os.listdir(root_dir):
    file_path = os.path.join(root_dir, file_name)
    # Check if it's a file and ends with .csv or .pdf
    if os.path.isfile(file_path):
        if file_name.endswith(".csv"):
            shutil.move(file_path, os.path.join(csv_folder, file_name))
        elif file_name.endswith(".pdf"):
            shutil.move(file_path, os.path.join(pdf_folder, file_name))

print("Files moved successfully.")
