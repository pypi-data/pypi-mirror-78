import os
import setuptools

with open('C:\projects\morpholog\README.txt') as readme_file:
    README = readme_file.read()

setuptools.setup(
     name='morpholog',  
     version='1.4',
     license='MIT',
     author="Constantin Werner",
     author_email="const.werner@gmail.com",
     description="Morphological tokenizer for Russian is able to split words into morphemes: prefixes, roots, infixes, suffix and postfixes",
     include_package_data=True,
     long_description=README,
     keywords=['tokenizer', 'morphemes', 'NLP', 'russian'],
     url="https://github.com/constantin50/morpholog",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
