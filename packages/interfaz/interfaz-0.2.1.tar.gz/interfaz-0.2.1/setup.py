import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interfaz", # Replace with your own username
    version="0.2.1",
    author="Alejandro Lavagnino",
    author_email="alejandro.lavagnino@gmail.com",
    description="Funciones para controlar la interfaz por sockets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/astoctas/interfaz-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
  install_requires=[            # I get to this in a second
          'python-socketio'
      ],    
    python_requires='>=3.3',
)