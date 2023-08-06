from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='quhep',
    version='0.0.3',
    entry_points = {
        'console_scripts': [
            'quhep_tfq=quhep.train.train_tfq:main',
            'quhep_qsk=quhep.train.train_qsk:main',
            'averageROC=quhep.util.averageROC:main',
            'extracAUC=quhep.util.extracAUC:main',
            'inspecPQC=quhep.util.inspecPQC:main',
        ],
    },
    description='Quantum Machine Learning Framework for High Energy Physics',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Rui Zhang',
    author_email='rui.zhang@cern.ch',
    keywords=['Quantum Machine Learning', 'Tensorflow Quantum', 'Qiskit pyTorch'],
    url='https://github.com/chnzhangrui/quhep',
    download_url='https://pypi.org/project/quhep/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires, include_package_data=True)
