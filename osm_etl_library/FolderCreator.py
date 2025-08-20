import os
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Border, Side
from abc import ABC, abstractmethod

# Abstract Base Class for Folder Creation

class FolderCreator(ABC):
    @abstractmethod
    def create_folder(self):
        pass
# Concrete Implementations of FolderCreator

class AttributionFolderCreator(FolderCreator):

    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        # self.folder_names = folder_names
    
    def create_folder(self):

        folders = ["reports", "charts"]
        
        for folder in folders:
            folder_path = fr"{self.folder_path}\{folder}"
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder created: {folder_path}")

class ChartFolderCreator(FolderCreator):

    def __init__(self, folder_path: str ,areas: list):
        self.folder_path = folder_path
        self.areas = areas

    def create_folder(self):
        for area in self.areas:
            folder_path = fr"{self.folder_path}\charts\{area}"
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder created: {folder_path}")

class FolderCreatorPipeline:
    def __init__(self, folder_creators: list):
        self.folder_creators = folder_creators

    def create_folders(self):
        for creator in self.folder_creators:
            creator.create_folder()