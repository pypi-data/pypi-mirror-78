import setuptools

setuptools.setup(
    name="neural-transfer-CarlosH", # Replace with your own username
    version="0.0.1",
    author="CarlosH",
    author_email="iwishtherewasone@gmail.com",
    description="A small example package",
    install_requires=["torch", "torchvision",
                      "argparse", "PIL", "matplotlib"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning"
        ],
    package_data={
        ## All the images need to be in jpg format
        "": ["*.jpg"] },
    python_requires='>=3.6',
)
