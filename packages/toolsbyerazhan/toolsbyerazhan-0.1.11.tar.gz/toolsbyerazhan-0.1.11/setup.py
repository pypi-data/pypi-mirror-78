from setuptools import setup, find_packages

setup(
    name = "toolsbyerazhan",
    version = "0.1.11",

    keywords = ( "toolsbyerazhan"),
    description = "some useful tools",
    long_description = "some useful common tools",
    license = "MIT Licence",

    url = "https://github.com/erazhan/CommonTools",
    author = "erazhan",
    author_email = "erazhan@163.com",
    
    python_requires='>=3.7.1',#不需要太高的版本
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["tensorflow==2.2.0"]
)
