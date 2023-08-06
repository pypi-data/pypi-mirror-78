from setuptools import setup

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(
    name='matgen',
    version='0.1.1',
    author='junruoyu-zheng',
    author_email='zhengjry@outlook.com',
    url='https://gitee.com/junruoyu-zheng/mat-gen',
    description=u'Fast matrix generation in python, including python style and matlab style support',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['matgen'],
    install_requires=['numpy'],
    entry_points={},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)