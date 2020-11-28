from distutils.core import setup
from setuptools import find_packages

INSTALL_REQUIREMENTS = [
    
]

TEST_REQUIRES = [
    'pytest',    
]

PACKAGES = find_packages('src')

if __name__ == '__main__':
    setup(
        name='python-mongodb-runner',
        version='0.1.0',
        package_dir={'': 'src'},
        packages=PACKAGES,
        url='',
        license='',
        author='Alexander Balkum',
        author_email='',
        description='Mongodb Instance Runner',
        install_requires=INSTALL_REQUIREMENTS,
        test_require=TEST_REQUIRES,
        include_package_data=True
    )