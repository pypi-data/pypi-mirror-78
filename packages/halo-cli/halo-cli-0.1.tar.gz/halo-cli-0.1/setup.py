from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/halolib-0.13.8.tar.gz -r pypitest
# twine upload dist/halo_bian-0.13.8.tar.gz -r pypi
setup(
    name='halo-cli',
    version='0.1',
    #py_modules=['bob'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==7.1.2','PyInquirer==1.0.3','rich==5.1.2','pyfiglet==0.8post1','colorama==0.4.3','termcolor==1.1.0','six==1.15.0',
        'pip==19.0.3','jsonschema==2.6.0',
        'flex==6.14.1','swagger-py-codegen==0.4.0'
    ],
    entry_points='''
        [console_scripts]
        hlo=halocli.main:start
    ''',
    python_requires='>=3.6',
)