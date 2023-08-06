from distutils.core import setup
from os import path

setup(
  name = 'swearfilter',
  packages = ['swearfilter'],
  version = '0.4',
  license='MIT',
  description = 'Filter and remove swearwords for your (chat)apps.',
  long_description='We do not want any vulgar language in our chat apps. swearfilter helps you with this, and replaces any swearword with "*"!',
  author = 'Georges Abdulahad',
  author_email = 'ghg.abdulahad@gmail.com',
  url = 'https://github.com/GHGDev-11/swearfilter',
  download_url = 'https://github.com/GHGDev-11/swearfilter/archive/0.4.tar.gz',
  keywords = ['swearwords', 'filtering'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)