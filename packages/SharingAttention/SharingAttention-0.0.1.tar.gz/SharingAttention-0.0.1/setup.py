import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SharingAttention",
    version="0.0.1",
    author="Shanfeng Hu",
    author_email="shanfeng.hu1991@gmail.com",
    description="Sharing attention in generative adversarial networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shanfenghu/SharingAttention",
    py_modules=["models", "operators", "train", "utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
