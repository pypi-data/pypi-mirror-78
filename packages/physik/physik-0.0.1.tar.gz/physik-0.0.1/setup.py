from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='physik',
    version='0.0.1',
    description='A python physics library',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Miguel Barroso',
    author_email='miguelferreirabarroso6@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='physics',
    packages=find_packages(),
    install_requires=['']
)
