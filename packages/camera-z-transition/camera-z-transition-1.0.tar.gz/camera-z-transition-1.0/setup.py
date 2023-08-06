from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='camera-z-transition',
    version='1.0',
    description='This package provides quick and easy way to estimate the camera transition on the z axis given an optical flow.',
    license="MIT",
    keywords=['video', 'optical-flow', 'camera', 'camera-motion', 'motion field', 'camera transition', 'camera movement'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tamas Suveges',
    url='https://github.com/stamas02/camera_z_transition',
    download_url='https://github.com/stamas02/camera_z_transition/archive/v_01.tar.gz',
    author_email='stamas01@gmail.com',
    packages=['camera_z_transition'],
    install_requires=['scipy', 'numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
