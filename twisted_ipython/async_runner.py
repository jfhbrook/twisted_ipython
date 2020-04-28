class _TwistedRunner:
    def __call__(self, coro):
        """
        Handler for Twisted autoawait
        """

        import asyncio
        from twisted.internet.defer import ensureDeferred

        loop = asyncio.get_event_loop()

        # It would be really nice if this worked, and I personally think it's
        # technically possible, but as of today this will throw a RuntimeError
        # with the message "This event loop is already running".
        #
        # I've confirmed that this will also throw the same error if you run
        # asyncio.get_event_loop().run_until_complete(some_coro) inside
        # a Jupyter cell, which is frankly bizarre because that's exactly
        # what is happening in the IPython loop_runner:
        #
        # https://github.com/ipython/ipython/blob/master/IPython/core/async_helpers.py#L28
        #
        # I have a couple of ideas for what might be happening here, none
        # of which I can prove:
        #
        # - IPython manually shuts down the asyncio reactor before running
        #   an async function, then starts it up again. I can't find any
        #   code that looks like it does this.
        # - IPython does something bonkers with the scope of the cell, such
        #   that inside the loop_runner importing asyncio works against a
        #   fresh environment that creates a new loop. IPython *does* do
        #   weird stuff with the coroutine's scope -
        #   https://github.com/ipython/ipython/blob/master/IPython/core/interactiveshell.py#L130 -
        #   but it's not clear how this would change the behavior in the way
        #   I'm seeing.
        #
        # What's even weirder is that I've tried to edit the code that I think
        # should be getting executed to raise exceptions and can't get Jupyter
        # to log *or* crash. In particular, I've tried this in two places:
        #
        # - https://github.com/ipython/ipython/blob/master/IPython/core/interactiveshell.py#L2884
        # - https://github.com/ipython/ipython/blob/master/IPython/core/async_helpers.py#L27
        #
        # I fully believe that IPython would make print violate my expectations,
        # but it seems unlikely that raising exceptions wouldn't work here. The
        # most likely explanation is that I'm misunderstanding what code is
        # being executed - either in terms of what package path is getting
        # loaded or in terms of what code path is being executed. This seems
        # strange. I am very confused.
        #
        # If you have deep knowledge of IPython/Jupyter internals, PLEASE
        # talk to me.
        return loop.run_until_complete(ensureDeferred(coro).asFuture(loop))

    def __str__(self):
        return 'twisted'


twisted_runner = _TwistedRunner()
