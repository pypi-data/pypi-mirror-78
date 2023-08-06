import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aioface",
    version="0.0.1",
    author="Kirill Kuzin",
    author_email="offkirillkuzin@gmail.com",
    description="aioface is a powerful and simple asynchronous framework "
                "for the Facebook Messenger API written in Python 3.7.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kirillkuzin/aioface",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers'
    ],
    project_urls={
        'Source': 'https://github.com/kirillkuzin/aioface'
    },
    install_requiers=[
        'aiohttp>=3.6.2'
    ],
    python_requires='>=3.7',
)
