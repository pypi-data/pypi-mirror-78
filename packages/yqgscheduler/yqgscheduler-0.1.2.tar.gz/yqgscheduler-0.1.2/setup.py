from setuptools import find_packages, setup

setup(
    name='yqgscheduler',
    version='0.1.2',
    author="xhgao",
    author_email="xhgao@yangqianguan.com",
    description="分布式scheduler的executor部分的python实现",
    packages=find_packages(exclude=["unittest"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)