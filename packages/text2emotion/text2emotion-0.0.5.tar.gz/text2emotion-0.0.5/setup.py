from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding="utf8") as f:
        README = f.read()
    return README


setup(
    name="text2emotion",
    version="0.0.5",
    description="Detecting emotions behind the text, text2emotion package will help you to understand the emotions in textual meassages.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/aman2656/text2emotion-library",
    author="text2emotion Team",
    author_email="Text2Emotion@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    packages=find_packages(),
    install_requires=["nltk", "emoji>=0.6.0"],
    include_package_data=True
)
