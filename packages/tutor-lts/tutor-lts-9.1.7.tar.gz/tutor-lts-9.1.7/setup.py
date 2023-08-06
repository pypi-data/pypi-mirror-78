import io
import os
from setuptools import setup, Extension, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), "rt", encoding="utf8") as f:
    readme = f.read()

about = {}
with io.open(
    os.path.join(here, "tutorlts", "__about__.py"), "rt", encoding="utf-8",
) as f:
    exec(f.read(), about)  # pylint: disable=exec-used


def ext_modules():
    if os.path.exists(os.path.join(here, "tutorlts", "lts.pyx")):
        from Cython.Build import cythonize  # pylint: disable=import-outside-toplevel

        return cythonize(
            ["tutorlts/lts.pyx"],
            compiler_directives={"language_level": 3, "emit_code_comments": False},
        )
    return [Extension("tutorlts.lts", ["tutorlts/lts.c"])]


setup(
    name="tutor-lts",
    version=about["__version__"],
    url="https://overhang.io/tutor/lts",
    project_urls={
        "Homepage": "https://overhang.io/tutor/lts",
    },
    author="Overhang.IO",
    description="Tutor LTS management plugin",
    long_description=readme,
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.5",
    install_requires=["tutor-openedx>=3.9.0", "pycryptodome", "appdirs"],
    entry_points={"tutor.plugin.v0": ["lts = tutorlts.plugin"]},
    ext_modules=ext_modules(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
