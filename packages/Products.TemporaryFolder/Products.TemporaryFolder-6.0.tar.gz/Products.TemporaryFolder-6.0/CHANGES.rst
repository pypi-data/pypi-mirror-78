Changelog
=========

6.0 (2020-09-01)
----------------

- split ``Products.ZODBMountPoint`` into separate package
  and removed all code that automatically instatiates a temporary
  folder and sessioning artifacts on Zope startup.
  (`#12
  <https://github.com/zopefoundation/Products.TemporaryFolder/issues/12>`_)


5.3 (2019-04-15)
----------------

- improve the README

- Specify supported Python versions using ``python_requires`` in setup.py
  (`Zope#481 <https://github.com/zopefoundation/Zope/issues/481>`_)

- Added support for Python 3.8


5.2 (2018-11-06)
----------------

- Add support for Python 3.7.

- Update forms to Bootstrap ZMI.
  (`#6 <https://github.com/zopefoundation/Products.TemporaryFolder/pull/6>`_)

- Fix logging traceback in Python 2.
  [pbauer]

- Fix creating a temp_folder in Python 2.
  (`#7 <https://github.com/zopefoundation/Products.TemporaryFolder/pull/7>`_)


5.1 (2018-06-06)
----------------

- Bring back Application initialization (creation of BrowserIdManager and
  SessionDataManager in the ZODB on first startup).
  This release requires Zope >= 4.0b5.

- Drop support for Python 3.4.


5.0 (2018-04-13)
----------------

- Remove dysfunctional LowConflictConnection.

- Add support for Python 3.4, 3.5 and 3.6.

4.0 (2016-08-02)
----------------

- Add in code of `Products.TemporaryFolder` and `Products.ZODBMountPoint`.

- Require `Zope >= 4`.

3.0 (2016-08-02)
----------------

- Create a separate distribution called `Products.TemporaryFolder` without
  any code inside it. This allows projects to depend on this project
  inside the Zope 2.13 release line.

