K Network
=========

Development
-----------

If you want to run this project in a `virtualenv`_ to isolate it from
other Python projects on your system, create a virtualenv and activate
it.  Then run ``bin/install-reqs`` to install the dependencies for this
project into your Python environment.

In order to run K Network (or its tests), you'll need a PostgreSQL
database. By default, K Network will look for a PostgreSQL database
named "knet" on localhost.

You may need to create a ``knet/settings/local.py`` file with some
details of your local configuration.  See
``knet/settings/local.sample.py`` for a sample that can be copied to
``knet/settings/local.py`` and modified.

Once this configuration is done, you should be able to run ``./manage.py
syncdb --migrate``, then ``./manage.py runserver`` and access the site
in your browser at ``http://localhost:8000``.

You can run the tests with ``py.test``, or the `Selenium`_ tests with
``py.test knet/tests/selenium``.

.. _virtualenv: http://www.virtualenv.org
.. _Selenium: http://seleniumhq.org

To install the necessary Ruby gems for Compass/Sass development (only
necessary if you plan to modify Sass files and re-generate CSS), install
Bundler (``gem install bundler``) and then run ``bundle install``.

If you make changes to the client-side Handlebars templates in
``jstemplates/``, run ``bin/grunt`` to recompile the templates.
Alternatively, run ``bin/grunt watch`` (takes over a terminal) to watch for
changes to the templates and recompile automatically.

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
