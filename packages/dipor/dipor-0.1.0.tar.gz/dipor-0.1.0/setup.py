from setuptools import setup, find_packages

setup(
    name='dipor',
    version='0.1.0',
    description='Static Site Generator written in Python for ease of processes',
    url="https://github.com/vidhibagadia/dipor",
    author="Vidh Bagadia",
    author_email="vidbagadia@gmail.com",
    license="MIT",
    keywords='static site generator staticsitegenerator python jinja',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['markdown==3.2.2', 'Jinja2==2.11.2', 'html5print==0.1.2', 'Pygments==2.6.1'],
    entry_points={
        'console_scripts': [
            'dipor=dipor.cmd.start:main'
        ]
    })