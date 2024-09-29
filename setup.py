from setuptools import setup, find_packages

# python setup.py sdist bdist_wheel
# pip install dist/ScoringPy-0.0.2.tar.gz
# pip install dist/ScoringPy-0.0.2-py3-none-any.whl
# pip install --force-reinstall dist/ScoringPy-0.0.2-py3-none-any.whl
# twine upload dist/*




setup(
    name="AlertManager",  # The name of your package
    version="0.0.3",  # The version of your package
    author="Anri Tvalabeishvili, Kristine Dzneladze",  # Your name or organization
    author_email="QubdiSolutions@gmail.com",  # Your contact email
    description="AlertManager is an open-source Python library designed to streamline and enhance data validation processes for both local Pandas DataFrames and database tables.",  # A short description of your package
    long_description=open("README.md").read(),  # Long description read from a file
    long_description_content_type="text/markdown",  # The format of the long description (usually 'text/markdown')
    url="https://github.com/Qubdi/AlertManager",  # URL to your project's homepage (GitHub, etc.)
    packages=find_packages(),  # Automatically find and include all packages in the project
    install_requires=[
        # List your package dependencies here
        # Example: 'requests', 'numpy', etc.
    ],
    project_urls={
        'Documentation': 'https://timeline-manager.readthedocs.io/en/latest/index.html',
        'HomePage': 'https://github.com/Qubdi/AlertManager',
        'Tracker': 'https://github.com/Qubdi/AlertManager/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify the Python versions supported
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",  # OS compatibility
    ],
    python_requires='>=3.6',  # Specify the minimum Python version required
)
