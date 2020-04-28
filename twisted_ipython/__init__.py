from twisted_ipython.magic import install_autoawait


def load_ipython_extension(ipython):
    from twisted.internet.asyncioreactor import install  # noqa: F401
    install()

    install_autoawait(ipython)
