import setuptools

setuptools.setup(
    name='pulpatch',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=['setuptools'],
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)