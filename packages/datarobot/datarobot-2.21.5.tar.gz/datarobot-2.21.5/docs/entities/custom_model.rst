.. _custom_models:

#############
Custom Models
#############

Custom models provide users the ability to run arbitrary modeling code in an environment defined by the user.

Manage Execution Environments
*****************************

Execution Environment defines the runtime environment for custom models.
Execution Environment Version is a revision of Execution Environment with an actual runtime definition.
Please refer to DataRobot User Models (https://github.com/datarobot/datarobot-user-models) for sample
environments.

Create Execution Environment
===============================

To create an Execution Environment run:

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.create(
        name="Python3 PyTorch Environment",
        description="This environment contains Python3 pytorch library.",
    )

    execution_environment.id
    >>> '5b6b2315ca36c0108fc5d41b'

There are 2 ways to create an Execution Environment Version: synchronous and asynchronous.

Synchronous way means that program execution will be blocked until an Execution Environment Version
creation process is finished with either success or failure:

.. code-block:: python

    import datarobot as dr

    # use execution_environment created earlier

    environment_version = dr.ExecutionEnvironmentVersion.create(
        execution_environment.id,
        docker_context_path="datarobot-user-models/public_dropin_environments/python3_pytorch",
        max_wait=3600,  # 1 hour timeout
    )

    environment_version.id
    >>> '5eb538959bc057003b487b2d'
    environment_version.build_status
    >>> 'success'

Asynchronous way means that program execution will be not blocked, but an Execution Environment Version
created will not be ready to be used for some time, until it's creation process is finished.
In such case, it will be required to manually call :meth:`~datarobot.ExecutionEnvironmentVersion.refresh`
for the Execution Environment Version and check if its `build_status` is "success".
To create an Execution Environment Version without blocking a program, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    # use execution_environment created earlier

    environment_version = dr.ExecutionEnvironmentVersion.create(
        execution_environment.id,
        docker_context_path="datarobot-user-models/public_dropin_environments/python3_pytorch",
        max_wait=None,  # set None to not block execution on this method
    )

    environment_version.id
    >>> '5eb538959bc057003b487b2d'
    environment_version.build_status
    >>> 'processing'

    # after some time
    environment_version.refresh()
    environment_version.build_status
    >>> 'success'

List Execution Environments
===========================

Use the following command to list execution environments available to the user.

.. code-block:: python

    import datarobot as dr

    execution_environments = dr.ExecutionEnvironment.list()
    execution_environments
    >>> [ExecutionEnvironment('[DataRobot] Python 3 PyTorch Drop-In'), ExecutionEnvironment('[DataRobot] Java Drop-In')]

    environment_versions = dr.ExecutionEnvironmentVersion.list(execution_environment.id)
    environment_versions
    >>> [ExecutionEnvironmentVersion('v1')]

Refer to :class:`~datarobot.ExecutionEnvironment` for properties of the execution environment object and
:class:`~datarobot.ExecutionEnvironmentVersion` for properties of the execution environment object version.

You can also filter the execution environments that are returned by passing a string as `search_for` parameter -
only the execution environments that contain the passed string in name or description will be returned.

.. code-block:: python

    import datarobot as dr

    execution_environments = dr.ExecutionEnvironment.list(search_for='java')
    execution_environments
    >>> [ExecutionEnvironment('[DataRobot] Java Drop-In')]

Execution environment versions can be filtered by build status.

.. code-block:: python

    import datarobot as dr

    environment_versions = dr.ExecutionEnvironmentVersion.list(
        execution_environment.id, dr.EXECUTION_ENVIRONMENT_VERSION_BUILD_STATUS.PROCESSING
    )
    environment_versions
    >>> [ExecutionEnvironmentVersion('v1')]

Retrieve Execution Environment
=================================

To retrieve an execution environment and an execution environment version by identifier,
rather than list all available ones, do the following:

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.get(execution_environment_id='5506fcd38bd88f5953219da0')
    execution_environment
    >>> ExecutionEnvironment('[DataRobot] Python 3 PyTorch Drop-In')

    environment_version = dr.ExecutionEnvironmentVersion.get(
        execution_environment_id=execution_environment.id, version_id='5eb538959bc057003b487b2d')
    environment_version
    >>> ExecutionEnvironmentVersion('v1')

Update Execution Environment
===============================

To update name and/or description of the execution environment run:

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.get(execution_environment_id='5506fcd38bd88f5953219da0')
    execution_environment.update(name='new name', description='new description')

Delete Execution Environment
===============================

To delete the execution environment and execution environment version, use the following commands.

.. code-block:: python

    import datarobot as dr

    execution_environment = dr.ExecutionEnvironment.get(execution_environment_id='5506fcd38bd88f5953219da0')
    execution_environment.delete()

Get Execution Environment build log
======================================

To get execution environment version build log run:

.. code-block:: python

    import datarobot as dr

    environment_version = dr.ExecutionEnvironmentVersion.get(
        execution_environment_id='5506fcd38bd88f5953219da0', version_id='5eb538959bc057003b487b2d')
    log, error = environment_version.get_build_log()

Manage Custom Models
********************

Custom Inference Model is user-defined modeling code that supports making predictions against it.
Custom Inference Model supports regression and binary classification target types.

To upload actual modeling code Custom Model Version must be created for a custom model.
Please see :ref:`Custom Model Version documentation <custom_model_versions>`.

Create Custom Inference Model
=============================

To create a regression Custom Inference Model run:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.REGRESSION,
        target_name='MEDV',
        description='This is a Python3-based custom model. It has a simple PyTorch model built on boston housing',
        language='python'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

When creating a binary classification Custom Inference Model,
`positive_class_label` and `negative_class_label` must be set:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.create(
        name='Python 3 PyTorch Custom Model',
        target_type=dr.TARGET_TYPE.BINARY,
        target_name='readmitted',
        positive_class_label='False',
        negative_class_label='True',
        description='This is a Python3-based custom model. It has a simple PyTorch model built on 10k_diabetes dataset',
        language='Python 3'
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'


List Custom Inference Models
============================

Use the following command to list Custom Inference Models available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomInferenceModel.list()
    >>> [CustomInferenceModel('my model 2'), CustomInferenceModel('my model 1')]

    # use these parameters to filter results:
    dr.CustomInferenceModel.list(
        is_deployed=True,  # set to return only deployed models
        order_by='-updated',  # set to define order of returned results
        search_for='model 1',  # return only models containing 'model 1' in name or description
    )
    >>> CustomInferenceModel('my model 1')

Please refer to :meth:`~datarobot.CustomInferenceModel.list` for detailed parameter description.

Retrieve Custom Inference Model
===============================

To retrieve a specific Custom Inference Model, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomInferenceModel.get('5ebe95044024035cc6a65602')
    >>> CustomInferenceModel('my model 1')

Update Custom Model
===================

To update Custom Inference Model properties execute the following:

.. code-block:: python

    import datarobot as dr

    custom_model = dr.CustomInferenceModel.get('5ebe95044024035cc6a65602')

    custom_model.update(
        name='new name',
        description='new description',
    )

Please, refer to :meth:`~datarobot.CustomInferenceModel.update` for the full list of properties that can be updated.

Download latest revision of Custom Inference Model
==================================================

To download content of the latest Custom Model Version of `CustomInferenceModel` as a ZIP archive:

.. code-block:: python

    import datarobot as dr

    path_to_download = '/home/user/Documents/myModel.zip'

    custom_model = dr.CustomInferenceModel.get('5ebe96b84024035cc6a6560b')

    custom_model.download_latest_version(path_to_download)

.. _custom_inference_model_assign_data:

Assign training data to Custom Inference Model
==============================================

To assign training data to Custom Inference Model, run:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/trainingDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model = dr.CustomInferenceModel.get('5ebe96b84024035cc6a6560b')

    custom_model.assign_training_data(dataset.id)

To assign training data without blocking a program, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/trainingDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model = dr.CustomInferenceModel.get('5ebe96b84024035cc6a6560b')

    custom_model.assign_training_data(
        dataset.id,
        max_wait=None
    )

    custom_model.training_data_assignment_in_progress
    >>> True

    # after some time
    custom_model.refresh()
    custom_model.training_data_assignment_in_progress
    >>> False

Note: training data must be assigned to retrieve feature impact from Custom Inference Image.
Please see to :ref:`Custom Inference Image documentation <custom_inference_image_feature_impact>`.

.. _custom_model_versions:

Manage Custom Model Versions
******************************

Modeling code for Custom Inference Models can be uploaded by creating a Custom Model Version.

Create Custom Model Version
===========================

Upload actual custom model content by creating a clean Custom Model Version:

.. code-block:: python

    import os
    import datarobot as dr

    custom_model_folder = "datarobot-user-models/model_templates/python3_pytorch"

    # add files from the folder to the custom model
    model_version = dr.CustomModelVersion.create_clean(
        custom_model_id=custom_model.id,
        folder_path=custom_model_folder,
    )

    custom_model.id
    >>> '5b6b2315ca36c0108fc5d41b'

    # or add a list of files to the custom model
    model_version_2 = dr.CustomModelVersion.create_clean(
        custom_model_id=custom_model.id,
        files=[(os.path.join(custom_model_folder, 'custom.py'), 'custom.py')],
    )

To create a new Custom Model Version from a previous one, with just some files added or removed, do the following:

.. code-block:: python

    import os
    import datarobot as dr

    custom_model_folder = "datarobot-user-models/model_templates/python3_pytorch"

    file_to_delete = model_version_2.items[0].id

    model_version_3 = dr.CustomModelVersion.create_from_previous(
        custom_model_id=custom_model.id,
        files=[(os.path.join(custom_model_folder, 'custom.py'), 'custom.py')],
        files_to_delete=[file_to_delete],
    )

Please refer to :class:`~datarobot.models.custom_model_version.CustomModelFileItem` for description of custom model file properties.

List Custom Model Versions
==========================

Use the following command to list Custom Model Versions available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelVersion.list(custom_model.id)

    >>> [CustomModelVersion('v2.0'), CustomModelVersion('v1.0')]

Retrieve Custom Model Version
=============================

To retrieve a specific Custom Model Version, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelVersion.get(custom_model.id, custom_model_version_id='5ebe96b84024035cc6a6560b')

    >>> CustomModelVersion('v2.0')

Update Custom Model Version
===========================

To update Custom Model Version description execute the following:

.. code-block:: python

    import datarobot as dr

    custom_model_version = dr.CustomModelVersion.get(
        custom_model.id,
        custom_model_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_model_version.update(description='new description')

    custom_model_version.description
    >>> 'new description'

Download Custom Model Version
=============================

Download content of the Custom Model Version as a ZIP archive:

.. code-block:: python

    import datarobot as dr

    path_to_download = '/home/user/Documents/myModel.zip'

    custom_model_version = dr.CustomModelVersion.get(
        custom_model.id,
        custom_model_version_id='5ebe96b84024035cc6a6560b',
    )

    custom_model_version.download(path_to_download)


Manage Custom Model Tests
*************************

A Custom Model Test represents testing performed on custom models.

Create Custom Model Test
========================

To create Custom Model Test, run:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/testDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        environment_id=execution_environment.id,
        environment_version_id=environment_version.id,
        dataset_id=dataset.id,
        max_wait=3600,  # 1 hour timeout
    )

    custom_model_test.overall_status
    >>> 'succeeded'

To start Custom Model Test without blocking a program until the test finishes, set `max_wait` to `None`:

.. code-block:: python

    import datarobot as dr

    path_to_dataset = '/home/user/Documents/testDataset.csv'
    dataset = dr.Dataset.create_from_file(file_path=path_to_dataset)

    custom_model_test = dr.CustomModelTest.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        environment_id=execution_environment.id,
        environment_version_id=environment_version.id,
        dataset_id=dataset.id,
        max_wait=None,
    )

    custom_model_test.overall_status
    >>> 'in_progress'

    # after some time
    custom_model_test.refresh()
    custom_model_test.overall_status
    >>> 'succeeded'

In case a test fails, do the following to examine details of the failure:

.. code-block:: python

    for name, test in custom_model_test.detailed_status.items():
        print('Test: {}'.format(name))
        print('Status: {}'.format(test['status']))
        print('Message: {}'.format(test['message']))

    print(custom_model_test.get_log())


To cancel a Custom Model Test, simply run:

.. code-block:: python

    custom_model_test.cancel()


List Custom Model Tests
=======================

Use the following command to list Custom Model Tests available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelTest.list(custom_model_id=custom_model.id)
    >>> [CustomModelTest('5ec262604024031bed5aaa16')]

Retrieve Custom Model Test
===========================

To retrieve a specific Custom Model Test, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomModelTest.get(custom_model_test_id='5ec262604024031bed5aaa16')
    >>> CustomModelTest('5ec262604024031bed5aaa16')

.. _custom_inference_image:

Manage Custom Inference Images
******************************

A Custom Inference Image pins a Custom Model, a Custom Model Version, an Execution Environment, and an Execution Environment version.
The pinned image is used when deploying the custom model or when retrieving feature impact.

Create Custom Inference Image
=============================

To create a Custom Inference Image, run:

.. code-block:: python

    import datarobot as dr

    custom_inference_image = dr.CustomInferenceImage.create(
        custom_model_id=custom_model.id,
        custom_model_version_id=model_version.id,
        environment_id=execution_environment.id,
        environment_version_id=environment_version.id,
    )

    custom_inference_image
    >>> CustomInferenceImage('5ec26cfeb5ec7911cdae91b4')

List Custom Inference Images
============================

Use the following command to list Custom Inference Images available to the user:

.. code-block:: python

    import datarobot as dr

    dr.CustomInferenceImage.list()
    >>> [CustomInferenceImage('5ec26cfeb5ec7911cdae91b4')]

    # use these parameters to filter results:
    dr.CustomInferenceImage.list(
        # return only images with specified testing status
        testing_status='succeeded',
        # return only images with specified custom model id
        custom_model_id='5ec26cf25f2cc902bcceefd4',
        # return only images with specified custom model version id
        custom_model_version_id='5ec26cf53f750d11cdcec506',
        # return only images with specified execution environment id
        environment_id='5eb5299e4eda7b021026d696',
        # return only images with specified execution environment version id
        environment_version_id='5eb5299f9bc0570096487b14',
    )
    >>> [CustomInferenceImage('5ec26cfeb5ec7911cdae91b4')]

Please refer to :meth:`~datarobot.CustomInferenceModel.list` for detailed parameter description.

Retrieve Custom Inference Image
===============================

To retrieve a specific Custom Inference Image, run:

.. code-block:: python

    import datarobot as dr

    dr.CustomInferenceImage.get('5ec26cfeb5ec7911cdae91b4')
    >>> CustomInferenceImage('5ec26cfeb5ec7911cdae91b4')

.. _custom_inference_image_feature_impact:

Retrieve Custom Inference Model feature impact
==============================================

To retrieve Custom Inference Model feature impact, training data must be assigned to a Custom Inference Model.
Please refer to :ref:`Custom Inference Model documentation <custom_inference_model_assign_data>`.
If training data is assigned, run the following to get feature impact:

.. code-block:: python

    import datarobot as dr

    image = dr.CustomInferenceImage.get('5ec26cfeb5ec7911cdae91b4')

    image.get_feature_impact()
    >>> [{'featureName': 'B', 'impactNormalized': 1.0, 'impactUnnormalized': 1.1085356209402688, 'redundantWith': 'B'}...]
