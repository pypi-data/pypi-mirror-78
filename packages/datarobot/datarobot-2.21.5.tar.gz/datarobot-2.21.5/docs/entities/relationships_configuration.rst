.. _relationships_configuration:

###########################
Relationships Configuration
###########################
A Relationships configuration specifies specifies additional datasets to be included to a project
and how these datasets are related to each other, and the primary dataset.
When a relationships configuration is specified for a project,
Feature Discovery will create features automatically from these datasets.


Create Relationships Configuration
**********************************
You can create a relationships configuration from the uploaded catalog items.
After uploading all the secondary datasets in the AI Catalog

- Create the datasets definiton to define which datasets to be used as secondary datasets along with its details
- Create the relationships among the above datasets


.. code-block:: python

    import datarobot as dr
    # Example of LendingClub project which has two datasets profile and transaction
    >>> dataset_definitions = [
        {
            'identifier': 'transaction',
            'catalogVersionId': '5ec4aec268f0f30289a03901',
            'catalogId': '5ec4aec268f0f30289a03900',
            'primaryTemporalKey': 'Date',
            'snapshotPolicy': 'latest',
        },
        {
            'identifier': 'profile',
            'catalogId': '5ec4aec1f072bc028e3471ae',
            'catalogVersionId': '5ec4aec2f072bc028e3471b1',
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
    >>> relationship_config = dr.RelationshipsConfiguration.create(dataset_definitions=dataset_definitions, relationships=relationships)

You can use the following commands to view the relationships configuration ID:

.. code-block:: python

    >>> relationship_config.id
    u'5506fcd38bd88f5953219da0'

Retrieving Relationships Configuration
**************************************

You can retrieve specific relationships configuration using the ID


.. code-block:: python

    >>> relationship_config_id = '5506fcd38bd88f5953219da0'
    >>> relationship_config = dr.RelationshipsConfiguration(id=relationship_config_id).get()
    >>> relationship_config.id == relationship_config_id
    True
    # Get all the datasets used in this relationships configuration
    >> len(relationship_config.dataset_definitions) == 2
    True
    >> relationship_config.dataset_definitions[0]
    {
        'feature_list_id': '5ec4af93603f596525d382d3',
        'snapshot_policy': 'latest',
        'catalog_id': '5ec4aec268f0f30289a03900',
        'catalog_version_id': '5ec4aec268f0f30289a03901',
        'primary_temporal_key': 'Date',
        'is_deleted': False,
        'identifier': 'transaction',
        'feature_lists':
            [
                {
                    'name': 'Raw Features',
                    'description': 'System created featurelist',
                    'created_by': 'User1',
                    'creation_date': datetime.datetime(2020, 5, 20, 4, 18, 27, 150000, tzinfo=tzutc()),
                    'user_created': False,
                    'dataset_id': '5ec4aec268f0f30289a03900',
                    'id': '5ec4af93603f596525d382d1',
                    'features': [u'CustomerID', u'AccountID', u'Date', u'Amount', u'Description']
                },
                {
                    'name': 'universe',
                    'description': 'System created featurelist',
                    'created_by': 'User1',
                    'creation_date': datetime.datetime(2020, 5, 20, 4, 18, 27, 172000, tzinfo=tzutc()),
                    'user_created': False,
                    'dataset_id': '5ec4aec268f0f30289a03900',
                    'id': '5ec4af93603f596525d382d2',
                    'features': [u'CustomerID', u'AccountID', u'Date', u'Amount', u'Description']
                },
                {
                    'features': [u'CustomerID', u'AccountID', u'Date', u'Amount', u'Description'],
                    'description': 'System created featurelist',
                    'created_by': u'Garvit Bansal',
                    'creation_date': datetime.datetime(2020, 5, 20, 4, 18, 27, 179000, tzinfo=tzutc()),
                    'dataset_version_id': '5ec4aec268f0f30289a03901',
                    'user_created': False,
                    'dataset_id': '5ec4aec268f0f30289a03900',
                    'id': u'5ec4af93603f596525d382d3',
                    'name': 'Informative Features'
                }
            ]
    }
    # Get information regarding how the datasets are connected among themselves as well as primary dataset
    >> relationship_config.relationships
    [
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

Updating details of Relationships Configuration
***********************************************

You can update the details of the relationships configuration


.. code-block:: python

    >>> relationship_config_id = '5506fcd38bd88f5953219da0'
    >>> relationship_config = dr.RelationshipsConfiguration(id=relationship_config_id)
    # Remove the obsolete datasets definition and its relationships
    >>> new_datasets_definiton =
    [
        {
            'identifier': 'user',
            'catalogVersionId': '5c88a37770fc42a2fcc62759',
            'catalogId': '5c88a37770fc42a2fcc62759',
            'snapshotPolicy': 'latest',
        },
    ]

    # Get information regarding how the datasets are connected among themselves as well as primary dataset
    >>> new_relationships =
    [
        {
            'dataset2Identifier': 'user',
            'dataset1Keys': ['user_id', 'dept_id'],
            'dataset2Keys': ['user_id', 'dept_id'],
        },
    ]
    >>> new_config = relationship_config.replace(new_datasets_definiton, new_relationships)
    >>> new_config.id == relationship_config_id
    True
    >>> new_config.datasets_definition
    [
        {
            'identifier': 'user',
            'catalogVersionId': '5c88a37770fc42a2fcc62759',
            'catalogId': '5c88a37770fc42a2fcc62759',
            'snapshotPolicy': 'latest',
        },
    ]
    >>> new_config.relationships
    [
        {
            'dataset2Identifier': 'user',
            'dataset1Keys': ['user_id', 'dept_id'],
            'dataset2Keys': ['user_id', 'dept_id'],
        },
    ]

Delete Relationships Configuration
**********************************

You can delete the relationships configuration which is not used by any project

.. code-block:: python

    >>> relationship_config_id = '5506fcd38bd88f5953219da0'
    >>> relationship_config = dr.RelationshipsConfiguration(id=relationship_config_id)
    >>> result = relationship_config.get()
    >>> result.id == relationship_config_id
    True
    # Delete the relationships configuration
    >>> relationship_config.delete()
    >>> relationship_config.get()
    ClientError: Relationships Configuration 5506fcd38bd88f5953219da0 not found
