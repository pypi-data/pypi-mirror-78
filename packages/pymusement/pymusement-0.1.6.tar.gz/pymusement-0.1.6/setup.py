from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='pymusement',
      version='0.1.6',
      description='A python package and CLI to get wait times for rides at various theme parks',
      url='https://github.com/TheMarauder95/PyMusement',
      author='Josh Shrawder',
      author_email="joshshrawder@gmail.com",
      license='MIT',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      include_package_data=True,
      download_url = 'https://github.com/TheMarauder95/pymusement/archive/0.1.0.tar.gz',
      install_requires=[
        'requests',
        'beautifulsoup4',
        'python-dateutil',
        'Click'
      ],
      entry_points= {
          'console_scripts' :
                'pymusement = pymusement.scripts.cli:cli'
                    }, 
      zip_safe=False)



