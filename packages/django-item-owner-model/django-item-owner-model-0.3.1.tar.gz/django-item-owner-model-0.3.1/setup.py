import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines()]

setup(
    name="django-item-owner-model",
    version="0.3.1",
    description="Data item has owner and can be shared to other users. Login user can only see owned or shared data items. User with permit_all permission can see all data items.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    url="https://github.com/zencore-cn/zencore-issues",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django-item-owner-model"],
    packages=find_packages(".", exclude=("django_item_owner_model_example", "django_item_owner_model_example.migrations", "django_item_owner_model_demo")),
    py_modules=["django_item_owner_model"],
    install_requires=requires,
    zip_safe=False,
)
