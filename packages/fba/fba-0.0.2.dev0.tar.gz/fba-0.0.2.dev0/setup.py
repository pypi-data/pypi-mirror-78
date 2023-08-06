from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='fba',
    version='0.0.2dev',
    author='JD',
    description='Tools for feature barcoding analyses',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jlduan/fba',
    packages=find_packages(),
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    # ],
    python_requires='>=3.6',
    install_requires=[
        'biopython',
        'regex',
        'pysam',
        'pandas',
        'numpy',
        'umi_tools'
    ],
    entry_points={
        'console_scripts': ['fba=fba.__main__:main'],
    }
)
