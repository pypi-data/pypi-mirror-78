from setuptools import find_packages, setup

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='notesplit',
    version='1.0.1',
    description="Write your private diary in text files, and share parts of it with someone else's diaries.",
    long_description=long_description,
    long_description_content_type='text/rst',
    url='https://github.com/mindey/notesplit',
    author='Mindey',
    author_email='~@mindey.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'notesplit=notesplit.split:main'
        ],
    }
)
