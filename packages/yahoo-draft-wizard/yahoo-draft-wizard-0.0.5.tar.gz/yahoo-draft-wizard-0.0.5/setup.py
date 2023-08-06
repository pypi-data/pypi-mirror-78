import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yahoo-draft-wizard", # Replace with your own username
    version="0.0.5",
    author="James Whiting",
    author_email="jlwhiting@outlook.com",
    description="Dynamically recommends picks for your yahoo fantasy football draft",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jwaggie14/yahoo-draft-wizard",
    install_requires=[
        'numpy',
        'pandas',
        'yahoo_oauth'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
