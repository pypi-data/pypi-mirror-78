from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="snaptimer",
    version="0.0.1",
    author="Ron Chang",
    author_email="ron.hsien.chang@gmail.com",
    description="A colorful timer which handling basic information and allow to add info manually.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ron-Chang/snap_timer",
    packages=find_packages(),
    license='MIT',
    python_requires='>=3.6',
    exclude_package_date={'':['.gitignore', 'dev', 'test', 'setup.py']},
    install_requires=[
        'colorama==0.4.3',
    ]
)
