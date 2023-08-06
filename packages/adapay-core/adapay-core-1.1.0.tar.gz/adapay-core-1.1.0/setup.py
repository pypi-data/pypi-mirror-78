from setuptools import setup
import io
import re

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('adapay_core/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='adapay-core',
    version=version,
    author="adapay developers",
    author_email="hi@adapay.tech",
    install_requires=['requests>=2.22.0',
                      'pycryptodome>=3.8.2',
                      'paho-mqtt>=1.4.0',
                      'fishbase>=1.1.15'],
    url='https://www.adapay.tech/',
    description='common utils of adapay sdk',
    long_description=readme,
    packages=['adapay_core'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]

)
