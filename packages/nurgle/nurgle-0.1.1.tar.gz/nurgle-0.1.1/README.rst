======
nurgle
======


.. image:: https://img.shields.io/pypi/v/nurgle.svg
        :target: https://pypi.python.org/pypi/nurgle

.. image:: https://img.shields.io/travis/@Herout/nurgle.svg
        :target: https://travis-ci.com/@Herout/nurgle

.. image:: https://readthedocs.org/projects/nurgle/badge/?version=latest
        :target: https://nurgle.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Decorator based error handling for Python, all props to `merry <https://github.com/miguelgrinberg/merry>`_ by Miguel Grinberg.
This is a naive extension of merry, and should not be used in production. Us on your own risk. Nurgle can be used in batch processing,
where you need to be informed of the first run with failure and/or first run that recovered from failure.


* Free software: MIT license
* Documentation: https://nurgle.readthedocs.io.



Features
--------

For basic information about its use case, please see original `README <https://github.com/miguelgrinberg/merry/blob/master/README.md>`_

`Nurgle` is a drop-in replacement of `Merry`. On top of parameters provided by `Merry`, `Nurgle` object can be constructed as follows::

    from nurgle import Nurgle
    nurgle = Nurgle(slack_token="<your-slack-token>", slack_channel="<channel-to-write-to>", state_file="/path/to/a-file.nurgle.state")
    

If decorated code throws an exception
-------------------------------------

Nurgle looks for state_file in order to determine, if previous run failed as well.

* If the file does not exist, previous run did not fail, and the exception is sent into the Slack channel.
* If the file does exist, content is read and compared to stringified current exception.
  If the exception is not the same, we failed for different reason, and the exception is sent into the Slack channel.
  
Otherwise, exception is not sent.

If decorated code does not throw an exception
---------------------------------------------

Nurgle looks for state_file in order to determine, if previous run failed or not.

* If the file does not exist, previous run also did not fail, and nothing is sent to the Slack channel.
* If the file does exists, previous run failed:
    * "recovery" message is sent to the Slack channel.
    * afterwards, state_file is deleted.