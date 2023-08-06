from setuptools import setup

setup(
    name='sqlconnection',
    packages=['sqlconnection'],
    package_dir={'sqlconnection': 'src/sqlconnection'},
    version='0.2.2',
    license='MIT',
    platforms='cross-platfom, platform-independent',
    description='SQL Connections and Queries Handler',
    author='Yogesh Yadav',
    author_email='yogesh@byprice.com',
    url='https://github.com/ByPrice/sqlconnection',
    download_url='https://github.com/ByPrice/sqlconnection',
    keywords=['postgres', 'psql', 'postgresql'],
    install_requires=[
        'psycopg2-binary>=2.8.4', 'python-dotenv>=0.10.3"'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
    ],
)
