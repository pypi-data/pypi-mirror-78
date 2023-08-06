import setuptools
import os

here = os.path.dirname(os.path.realpath(__file__))

requirements = []
if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as f:
        requirements = [line.strip() for line in f]

info = {}
with open(os.path.join(here, "multi_realsense_manager", "__info__.py")) as f:
    exec(f.read(), info)

setuptools.setup(
    name=info["__title__"],
    version=info["__version__"],
    author=info["__author__"],
    author_email=info["__author_email__"],
    description=info["__description__"],
    long_description='Examples and detials are in "multi_realsense_manager/multi_realsense_manager.py#L248-301"',
    long_description_content_type="text/markdown",
    url=info["__url__"],
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
