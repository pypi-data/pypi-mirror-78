# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository pypi dist/*
#
# more info here:
# https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi

import setuptools

setuptools.setup(name = 'gamelan_sequencer',
    version = '1.0.0',
    author = 'Rego Sen',
    author_email = 'regosen@gmail.com',
    url = 'https://github.com/regosen/gamelan_sequencer',
    description = 'Python Sequencer for Gamelan Music',
    long_description = open("README.md","r").read(),
    long_description_content_type = "text/markdown",
    license = 'MIT',
    keywords = 'music songwriting indonesia javanese balinese kepatihan gamelan',
    packages=setuptools.find_packages(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Editors'
    ],
)