from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="hello-world3108",
    author="iNeuron",
    author_email="",
    maintainer="iNeuron",
    maintainer_email="support@iNeuron.com",
    description="Python API for Automated ML",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="http://autoneuro.ml",
    project_urls={
        "Documentation": "https://github.com/nabeelfahmi12/AutoNeuro-Documentation",
        "Source Code": "https://github.com/viratsagar/Autoneuro",
    },
    version="1.0.5.2.5",
    # Make sure to remove stale files such as the egg-info before updating this:
    # https://stackoverflow.com/a/26547314
    package_data={"": ["*.txt", "*.md"]},
    python_requires=">=3.6",
    install_requires=[
        "liac-arff>=2.4.0",
        "xmltodict",
        "requests",
        "scikit-learn>=0.18",
        "python-dateutil",  # Installed through pandas anyway.
        "pandas>=1.0.0",
        "scipy>=0.13.3",
        "numpy>=1.6.2",
    ],
    extras_require={
        "test": [
            "matplotlib",
            "pytest",
            "pytest-xdist",
        ],
        "examples": [
            "matplotlib",
            "jupyter",
            "notebook",
            "ipykernel",
            "seaborn",
        ],
        "examples_unix": ["fanova",],
    },
    classifiers=[
        "Intended Audience :: Developers ",
        'Intended Audience :: End Users/Desktop',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development ",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",

    ],
)