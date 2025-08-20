import openpyxl
import pandas as pd
from abc import ABC, abstractmethod

# Classes for Data Writing

class DataWriter(ABC):
    @abstractmethod
    def write_dataframes(self, area: str):
        pass

class ExcelWriter(DataWriter):
    def __init__(self, excel_dict: dict, folder_path: str):
        self.excel_dict = excel_dict
        self.folder_path = folder_path

    def write_dataframes(self):
        try:
            with pd.ExcelWriter(self.folder_path, engine='openpyxl') as writer:
                for sheet_name, df in self.excel_dict.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            return print(f"step: write_excel_sheets, ✅ Excel file '{self.folder_path}' created successfully with {len(self.excel_dict)} sheets.")
        except Exception as e:
            return f"step: write_excel_sheets, ❌ Error creating Excel file '{self.folder_path}': {e}"

