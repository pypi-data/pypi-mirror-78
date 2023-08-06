.. _visualai:

##################
Visual AI Projects
##################


Visual AI project support image data for modeling. The modeling
must occur within a project that has one dataset used as the source
to train the models.



Create a Visual AI Project
**************************

Setting up a Visual AI project requires you to create a dataset. The
various ways to do this are covered in detail in DataRobot Platform
Documentation, `Using Visual AI <https://app.datarobot.com/docs/modeling/visual-ai/index.html>`_,
Preparing Your Dataset.

For the examples given here the images are partitioned into named
directories. The named directories serve as the class names that
will be applied to images used in predictions. For example: to predict on
images of food found at a baseball game, then some of the directory names
might be hotdog, hamburger, and popcorn.

::

    /home/user/data/imagedataset
        ├── hamburger
        │   ├── hamburger01.jpg
        │   ├── hamburger02.jpg
        │   ├── …
        └── hotdog
            ├── hotdog01.jpg
            ├── hotdog02.jpg
            ├── …


You then compress the directory containing the named directories into a
ZIP file, creating the dataset used for the project.

.. code-block:: python

    from datarobot.models import Project, Dataset
    dataset = Dataset.create_from_file(file_path='/home/user/data/imagedataset.zip')
    project = Project.create_from_dataset(dataset.id, project_name='My Image Project')


Target
======

Since this example uses named directories the target name must be
``class``, which will contain the name of each directory in the ZIP
file. 



Other Parameters
================

Setting modeling parameters, such as partitioning method, queue mode,
etc, functions in the same way as starting a non-image project.



Start Modeling
**************

Once you have set modeling parameters, use the following code structure
to specify parameters and start the modeling process.

.. code-block:: python

    from datarobot import AUTOPILOT_MODE
    project.set_target(target='class', mode=AUTOPILOT_MODE.FULL_AUTO)


You can also pass optional parameters to ``project.set_target``
to change aspects of the modeling process. Some of those parameters
include:

* ``worker_count`` -- int, sets the number of workers used for modeling.

* ``partitioning_method`` -- ``PartitioningMethod`` object.


For a full reference of available parameters, see
:meth:`Project.set_target <datarobot.models.Project.set_target>`.

You can use the ``mode`` parameter to set the Autopilot mode.
``AUTOPILOT_MODE.FULL_AUTO``, is the default, triggers modeling
with no further actions necessary. Other accepted modes include
``AUTOPILOT_MODE.MANUAL`` for manual mode (choose your own models to run
rather than running the full Autopilot) and ``AUTOPILOT_MODE.QUICK`` to
run on a more limited set of models and get insights more quickly
("quick run").



Interact with a Visual AI Project
*********************************

The following code snippets may be used to access Visual AI images and
insights.



List Sample Images
==================

Sample images allow you to see a subset of images, chosen by DataRobot,
in the dataset. The returned ``SampleImage`` objects have an associated
``target_value`` that will allow you to categorize the images (e.g.
hamburger or hotdog). Until the project has reached specific stages of
modeling the ``target_value`` will be ``None``.


.. code-block:: python
	
    import io
    import PIL.Image

    from datarobot.models import Project
    from datarobot.models.visualai import SampleImage

    project_name = "My Image Project"
    column_name = "image"

    project = Project.list(search_params={"project_name": project_name})[0]
    for sample in SampleImage.list(project.id, column_name):
        # Display the image in the GUI
        bio = io.BytesIO(sample.image.image_bytes)
        img = PIL.Image.open(bio)
        img.show()

The results would be images such as:

.. image:: images/visualai/hamburger_0.jpg

.. image:: images/visualai/hotdog_0.jpg


List Duplicate Images
=====================

Duplicate images, images with different names but are determined by DataRobot
to be the same, may exist in a dataset. If this happens, the code returns
one of the images and the number of times it occurs in the dataset.

.. code-block:: python
	
    from datarobot.models import Project
    from datarobot.models.visualai import DuplicateImage

    project_name = "My Image Project"
    column_name = "image"

    project = Project.list(search_params={"project_name": project_name})[0]
    for duplicate in DuplicateImage.list(project.id, column_name):
        # To show an image see the previous sample image example
        print(f"Image id = {duplicate.image.id} has {duplicate.count} duplicates")


Activation Maps
===============

Activation maps are overlaid on the images to show which images areas
the model is using when making predictions.

Detailed explanations are available in DataRobot Platform
Documentation, `Model insights <https://app.datarobot.com/docs/modeling/visual-ai/vai-insights.html>`_.


Compute Activation Maps
-----------------------

You must compute activation maps before retrieving. The following snippet
is an example of starting the computation. For each project and model,
DataRobot returns a URL that can be used to determine when the computation
is complete.

.. code-block:: python

    from datarobot.models import Project
    from datarobot.models.visualai import ImageActivationMap

    project_name = "My Image Project"
    column_name = "image"

    project = Project.list(search_params={"project_name": project_name})[0]
    for model_id, feature_name in ImageActivationMap.models(project.id):
        if feature_name == column_name:
            ImageActivationMap.compute(project.id, model_id)


List Activation Maps
--------------------

After activation maps are computed, you can download them from the
DataRobot server. The following snippet is an example of how to get the
activation maps for a project and model and print out the
``ImageActivationMap`` object.

The activation map is a 2D matrix of values in the range [0, 255].

.. code-block:: python

    from datarobot.models import Project
    from datarobot.models.visualai import ImageActivationMap

    project_name = "My Image Project"
    column_name = "image"

    project = Project.list(search_params={"project_name": project_name})[0]
    for model_id, feature_name in ImageActivationMap.models(project.id):
        for amap in ImageActivationMap.list(project.id, model_id, column_name):
            print(amap)


When ``ImageActivationMap.activation_values`` are used to adjust the
brightness of each region, the images would look similar to:

.. image:: images/visualai/hamburger_0_map.png

.. image:: images/visualai/hotdog_0_map.png



Image Embeddings
================

Image embeddings map individual images into a vector embedding space. An
individual embedding may be used to perform linear computations on the
images.

Detailed explanations are available in DataRobot Platform
Documentation, `Model insights <https://app.datarobot.com/docs/modeling/visual-ai/vai-insights.html>`_.


Compute Image Embeddings
------------------------

You must compute image embeddings before retrieving. The following snippet
is an example of how to start the computation. For each project and model,
DataRobot returns a URL that can be used to determine when the computation
is complete.

.. code-block:: python

    from datarobot.models import Project
    from datarobot.models.visualai import ImageEmbedding

    project_name = "My Image Project"
    column_name = "image"

    project = Project.list(search_params={"project_name": project_name})[0]
    for model_id, feature_name in ImageEmbedding.models(project.id):
        url = ImageEmbedding.compute(project.id, model_id)
        print(url)


List Image Embeddings
---------------------

After image embeddings are computed, you can download them from the
DataRobot server. The following snippet is an example of how to get the
embeddings for a project and model and print out the ``ImageEmbedding``
object.

.. code-block:: python

    from datarobot.models import Project
    from datarobot.models.visualai import ImageEmbedding

    project_name = "My Image Project"
    column_name = "image"

    project = Project.list(search_params={"project_name": project_name})[0]
    for model_id, feature_name in ImageEmbedding.models(project.id):
        for embedding in ImageEmbedding.list(project.id, model_id, column_name):
            print(embedding)






