import setuptools

with open("README.md") as f:
      LONGDESCRIPTION = f.read()

setuptools.setup(
      name='telebotapi',
      version='0.2',
      description="A telegram bot api for telegram, with asynchronous polling",
      url='https://github.com/topongo/telebotapi',
      author='Lorenzo Bodini',
      author_email='lorenzo.bodini.private@gmail.com',
      packages=['telebotapi'],
      python_requires='>=3.6',
      license="GPL3",
      long_description=LONGDESCRIPTION
)
