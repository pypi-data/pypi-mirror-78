from distutils.core import setup
import pypandoc
try:
    long_description = pypandoc.convert_file('README.md', 'rst')
    long_description = long_description.replace("\r","") # Do not forget this line
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()
setup(
name = 'samoy',         # How you named your package folder (MyLib)

packages = ['samoy'],   # Chose the same as "name"

version = '0.9',      # Start with a small number and increase it with every change you make

license='MIT',        

description = 'samoy is a Python package for machine learning and data science, built on top of Pandas inbuilt libraries. This package will be useful for data pre-processing before starting off any machine learning or data science project as it will ease your entire process of data cleaning without much input from the user',
long_description= long_description,      

author = 'Abhishek Pailwan,Priyanka Singh',                   # Type in your name

author_email = 'samoyapi@gmail.com',      # Type in your E-Mail

url = 'https://github.com/samoy-pckg/samoy',   # Provide either the link to your github or to your website

download_url =

'https://github.com/samoy-pckg/samoy/archive/v_0.9.zip',    # I explain this later on

keywords = ['DATA SCIENCE', 'MACHINE LEARNING', 'DATA CLEANING','DATA PREPROCESSING','FEATURE ENGINEERING','DESCRIPTIVE ANALYSIS','PREDICTIVE ANALYSIS','STATISTICAL MODELING','PYTHON','PYSPARK'],   # Keywords that define your package best

classifiers=[

    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',      # Define that your audience are developers

    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license

    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support

    'Programming Language :: Python :: 3.4',

    'Programming Language :: Python :: 3.5',

    'Programming Language :: Python :: 3.6',

  ],

)

 

