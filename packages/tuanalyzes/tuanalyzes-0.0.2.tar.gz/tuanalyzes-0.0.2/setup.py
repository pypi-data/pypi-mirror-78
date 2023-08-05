from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='tuanalyzes',
    version='0.0.2',
    description='',
    # long_description_content_type='text/markdown',
    # long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Tuan Anh Bui',
    author_email='kevbui.29@gmail.com',
    keywords=['Analyses', 'EDA', 'Important variables'],
    url='https://github.com/ubunTuan/analysis-functions.git'
)

install_requires = [
    'seaborn','matplotlib','sklearn','panda',
    'numpy','statsmodels','eli5'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)