import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BatchFiltering",
    version="0.0.2",
    author="Shanfeng Hu",
    author_email="shanfeng.hu1991@gmail.com",
    description="Batch filtering for generative adversarial networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shanfenghu/BatchFiltering",
    py_modules=["BatchFiltering"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
