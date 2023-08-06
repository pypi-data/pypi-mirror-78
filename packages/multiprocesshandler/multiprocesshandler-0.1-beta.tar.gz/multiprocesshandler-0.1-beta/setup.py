from distutils.core import setup

setup(
    name='multiprocesshandler',
    packages=['multiprocesshandler'],
    version='0.1-beta',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='GNU General Public License v3 (GPLv3)',
    description='A simple handler for multiprocessing in python with custom queue',
    author='Rhubenni Telesco',
    author_email='rhubenni.telesco+pydev@gmail.com',
    url='https://github.com/rhubenni/multiprocesshandler',
    download_url='https://github.com/rhubenni/multiprocesshandler/archive/0.1-beta.tar.gz',
    keywords=['MULTIPROCESSING', 'TASK QUEUING', 'PARALELISM'],
    install_requires=[
        ''
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
