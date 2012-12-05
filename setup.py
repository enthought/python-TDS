from setuptools import setup


setup(
    name='python-TDS',
    version='0.0.1',
    author='Parth Buch',
    author_email='parth.buch.115@gmail.com',
    description='A Python library for accessing the TaxDataSystems',
    license='MIT',
    install_requires=[
        'suds>=0.4',
    ],
    packages=[
        'TDS',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Topic :: Office/Business :: Financial',
        'Topic :: Internet :: WWW/HTTP',
    ],
)