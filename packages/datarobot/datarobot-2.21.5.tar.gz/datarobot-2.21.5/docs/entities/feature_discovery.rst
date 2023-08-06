.. _feature_discovery:

#################
Feature Discovery
#################
The Feature Discovery Project allows the user to generate features automatically
from the secondary datasets which is connect to the Primary dataset(Training dataset).
User can create such connection using Relationships Configuration.

Register Primary Dataset to start Project
*****************************************
To start the Feature Discovery Project you need to upload the primary (training) dataset
:ref:`projects`

.. code-block:: python

    import datarobot as dr
    >>> primary_dataset = dr.Dataset.create_from_file(file_path='your-training_file.csv')
    >>> project = dr.Project.create_from_dataset(primary_dataset.id, project_name='Lending Club')

Now, register all the secondary datasets which you want to connect with primary (training) dataset
and among themselves.

Register Secondary Dataset(s) in AI Catalog
*******************************************
You can register the dataset using
:meth:`Dataset.create_from_file<datarobot.Dataset.create_from_file>` which can take either a path to a
local file or any stream-able file object.

.. code-block:: python

    >>> profile_dataset = dr.Dataset.create_from_file(file_path='your_profile_file.csv')
    >>> transaction_dataset = dr.Dataset.create_from_file(file_path='your_transaction_file.csv')

Create Relationships Configuration
**********************************

Create the relationships configuration among the profile_dataset and transaction_dataset created above.

.. code-block:: python

    >>> profile_catalog_id = profile_dataset.id
    >>> profile_catalog_version_id = profile_dataset.version_id

    >>> transac_catalog_id = transaction_dataset.id
    >>> transac_catalog_version_id = transaction_dataset.version_id

    >>> dataset_definitions = [
        {
            'identifier': 'transaction',
            'catalogVersionId': transac_catalog_version_id,
            'catalogId': transac_catalog_id,
            'primaryTemporalKey': 'Date',
            'snapshotPolicy': 'latest',
        },
        {
            'identifier': 'profile',
            'catalogId': profile_catalog_id,
            'catalogVersionId': profile_catalog_version_id,
            'snapshotPolicy': 'latest',
        },
    ]

    >>> relationships = [
        {
            'dataset2Identifier': 'profile',
            'dataset1Keys': ['CustomerID'],
            'dataset2Keys': ['CustomerID'],
            'featureDerivationWindowStart': -14,
            'featureDerivationWindowEnd': -1,
            'featureDerivationWindowTimeUnit': 'DAY',
            'predictionPointRounding': 1,
            'predictionPointRoundingTimeUnit': 'DAY',
        },
        {
            'dataset1Identifier': 'profile',
            'dataset2Identifier': 'transaction',
            'dataset1Keys': ['CustomerID'],
            'dataset2Keys': ['CustomerID'],
        },
    ]

    # Create the relationships configuration to define connection between the datasets
    >>> relationship_config = dr.RelationshipsConfiguration.create(dataset_definitions=dataset_definitions, relationships=relationships)

Create Feature Discovery Project
********************************

Once done with relationships configuration you can start the Feature Discovery project

.. code-block:: python

    # Set the date-time partition column which is date here
    >>> partitioning_spec = dr.DatetimePartitioningSpecification('date')

    # Set the target for the project and start Feature discovery
    >>> project.set_target(target='BadLoan', relationships_configuration_id=relationship_config.id, mode='manual', partitioning_method=partitioning_spec)
    Project(train.csv)

Common Errors
-------------
Dataset registration Failed
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    datasetdr.Dataset.create_from_file(file_path='file.csv')
    datarobot.errors.AsyncProcessUnsuccessfulError: The job did not complete successfully.

Solution

* Check the internet connectivity sometimes network flakiness cause upload error
* Is the dataset file too big then you might want to upload using URL rather than file


Creating relationships configuration throws some error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    datarobot.errors.ClientError: 422 client error: {u'message': u'Invalid field data',
    u'errors': {u'datasetDefinitions': {u'1': {u'identifier': u'value cannot contain characters: $ - " . { } / \\'},
    u'0': {u'identifier': u'value cannot contain characters: $ - " . { } / \\'}}}}

Solution:

* Check the identifier name passed in datasets_definitions and relationships
* ``Pro tip: Dont use name of the dataset if you didnt specified the name of the dataset explicitly while registration``

.. code-block:: python

    datarobot.errors.ClientError: 422 client error: {u'message': u'Invalid field data',
    u'errors': {u'datasetDefinitions': {u'1': {u'primaryTemporalKey': u'date column doesnt exist'},
    }}}

Solution:

* Check if the name of the column passed as primaryTemporalKey is correct, its case-senstive