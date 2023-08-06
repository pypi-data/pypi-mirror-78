from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ormucoq2comparator',
  version='1.0',
  description='A basic comparator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Yihe Zhang',
  author_email='yihe@msn.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='comparator', 
  packages=find_packages(),
  install_requires=[''] 
)