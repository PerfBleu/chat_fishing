from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class config:
    host = 'localhost'
    port = '8000'



sqlitestring = f'sqlite:///{Path(os.path.dirname(__file__)).parent / "fish.db"}'