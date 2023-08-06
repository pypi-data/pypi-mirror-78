from setuptools import setup

setup(name='qflow',
      version='0.0.6',
      description='qflow package for personal use',
      long_description='qflow package for personal use',
      author='Guo Xiaoyong',
      author_email='guo.xiaoyong@gmail.com',
      url='https://github.com/guoxiaoyong/qflow',
      packages=['qflow'],
      install_requires=['recordclass'],
      setup_requires=['recordclass'],
      include_package_data=True,
      entry_points={
         'console_scripts': ['qflow=qflow.__main__:main'],
      },
)
