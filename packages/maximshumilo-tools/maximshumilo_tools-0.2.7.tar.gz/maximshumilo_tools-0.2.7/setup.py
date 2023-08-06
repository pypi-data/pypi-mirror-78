from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

requires = [
    'flask~=1.1.2',
    'requests~=2.24.0',
    'marshmallow~=3.7.1',
    'mongoengine~=0.20.0',
    'python-dotenv~=0.14.0',
    'boto3-stubs~=1.14.43.0',
    'boto3~=1.14.43',
    'setuptools~=49.6.0',
    'botocore~=1.17.43'
]

setup(
    name='maximshumilo_tools',
    version='0.2.7',
    packages=['ms_tools', 'ms_tools.flask', 'ms_tools.yandex_cloud'],
    url='https://t.me/MaximShumilo',
    license='',
    author='Maxim Shumilo',
    author_email='shumilo.mk@gmail.com',
    install_requires=requires,
    python_requires='~=3.8',
    include_package_data=True,
    long_description=long_description,
)
