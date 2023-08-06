import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='CipherModule',
     version='1.1',
     scripts=['Cipher.py'],
     author="Navid_d",
     author_email="Navid.dargahi@gmail.com",
     description="A python module to use ciphers easily",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Navid-d/Cipher",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
