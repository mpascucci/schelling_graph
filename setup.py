from setuptools import setup, find_packages

setup(
    name="shelling_graph",
    version="0.1.0",
    author="Marco Pascucci",
    author_email="marpas.paris@gmail.com",
    description="Simulateions of Schelling's segregation model on graphs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mpascucci/schelling_graph",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "matplotlib",
        "numpy",
        "termcolor",
        "mayavi>=0.6",
    ],
)