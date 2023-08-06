from setuptools import setup, find_packages

__version__ = "0.1.1"

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='wifimeter',
      version=__version__,
      description='Wifi Electricity Meter',
      url='https://github.com/deddiag/wifimeter.git',
      license='MIT License',
      packages=find_packages(),
      entry_points='''
        [console_scripts]
        wifimeter=wifimeter.cli:cli
      ''',
      install_requires=[
          'pytz',
          'click',
          'timeout_decorator'
      ],
      python_requires='>=2.7',
      long_description_content_type="text/markdown",
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
)
