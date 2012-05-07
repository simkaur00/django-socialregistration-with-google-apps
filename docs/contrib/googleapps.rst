Google Apps
======

- Add ``socialregistration.contrib.openid`` to your ``INSTALLED_APPS``

::

	INSTALLED_APPS = (
		'socialregistration',
		'socialregistration.contrib.googleapps'
	)


- Add ``socialregistration.contrib.openid.auth.OpenIDAuth`` to your ``AUTHENTICATION_BACKENDS``

::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'socialregistration.contrib.openid.auth.OpenIDAuth',
    )

- Anywhere in your templates:

::

	{% load googleapps %}
	{% googleapps_form %}

- If you are writing a Google Apps Marketplace application, add the following to your appmanifest.xml

::

      <Extension id="navLink" type="link">
        <Name>[Your App Name]</Name
        <Url>http://[[Your Site]]/[[socialregistration root]]/googleapps/redirect/?domain=${DOMAIN_NAME}</Url>
      </Extension>
