from codecs import open
from setuptools import setup, find_packages

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='intelab-ffmpeg-sdk',
    version='1.0.0a2',
    long_description=readme,
    long_description_content_type='text/markdown',
    # install_requires=requires,
    packages=find_packages(exclude=('tests', 'tests.*')),
    entry_points={
        'console_scripts': [
            'intelab_video = intelab_video.main:command_line_runner',
        ]
    },
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
