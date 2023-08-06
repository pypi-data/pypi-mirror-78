from setuptools import setup, find_packages

setup(name='nvuti',
      version='0.1',
      description='Package for use NvutiAPI parser',
      long_description='Package for use NvutiAPI parser',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='nvuti',
      url='http://github.com/DeadRain/NvutiAPI',
      author='Prozenq',
      author_email='kepera@inbox.ru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False)