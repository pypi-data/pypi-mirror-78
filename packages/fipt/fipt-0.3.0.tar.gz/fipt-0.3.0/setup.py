# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='fipt',
    version='0.3.0',
    description='A python module to analyze fast impedance tortuosity measurements.',
    long_description=readme,
    long_description_content_type='text/markdown',   
    author='Deniz Bozyigit',
    author_email='deniz195@gmail.com',
    url='https://github.com/deniz195/fipt-analysis',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs', 'examples', 'demo_results')),
    install_requires = ['lmfit>=1.0.0', 'numpy>=1.16.5', 'scipy>=1.3.1',],
    extras_require={
        'dev': [
            'pandas>=0.25.1', 
            'matplotlib>=3.0.0',
            'pytest>=5.2.1',
        ], 
        'full': [
            'pandas>=0.25.1', 
            'matplotlib>=3.0.0',
        ], 
    },    
    classifiers=[
        'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',     
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],    
)
