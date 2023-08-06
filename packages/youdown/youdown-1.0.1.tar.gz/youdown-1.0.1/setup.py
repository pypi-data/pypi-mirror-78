import setuptools
from setuptools import setup

setup(
    name='youdown',
    version='1.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/NatanielBR/YouDown',
    license='MIT',
    author='Neoold',
    author_email='',
    description='YouDown is a simple way do download video in youtube using pytube and convert using ffmpeg.',
    python_requires='>=3',
    install_requires=['ffmpeg-python','pytube3','requests','prompt-toolkit'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['youdown=youdown.youdown:main'],
    }
)
