from setuptools import setup

def readme():
    with open('dxc_helmet/README.md', 'rt') as file:
        return file.read()

setup(
    name='dxc_helmet',
    version='0.2.2',
    description='Helmet detector',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Jonathan Fernandes',
    license='MIT',
    packages=['dxc_helmet'],
    install_requires=[]
)