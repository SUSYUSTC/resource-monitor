import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="resource-monitor",
    author="Jiace Sun",
    author_email="susyustc@gmail.com",
    description="Monitor and plot CPU, Memory, GPU, GRAM usage of python program",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SUSYUSTC/resource-monitor",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["matplotlib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
