from twisted_ipython.async_runner import twisted_runner


def install_autoawait(ipython):
    ipython.loop_runner_map['twisted'] = (twisted_runner, True)
