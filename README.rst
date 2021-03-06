K Network
=========

Development
-----------

If you want to run this project in a `virtualenv`_ to isolate it from other
Python projects on your system, create a Python 3.3 virtualenv and activate it.
Then run ``bin/install-reqs`` to install the dependencies for this project into
your Python environment (you should re-run this whenever any file in the
``requirements/`` directory changes).

In order to run K Network (or its tests), you'll need a PostgreSQL database. By
default, K Network will look for a PostgreSQL database named "knet" on
localhost. To use a different database, set the ``DATABASE_URL`` environment
variable to a Postgres database URL; e.g. ``postgres://user@host/dbname``.

Once this configuration is done, you should be able to run ``./manage.py syncdb
--migrate``, then ``./manage.py runserver`` and access the site in your browser
at ``http://localhost:8000``.

Local development on this project requires `Node.js`_ >= 0.8.0 for JS linting
and tests. To install the necessary Node dependencies, first ``npm install -g
grunt-cli`` (once per system), then ``npm install`` (whenever ``package.json``
changes).

You can run the Python tests with ``py.test`` (or ``grunt pytest``), or the
``Selenium`` tests with ``py.test knet/tests/selenium`` (or ``grunt
selenium``).

You can lint the project's JS with ``grunt jshint`` and run the JS unit tests
with ``grunt qunit``.

You can compile Handlebars templates in the ``jstemplates/`` directory to the
compiled-templates file (``static/js/jstemplates.js``) with ``grunt handlebars``.

Just running ``grunt`` will perform all of the above tasks except the Selenium
tests.

``grunt dev`` will watch for changes to local files and automatically perform
an appropriate selection of the following tasks whenever changes are detected
to files in the ``static/js/``, ``jstests/``, ``jstemplates/``, ``templates/``
and ``knet/`` directories:

* compile Handlebars templates
* validate JS with `JSHint`_
* run the JS unit tests
* run the Python tests

Refer to the Gruntfile.js source and `Grunt`_ documentation for more info.

To install the necessary Ruby gems for Compass/Sass development (only
necessary if you plan to modify Sass files and re-generate CSS), install
Bundler (``gem install bundler``) and then run ``bundle install``.

.. _virtualenv: http://www.virtualenv.org
.. _Node.js: http://nodejs.org
.. _JSHint: http://www.jshint.com
.. _Grunt: http://gruntjs.com/

Deployment
----------

In addition to the above configuration, in any production deployment
this entire app should be served exclusively over HTTPS (since serving
authenticated pages over HTTP invites session hijacking
attacks). Ideally, the non-HTTP URLs should redirect to the HTTPS
version.

To turn on settings appropriate for a production deployment, set the
environment variable ``KNET_MODE=prod``.

You can run ``./manage.py checksecure`` to verify that settings are correctly
configured for a secure deployment.

This app also uses the `staticfiles contrib app`_ in Django for collecting
static assets from reusable components into a single directory for production
serving.  Under "runserver" in development this is handled automatically.  In
production, run ``./manage.py collectstatic`` to collect all static assets
using the storage engine configured by the ``KNET_STATICFILES_STORAGE`` env
var, and make those collected assets available by HTTP at ``KNET_STATIC_URL``.

.. _staticfiles contrib app: http://docs.djangoproject.com/en/1.5/howto/static-files/
