import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="chatbotmaker",
    version="0.0.11",
    author="Dominique MICHEL",
    author_email="dominique.michel@epita.fr",
    description="This package automates the process of bot creation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dominique57/ChatBotMaker",
    packages=setuptools.find_packages(exclude=["*.tests"]),
    install_requires=[
        'sqlalchemy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
