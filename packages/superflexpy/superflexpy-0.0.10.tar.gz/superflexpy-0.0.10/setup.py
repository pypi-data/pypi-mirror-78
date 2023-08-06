import setuptools

setuptools.setup(
    name='superflexpy',
    version='0.0.10',
    author='Marco Dal Molin',
    author_email='marco.dalmolin.1991@gmail.com',
    description='Framework for building hydrological models',
    license='Apache Software License',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',  # https://martin-thoma.com/software-development-stages/
    ],
    install_requires=[
        'numpy>=1.16.4',
        'numba>=0.49.0',
    ],
)
