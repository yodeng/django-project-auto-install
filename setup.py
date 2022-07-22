import os
import sysconfig

from setuptools import setup, find_packages
from setuptools.extension import Extension

__version__ = "1.0.0"


def listdir(path):
    df = []
    for a, b, c in os.walk(path):
        if os.path.basename(a).startswith("__"):
            continue
        for i in c:
            if i.startswith("__"):
                continue
            p = os.path.join(a, i)
            df.append(p)
    return df


def getExtension():
    extensions = []
    for f in listdir("src"):
        e = Extension(os.path.splitext(f)[0][4:].replace(os.path.sep, "."),
                      [f, ], extra_compile_args=["-O3", ],)
        e.cython_directives = {
            'language_level': sysconfig._PY_VERSION_SHORT_NO_DOT[0]}
        extensions.append(e)
    return extensions


def getdes():
    des = ""
    with open(os.path.join(os.getcwd(), "README.md")) as fi:
        des = fi.read()
    return des


setup(
    name="kpipe",
    version=__version__,
    packages=find_packages(),
    license="BSD",
    install_requires=["Django==2.0.0", "requests", "cython"],
    python_requires='>=3.7, <3.10',
    ext_modules=getExtension(),
    long_description=getdes(),
    long_description_content_type='text/markdown',

    entry_points={
        'console_scripts': [
            'kpipe = kpipe.main:main',
        ]
    }
)
