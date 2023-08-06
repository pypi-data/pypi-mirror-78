import os
import setuptools


def get_requirements():
    cwd = os.path.dirname(os.path.realpath(__file__))
    req_file = os.path.join(cwd, 'requirements.txt')
    with open(req_file, 'r') as fp:
        reqs = fp.read().splitlines()

    for i, pkg in enumerate(reqs):
        if '-e ' in pkg:
            git_link = pkg.split()[-1]
            pkg_name = pkg.split('=')[-1]
            reqs[i] = f'{pkg_name} @ {git_link}'

    return reqs


def get_version():
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(cwd, 'guardcam', '__init__.py'), 'r') as fp:
        lines = fp.read().splitlines()

    for line in lines:
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

    raise Exception('Could not retrieve version number')


setuptools.setup(
    name="guardcam",
    version=get_version(),
    author="Milogav",
    description="Visual movement detector in python with remote notifications",
    url='https://github.com/Milogav/GuardCam',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',

    install_requires=[get_requirements()],
    entry_points={
            "console_scripts": [
                "guardcam-start-detector = apps.start_detector:main",
            ]
        }
)
