from setuptools import find_packages
from setuptools import setup

setup(
    name='data_center',
    version='1.0.0',
    packages=find_packages(),
    license='MIT',
    author='yepeng dev team',
    description='qilin data center',
    entry_points={
        'console_scripts': [
            # 'tamc-service = src.message.rabbitmq_listener:main',
            # 'tamc-run-strategy = src.quant.run_mm_strategy:main',
            # 'tamc-analyze-log = src.scheduler.app:main',
            # 'tamc-mock-remote = src.message.mock_remote_server:main'
        ]
    }
)
