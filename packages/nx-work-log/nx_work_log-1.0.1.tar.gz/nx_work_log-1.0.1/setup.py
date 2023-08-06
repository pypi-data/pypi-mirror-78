from setuptools import setup
import pathlib

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print('WARNING: sphinx not available, not building docs')

here = pathlib.Path(__file__).parent.resolve()

name = 'nx_work_log'

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

setup(

    name=name,
    description='NX Solutions Work Log',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    url='https://xanderhendriks.github.io/nx-work-log',

    author='Xander Hendriks',
    author_email='xander.hendriks@nx-solutions.com',

    classifiers=[  # Optional
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=['nx_work_log'],

    python_requires='>=3.6',
    install_requires=['pywin32 ; platform_system=="Windows"'],
    setup_requires=[
        'setuptools_scm',
        'wheel',
    ],

    extras_require={
        'dev': ['check-manifest', 'flake8'],
        'test': ['pytest'],
        'doc': ['sphinx', 'sphinx-rtd-theme'],
    },

    package_data={
        'nx_work_log': ['nx_work_log.rc', 'SysTrayPaused.ico', 'SysTrayRunning.ico'],
    },

    entry_points={
        'gui_scripts': [
            'nxworklog=nx_work_log.win_app:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/xanderhendriks/nx-work-log/issues',
        'Source': 'https://github.com/xanderhendriks/nx-work-log',
    },

    use_scm_version={
        'relative_to': __file__,
        'write_to': 'nx_work_log/version.py',
    },

    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'source_dir': ('setup.py', 'doc'),
        }
    },
)
