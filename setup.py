from setuptools import setup, find_packages

# Load reStructedText description.
# Online Editor   - http://rst.ninjs.org/
# Quick Reference - http://docutils.sourceforge.net/docs/user/rst/quickref.html
readme = open('README.rst', 'r', encoding='utf-8')
longdesc = readme.read()
readme.close()

# See
# https://packaging.python.org/tutorials/packaging-projects/
# https://python-packaging.readthedocs.io/en/latest/non-code-files.html
setup(
    name='busm',
    version='0.9.0',
    description='Help you get stdout of function execution through Email, Telegram and Line Notify.',
    long_description=longdesc,
    packages=find_packages(),
    url='https://github.com/virus-warnning/busm',
    license='MIT',
    author='Raymond Wu',
    package_data={
        'busm': ['conf/*']
    },
    install_requires=[
        'requests', 'PyYAML'
    ],
    python_requires='>=3.5'
)
