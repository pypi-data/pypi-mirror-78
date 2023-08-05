import pathlib

from setuptools import setup


PROJECT_ROOT = pathlib.Path(__file__).parent
PROJECT_NAME = 'locust-plugin-result'
COPYRIGHT = u"Copyright (c) 2020 Lars Hupfeldt Nielsen, Hupfeldt IT - for UFST"
PROJECT_AUTHORS = u"Lars Hupfeldt Nielsen"
PROJECT_EMAILS = 'lhn@hupfeldtit.dk'
PROJECT_URL = "https://github.com/lhupfeldt/locust-plugin-result"
SHORT_DESCRIPTION = 'Locust plugin for providing FAIL/PASS result of test run.'
LONG_DESCRIPTION = open(PROJECT_ROOT / "README.rst").read()


with open(PROJECT_ROOT/'requirements.txt') as ff:
    install_requires = ff.readlines()


if __name__ == "__main__":
    setup(
        name=PROJECT_NAME,
        version_command=('git describe', 'pep440-git'),
        author=PROJECT_AUTHORS,
        author_email=PROJECT_EMAILS,
        packages=['locust_plugin_result'],
        package_dir={'locust_plugin_result': 'src'},
        zip_safe=True,
        include_package_data=False,
        python_requires='>=3.6.0',
        install_requires=install_requires,
        setup_requires='setuptools-version-command~=2.2',
        url=PROJECT_URL,
        description=SHORT_DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/x-rst',
        license='BSD',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Software Development :: Testing',
        ],
    )
