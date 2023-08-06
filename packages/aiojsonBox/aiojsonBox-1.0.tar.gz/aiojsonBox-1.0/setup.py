from setuptools import setup

requirements = [
    "aiohttp",
    "aiofiles"
]

setup(
    name='aiojsonBox',
    version='1.0',
    description="lib for jsonbox.io",
    author="dark0ghost",
    url='https://github.com/dark0ghost/jsonbox-python',
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    classifiers=[
        'Natural Language :: English',
    ],
)