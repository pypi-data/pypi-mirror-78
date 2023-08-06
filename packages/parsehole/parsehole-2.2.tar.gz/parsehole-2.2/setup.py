import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='parsehole',  
     version='2.2',
    #  scripts=['parsehole'] ,
     author="Victoria Austin",
     author_email="victoriaaustin97@gmail.com",
     description="Sentence conjunction parsing package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/vaustin33/parsehole",
     install_requires=[
          'numpy', 'gensim', 'nltk', 'bllipparser'
      ],
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )