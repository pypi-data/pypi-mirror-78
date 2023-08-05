import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PygameLord", 
    version="0.0.3",
    author="LordLynx",
    description="A pakage to help in game development with Pygame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={
        "": ["*.txt", "*.md"],
        "PygameLord": ["Manual.pdf","Examples/*.*", "Examples/*.py", "Examples/Sounds/*.*","Examples/Images/*.*",]
        },
    packages=['PygameLord'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)