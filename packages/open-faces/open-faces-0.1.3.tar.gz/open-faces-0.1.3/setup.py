from setuptools import setup, find_packages

requirements = [
    'numpy',
    'pandas',
    'gdown',
    'opencv-python',
    'flask',
    'Pillow',
    'dlib',
    'keras',
    'tensorflow',
]

__version__ = '0.1.3'

setup(
    # Metadata
    name='open-faces',
    version=__version__,
    author='CachCheng',
    author_email='tkggpdc2007@163.com',
    url='https://github.com/CachCheng/OpenFaces',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    description='Open Faces Toolkit',
    license='Apache-2.0',
    packages=find_packages(exclude=('docs', 'tests', 'scripts')),
    zip_safe=True,
    include_package_data=True,
    install_requires=requirements,
)
