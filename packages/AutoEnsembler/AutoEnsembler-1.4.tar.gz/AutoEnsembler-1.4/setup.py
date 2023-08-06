from setuptools import setup


from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='AutoEnsembler',
      packages=['AutoEnsembler'],
      version='1.4',
      license='MIT',
      description='This AutoEnsembler helps you to find the best Ensemble model for you',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Nilesh Chilka', 
      author_email = 'nileshchilka1@gmail.com',
      keywords = ['AUTOENSEMBLE', 'ENSEMBLE' , 'MACHINE LEARNING'],
      install_requires=['numpy','scikit-learn'],
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ])
