from setuptools import find_packages, setup


setup(
    # dependency_links=['https://pypi.tuna.tsinghua.edu.cn/simple/flask'],
    name='gctest',
    description='Test Flask Sample',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author='ChenJie',
    author_email='chenjie@galachip.com',
    install_requires=[
        'flask',
        'requests',
    ],
    entry_points = {'console_scripts': [
        'gctest = gctest.test:main',
    ]},
)