from setuptools import find_packages, setup


def get_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="NotionX",
    version="0.1",
    url="https://github.com/JezaChen/mumu-notion",
    author="Jeza Chen",
    author_email="jezachen@163.com",
    description="NotionX, a simple, easy-to-use Notion client, is based on the official SDK modification",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("*examples", "*examples.*")),
    python_requires=">=3.7, <4",
    install_requires=[
        "httpx >= 0.23.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
    package_data={"notionx": ["py.typed"]},
)
