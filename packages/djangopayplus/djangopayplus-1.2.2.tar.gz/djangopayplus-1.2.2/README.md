# Momo Payment Package

A mobile money payment package.


Requirements
---

* python > 3.5.x
* django > 2.2.x
* djangorestframework > 3.11.x
* requests > 2.24.x


### ***Nb***: Use a python env for project isolation


Quick start
-----------

1. Add "momo_pay" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...\
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'momopay',\
    ]

2. Include the momo_pay URLconf in your project urls.py like this::

    path('momo_pay/', include('momopay.urls')),

3. Run ``python manage.py migrate`` to create the momopay models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a payment (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/momopay/ to participate in the poll.