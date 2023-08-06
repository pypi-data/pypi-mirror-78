import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rcl',
    version='0.1.2',
    author='Ben Ryder',
    author_email='dev@benryder.me',
    description='A simple command line wrapper for rclone focused on easy folder syncing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['rclone', 'rclone-wrapper'],
    url='https://github.com/Ben-Ryder/rcl',
    download_url='https://github.com/Ben-Ryder/rcl/archive/v0.1.2.tar.gz',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'toml'
    ],
    entry_points='''
        [console_scripts]
        rcl=rcl.main:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    license='GPLV3',
)
