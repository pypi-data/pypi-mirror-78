from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pythonsemver',
  version='0.0.1',
  description='this is used for redirection by lambda edge and for semantic-versioning',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/chakri1998/npmsemver',  
  author='Devarakonda Chakradhar',
  author_email='chakradhar1998@outlook.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='semantic-versioning, lambda edge url redirection', 
  packages=find_packages(),
  install_requires=[''] 
)
