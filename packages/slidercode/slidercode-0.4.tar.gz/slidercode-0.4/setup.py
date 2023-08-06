import setuptools

with open("README.md", "r") as reader:
    long_description = reader.read()

with open("requirements.txt", "r") as reader:
    install_requires = [i.strip() for i in reader]

setuptools.setup(
    name="slidercode", 
    version="0.4", 
    author="Barneyness", 
    author_email="1163060039@qq.com", 
    description="SDK about slider code", 
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    url="https://pypi.org/project/slidercode/", 
    packages=setuptools.find_packages(), 
    install_requires=install_requires, 
    classifiers=["Programming Language :: Python :: 3","License :: OSI Approved :: MIT License","Operating System :: OS Independent",],
)



