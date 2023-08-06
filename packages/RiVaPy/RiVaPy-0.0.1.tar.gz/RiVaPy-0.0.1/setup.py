import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RiVaPy",
    version="0.0.1",
    author="RIVACON Team",
    author_email="devops@rivacon.com",
    description="Risk & Valuation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RIVACON/RiVaPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Jupyter",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
    ],
    python_requires='>=3.5',
)
