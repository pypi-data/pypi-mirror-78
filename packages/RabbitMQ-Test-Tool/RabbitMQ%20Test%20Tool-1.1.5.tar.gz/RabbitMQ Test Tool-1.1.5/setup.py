import setuptools
import subprocess
from os import path


def long_description():
    this_directory = path.abspath(path.dirname(__file__))
    try:
        with open(path.join(this_directory, 'README.md'),
                  encoding='utf-8') as f:
            return f.read()
    except TypeError:
        with open(path.join(this_directory, 'README.md')) as f:
            return f.read()


def get_version():
    try:
        git = subprocess.run(['git', 'describe', '--tags'],
                             stdout=subprocess.PIPE, universal_newlines=True)
        full_version = git.stdout.strip()[1:]
    except AttributeError:
        git = subprocess.Popen(['git', 'describe', '--tags'],
                               stdout=subprocess.PIPE, universal_newlines=True)
        stdout_raw, stderr_raw = git.communicate()
        git.wait()
        full_version = stdout_raw.strip()[1:]
    except Exception:
        print("Cannot read version")
        raise

    try:
        git = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'],
                             stdout=subprocess.PIPE, universal_newlines=True)
        abbreviated_version = git.stdout.strip()[1:]
    except AttributeError:
        git = subprocess.Popen(['git', 'describe', '--tags', '--abbrev=0'],
                               stdout=subprocess.PIPE, universal_newlines=True)
        stdout_raw, stderr_raw = git.communicate()
        git.wait()
        abbreviated_version = stdout_raw.strip()[1:]
    except Exception:
        print("Cannot read version")
        raise

    local_version = full_version.replace(abbreviated_version, '')

    if len(local_version) > 0:
        version = (abbreviated_version + '+'
                   + local_version[1:].replace('-', '.'))
    else:
        version = abbreviated_version

    return version


setuptools.setup(
    name="RabbitMQ Test Tool",
    version=get_version(),
    description="A simple test script to test a RabbitMQ cluster",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Nicolas Bock",
    packages=['rabbitmqtesttool'],
    entry_points={
        "console_scripts": [
            "rabbitmq-test-tool = rabbitmqtesttool.main:main",
        ],
    }
)
