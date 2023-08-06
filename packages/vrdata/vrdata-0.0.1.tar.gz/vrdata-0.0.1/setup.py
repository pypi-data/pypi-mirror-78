import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vrdata", 
    version="0.0.1",
    author="Faruk Hammoud",
    author_email="farukhammoud@student-cs.fr",
    description="Enables connection to Viarezo Data Services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://vrdata.viarezo.fr",
    packages=setuptools.find_packages(),
	install_requires=[
   'requests',
   'json',
   'getpass',
   'pymongo'
	],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
