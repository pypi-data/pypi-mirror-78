from setuptools import find_packages, setup


setup(
    # dependency_links=['https://pypi.tuna.tsinghua.edu.cn/simple/flask'],
    name='gc_monitor',
    description='Test Flask Sample',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author='ChenJie',
    author_email='chenjie@galachip.com',
    install_requires=[
        'Flask', 'blinker', 'Flask-restful',
        'raven',
        'requests',
    ],
    entry_points = {'console_scripts': [
        'gc_monitor = gc_monitor.monitor:main',
    ]},
)