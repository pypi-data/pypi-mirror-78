import setuptools

with open("README_PyPI.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyBlackScholesAnalytics",
    version="0.0.1",
    author="Gabriele Pompa",
    author_email="gabriele.pompa@gmail.com",
    description="Options and Option Strategies analytics under the Black-Scholes Model for educational purpose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabrielepompa88/pyBlackScholesAnalytics",
	project_urls={
	'Repository':  "https://github.com/gabrielepompa88/pyBlackScholesAnalytics"
	},
    packages=setuptools.find_packages(),
    classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Financial and Insurance Industry',
		'Intended Audience :: Education',
		'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	keywords='finance black-scholes education',
    python_requires='>=3.6',
)