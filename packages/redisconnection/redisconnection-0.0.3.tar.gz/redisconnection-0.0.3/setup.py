from setuptools import setup

setup(
    name='redisconnection',
    packages=['redisconnection'],
    package_dir={'redisconnection': 'src/redisconnection'},
    version='0.0.3',
    license='MIT',
    platforms='cross-platfom, platform-independent',
    description='Redis Connections and Queries Handler',
    long_description='Dependencies: redis',
    author='Yogesh Yadav',
    author_email='yogesh@byprice.com',
    url='https://github.com/ByPrice/redisconnection',
    download_url='https://github.com/ByPrice/redisconnection',
    keywords=['redis', 'redis-queries', 'redis-connection-wrapper'],
    install_requires=[
        'redis==3.4.1', 'python-dotenv==0.12.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
    ],
)
