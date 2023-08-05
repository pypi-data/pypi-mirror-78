import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="waste_uploader",
    version="0.0.9",
    author="Roman Dymov",
    author_email="r.dymov@mpgames.rocks",
    description="Upload script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.7',
    install_requires=[
          'awscli>=1.18.31',
          'requests==2.23.0',
          'aws_requests_auth>=0.4.3',
      ],
    entry_points={
          'console_scripts': [
              'waste-uploader = waste_uploader.__main__:main'
          ]
      },
)
