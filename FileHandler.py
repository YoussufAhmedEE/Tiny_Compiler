import os
class FileHandler:
    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        except IOError as e:
            raise IOError(f"An error occurred while reading the file: {e}")
        
    def write_file(file_path:str, file_name:str,content):
        try:
            output_file_name = "output_" + os.path.basename(file_name)
            with open(output_file_name, 'w') as f:
                print(content, file=f)
            print(f"File {output_file_name} successfully created!")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        except IOError as e:
            raise IOError(f"An error occurred while reading the file: {e}")
        
        
    