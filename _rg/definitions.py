import os

ROOT_DIR = os.path.abspath(os.path.split(__file__)[0])  # https://stackoverflow.com/a/25389715
IMAGE_DIR = os.path.join(ROOT_DIR, "images")
TEST_OUTPUT_DIR = os.path.join(ROOT_DIR, "../tests/out")
