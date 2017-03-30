from setuptools import setup, find_packages

setup(name='pydere',
      version='0.1',
      description='',
      url='',
      author='Narumi',
      author_email='',
      license='',
      packages=find_packages(),
      install_requires=['requests', 'beautifulsoup4', 'wget'],
      zip_safe=False,
      entry_points={'console_scripts': ['pydere=pydere.pydere:main']})
