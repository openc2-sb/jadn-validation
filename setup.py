from setuptools import setup
 
setup(
    name="jadnvalidation",
    version="2.5.0", 
    packages=["jadnvalidation", "jadnvalidation.data_validation", "jadnvalidation.data_validation.formats", "jadnvalidation.data_validation.schemas", "jadnvalidation.models", "jadnvalidation.models.jadn", "jadnvalidation.utils", "jadnvalidation.models.jadn"],
    install_requires=[
        "jsonpointer",
        "pytest",
        "netaddr",
        "numpy",
        "rfc3986",
        "rfc3987",
        "strict-rfc3339",
        "typing-extensions",
        "uri-template",
        "validators",
        "iso8601"
    ]    
)