from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyQt5-comet',
    version='1.0.3',
    packages=['PyLib'],
    url='https://github.com/SkyBlueEternal/PyQt5-comet',
    license='GNU General Public License v3.0',
    author='柠檬菠萝',
    author_email='white.mi@yahoo.com',
    description='PyQt5开发框架',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[
        'main',
        'PyLib.__init__',
        'PyLib.Controller',
        'PyLib.MainUi',
        'PyLib.Module-Test',
        'PyLib.ProgramManagement',
    ],
    python_requires='>=3.7'
)
