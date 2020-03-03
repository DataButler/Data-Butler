import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_butler",  # Replace with your own username
    version="0.0.9",
    author="Rahul Madhu",
    author_email="rahul.madhu93@gmail.com",
    description="A data cataloguing package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DataButler/Data-Butler",
    packages=setuptools.find_packages(),
    install_requires=['geonamescache', 'pycountry', 'matplotlib', 'pandas', 'PrettyTable'],
    py_modules=['data_butler'],
    dependency_links=['https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)