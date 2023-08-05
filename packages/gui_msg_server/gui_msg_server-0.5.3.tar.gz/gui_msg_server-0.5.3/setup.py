from setuptools import setup, find_packages

setup(
    name='gui_msg_server',
    version='0.5.3',
    description='Python GUI Messenger Server',
    author='Vlad Chekunov',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex',]
    )