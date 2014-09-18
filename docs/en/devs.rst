===========
Development
===========


The project is open to all contributions, the easiest way is to start by forking
the `project <https://github.com/possum-software/possum/>`_ and consult
tasks list: `Issues <https://github.com/possum-software/possum/issues>`_.

Version number
==============

Here the development cycle adopted for release version:

.. image:: ../images/cycle_of_versions.png
   :alt: Development cycle

An example for version 1.0:

* 1.0.rc?: additions of features are blocked, only bug fixes
* 1.0: stable version
* 1.0.1: only bug fixes on stable version

Coding convention
=================

The coding convention used for the project following the
`Style Guide for Python Code (PEP 8) <http://www.python.org/dev/peps/pep-0008/>`_.

Compliance with agreements is verified by Jenkins,
the results are available here:
`Jenkins <http://jenkins.possum-software.org/>`_.

In short:

* tabulation must be 4 spaces
* maximum line length: 79 characters (and 72 for docstrings/comments)

How to contribute
=================

Firstly, you must have an account on `Github <https://github.com>`_.

You have to create a fork `here <https://github.com/possum-software/possum>`_
(top right).

Now, you will use your fork. This is an example with my username 
**sbonnegent**. Full documentation is on
`Github (fork a repo) <https://help.github.com/articles/fork-a-repo>`_.

In short::

  $ git clone git@github.com:sbonnegent/possum.git possum-software
  $ cd possum-software
  $ git remote add upstream git@github.com:possum-software/possum.git
  $ git fetch upstream
  $ cp possum/settings_dev.py possum/settings.py
  $ ./make update
  $ echo "make changes"
  $ git commit -a -m "cool stuff"
  $ git push

Changes are in your fork, now you can create a pull request directly on Github.

After that, you must check state of your request on
`Jenkins (pull_requests) <http://jenkins.possum-software.org/job/pull_requests/violations/>`_.
if the number of violations is up, your request will not be accepted.

You can fetch any new changes from the original repository and merge it
to your fork with::

  $ git fetch upstream
  $ git merge upstream/dev

Or view differences with::

  $ git diff upstream/dev

Change in class
===============

After any change in the definitions of models, it will
update patterns with South and demo data. This command
will do it for us:

::

  ./make models_changed


Remenber to add new migration file on git.

Base
====

Main class in this part is Facture_.

.. image:: ../images/models-base.png
   :height: 100
   :width: 200
   :scale: 50
   :alt: Schéma des classes d'objets

Categorie
---------
.. automodule:: possum.base.models.category
   :members:

Config
------
.. automodule:: possum.base.models.config
   :members:

Facture
-------
.. automodule:: possum.base.models.bill
   :members:

Follow
------
.. automodule:: possum.base.models.follow
   :members:

Generic
-------
.. automodule:: possum.base.models.generic
   :members:

Location
--------
.. automodule:: possum.base.models.location
   :members:

Options
-------
.. automodule:: possum.base.models.options
   :members:

Payment
--------
.. automodule:: possum.base.models.payment
   :members:

Printer
-------
.. automodule:: possum.base.models.printer
   :members:

Produit
-------
.. automodule:: possum.base.models.product
   :members:

ProduitVendu
------------
.. automodule:: possum.base.models.product_sold
   :members:

VAT
---
.. automodule:: possum.base.models.vat
   :members:

VATOnBill
---------
.. automodule:: possum.base.models.vatonbill
   :members:

Stats
=====

.. image:: ../images/models-stats.png
   :height: 100
   :width: 200
   :scale: 50
   :alt: Schéma des classes d'objets

.. automodule:: possum.stats.models
   :members:

