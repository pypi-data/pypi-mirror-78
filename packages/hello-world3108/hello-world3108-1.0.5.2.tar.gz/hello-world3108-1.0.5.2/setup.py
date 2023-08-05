from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="hello-world3108",
    version="1.0.5.2",
    description="A Python package to get say hello to everyone",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sandmadh/projectWork",
    author="Sandhya Mulay",
    author_email="sandhya.mulay20@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["hello_world_sandhya"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "hello-world-sandhya=hello_world_sandhya.app:say_hello",
        ]
    },
)