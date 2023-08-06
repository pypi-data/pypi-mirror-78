import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))

try:
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except TypeError:
    with open(path.join(this_directory, 'README.md')) as f:
        long_description = f.read()

setuptools.setup(
    name="RabbitMQ Test Tool",
    version="1.1.3",
    description="A simple test script to test a RabbitMQ cluster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nicolas Bock",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "rabbitmq-test-tool = rabbitmqtesttool.main:main",
        ],
    }
)
