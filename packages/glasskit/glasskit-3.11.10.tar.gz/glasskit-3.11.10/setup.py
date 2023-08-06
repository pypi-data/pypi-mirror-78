from setuptools import setup, find_packages


setup(
    name="glasskit",
    version="3.11.10",
    description="a micro webframework based on flask and pymongo",
    url="https://gitlab.com/viert/glasskit",
    author="Pavel Vorobyov",
    author_email="aquavitale@yandex.ru",
    license="MIT",
    packages=[pkg for pkg in find_packages() if pkg.startswith("glasskit")],
    include_package_data=True,
    package_data={"glasskit": ["*.txt", "*.py", "*.tmpl"]},
    install_requires=[
        "jinja2",
        "flask",
        "pymongo",
        "mongomock",
        "cachelib",
        "lazy_object_proxy",
        "ipython",
        "requests",
        "mtprof",
        "simplejson",
    ],
    entry_points={"console_scripts": ["glasskit=glasskit.__main__:main",]},
)
