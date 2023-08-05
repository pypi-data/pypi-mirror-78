from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='python-pysh',
    version='0.0.2',
    description='A Python package that mimics the Oh-My-ZSH shell. This package creates a colorful ZSH prompt.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Python3-8/python-pysh',
    author='Pranav Balaji Pooruli',
    author_email='pranav.pooruli@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    packages=['pysh'],
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pysh=pysh.pysh:main',
        ]
    },
)
