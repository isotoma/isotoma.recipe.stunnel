Stunnel buildout recipe
=======================

An example of a standard setup::

    [stunnel:ssl]
    name = ssl
    accept = 0.0.0.0:443
    connect = 127.0.0.1:8080

    [stunnel]
    recipe = isotoma.recipe.stunnel
    pidfile = /var/run/stunnel.pid


Mandatory parameters
--------------------

backends
    A list of backend parts

Backend parameters
------------------

name
    A name for the backend
accept
    A port and interface to listen on
connect
    A port to proxy traffic to after stripping SSL

Optional parameters
-------------------

pidfile
    Where to save the pidfile

