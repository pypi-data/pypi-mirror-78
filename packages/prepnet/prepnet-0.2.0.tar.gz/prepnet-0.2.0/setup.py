from setuptools import setup
from pathlib import Path

# Get version from main script
__version__ = None

src_dir = Path(__file__).parent.absolute()
version_file = src_dir / 'prepnet' / 'version.py'
with open(version_file, 'r') as fp:
    exec(fp.read())

fndoc = Path(src_dir) / 'README.md'
with open(fndoc, 'r') as fp:
    README = fp.read()

setup(
    name='prepnet',
    version=__version__,
    description='Reconstructable preprocessor library',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT Licences',
    url='https://github.com/elda27/prepnet',
    author='elda27',
    author_email='elda27.prog@gmail.com',
    platforms=['any'],
    install_requires=[
        "numpy",
        "pandas"
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage'
        ],
    },
    packages=[
        'prepnet',
        'prepnet.core',
        'prepnet.executor',
        'prepnet.impute',
        'prepnet.normalize',
        'prepnet.category',
        'prepnet.functional',
        'prepnet.math',
        'prepnet.extra',
        'prepnet.time',
    ],
    zip_safe=False,
    python_requires='>=3.6',
    classifiers=[
        # (https://pypi.org/pypi?%3Aaction=list_classifiers)
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft',
        'Operating System :: Microsoft :: MS-DOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Science/Research',
        
    ],
    # keywords=None,
)