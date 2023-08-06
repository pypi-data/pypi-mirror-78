import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="psorus",
    version="0.1",
    author="Simon Klüttermann",
    author_email="Simon.Kluettermann@gmx.de",
    description="A Graph Autoencoder Library for Tensorflow and Keras",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psorus/grapa/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
	'tensorflow',
	'keras',
	'numpy',
      ],
    download_url='https://github.com/psorus/grapa/archive/0.1.tar.gz',
    
)  
