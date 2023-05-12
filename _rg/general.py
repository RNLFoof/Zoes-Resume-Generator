import importlib
import os
import re
from contextlib import contextmanager

from _rg import definitions


def tex_escape(text: str) -> str:
    text = text.replace("\\", r"\textbackslash")
    text = re.sub(r"([&%$#_{}])", r"\\\1", text)
    text = text.replace("~", r"\textasciitilde")
    text = text.replace("^", r"\textasciicircum")
    return text


def import_all_classes():
    class_path = os.path.join(
        definitions.ROOT_DIR,
        "classes")
    for root, _, class_filenames in os.walk(class_path):
        if "__pycache__" in root:
            continue
        for class_filename in class_filenames:
            class_name, _ = os.path.splitext(class_filename)
            class_path = re.sub(r"^.*?[/\\]_rg[/\\]", "_rg.", root)
            class_path = re.sub(r"[/\\]", ".", class_path)
            importlib.import_module(class_path + "." + class_name)


@contextmanager
def temp_cd(new_path: str):
    original_path = os.getcwd()
    try:
        os.chdir(new_path)
        yield None
    finally:
        os.chdir(original_path)
