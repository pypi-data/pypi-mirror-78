import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TextToolkit",
    version="0.0.3",
    author="Wesley Laurence",
    author_email="wesleylaurencetech@gmail.com",
    description="Toolkit for mining unstructured text information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesleyLaurence/TextToolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
		'pandas',
		'matplotlib',
		'seaborn'
	]
)