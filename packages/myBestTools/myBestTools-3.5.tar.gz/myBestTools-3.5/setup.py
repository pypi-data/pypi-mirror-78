from setuptools import setup
import os, sys

version = 0
if os.path.exists('dist'):
    from tools.myBestTools import *

    tool = Tool("local")
    version = max([float(tool.get_re(i, "myBestTools-(.*?)\.tar", False)) for i in os.listdir('dist')])
    version += 0.1
    version = round(version,1)

setup(name='myBestTools',
      version=version,
      description='my Tool',
      author='Du HongYu',
      author_email='837058201@qq.com',
      packages=['tools'],
      zip_safe=False,
      install_requires=[
          'pika',
          'requests',
          'lxml',
          'redis',
          'pymysql',
          'wrapt'
      ]
      )

message = 'twine upload dist/myBestTools-%s.tar.gz\nduhongyu\nduhongyu123A' % version
print(message)
print('pip install myBestTools -i https://pypi.org/project --upgrade --user')
