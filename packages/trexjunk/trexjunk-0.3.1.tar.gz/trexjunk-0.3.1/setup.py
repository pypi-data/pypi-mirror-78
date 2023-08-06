import setuptools
from pip._vendor.pkg_resources import require

setuptools.setup(
     name='trexjunk',  
     version='0.3.1',
     author="Jack Lok",
     author_email="sglok77@gmail.com",
     description="TRex junk library package",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
                        'python-dateutil',
                        'phonenumbers',
                       ],
 )

