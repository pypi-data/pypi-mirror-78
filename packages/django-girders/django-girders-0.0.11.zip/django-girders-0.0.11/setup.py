from pathlib import Path

from setuptools import find_packages, setup


readme_file = Path(__file__).parent / 'README.md'
with readme_file.open() as f:
    long_description = f.read()

setup(
    name='django-girders',
    version='0.0.11',
    description='Django utilities for data management applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    url='https://github.com/brianhelba/django-girders',
    project_urls={
        'Bug Reports': 'https://github.com/brianhelba/django-girders/issues',
        'Source': 'https://github.com/brianhelba/django-girders',
    },
    author='Kitware, Inc',
    author_email='kitware@kitware.com',
    keywords='django girder girders',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.0',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=['django>=3', 'django-configurations[database,email]'],
)
