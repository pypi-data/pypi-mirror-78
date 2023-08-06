from setuptools import setup, find_packages


setup(name='SivScriptsParsehlk',
    version='1.2.0',
    description='Convert HLK test result logs from XML format  to csv format',
    author='Komal',
    author_email='komalpreetx.kaur@intel.com',
    license='Commercial',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points = {
        'console_scripts': [
            'parse-hlk=siv.scripts.parsehlk.commandline:main'
        ],
    },
    install_requires=['pandas', 'xmltodict','sqlalchemy','Fernet','cryptography','mysql.connector'],
    tests_requires=['pytest', 'pytest-cov'],
    zip_safe=False)
