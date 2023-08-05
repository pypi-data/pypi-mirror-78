Description
===========

Introduction
------------

Miniscule is a library for flexible YAML-based configuration files, inspired by
Clojure's `Aero <https://github.com/juxt/aero>`_.

Example
-------

Create a file :code:`config.yaml` with the following contents:

.. code-block:: yaml

   server:
     host: !or [!env HOST, localhost]
     port: !or [!env PORT, 8000]
   debug: !env DEBUG
   database:
     name: my_database
     user: my_user
     password: !env DB_PASSWORD
     secret: !aws/sm secret

Then, in Python:

.. code-block:: python

  from miniscule import read_config

  config = read_config('config.yaml')

Now, :code:`config` holds a dictionary with the structure of the
:code:`config.yaml` file, in which the tagged fields have been replaced.
