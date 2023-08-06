from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mavenn',
      version='0.15',
      description='package for inferring models of sequence-function relationships from mave datasets',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
      keywords='mave, mpa',
      url='http://mavenn.readthedocs.io',
      author='Ammar Tareen, Justin B. Kinney',
      author_email='tareen@cshl.edu',
      license='MIT',
      packages=['mavenn'],
      include_package_data=True,
      install_requires=[
        'numpy',
		'matplotlib',
		'pandas',
		'tensorflow',
		'sklearn',
		'scikit-learn>=0.22',
		'logomaker',
		'seaborn'
      ],
      zip_safe=False)