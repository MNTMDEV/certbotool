from setuptools import setup, find_packages

setup(
    name="certbotool",
    version="1.0.0",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'aliyun_python_sdk_alidns',
        'aliyun_python_sdk_core',
        'apscheduler',
        'requests',
        'setuptools',
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
