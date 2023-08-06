from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

setup(
    name='fatcat',
    version='0.0.1',
    description='FatCat Hosting Package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://fatcat.bike',
    author='INfoUpgraders',
    author_email="infoupgraders@gmail.com",
    license='MIT',
    classifiers=classifiers,
    keywords='fatcat',
    packages=find_packages(),
    install_requires=['requests']
)
