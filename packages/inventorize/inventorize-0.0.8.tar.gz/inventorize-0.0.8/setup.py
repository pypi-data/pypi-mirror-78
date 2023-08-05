from setuptools import setup, find_packages


setup(
    name="inventorize", 
    version="0.0.8",
    author="Haytham Omar",
    author_email="haytham@rescaleanalytics.com",
    description="inventory analytics,revenue management and cost calculations for SKUs",
    keywords=['inventory','pricing'],
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    
    packages=find_packages(),
    install_requires=[
        'scipy','scikit-learn',
        'pandas>=0.23.3',
        'numpy>=1.14.5'
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)