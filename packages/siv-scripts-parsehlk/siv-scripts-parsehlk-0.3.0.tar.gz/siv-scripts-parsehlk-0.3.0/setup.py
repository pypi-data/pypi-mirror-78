from setuptools import setup, find_packages


setup(name='siv-scripts-parsehlk',
    version='0.3.0',
    description='Convert HLK test result logs from XML format  to csv format',
    author='Komal',
    author_email='komalpreetx.kaur@intel.com',
    packages=['SivParseHLK'],
    license='Commercial',
    entry_points = {
        'console_scripts': [
            'parse-hlk=siv.scripts.parsehlk.commandline:main'
        ],
    },
    install_requires=[ 'pandas','cryptography','mysql.connector','Fernet','sqlalchemy'])
    
