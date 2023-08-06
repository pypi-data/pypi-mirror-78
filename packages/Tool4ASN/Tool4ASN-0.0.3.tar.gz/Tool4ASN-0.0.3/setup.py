from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='Tool4ASN',
      version='0.0.3',
      description='Python module able to download a file from FTP and subset it using time-range,bounding-box,variables and depths',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/Tool4ASN",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      python_requires='>=3',
      zip_safe=False,
      platforms='OS Independent',

      include_package_data=True,
      package_data={
        'Tool4ASN' : ['SRC/','IMAGES/','Script/']

      },

      install_requires=[
        'ftputil>=3.4',
        


      ],

      packages=find_packages(),

      entry_points={
        'console_scripts':['Tool4ASN = Tool4ASN.__main__:main']
        
      },
      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
