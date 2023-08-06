from typing import Dict, Optional, overload

def find_dotenv(
    *, variable: Optional[str]=...,
    filename: str=...,
    path: str=...,
    find: bool=...
) -> Optional[str]:
    ...
@overload
def read_dotenv(file_path: None) -> None: ...
@overload
def read_dotenv(
    file_path: str
) -> Optional[Dict[str, str]]:
    ...
def parse(dotenv: str) -> Dict[str, str]: ...
