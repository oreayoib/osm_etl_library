# Classes for Data Loading

import pandas as pd
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load_dataframes(self, area: str):
        pass

class CSVLoader(DataLoader):

    def __init__(self, folder_path: str,  area: str):
        self.folder_path = folder_path
        self.area = area

    def load_dataframes(self):
        
        tables = []

        area = self.area.replace(' ', '')

        tables = [f"{area}_points", f"{area}_lines", f"{area}_areas", f"{area}_collections"]

        final_df = pd.DataFrame() 

        for table in tables:

            try:

               df = pd.read_csv(fr"{self.folder_path}\tables\{table}.csv", low_memory=False)

            except FileNotFoundError:
                print(f"File {table}.csv not found in {self.folder_path}. Skipping this table.")
                continue

            if not df.empty and not final_df.empty:
                final_df = pd.concat([final_df, df], ignore_index=True)
            elif  final_df.empty:
                final_df = df
            
            if not final_df.empty:
                final_df['unknown'] = None
                final_df.loc[final_df['feature_type'] == "unknown", 'unknown'] = "unknown"

        return final_df
        