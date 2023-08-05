import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySimpleTest", # Replace with your own username
    version="1.0.2",
    author="Bruce Wang",
    author_email="binghuiwang0726@gmail.com",
    description="A very simple python test framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Time-Coder/PySimpleTest",
    packages=setuptools.find_packages(),
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "Operating System :: Windows",
    # ],
    install_requires=[
        'PySimpleGUI',
        'pywin32',
        'pyttsx3'
    ],
    python_requires='>=3.6'
)