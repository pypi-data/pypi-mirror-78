from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='futils-grab',
    version='0.0.2',
    description='a unix filter for extracting tokens',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/folkol/grab',
    author='folkol',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Filters',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='shell, unix filter',
    py_modules=["grab"],
    python_requires='>=3.6, <4',
    entry_points={
        'console_scripts': [
            'grab=grab:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/folkol/grab/issues',
        'Source': 'https://github.com/folkol/grab',
    },
)
