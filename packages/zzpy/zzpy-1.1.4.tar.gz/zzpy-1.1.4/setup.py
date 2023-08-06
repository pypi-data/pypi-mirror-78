from setuptools import setup, find_packages

setup(
    name="zzpy",
    version="1.1.4",
    keywords=["pip", "zzpy", "utils"],
    description="Python3 utilities",
    long_description="Python3 utilities",
    license="MIT Licence",

    url="https://github.com/zerocpp/zzpy",
    author="zerocpp",
    author_email="85642468@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pymongo", "pymysql",
                      "redis", "tqdm", "jsonlines", "pandas", "oss2", "openpyxl", "elasticsearch", "Deprecated"]
)
