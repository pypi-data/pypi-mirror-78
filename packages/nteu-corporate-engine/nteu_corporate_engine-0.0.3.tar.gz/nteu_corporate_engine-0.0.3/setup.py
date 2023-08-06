from setuptools import setup

setup(
    name='nteu_corporate_engine',
    version='0.0.3',
    description='NTEU corporate translation engine',
    url='https://github.com/Pangeamt/nteu-corporate-engine',
    author='PangeaMT',
    author_email='a.cerda@pangeanic.es',
    license='MIT',
    packages=[
        'nteu_corporate_engine'
    ],
    install_requires=[
        "aiohttp==3.6.2",
        "click",
        "pangeamt-nlp==0.4.39",
        "PyYAML",
        "uvloop"
    ],
    zip_safe=False
)
