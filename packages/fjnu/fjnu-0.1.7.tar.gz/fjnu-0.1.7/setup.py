# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

setup(
    name='fjnu',  # 包的名字
    author='listener',  # 作者
    version='0.1.7',  # 版本号
    license='MIT',

    description='通过封装web api接口制作而成',  # 描述
    long_description='''long description''',
    author_email='765934517@qq.com',  # 你的邮箱**
    # url='https://blog.csdn.net/xc_zhou',  # 可以写github上的地址，或者其他地址
    # 包内需要引用的文件夹
    # packages=setuptools.find_packages(exclude=['url2io',]),
    packages=["fjnu"],
    # keywords='NLP,tokenizing,Chinese word segementation',
    # package_dir={'jieba':'jieba'},
    # package_data={'jieba':['*.*','finalseg/*','analyse/*','posseg/*']},

    # 依赖包
    install_requires=[
        'requests >= 2.19.1',
    ],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        # 'Operating System :: Microsoft'  # 你的操作系统  OS Independent      Microsoft
        # 'Intended Audience :: listener',
        # 'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=True,
)