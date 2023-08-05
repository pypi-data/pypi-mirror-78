from setuptools import setup


with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='pymw',
    version='0.9.0',
    author='5j9',
    author_email='5j9@users.noreply.github.com',
    description="A thin MediaWiki client using requests.",
    license='GNU General Public License v3 (GPLv3)',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/5j9/pymw',
    packages=['pymw'],
    python_requires='>=3.9',
    install_requires=['requests'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Environment :: Web Environment'],
    zip_safe=True)
