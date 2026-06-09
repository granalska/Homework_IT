import argparse
import asyncio
import os
import shutil
import logging

#налаштування логування помилок
logging.basicConfig(filename="errors.log", level=logging.ERROR)

#функція, яка читає всі файли в папці
async def read_all_files(source_folder, target_folder):
    for current_folder, subfolders, files in os.walk(source_folder):
        for file_name in files:
            full_file_path = os.path.join(current_folder, file_name)
            await copy_one_file(full_file_path, target_folder)

#функція копіювання одного файлу
async def copy_one_file(file_path, target_folder):
    try:
        file_extension = file_path.split(".")[-1]
        new_folder_path = os.path.join(target_folder, file_extension)
        os.makedirs(new_folder_path, exist_ok=True)
        shutil.copy(file_path, new_folder_path)

    except Exception as error:
        logging.error(str(error))

#головна функція програми
async def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--source_folder", default="source")
    argument_parser.add_argument("--target_folder", default="target")
    arguments = argument_parser.parse_args()

    await read_all_files(arguments.source_folder, arguments.target_folder)

#запуск програми
if __name__ == "__main__":
    asyncio.run(main())