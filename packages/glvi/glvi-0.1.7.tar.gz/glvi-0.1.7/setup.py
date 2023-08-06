import setuptools

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
install_requires = [
    "scikit-learn >= 0.20.0",
    "numpy >= 1.11.0",
    "scipy >= 0.17.0",
    "joblib >= 0.11.0"]
setuptools.setup(name='glvi',
                 version='0.1.7',
                 description='Local variable importance from a global model',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='TaoLi',
                 author_email='lp1559345469@gmail.com',
                 url='https://github.com/PowderL/Local-variable-importance-from-a-global-mode',
                 keywords='random forests variable importance ',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 include_package_data=True,
                 python_requires=">=3.6",
                 install_requires = install_requires,
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     "Intended Audience :: Science/Research",
                     "Operating System :: Microsoft :: Windows :: Windows 10",
                     "Operating System :: POSIX",
                     "Operating System :: Unix",
                     "Operating System :: MacOS",
                     "License :: Freeware",
	                 "Natural Language :: English"
                 ])