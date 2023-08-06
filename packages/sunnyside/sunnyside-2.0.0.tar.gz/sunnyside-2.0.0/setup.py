import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sunnyside",
    version="2.0.0",
    author="Jun Qi Li",
    author_email="JunQi.Li63@myhunter.cuny.com",
    description="Mini python wrapper for OpenWeather API's one call, current and forecast5 services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junqili259/Sunnyside/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
