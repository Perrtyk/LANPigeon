import os

def prompt_save(data):
    user_input = input('Save Results?\n(1): Yes\n(2): No\n')
    if user_input == '1':
        save_txt(data)
    else:
        print(f"File not saved.")

def save_txt(data: str) -> None:
    while True:
        file_path = input("Enter the file path to save the file (e.g. C:/logs/my_file.txt): ")
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist. Please create it or choose a different directory.")
        else:
            break

    with open(file_path, 'w') as f:
        f.write(data)

    print(f"File saved to {file_path}")
