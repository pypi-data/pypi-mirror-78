from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='input_simple',
    version='1.0.0',
    description='A Library for facilitating input operations',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Saikat Sahana',
    author_email='saikatsahana91@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='inputmodule input inputsimple',
    packages=find_packages(),
    install_requires=['xlrd', 'exrex']
)
