from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    # Mandatory and initial setup
    name='vbelts',
    version='0.0.2',
    description='Utilities for v-belt dimensioning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    author='Glademir Karpinski Junior, Hector Balke Nodari',
    author_email='gkarpinskijr@gmail.com, hectornodari@gmail.com',

    # Secondary setup
    url='https://github.com/traumatic-monotype/vbelts',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        ],
    extras_require = {"dev": ["pytest>=6.0.1","check-manifest>=0.42",]},
    
)
