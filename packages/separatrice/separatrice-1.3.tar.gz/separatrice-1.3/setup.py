import os
import setuptools

with open('C:\projects\separatrice\README.txt') as readme_file:
    README = readme_file.read()

setuptools.setup(
     name='separatrice',  
     version='1.3',
     license='MIT',
     author="Constantin Werner",
     author_email="const.werner@gmail.com",
     description="Separatrice is able to separate a text into sentences and a sentence into clauses (russian)",
     include_package_data=True,
     long_description=README,
     keywords=['tokenizer', 'splitter', 'NLP', 'russian','clauses'],
     url="https://github.com/constantin50/splitter",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
