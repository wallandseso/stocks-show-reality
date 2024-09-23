import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="stocks-show-reality",
    version="0.0.1",
    py_modules=["stocks-show-reality"],
    author="wallandseso",
    author_email="wallandseso@gmail.com",
    description="A simple package to show stock infos reality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wallandseso/stocks-show-reality",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests', 'pandas', 'web3_calculator'
    ],
    project_urls={
        'Source': "https://github.com/wallandseso/stocks-show-reality",
    }
)