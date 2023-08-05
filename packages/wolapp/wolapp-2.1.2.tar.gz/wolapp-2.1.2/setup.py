import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='wolapp',
                 version='2.1.2',
                 description='WOL applicaion',
                 long_description=long_description,
                 author='Kratinn.com',
                 author_email='developer@viriminfotech.com',
                 license='Virim',
                 url="https://github.com/emb-karan/espapp-pkg",
                 packages=setuptools.find_packages(),
                 package_dir={'WOL_App': 'espapp'},
                 package_data={'espapp': ['data/*']},
                 include_package_data=True,
                 platforms='Linux',
                 python_requires='!=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
                 install_requires=[
                     'uuid',
                     'python-crontab',
                     'requests',
                 ],
                 entry_points={
                     'console_scripts': [
                         'wolapp=espapp.esp:main',
                     ],
                 },
                 )
