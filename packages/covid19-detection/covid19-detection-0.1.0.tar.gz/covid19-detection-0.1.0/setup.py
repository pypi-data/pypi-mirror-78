from setuptools import setup, find_packages

setup(
    name='covid19-detection',
    version='0.1.0',
    description='Detection of COVID-19 from Chest X-Ray Images',
    author='Franco Ruggeri, Fredrik Danielsson, Muhammad Tousif Zaman, Milan Jolić',
    author_email='fruggeri@kth.se, fdaniels@kth.se, mtzaman@kth.se, jolic@kth.se',
    license='GPL',
    packages=find_packages(include=['covid19', 'covid19.*']),
    include_package_data=True,
    url='https://github.com/franco-ruggeri/dd2424-covid19-detection'
)
