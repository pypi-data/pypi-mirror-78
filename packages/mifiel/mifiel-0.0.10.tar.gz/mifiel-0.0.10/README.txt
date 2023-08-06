Mifiel Python Library
=====================

|Coverage Status| |Build Status| |PyPI version|

Pyton library for `Mifiel <https://www.mifiel.com>`__ API. Please read
our `documentation <http://docs.mifiel.com>`__ for instructions on how
to start using the API.

Installation
------------

.. code:: bash

    pip install mifiel

Usage
-----

To start using the API you will need an APP\_ID and a APP\_SECRET which
will be provided upon request (contact us at hola@mifiel.com).

You will first need to create an account in
`mifiel.com <https://www.mifiel.com>`__ since the APP\_ID and
APP\_SECRET will be linked to your account.

Document methods:
~~~~~~~~~~~~~~~~~

For now, the only methods available are **find** and **create**.
Contributions are greatly appreciated.

-  Find:

.. code:: python

    from mifiel import Document, Client
    client = Client(app_id='APP_ID', secret_key='APP_SECRET')

    doc = Document.find(client, 'id')
    document.original_hash
    document.file
    document.file_signed
    # ...

-  Create:

.. code:: python

    from mifiel import Document, Client
    client = Client(app_id='APP_ID', secret_key='APP_SECRET')

    signatories = [
      { 
        'name': 'Signer 1', 
        'email': 'signer1@email.com', 
        'tax_id': 'AAA010101AAA' 
      },
      { 
        'name': 'Signer 2', 
        'email': 
        'signer2@email.com', 
        'tax_id': 'AAA010102AAA'
      }
    ]
    # Providde the SHA256 hash of the file you want to sign.
    doc = Document.create(client, signatories, dhash='some-sha256-hash')
    # Or just send the file and we'll take care of everything.
    # We will store the file for you. 
    doc = Document.create(client, signatories, file='test/fixtures/example.pdf')

    doc.id # -> '7500e528-ac6f-4ad3-9afd-74487c11576a'
    doc.id # -> '7500e528-ac6f-4ad3-9afd-74487c11576a'

-  Save Document related files

.. code:: python

    from mifiel import Document, Client
    client = Client(app_id='APP_ID', secret_key='APP_SECRET')

    doc = Document.find(client, 'id')
    # save the original file
    doc.save_file('path/to/save/file.pdf')
    # save the signed file (original file + signatures page)
    doc.save_file_signed('path/to/save/file-signed.pdf')
    # save the signed xml file
    doc.save_xml('path/to/save/xml.xml')

Development
-----------

Install dependencies
~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    pip install -r requirements.txt

Test
----

Just clone the repo, install dependencies as you would in development
and run ``nose2`` or ``python setup.py test``

Contributing
------------

1. Fork it ( https://github.com/Mifiel/python-api-client/fork )
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create a new Pull Request

.. |Coverage Status| image:: https://coveralls.io/repos/github/Mifiel/python-api-client/badge.svg?branch=master
   :target: https://coveralls.io/github/Mifiel/python-api-client?branch=master
.. |Build Status| image:: https://travis-ci.org/Mifiel/python-api-client.svg?branch=master
   :target: https://travis-ci.org/Mifiel/python-api-client
.. |PyPI version| image:: https://badge.fury.io/py/mifiel.svg
   :target: https://badge.fury.io/py/mifiel
