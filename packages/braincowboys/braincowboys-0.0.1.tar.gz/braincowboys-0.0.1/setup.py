from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="braincowboys",
    version="0.0.1",
    author="Eyal Gal",
    author_email="eyalgl@gmail.com",
    description="Brain Computations in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=[],
    url="https://github.com/gialdetti/braincowboys/",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    # package_data={'datasets': ['braincowboys/resources/*']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)

