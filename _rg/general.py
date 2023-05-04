import importlib
import os
import re


def tex_escape(text: str) -> str:
    text = text.replace("\\", r"\textbackslash")
    text = re.sub(r"([&%$#_{}])", r"\\\1", text)
    text = text.replace("~", r"\textasciitilde")
    text = text.replace("^", r"\textasciicircum")
    return text


def import_all_classes():
    class_path = os.path.join(
        os.path.split(__file__)[0],
        "classes")
    for class_filename in os.listdir(class_path):
        class_name, _ = os.path.splitext(class_filename)
        importlib.import_module("_rg.classes." + class_name)
