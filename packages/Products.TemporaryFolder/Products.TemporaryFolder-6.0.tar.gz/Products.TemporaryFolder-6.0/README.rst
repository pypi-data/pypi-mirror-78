.. image:: https://travis-ci.org/zopefoundation/Products.TemporaryFolder.svg?branch=master
   :target: https://travis-ci.org/zopefoundation/Products.TemporaryFolder

.. image:: https://coveralls.io/repos/github/zopefoundation/Products.TemporaryFolder/badge.svg?branch=master
   :target: https://coveralls.io/github/zopefoundation/Products.TemporaryFolder?branch=master

.. image:: https://img.shields.io/pypi/v/Products.TemporaryFolder.svg
   :target: https://pypi.org/project/Products.TemporaryFolder/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/Products.TemporaryFolder.svg
   :target: https://pypi.org/project/Products.TemporaryFolder/
   :alt: Supported Python versions

Overview
========

Zope temporary storage / folder support.


Please note
-----------
`Temporary Folders` and the `temporarystorage` ZODB storage depend on
the ``tempstorage`` package, which is known to randomly lose data under Zope
4 and up. If you want to use the sessioning support in Zope please visit
https://zope.readthedocs.io/en/latest/zopebook/Sessions.html#alternative-server-side-session-backends-for-zope-4
for alternate sessioning implementations that don't use `Temporary Folder`.

Because it is unsafe, Zope will no longer magically create a
`Temporary Folder` object at ``/temp_folder``. If you think you still need a 
`Temporary Folder`, please add a temporary storage database definition like
the one below to your Zope configuration, restart Zope, and use the ZMI add
list to create an object of type `ZODB Mount Point`. If the storage
configuration is valid you will see a list of configured mount points and the
option to create the container in the ZODB::

  <zodb_db temporary>
      <temporarystorage>
        name Temporary database (for sessions)
      </temporarystorage>
      mount-point /temp_folder
      container-class Products.TemporaryFolder.TemporaryContainer
  </zodb_db>
