from setuptools import setup

setup(
    name='demographer',
    version='1.0.4',
    author='Zach Wood-Doughty, Paiheng Xu, Xiao Liu, Praateek Mahajan, Rebecca Knowles, Josh Carroll, Mark Dredze',  # noqa
    author_email='mdredze@cs.jhu.edu',
    packages=['demographer'],
    package_dir={'demographer': 'demographer'},
    package_data={'demographer': ['data/*']},
    include_package_data=True,
    url='https://bitbucket.org/mdredze/demographer',
    download_url='https://bitbucket.org/mdredze/demographer/get/0.1.2.zip',
    license='LICENSE.txt',
    description='Simple name demographics for Twitter names',
    long_description_content_type="text/x-rst",
    long_description="Demographer is a Python package that predicts demographic characteristics from information in a single tweet. It's designed for Twitter, where it takes the name of the user and returns information about their likely demographics.",  # noqa
    install_requires=[
        "numpy",
        "scikit-learn",
    ]
)
