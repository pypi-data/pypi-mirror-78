import setuptools

def readme():
	with open("README.md") as f:
		README = f.read()
	return README

setuptools.setup(
    name="loanpy", # Replace with your own username
    version="0.0.5",
    author="Viktor Martinovic",
    author_email="viktor.martinovic@hotmail.com",
    description="framework for detecting old loanwords",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/martino-vic/Framework-for-computer-aided-borrowing-detection",
    license="Creative Commons Attribution 4.0 International",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: OS Independent",
    ],
    packages=["loanpy"],
    include_package_data=True,
    install_requires=["pandas","lingpy","nltk","epitran","gensim"],
    python_requires='>=3.6',
)