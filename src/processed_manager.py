import os

class ProcessedManager:
    def __init__(self, processed_file: str):
        self.processed_file = processed_file

    # Function to check if an id has been processed
    def already_processed_id(self, id: int) -> bool:
        if not os.path.exists(self.processed_file):
            return False  # If the file does not exist, the id has not been processed

        with open(self.processed_file, 'r') as f:
            processed_ids = f.read().splitlines()  # Read and split the file into a list of ids

        return str(id) in processed_ids

    # Function to add an id to the "processed" file
    def save_id(self, id: int):
        with open(self.processed_file, 'a') as f:
            f.write(str(id) + '\n')
