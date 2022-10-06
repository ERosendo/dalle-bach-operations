import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PICTURE_PATH = os.getenv('ROOT_PATH')
PICTURE_FOLDER = os.getenv('PICTURE_FOLDER')

def check_folder_distribution():
    picture_path = Path(PICTURE_PATH)
    picture_folder = picture_path / PICTURE_FOLDER
   
    if not picture_folder.exists():
        picture_folder.mkdir()

    original_folder = picture_folder / 'originals'
    if not original_folder.exists():
        original_folder.mkdir()

    first_generation_folder = picture_folder / 'first_generation'
    if not first_generation_folder.exists():
        first_generation_folder.mkdir()

    second_generation_folder = picture_folder / 'second_generation'
    if not second_generation_folder.exists():
        second_generation_folder.mkdir()
    
    third_generation_folder = picture_folder / 'third_generation'
    if not third_generation_folder.exists():
        third_generation_folder.mkdir()
        

def get_path_by_generation(generation:int)->str:
    picture_path = Path(PICTURE_PATH)
    picture_folder = picture_path / PICTURE_FOLDER
    
    match generation:
        case 1:
            return picture_folder / 'first_generation'
        case 2:
            return picture_folder / 'second_generation'
        case 3:
            return picture_folder / 'third_generation'
        case _:
            return picture_folder / 'originals'
        
        
def get_folder_by_generation(generation:int)->str:
    
    match generation:
        case 1:
            return 'first_generation'
        case 2:
            return 'second_generation'
        case 3:
            return 'third_generation'
        case _:
            return 'originals'
        