import setuptools

__version__ = "0.0.3"

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='shandlers',
    version=__version__,
    author='GonzaloSaad',
    author_email='saad.gonzalo.ale@gmail.com',
    description="A python lib that provides handlers for serverless events",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/GonzaloSaad/shandlers',
    packages=setuptools.find_packages(),
    keywords='python aws serverless',
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
