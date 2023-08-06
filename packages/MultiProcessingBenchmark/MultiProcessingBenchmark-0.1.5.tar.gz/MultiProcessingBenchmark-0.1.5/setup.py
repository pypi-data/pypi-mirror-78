from setuptools import setup, find_packages

setup(name='MultiProcessingBenchmark',
      version='0.1.5',
      url='https://github.com/srivassid/MultiProcessingBenchmark',
      license='MIT',
      author='Siddharth Srivastava',
      author_email='s.srivas@hotmail.com',
      description='Benchmarking library single core vs multi core for common pandas functions',
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False)