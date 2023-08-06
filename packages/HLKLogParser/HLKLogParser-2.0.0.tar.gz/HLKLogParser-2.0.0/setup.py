from setuptools import setup

def readme():
    with open('README.md') as f:
        README=f.read()
    return README

setup(name='HLKLogParser',
    version='2.0.0',
    description='Conversion of HLK Xml format logs to CSV format',
    long_description=readme(),
    author='Komal',
    author_email='komalpreetx.kaur@intel.com',
    license='Commercial',
    packages=['XMLtoCSV'],
    install_requires=['pandas','cryptography','mysql.connector','Fernet','sqlalchemy'],
    #include_package_data=True,
    zip_safe=False)