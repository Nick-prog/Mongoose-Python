import os
import tkinter as tk
import pandas as pd
from pathlib import Path
from tkinter.filedialog import askopenfilename

class CSV:

    def __init__(self):
        self.file_path = None
        self.file_base = None
        self.file_name = None

    def find(self) -> None:
        default = str(os.path.join(Path.home(), "Downloads"))

        tk.Tk().withdraw()
        self.file_path = askopenfilename(initialdir = default, title='Select an CSV file')
        self.file_base, self.file_name = os.path.split(self.file_path)

        print(f'{self.file_name} selected!')

        if not self.file_name.endswith('.csv'):
            raise RuntimeError(f"Can't process {self.file_name[-3:]} files.")
        
    def read(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.file_path)
            print(len(df))
            return df
        except Exception as e:
            print(f'Error occured during reading. {e}')
            raise RuntimeError("Couldn't perform read() method under CSV class.")
        
    def search(self, key: str, value: str, df: pd.DataFrame) -> pd.DataFrame:
        return df[df[key] == value]
        
