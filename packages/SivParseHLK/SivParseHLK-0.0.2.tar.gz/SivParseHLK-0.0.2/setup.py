from setuptools import setup, find_packages


setup(name='SivParseHLK',
    version='0.0.2',
    description='Convert HLK test result logs from XML format  to csv format',
    author='Komal',
    author_email='komalpreetx.kaur@intel.com',
    license='Commercial',
    packages=['SivParseHLK'],
    install_reuires=['pandas','cryptography','mysql.connector','Fernet','sqlalchemy'],
    zip_safe=False)