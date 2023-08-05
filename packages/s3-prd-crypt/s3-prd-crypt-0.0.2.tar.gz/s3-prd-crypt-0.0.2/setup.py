from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='s3-prd-crypt',
    version='0.0.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=install_requires,
    # metadata to display on PyPI
    author="NAV IKT",
    description="",
    license="MIT",
    keywords="",
    url="https://github.com/navikt"
)
