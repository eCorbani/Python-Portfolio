from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="corbani-image-processing-package",
    version="0.0.1",
    author="Edson Luis Corbani",
    author_email="corbani.edson@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eCorbani/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)
