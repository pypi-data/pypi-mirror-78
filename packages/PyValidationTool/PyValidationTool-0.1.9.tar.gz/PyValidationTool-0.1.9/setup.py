import platform

from setuptools import setup, find_packages
from codecs import open
from os import path

VERSION = '0.1.9'

requires = []

# system = platform.system()
# if system == 'Darwin':
#     requires.append('pyobjc-framework-Quartz')
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='PyValidationTool',     # package name
    version=VERSION,        # version
    description='Common validation method in China.',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='common validation tool 身份证手机号码中文名字验证类',   # 关键字
    author='Simon_He',     # 作者
    author_email='simonheusing@gmail.com',
    maintainer='Simon_He',
    maintainer_email='simonheusing@gmail.com',
    url='https://github.com/Wuliaodewo/PyValidationTool', # 项目目录
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=requires,      # 上层依赖的包
)