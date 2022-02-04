from setuptools import setup, find_namespace_packages

setup(name='clean-folder-01',
      version='1.0.0',
      description='Sort your folder',
      url='https://github.com/DianaKB/clean_folder',
      author='Diana Kovalchuk',
      author_email='dianakovalhyk@ukr.net',
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:print_result']}
      )
