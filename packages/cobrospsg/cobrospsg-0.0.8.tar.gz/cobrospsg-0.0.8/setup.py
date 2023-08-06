from setuptools import setup, find_packages
 
classifiers = [
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cobrospsg',
  version='0.0.8',
  description='Paquete con funciones para modelos predictivos de Cobros de Prosegur',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Martin Ehman',
  author_email='martinehman90@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='aws,prosegur', 
  packages=find_packages(),
  install_requires=[''] 
)