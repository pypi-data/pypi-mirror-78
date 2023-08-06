from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='dpye',
  version='0.0.2',
  description= 'discord.py-easy',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='𝘼𝙦𝙪𝙖 𝙠𝙪𝙣 ⚚',
  author_email='sasha136125429@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['discord', 'discord.py', 'easy', 'discord.py-easy'], 
  packages=find_packages(),
  install_requires=[''] 
)
