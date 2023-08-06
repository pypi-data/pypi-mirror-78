from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='termsnake',
    version='0.0.1',
    description='A Python package that creates a nice snake game for your terminal.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Python3-8/termsnake',
    author='Pranav Balaji Pooruli',
    author_email='pranav.pooruli@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['termsnake'],
    include_package_data=True,
    install_requires=find_packages(),
    entry_points={
        'console_scripts': [
            'snake=termsnake.snake:main',
        ]
    },
)
