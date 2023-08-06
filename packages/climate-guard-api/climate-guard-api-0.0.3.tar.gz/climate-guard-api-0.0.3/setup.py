import setuptools


def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


packages = setuptools.find_packages(exclude=['tests*'])
requirements = requirements()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="climate-guard-api",  # Replace with your own username
    version="0.0.3",
    author="oberdev",
    author_email="qovalski@gmail.com",
    description="Climate Guard Api for boxes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
