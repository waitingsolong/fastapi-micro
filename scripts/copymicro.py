import os
import re
import shutil
import argparse

"""
    Description:
This script copies the microservice folder named `app/microservices/<from_name>` and renames it to `app/microservices/<to_name>`. 
After that, it replaces all occurrences of `<from_name>` with `<to_name>` in the file and directory names, as well as in the contents of all files, respecting case sensitivity.

    How to use:
1. Navigate to the project root.
2. Run the script with the microservice names as arguments:

> python ./scripts/copymicro.py <old_service> <new_service>
"""

def copy_and_rename_service(from_name, to_name):
    source_dir = os.path.join('app', 'microservices', from_name)
    target_dir = os.path.join('app', 'microservices', to_name)

    if not os.path.exists(source_dir):
        print(f"Error: directory {source_dir} not found!")
        return

    shutil.copytree(source_dir, target_dir)
    print(f"Copied directory {source_dir} to {target_dir}")
    
    rename_files_and_dirs(target_dir, from_name, to_name)
    replace_content_in_files(target_dir, from_name, to_name)

def rename_files_and_dirs(root_dir, from_word, to_word):
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Rename files
        for name in files:
            new_name = replace_with_case(name, from_word, to_word)
            if new_name != name:
                os.rename(os.path.join(root, name), os.path.join(root, new_name))

        for name in dirs:
            new_name = replace_with_case(name, from_word, to_word)
            if new_name != name:
                os.rename(os.path.join(root, name), os.path.join(root, new_name))

def replace_content_in_files(root_dir, from_word, to_word):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                new_content = replace_with_case(content, from_word, to_word)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

            except UnicodeDecodeError as e:
                print(f"Could not read file {file_path} due to encoding error: {e}")

def replace_with_case(text, from_word, to_word):
    def case_sensitive_replacer(match):
        word = match.group(0)
        if word.isupper():
            return to_word.upper()
        elif word.islower():
            return to_word.lower()
        elif word.istitle():
            return to_word.capitalize()
        else:
            return to_word
    
    pattern = re.compile(re.escape(from_word), re.IGNORECASE)
    return pattern.sub(case_sensitive_replacer, text)

def create_arg_parser():
    parser = argparse.ArgumentParser(description="Copy and replace words in microservices with case sensitivity.")
    parser.add_argument('from_name', help='Name of the source microservice')
    parser.add_argument('to_name', help='New name for the microservice')
    return parser

if __name__ == '__main__':
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    from_name = args.from_name
    to_name = args.to_name

    copy_and_rename_service(from_name, to_name)
    print("Replacement completed!")
