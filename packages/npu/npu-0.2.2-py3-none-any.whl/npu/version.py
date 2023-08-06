import pkg_resources

__version__ = "0.2.2"

_module = "npu"


latest_version = pkg_resources.get_distribution(_module).version
if latest_version != __version__:
    print("Current version of npu library is {}. Latest version on pypi is {}".format(__version__, latest_version))
