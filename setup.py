from setuptools import find_packages
from setuptools import setup

setup(
    name='data-center',
    version='1.0.0',
    packages=find_packages(),
    license='MIT',
    author='shuyukeji dev team',
    description='qilin data center',
    entry_points={
        'console_scripts': [
            # 'test = engine.test:main'
        ]
    }
)
