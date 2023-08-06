from setuptools import setup,find_packages

requirements = [
    'mecab-python3==1.0.1',
    'unidic-lite',
]

setup(name='util_ds',
      version='0.5.0',
      description='A util for daily',
      author='Xuhong Guo',
      author_email='878153077@qq.com',
      packages=find_packages(),
      license='MIT',
      install_requires=requirements,
      zip_safe=False)