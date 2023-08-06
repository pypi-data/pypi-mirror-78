import setuptools

setuptools.setup(
    name='captionspackage', # Replace with your own username
    version='0.0.3',
    description='get captions',
    py_modules=["app"],
    package_dir={'':'src'},
    install_requires=[
        'flask',
    ],
)
