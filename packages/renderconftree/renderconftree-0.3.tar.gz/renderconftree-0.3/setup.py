from setuptools import setup, find_packages

setup(name='renderconftree',
    version = '0.3',
    description="Config tree readerer.",
    long_description="Write configurations files with values that contain python expressions that can refer to other configuration parameters.",
    author='C.D. Clark III',
    url='https://github.com/CD3/renderconfigtree',
    license="MIT License",
    platforms=["any"],
    packages=find_packages(),
    install_requires=['pyyaml','fspathtree>=0.3'],
    entry_points='''
      [console_scripts]
      render-config-file=renderconftree.scripts.render_config_file:main
    ''',
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
    python_requires='>=3.4',
    )
