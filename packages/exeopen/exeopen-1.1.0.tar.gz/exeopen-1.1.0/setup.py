from setuptools import setup

def readme():
    with open('README.md') as f:
        README=f.read()
    return README

setup(name='exeopen',
    version='1.1.0',
    description='Can open any inbuilt .exe in windows',
    long_description=readme(),
    author='Komal',
    author_email='komalpreetx.kaur@intel.com',
    license='Commercial',
    packages=['exePackage'],
    install_requires=['pandas','cryptography','mysql.connector','Fernet','sqlalchemy'],
    #include_package_data=True,
    #entry_points={"console_scripts":["exeopen=exePackage.cli:main"]},
    zip_safe=False)