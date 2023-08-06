from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='annotateonline',
version='0.1.33',
description='Annotate Online',
url='https://github.com/superannotateai/AO-python-cli',
author='Annotate Online',
license='MIT',
packages=['annotateonline.image_upload','annotateonline.pre_annotation_upload','annotateonline.pre_annotation_upload.panopticapi','annotateonline'],
entry_points = {
        'console_scripts': [
            'annotateonline = annotateonline.__main__:main'
        ]
    },
install_requires=[
    'boto3',
    'pillow',
    'cython',
    'numpy',
    'pycocotools',
    'matplotlib',
    'opencv-python',
],
zip_safe=False)