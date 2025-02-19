import os

def is_valid_memory_dump(file_path):
    return file_path.lower().endswith(".vmem")

def is_file_exists(file_path):
    return os.path.isfile(file_path)
