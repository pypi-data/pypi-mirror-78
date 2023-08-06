from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='fff_profile_picture',
    version='2.0.3',
    packages=['fff_profile_picture'],
    install_requires=['Pillow'],
    url='',
    license='LGPL',
    author='Alwin Lohrie (Niwla23)',
    author_email='alwin@kat-zentrale.de',
    description='A Module to generate profile pictures',
    long_description=readme,
    long_description_content_type="text/markdown",
    test_suite='nose.collector',
    tests_require=['nose'],
    keywords=['fff', 'fridaysforfuture', 'profilepicture', 'generator'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

)
