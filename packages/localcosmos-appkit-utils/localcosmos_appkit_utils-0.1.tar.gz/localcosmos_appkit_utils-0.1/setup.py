from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

install_requires = [
    'Pillow',
]

setup(
    name='localcosmos_appkit_utils',
    version='0.1',
    description='Local Cosmos AppKit utils. Creates images and more for mobile apps created with Local Cosmos.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='localcosmos, app kit, app kit utils',
    author='Thomas Uher',
    author_email='thomas.uher@sisol-systems.com',
    url='https://github.com/SiSol-Systems/localcosmos-appkit-utils',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=install_requires,
)
