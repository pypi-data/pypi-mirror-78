from setuptools import setup, find_packages

setup(
   name='Sthefreak',
   version='0.0.4',
   description='A Data Science toolkit',
   author='Suyash Dixit',
   author_email='ar-suyash.dixit@rakuten.com',
   packages=find_packages(),  #same as name
   install_requires=['bs4','requests'], #external packages as dependencies
)