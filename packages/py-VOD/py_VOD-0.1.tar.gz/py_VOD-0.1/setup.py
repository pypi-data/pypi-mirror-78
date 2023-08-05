from setuptools import setup

setup(
    name='py_VOD',
    version='0.1',
    packages=['pyvod'],
    url='',
    license='',
    author='jarbasAI',
    author_email='',
    include_package_data=True,
    install_requires=["requests", "bs4", "youtube-dl", "pafy",
                      "json_database", "m3u8"],
    description='video on demand'
)
