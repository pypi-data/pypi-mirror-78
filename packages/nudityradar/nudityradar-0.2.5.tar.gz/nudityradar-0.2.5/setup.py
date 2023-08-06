from setuptools import setup, Extension

setup(
    name='nudityradar',
    version='0.2.5',
    description="Nudity detection with re-trained Tensorflow MobileNet Model http://nudity.canaydogan.net",
    long_description=open('README.rst').read(),
    author='Can Aydogan',
    author_email='canaydogan89@gmail.com',
    url='https://github.com/canaydogan/nudity',
    license='MIT',
    packages=['nudityradar'],
    include_package_data=True,
    package_dir={'nudityradar': 'nudityradar'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords="nude, nudity, detection, pornographic, inappropriate content",
    install_requires=['tensorflow'],
    python_requires='>=3',
    entry_points={'console_scripts': ['nudity = nudity:main']}
)
