import os

file_path = "rir_model.pkl"

# Check if the file exists first
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} has been deleted.")
else:
    print(f"{file_path} does not exist.")
