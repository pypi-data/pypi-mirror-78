import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="panvalidator",
    version="0.0.1",
    author="Gennady Denisov",
    author_email="denisovgena@gmail.com",
    description="Primary Account Number validation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geaden/panvalidator",
    packages=setuptools.find_packages(),
    license='Apache',
    test_suite='nose.collector',
    tests_require=['nose'],
    install_requires=[
        'luhn',
    ],
    python_requires='>=3.6',
)
