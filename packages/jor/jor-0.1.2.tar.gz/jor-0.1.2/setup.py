from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='jor',
      version='0.1.2',
      author='Markus Helmer',
      url='https://github.com/mdhelmer/jor',
      description='Lighweight JOb Runner for reproducible research results in HPC environments',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
      ],
      python_requires='>=3.6',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[],
      zip_safe=True,
      include_package_data=True,
      scripts=['bin/jor'],
)
