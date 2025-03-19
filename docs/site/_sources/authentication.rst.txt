Authentication
==============

The client can be authenticated against the API using either OAuth (personal credentials) or API Keys.

====================
OAuth Authentication
====================

--------------
Pre requisites
--------------

The Azure CLI simplifies the process of acquiring an access token that can be used when making requests.
Follow `How to install the Azure CLI <https://learn.microsoft.com/en-us/cli/azure/install-azure-cli/>`_ if you haven't installed it yet.

-----------------------------
Signing in with the Azure CLI
-----------------------------

In your terminal run:

.. code-block:: console

    az login --scope api://beta.optimeering.com/.default --allow-no-subscriptions

----------------------
Configuring the Client
----------------------

The client will automatically use the credentials gained from the step above, so all you have to do is create it with the default configuration:

.. code-block:: python

    from optimeering_beta import OptimeeringClient
    client = OptimeeringClient()

======================
API Key Authentication
======================

--------------
Pre requisites
--------------

You will need to first generate an API Key. The easiest way to do that is by using the `/api/access/apikey/create <https://beta.optimeering.com/api/docs/auth/#/access/create_api_key/>`_

----------------------
Configuring the Client
----------------------

.. code-block:: python

    from optimeering_beta import Configuration, OptimeeringClient
    configuration = Configuration(api_key="SecretKeyHere")
    client = OptimeeringClient(configuration=configuration)

