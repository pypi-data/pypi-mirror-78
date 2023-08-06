__version__ = None

try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("pyground").version
except Exception:
    pass
