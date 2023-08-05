from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = []
    for line in f.readlines():
        line = line.strip()
        line and install_requires.append(line)

setup(
    name='digger',
    version='0.0.1',
    author='Lee',
    author_email='294622946@qq.com',
    url='https://github.com/Dog-Egg/digger',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['digger = digger.script:main']
    }
)
