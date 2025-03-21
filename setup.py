from setuptools import setup, find_packages

setup(
    name="expense-tracker-cli",
    version="0.1.0",
    author="TNorth1",
    description="A command-line expense tracker",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TNorth1/expense-tracker-cli",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.3",
        "rich>=13.9.4",
        "platformdirs>=4.3.6",
        "XlsxWriter>=3.2.0",
        "pydantic>=2.0.0"
    ],
    entry_points={
        "console_scripts": ["exptrack=src.main:main"],
    },
    python_requires=">=3.9",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="expense tracker CLI",
    include_package_data=True,
)
