from setuptools import setup

setup(name='fmqlreports',
      description = 'FMQL Reports',
      long_description = """A Python framework and set of executables for generating specific reports on VistA data cached using FMQL and reduced using fmqlutils.""",
      version='0.57',
      install_requires = [
          'fmqlutils>=3.0',
          'python-dateutil'
      ],
      # install_requires=["pytz"], - problem OSX
      classifiers = ["Development Status :: 4 - Beta", "Programming Language :: Python :: 3"],
      url='http://github.com/Caregraf',
      license='Apache License, Version 2.0',
      keywords='VistA,FileMan,CHCS,FMQL,Caregraf',
      package_dir = {'fmqlreports': ''},
      packages = ['fmqlreports', 'fmqlreports.basics', 'fmqlreports.patient', 'fmqlreports.user', 'fmqlreports.imaging', 'fmqlreports.visit', 'fmqlreports.ifc', 'fmqlreports.directory'],
      entry_points = {
      }
)
