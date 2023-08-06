import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="har2tavern",
    version="0.0.1",
    author="dongfangtianyu",
    description="Generate yaml test cese from HAR file",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dongfangtianyu/har2tavern",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=["tavern>=1.4.0", "click"],
    entry_points={"console_scripts": ["har2tavern = har2tavern.main:main",],},
)
