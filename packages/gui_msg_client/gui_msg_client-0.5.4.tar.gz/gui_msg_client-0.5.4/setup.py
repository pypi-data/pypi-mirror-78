from setuptools import setup, find_packages

setup(
    name='gui_msg_client',
    version='0.5.4',
    description='Python GUI Messenger Client',
    author='Vlad Chekunov',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex',]
    )