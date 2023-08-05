import setuptools
import distutils.sysconfig


setuptools.setup(
    name= 'windwardrestapi',
    version = '1.0.5',
    description = 'Python client for the Windward RESTful Engine',
    long_description = '',
    url = 'http://www.windward.net/products/restful/',
    author = 'Windward Studios',
    author_email ='support@windward.net',
    install_requires = ['requests', 'six'],
    packages = setuptools.find_packages(where='src'),
    data_files = [(distutils.sysconfig.get_python_lib(), ["src\windwardrestapi\pytransform\_pytransform.dll"])],
    package_dir = {'': 'src'}
)
