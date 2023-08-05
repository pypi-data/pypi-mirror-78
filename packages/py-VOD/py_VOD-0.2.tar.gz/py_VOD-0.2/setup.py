from setuptools import setup

setup(
    name='py_VOD',
    version='0.2',
    packages=['pyvod'],
    url='https://github.com/OpenJarbas/pyvod/',
    license='Apache',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    include_package_data=True,
    install_requires=["requests", "bs4", "youtube-dl", "pafy",
                      "json_database", "m3u8"],
    description='video on demand'
)
