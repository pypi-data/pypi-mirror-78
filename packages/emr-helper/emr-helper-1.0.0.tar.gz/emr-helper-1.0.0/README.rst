==========
EMR Helper
==========

The EMR Helper library tries to help when setting up and managing an EMR cluster.

AWS EMR has three distinct objects:

- Cluster
- Fleet
- Step

This library collects some of the most common types of these elements and manages them at the python class level.

Dependencies
============

- Boto3

Classes
=======

Step
-----

There is a general class `Step` to wrap all subtypes of steps. Currently there are only **CommandRunnerStep** implemented to launch a Command Runner step.

You can create a step as follow:

.. code:: python

    import boto3
    from emrhelper import CommandRunnerStep

    step = CommandRunnerStep(
                name='StepName',
                args=process_arguments)

It can be added to a cluster before it starts (see Cluster) or append to a started cluster:

    step.run_on_cluster('clusterID')

If *clusterID* is None, step is added to any available cluster.

Fleet
------

The instance fleets configuration for a cluster contains instances information for computation capacity of cluster. As steps, there is a main class 'Fleet' and several subclasses: OnDemandFleet and SpotFleet, depending on whether you want to launch spot or on-demand instances.

You can create a fleet as follow:

.. code-block:: python

    from emrhelper import SpotFleet

    fleet = SpotFleet(name='My Fleet', capacity=4, fleet_type='CORE')

    fleet.add_instance_config(instance_type='r5d.xlarge', capacity=2)
    fleet.add_instance_config(instance_type='r5d.2xlarge', capacity=4)

Cluster
-------

You can create a cluster, add steps and fleets, and run it.

.. code-block:: python

    from emrhelper import Cluster

    cluster = Cluster(
        name='my-cluster',
        key_pair='keypair',
        subnets='...',
        sg_master='...',
        sg_slave='...',
        sg_service='...',
        instance_profile='...',
        service_role='...',
        log_uri='...'
    )

    cluster.add_step(step)
    cluster.add_fleet(fleet)

    cluster.run_cluster()

You can add as many steps and fleets as you need.

Installation
============

.. code-block:: bash

    pip install emrhelper
