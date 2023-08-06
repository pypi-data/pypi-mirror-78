import setuptools

import jocasta

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jocasta',
    version=jocasta.__version__,
    author='Chris Hannam',
    author_email='ch@chrishannam.co.uk',
    description='Fetch sensor data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chrishannam/jocasta',
    packages=setuptools.find_packages(exclude=('tests', 'examples')),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'adafruit-io~=2.4.0',
        'click~=7.1.2',
        'dweepy~=0.3.0',
        'influxdb~=5.3.0',
        'pyserial~=3.4',
        'psutil~=5.7.0',
        'redis~=2.10.6',
        'tabulate~=0.8.7',
    ],
    include_package_data=True,
    entry_points={'console_scripts': ['jocasta=jocasta.collector:main']},
)
