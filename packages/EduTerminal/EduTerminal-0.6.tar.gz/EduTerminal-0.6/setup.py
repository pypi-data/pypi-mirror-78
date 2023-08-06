from setuptools import setup, find_packages

setup(name='EduTerminal',
      version='0.6',
      description='Edu tatar library for open-sources projects ',
      packages=['EduTerminal'],
      install_requires=[
          'requests',
          'bs4',
          'wheel'],
      author_email='alphaste08@gmail.com',
      zip_safe=False)