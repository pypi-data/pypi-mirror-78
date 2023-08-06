from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='TkLogin',
      version='0.0.4',
      description='Python Tkinter login',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/TkLogin",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      python_requires='>=3',
      zip_safe=False,
      platforms='OS Independent',

      include_package_data=True,
      package_data={
        'TkLogin' : ['Data/Users_Database.json']

      },

      install_requires=[
        'ftputil>=3.4',
        


      ],

      packages=find_packages(),

      entry_points={
        'console_scripts':['TkLogin = TkLogin.__main__:main']
        
      },
      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
