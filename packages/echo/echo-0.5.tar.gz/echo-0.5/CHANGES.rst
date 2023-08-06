Full changelog
==============

0.5 (2020-11-08)
----------------

* Add the ability to specify for ``SelectionCallbackProperty`` whether to
  compare choices using equality or identity. [#26]

* Fixed an issue that could lead to ``CallbackContainer`` returning dead
  weak references during iteration. [#27]

0.4 (2020-05-04)
----------------

* Added the ability to add arbitrary callbacks to ``CallbackDict`` and
 ``CallbackList`` via the ``.callbacks`` attribute. [#25]

0.3 (2020-05-04)
----------------

* Fix setting of defaults in callback list and dict properties. [#24]

0.2 (2020-04-11)
----------------

* Python 3.6 or later is now required. [#20]

* Significant refactoring of the package. [#20]

0.1 (2014-03-13)
----------------

* Initial version
