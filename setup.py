import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

with open("VERSION.txt", "r") as v:
    version = v.read().strip()

PACKAGE_NAME = "mbt_tboxtester"

setuptools.setup(
    name=PACKAGE_NAME,
    version=version,
    author="Michele Romani",
    author_email="michele.romani@mybraintech.com",
    description="Tool to test the serial messages sent using MBT TriggerBox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbt-michele-r/Research.TriggerBoxTester",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 license",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
