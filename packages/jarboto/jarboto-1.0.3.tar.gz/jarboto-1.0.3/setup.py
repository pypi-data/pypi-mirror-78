from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='jarboto',
    packages=['jarboto'],
    version='1.0.3',
    license='LICENSE.txt',
    description='JARVICE container environment config wrapper for boto3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nimbix, Inc.',
    author_email='noreply@nimbix.net',
    url='https://github.com/nimbix/jarboto',
    download_url='https://github.com/nimbix/jarboto/archive/v1.0.3.tar.gz',
    keywords=['s3', 'boto3', 'JARVICE'],
    install_requires=[
        'boto3',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
