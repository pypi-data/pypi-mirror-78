import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whatsappguru",
    version="0.2.4",
    author="Lorenzo Coacci",
    author_email="lorenzo@coacci.com",
    description="The package contains the tools to analyze your WhatsApp chats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lollococce/whatsappguru",
    packages=setuptools.find_packages(),
    keywords='',
    license='MIT',
    include_package_data=True,
    install_requires=[
        'pandas',
        'emoji',
        'progressbar',
        'uuid',
        'iago',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ]
)
