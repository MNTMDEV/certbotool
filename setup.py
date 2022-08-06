from setuptools import setup, find_packages

setup(
    name="certbotool",
    version="1.0.0",
    keywords=[],
    description="certbot toolkit",
    long_description="certbot toolkit",
    license="GPL Licence",
    python_requires='>=3.6',

    url="https://www.mntmdev.com",
    author="mntmdev",
    author_email="admin@mntmdev.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'aliyun_python_sdk_alidns',
        'aliyun_python_sdk_core',
        'APScheduler',
        'requests',
        'setuptools'
    ],
    
    scripts=[],
    entry_points={
        'console_scripts': [
         'certbotool = certbotool.cli:main',
         'certbotool-crond = certbotool.crond:main'
        ]
    },
    data_files=[
        ('/etc/certbotool', ['deploy/daemon.json']),
        ('/etc/certbotool/conf.d',
         ['deploy/dnspod.json.template', 'deploy/aliyun.json.template']),
        ('/usr/lib/systemd/system', ['deploy/certbotool-crond.service']),
    ]
)
