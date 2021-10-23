import setuptools

setuptools.setup(
    name='sbident',
    version='0.1',
    author='Ben Engebreth',
    author_email='ben.engebreth@gmail.com',
    description='A Python library for querying the JPL Small Body Identification API',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/bengebre/sbident',
    project_urls = {'Issues': 'https://github.com/bengebre/sbident/issues'},
    license='MIT',
    packages=['sbident'],
    install_requires=['requests', 'pandas', 'astropy'],
)
