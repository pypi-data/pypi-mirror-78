"""Setup for the foggy package."""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Tamara Pletzer",
    author_email="tamara.pletzer@gmail.com",
    name='foggy',
    license="MIT",
    description='foggy is a python package for using a CNN to predict fog at airports',
    version='v1.0',
    long_description=README,
    url='https://gitlab.com/tamara.pletzer/foggy',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=['cfgrib', 'pandas', 'numpy', 'pytest-shutil', 'tensorflow', 'matplotlib',
                        'cartopy', 'scipy', 'imblearn', 'scikit-learn'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)