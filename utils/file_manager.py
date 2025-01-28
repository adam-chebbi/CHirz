import os
import shutil

# File Manager Utility
class FileManager:
    def __init__(self, base_upload_dir):
        self.base_upload_dir = base_upload_dir
        self.cv_dir = os.path.join(base_upload_dir, 'cvs')
        self.jd_dir = os.path.join(base_upload_dir, 'jds')
        self.ensure_directories()

    def ensure_directories(self):
        os.makedirs(self.cv_dir, exist_ok=True)
        os.makedirs(self.jd_dir, exist_ok=True)

    def save_file(self, file, file_type):
        if file_type == 'cv':
            save_path = self.cv_dir
        elif file_type == 'jd':
            save_path = self.jd_dir
        else:
            raise ValueError("Invalid file type. Use 'cv' or 'jd'.")

        file_path = os.path.join(save_path, file.filename)
        file.save(file_path)
        return file_path

    def list_files(self, file_type):
        if file_type == 'cv':
            directory = self.cv_dir
        elif file_type == 'jd':
            directory = self.jd_dir
        else:
            raise ValueError("Invalid file type. Use 'cv' or 'jd'.")

        return os.listdir(directory)

    def delete_file(self, file_name, file_type):
        if file_type == 'cv':
            directory = self.cv_dir
        elif file_type == 'jd':
            directory = self.jd_dir
        else:
            raise ValueError("Invalid file type. Use 'cv' or 'jd'.")

        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def rename_file(self, old_name, new_name, file_type):
        if file_type == 'cv':
            directory = self.cv_dir
        elif file_type == 'jd':
            directory = self.jd_dir
        else:
            raise ValueError("Invalid file type. Use 'cv' or 'jd'.")

        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            return new_path
        return None

    def clear_all_files(self, file_type):
        if file_type == 'cv':
            directory = self.cv_dir
        elif file_type == 'jd':
            directory = self.jd_dir
        else:
            raise ValueError("Invalid file type. Use 'cv' or 'jd'.")

        shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
