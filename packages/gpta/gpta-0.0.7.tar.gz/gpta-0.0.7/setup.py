from setuptools import setup

setup(name='gpta',
      version='0.0.7',
      description='gpta',
      long_description='gpta',
      author='Guo Xiaoyong',
      author_email='guo.xiaoyong@gmail.com',
      url='https://github.com/guoxiaoyong/gpta',
      packages=['gpta'],
      install_requires=['qflow', 'pandas'],
      setup_requires=['qflow', 'pandas'],
      include_package_data=True,
      entry_points={
         'console_scripts': [
             'gdump=gpta.dump:main',
             'gplot=gpta.plot:main',
             'gcat=gpta.cat:main',
         ],
      },
)
