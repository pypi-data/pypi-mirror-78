from setuptools import find_packages, setup

setup(
    name='yqgscheduler',
    version='0.1.0',
    author="xhgao",
    author_email="xhgao@yangqianguan.com",
    description="分布式scheduler的executor部分的python实现",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)