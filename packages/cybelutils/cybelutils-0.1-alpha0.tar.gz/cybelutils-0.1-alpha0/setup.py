from distutils.core import setup
setup(
    name='cybelutils',
    packages=['cybelutils'],
    version='0.1-alpha0',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='GNU General Public License v3 (GPLv3)',
    description='Swiss knife package with multiples usages',
    author='Rhubenni Telesco',
    author_email='rhubenni.telesco+pydev@gmail.com',
    url='https://github.com/rhubenni/cybelutils',
    download_url='https://github.com/rhubenni/cybelutils/archive/0.1-alpha0.tar.gz',
    keywords=['UTILS', 'CRYPTO', 'SODIUM', 'FILESYSTEM'],
    install_requires=[
        'pynacl'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
