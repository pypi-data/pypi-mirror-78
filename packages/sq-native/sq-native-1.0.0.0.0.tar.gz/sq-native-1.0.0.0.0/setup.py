import io
import os

import setuptools

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ABOUT_PATH = os.path.join(
    ROOT_DIR, "sq_native", "__about__.py")
ABOUT = {}  # type: ignore

# Read the version from the source
with io.open(ABOUT_PATH, encoding="utf-8") as f:
    exec(f.read(), ABOUT)

setuptools.setup(version=ABOUT["__version__"])
