import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='django-docrootcms-tagulous',
      version='0.12',
      description='Fork of the django-tagulous patched to work with Django 3',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/sstacha/django-docrootcms-tagulous',
      author='Steve Stacha',
      author_email='sstacha@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
      ],
      python_requires='>=3.6',
      install_requires=[
          'django',
      ],
)
