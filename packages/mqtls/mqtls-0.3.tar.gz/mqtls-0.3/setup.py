from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mqtls',
    packages=['mqtls'],
    version='0.3',
    license='wtfpl',
    description='MqTLS client for python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Efrén Boyarizo',
    author_email='efren@boyarizo.es',
    url='https://github.com/efrenbg1/mqtls-python',
    download_url='https://github.com/efrenbg1/mqtls-python/archive/0.3.tar.gz',
    keywords=['MqTLS', 'gobroker', 'client'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools'
    ],
)
