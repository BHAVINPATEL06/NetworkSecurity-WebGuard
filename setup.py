'''
The setup.py file is an essential part of packaging and distributing python projects.
It is used to setuptools (or distutils in python older version) to define the configuration 
of our projects, such as metadata, dependencies, and entry points.
'''


from setuptools import setup, find_packages
## find_packages is a utility function that automatically finds the __init__.py files from the folder 
## and lists them as packages to be included in the distribution.

from typing import List

def get_requirements() -> List[str]:
    "This Function will return the list of requirements from requirements.txt file"
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt','r') as file:
            ## Read lines from requirements.txt file
            lines = file.readlines()
            ## Process each line
            for line in lines:
                requirement = line.strip()
                ## Ignore empty lines and '-e .'
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_lst

setup(
    name = "NetworkSecurityProject",
    version="0.0.1",
    author="Bhavin Patel",
    author_email="bhavinpatel24246@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)