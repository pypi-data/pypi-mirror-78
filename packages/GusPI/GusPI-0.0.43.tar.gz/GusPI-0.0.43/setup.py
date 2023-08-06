import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GusPI",
    version="0.0.43",
    author="Randy Geszvain",
    author_email="randy.geszvain@gmail.com",
    description="This open-source python package aims to provide statistical support in supply chain analytics and finance/accounting analytics. We welcome everyone to use this python package for personal or professional projects. Please let us know any feedback you have. We'd love to improve the package and add feature enhancements to benefit researchers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ygeszvain/GusPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
