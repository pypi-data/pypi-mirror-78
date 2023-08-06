from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'icdMapping',        
  packages = ['icdMapping'],  
  version = '0.11',      
  license='MIT',        
  description = 'Identify diseases from ICD code list',   
  include_package_data=True,
  author = 'Xiaoqian Jiang, Luyao Chen',                  
  author_email = 'your.email@domain.com',      
  url = 'https://github.com/Luyaochen1/icdMapping',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Luyaochen1/icdMapping/archive/v0.11.tar.gz',     
  keywords = ['icd 9', 'icd 10', 'diseases'],   
  install_requires=[            # I get to this in a second
          'pandas',
        ],
  classifiers=[
    'Development Status :: 3 - Alpha',       
    'Intended Audience :: Developers',       
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7', 
    'Programming Language :: Python :: 3.8',
  ],
)
