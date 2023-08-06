import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="link-crab",
    version="0.2.0",
    author="Krisztián Pál Klucsik",
    author_email="klucsik.krisztian@gmail.com",
    description="A link crawler and permission testing tool for websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/klucsik/link-crab",
    packages=setuptools.find_packages(),
    install_requires=[
          'beautifulsoup4',
          'colorama',
          'Flask',
          'Flask-user',
          'Flask-babelex',
          'email_validator',
          'PyYAML',
          'requests',
          'selenium',
          'pytest'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)