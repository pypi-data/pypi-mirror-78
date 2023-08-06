from setuptools import setup

setup(name='fmqlutils',
      description = 'FMQL Utilities',
      long_description = """A Python framework and set of executables for caching datasets from FileMan systems using FMQL. Includes support for data analysis and modeling""",
      version='3.4',
      install_requires = [
          'rpcutils>=3.0',
          'python-dateutil'
          # 'pytz>=2019.1'
      ],
      python_requires='>=3.4, <4',
      classifiers = ["Development Status :: 4 - Beta", "Programming Language :: Python :: 3"],
      url='http://github.com/Caregraf/fmqlutils',
      license='Apache License, Version 2.0',
      keywords='VistA,FileMan,CHCS,FMQL',
      package_dir = {'fmqlutils': ''},
      packages = ['fmqlutils', 'fmqlutils.cacher', 'fmqlutils.typer', 'fmqlutils.reporter'],
      entry_points = {
          'console_scripts': ['fmqlcacher=fmqlutils.cacher.cacher:main', 'fmqlv2er=fmqlutils.cacher.v2er:main', 'fmqlrecacher=fmqlutils.cacher.recacher:main', 'fmqlcachehealth=fmqlutils.reporter.cacheHealthReporter:main', 'fmqltyper=fmqlutils.typer.reduceReportType:main']
      }
)
