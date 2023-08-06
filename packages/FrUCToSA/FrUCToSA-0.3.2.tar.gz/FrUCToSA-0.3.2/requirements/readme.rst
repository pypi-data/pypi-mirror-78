 Each file in the "requirements" is meant to have a list of packages needed to work
with FrUCToSA.

For instance,

* ``devel.text`` for development (tox uses this for testing, see ``tox.ini``)
* ``production.text`` for normal usage of FrUCToSA (the ``setup.py`` should provision
  this, though)

They can be used to set up the virtual environment with::

  (venv) $ pip install -r requirements/devel.text

for instance.



