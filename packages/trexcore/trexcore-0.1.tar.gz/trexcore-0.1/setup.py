import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='trexcore',  
     version='0.1',
     author="Jack Lok",
     author_email="sglok77@gmail.com",
     description="TRex Core library package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://bitbucket.org/lokjac/trexcore",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[            # I get to this in a second
          'python-dateutil',
          'stripe',
          'urllib3',
          'phonenumbers',
          'email_validator',
          'Flask-Mail',
          'Flask-Script',
          'mailjet_rest',
          'sendgrid',
      ],
 )

