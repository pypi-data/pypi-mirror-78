from setuptools import setup, find_packages

setup(
  name = 'buildcage',
  packages=find_packages(),
  include_package_data=True,
  version = '0.0.3',
  description = 'Python script to build cage optimimized by OPLS-AA',
  author = 'Kexin Zhang',
  author_email = 'zhangkx2@shanghaitech.edu.cn',
  license='MIT',
  keywords = ['computational chemistry', 'force fields', 'molecular dynamics',"pore materials"],
  classifiers = [
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        ],
  install_requires=['numpy',"networkx"],
  entry_points={
        'console_scripts': [
            'buildcage=buildcage.buildcage:main',
        ],
    },

)
