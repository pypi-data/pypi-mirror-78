from setuptools import setup

about = {}
with open("engformat/__about__.py") as fp:
    exec(fp.read(), about)

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(name='engformat',
      version=about['__version__'],
      description='Tools for displaying engineering calculations according to the Engineering Standard Format',
      url='https://github.com/eng-tools/engformat',
      long_description=readme,
      author='Maxim Millen',
      author_email='millen@fe.up.pt',
      license='MIT',
      packages=[
        'engformat',
    ],
    install_requires=[
        "numpy",
        "bwplot>=0.2.10",
        "sfsimodels",
        "matplotlib",
        "eqsig"
    ],
      zip_safe=False)