import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="symcon", # Replace with your own username
    version="0.0.1",
    author="Thorsten Mueller",
    author_email="MrThorstenM@gmx.net",
    description="Python module for ip-symcon api calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thorstenMueller/symcon-python/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],

)

