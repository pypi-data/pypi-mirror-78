from setuptools import setup
import setuptools

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='l_pdseries_2_l_dfs',
      version='0.1',
      description='Creating list of series to list of dfs',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Visualization'
      ],
      keywords='list of Pandas series to list of pandas data frame',
      url='http://github.com/YogenderPalChandra/pandasSeries2pandasDf',
      author='Yogender Pal Chandra',
      python_requires=">=3.6",
      author_email='yogender027mae@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      zip_safe=False)

