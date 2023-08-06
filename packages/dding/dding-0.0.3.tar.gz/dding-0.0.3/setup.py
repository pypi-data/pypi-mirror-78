# -*- coding: utf-8 -*-
import os

import setuptools

setuptools.setup(
    name='dding',
    version='0.0.3',
    keywords='dding',
    description='钉钉自定义机器人.',
    # version = dding.__version__,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dding = dding.cmdline:main',
        ],
    },
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='charlessoft',
    author_email='charlessoft@qq.com',

    url='https://github.com/charlessoft/dding',
    packages=setuptools.find_packages(),
    license='MIT'
)
