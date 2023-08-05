from setuptools import setup, find_packages

setup(name='choomah-exception',
      version='0.1',
      description='- The playing of the said "choomah scream" everytime an exception is captured (similar to oooOOOOAAAAAAAAAAA )',
      url='https://github.com/christopher-turnbull/choomah',
      author='Christopher Turnbull',
      author_email='cturnbull27995@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      python_requires='>=3.6'
      )


# import setuptools
#
# with open("README.md", "r") as fh:
#     long_description = fh.read()
#
# setuptools.setup(
#     name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
#     version="0.0.1",
#     author="Example Author",
#     author_email="author@example.com",
#     description="A small example package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
# ,
# )