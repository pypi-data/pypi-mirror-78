from setuptools import setup

from spplot import meta 


with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name=meta.NAME,
  version=meta.VERSION,
  description=meta.DESC,
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/adzierzanowski/spplot',
  author='Aleksander Dzierżanowski',
  author_email='a.dzierzanowski1@gmail.com',
  license='MIT',
  packages=['spplot'],
  python_requires='>=3.6',
  include_package_data=True,
  install_requires=['drawille', 'pyserial'],
  entry_points={
    'console_scripts': [
      'spplot = spplot.__main__:main'
    ]
  },
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Embedded Systems',
    'Topic :: Terminals :: Serial',
    'Topic :: Utilities'
  ],
  zip_safe=False
)
