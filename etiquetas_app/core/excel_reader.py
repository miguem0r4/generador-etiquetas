from pathlib import Path
from typing import List

import pandas as pd


def read_names(excel_path: Path) -> List[str]:
    df = pd.read_excel(str(excel_path), header=None)
    nombres = df.iloc[:, 0].dropna().tolist()
    return [str(n) for n in nombres]
