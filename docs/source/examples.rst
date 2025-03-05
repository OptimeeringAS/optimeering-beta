Code Examples
========

You can see full working examples in our Github repository: https://github.com/OptimeeringAS/optimeering-beta/tree/main/examples

==============================
Working with Prediction Series
==============================

The following examples show how to use the ``list_series`` method to get the prediction series you want to work with, and then retrieve predction events.

``list_series`` allows for the following filter parameters:

* product
* unit_type
* statistic
* area

You can find the available values for each parameter by using the ``list_parameters`` method. For example to get the availabe ``area`` values:

.. code-block:: python

    areas = client.predictions_api.list_parameters("area")

The above returns a dictionary, where the keys are the values that can be used in the filters.

.. code-block:: json

    {
        "SE2": null,
        "SE1": null,
        "FI": "Price area for Finland",
        "NO4": null,
        "NO3": null,
        "DK2": null,
        "SE4": null,
        "DK1": null,
        "NO2": null,
        "NO5": null,
        "SE3": null,
        "NO1": null
    }

You can then, for example, use list comprehension to filter out only the Norwegian areas:

.. code-block:: python

    norwegian_areas = [area for area in areas.keys() if "NO" in area]

    # [
    #     "NO4",
    #     "NO3",
    #     "NO2",
    #     "NO5",
    #     "NO1"
    # ]

This can then be used when retrieving the prediction series:

.. code-block:: python

    series = client.predictions_api.list_series(area=norwegian_areas)

The ``series`` object above is of type :any:`PredictionsSeriesList`. If you like to explore the series as a Pandas dataframe, you can call ``to_pandas()`` on this object.

You can also easily filter a :any:`PredictionsSeriesList` by using the ``filter()`` method. This method takes in the same filters as you can use when calling ``list_series``. 

It can also be used to filter on other parameters of a :any:`PredictionSeries` such as ``unit`` and ``id``. For example, to filter out only series with a ``product`` of ``Imbalance`` and ``statistic`` of ``Point``:

.. code-block:: python

    filtered_series = series.filter(product=["Imbalance"], statistic=["Point"])

.. note::
    Remember that the arguments of ``filter()`` and ``list_series()`` are lists, so you can filter on multiple values for each parameter.

    You should always try to pass as many filters into ``list_series()`` as possible, as this will reduce the amount of data that needs to be transferred from the server to your client.

Now that we have the appropriate series, we can retrieve the prediction events for these series, by simply calling the following:

.. code-block:: python

    data = filtered_series.datapoints(start="-P1W")

This is the same as calling the ``retrieve()`` method as shown below. Note that here we are using the ``series_ids`` attribute of the :any:`PredictionsSeriesList` object:

.. code-block:: python

    data = client.predictions_api.retrieve(series=filtered_series.series_ids)

This will return a :any:`PredictionsData` object, which can be converted to a Pandas dataframe by calling ``to_pandas()`` on it, with a ``unpack_value_method``. The ``unpack_value_method`` can be one of:

* ``retain_original``
* ``new_rows``
* ``new_columns``

See the :any:`PredictionsDataList.to_pandas` method for more information on each of the methods.

==============================
Working with Prediction Versions
==============================

The ``list_version`` method takes in the same arguments as the ``list_series`` method. The difference is that it returns a :any:`PredictionsVersionList` object, which contains :any:`PredictionVersion` objects. These have an additional ``version`` field.

:any:`PredictionVersionList` also has a ``filter()`` method, which is useful for selecting the ``version`` you want. For example:

.. code-block:: python

    versions = client.predictions_api.list_version(area=norwegian_areas, product=["Imbalance"], statistic=["Point"])
    filtered_versions = versions.filter(version=["1.2.1"])

To retrieve versioned data you can use the ``retrieve_versioned`` method as shown below:

.. code-block:: python

    data = client.predictions_api.retrieve_versioned(versioned_series=filtered_versions, start="-P1M", include_simulated=True)

Alternatively, you can define the ``versioned_series`` using a list of :any:`VersionedSeries` objects:

.. code-block:: python

    filtered_versions = [
        VersionedSeries(series_id=47, version="1.2.1"),
        VersionedSeries(series_id=47, version="1.3.0")
    ]

    data = client.predictions_api.retrieve_versioned(versioned_series=filtered_versions, start="-P1M", include_simulated=True)

