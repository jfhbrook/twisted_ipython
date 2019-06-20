from twisted.internet.defer import ensureDeferred
import crochet
import twisted_ipython.config as config


def twisted_runner(coro):
    """
    A twisted runner for ipython's autoawait.

    This runner uses crochet and ensureDeferred to run a twisted coroutine in
    a blocking manner, as is required by the ipython API.
    """

    @crochet.wait_for(timeout=config.TIMEOUT)
    def run(coro):
        return ensureDeferred(coro)

    return run(coro)
