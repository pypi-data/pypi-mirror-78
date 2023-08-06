from setuptools import setup, find_packages

README = ''
with open('README.md', 'r') as f:
    README = f.read()
setup(
    name='vnm',
    version='0.3.1',
    packages=find_packages(),
    license='MIT',
    author='Rob "N3X15" Nelson',
    author_email='nexisentertainment@gmail.com',
    long_description=README,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'vnm = vnm.__main__:main'
        ]
    },
    install_requires=['setuptools', 'wheel', 'pip', 'ruamel.yaml']
)
