from distutils.core import setup
setup(
  name = 'icd2phenotype',        
  packages = ['icd2phenotype'],  
  version = '0.13',      
  license='MIT',        
  description = 'Identify phenotypes from ICD code list',   
  include_package_data=True,
  author = 'Xiaoqian Jiang, Luyao Chen',                  
  author_email = 'your.email@domain.com',      
  url = 'https://github.com/Luyaochen1/icd2phenotype',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Luyaochen1/icd2phenotype/archive/V_013.tar.gz',     
  keywords = ['icd 9', 'icd 10', 'phenotypes'],   
  install_requires=[            # I get to this in a second
          'pandas',
        ],
  classifiers=[
    'Development Status :: 3 - Alpha',       
    'Intended Audience :: Developers',       
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7', 
    'Programming Language :: Python :: 3.8',
  ],
)
