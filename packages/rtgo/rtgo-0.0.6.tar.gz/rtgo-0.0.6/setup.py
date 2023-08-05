import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rtgo",
    version="0.0.6",
    author="Thomas Rowlands, Emma Croot",
    author_email="thomas.s.rowlands@gmail.com, ec339@le.ac.uk",
    description="Quick and simple multithreading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Thomas-Rowlands/multithread",
    packages=setuptools.find_packages(),
    license='LICENCE.txt',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
