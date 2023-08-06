import boto3
import logging
from emr_helper.step import Step
from emr_helper.fleet import Fleet


class Cluster:

    @property
    def name(self):
        return self.__name

    @property
    def key_pair(self):
        '''EC2 key pair'''
        return self.__key_pair

    @property
    def subnets(self):
        '''List of subnets ids'''
        return self.__subnets

    @property
    def sg_master(self):
        '''Master security group id'''
        return self.__sg_master

    @property
    def sg_slave(self):
        '''Slave security group id'''
        return self.__sg_slave

    @property
    def sg_service(self):
        '''Service security group id'''
        return self.__sg_service

    @property
    def fleets(self):
        return self.__fleets

    @property
    def keep_alive(self):
        return self.__keep_alive

    @keep_alive.setter
    def keep_alive(self, value):
        if isinstance(value, bool):
            self.__keep_alive = value
        else:
            raise AttributeError('KEEP_ALIVE must be a boolean')

    @property
    def managed_scaling_policy(self):
        return self.__managed_scaling_policy

    @property
    def instance_profile(self):
        '''IAM instance profile name'''
        return self.__instance_profile

    @property
    def service_role(self):
        '''IAM service role name'''
        return self.__service_role

    @property
    def concurrency(self):
        '''Steps concurrency.'''
        return self.__concurrency

    @concurrency.setter
    def concurrency(self, value):
        if isinstance(value, int) and value > 0:
            self.__concurrency = value
        else:
            raise AttributeError('CONCURRENCY must be a positive integer.')

    @property
    def steps(self):
        '''List of steps'''
        return self.__steps

    @property
    def tags(self):
        '''List of tags'''
        return self.__tags

    @tags.setter
    def tags(self, value):
        if isinstance(value, dict):
            self.__tags = value
            if 'Name' not in self.__tags:
                self.__tags['Name'] = self.name
        else:
            raise AttributeError('TAGS must be a dict.')

    @property
    def applications(self):
        '''Applications list'''
        return self.__applications

    @applications.setter
    def applications(self, value):
        if isinstance(value, list):
            self.__applications = value
        else:
            raise AttributeError('APPLICATIONS must be a list.')

    @property
    def release(self):
        '''EMR Release'''
        return self.__release

    @property
    def log_uri(self):
        return self.__log_uri

    ###########################################################################
    def __init__(self,
                 name, key_pair, subnets,
                 sg_master, sg_slave, sg_service,
                 instance_profile, service_role,
                 log_uri, keep_alive=False,
                 min_capacity_units=None, max_capacity_unit=None,
                 max_core_capacity_units=None,
                 concurrency=1,
                 tags={}, applications=[],
                 release='emr-5.30.0',
                 client=None):
        self.__name = name
        self.__key_pair = key_pair
        self.__subnets = subnets
        self.__sg_master = sg_master
        self.__sg_slave = sg_slave
        self.__sg_service = sg_service
        self.__fleets = []
        self.__log_uri = log_uri
        self.keep_alive = (keep_alive)
        if min_capacity_units and max_capacity_unit and \
                max_core_capacity_units:
            self.__managed_scaling_policy = {
                'ComputeLimits': {
                    'UnitType': 'InstanceFleetUnits',
                    'MinimumCapacityUnits': min_capacity_units,
                    'MaximumCapacityUnits': max_capacity_unit,
                    'MaximumCoreCapacityUnits': max_core_capacity_units,
                    'MaximumOnDemandCapacityUnits': 0
                }
            }
        elif min_capacity_units or max_capacity_unit or \
                max_core_capacity_units:
            raise AttributeError('min_capacity_units, max_capacity_unit, \
                and max_core_capacity_units must be inform together')
        else:
            self.__managed_scaling_policy = None

        self.__instance_profile = instance_profile
        self.__service_role = service_role
        self.concurrency = (concurrency)
        self.__steps = []
        self.tags = (tags)
        self.applications = (applications)
        self.__release = release
        if client is None:
            self.__client = boto3.client('emr')
        else:
            self.__client = client

    def add_step(self, step):
        if isinstance(step, Step):
            logging.debug('Adding step: {}'.format(step.get_step()))
            self.__steps.append(step.get_step())
        else:
            raise AttributeError('STEP must be a CommandRunnerStep object.')

    def add_fleet(self, fleet):
        if isinstance(fleet, Fleet):
            logging.debug('Adding fleet: {}'.format(fleet.get_fleet()))
            self.__fleets.append(fleet.get_fleet())

        else:
            raise AttributeError('FLEET must be a SpotFleet object.')

    def run_cluster(self):
        ''' Run EMR cluster.

            Exceptions:
                RunClusterException: If there is no fleets or applications
            Return (dict):
                {
                    'id': (str),
                    'steps': [
                        {
                            'id': (str),
                            'name': (str)
                        },
                    ...
                    ]
                }
        '''
        if not len(self.fleets):
            raise RunClusterException('Empty fleets')
        if not len(self.applications):
            raise RunClusterException('Empty applications')
        if not len(self.steps):
            logging.warning('There is not any steps in cluster')

        response = self.__client.run_job_flow(
            Name=self.name,
            LogUri=self.log_uri,
            ReleaseLabel=self.release,
            Instances={
                'Ec2KeyName': self.key_pair,
                'Ec2SubnetIds': self.subnets,
                'EmrManagedMasterSecurityGroup': self.sg_master,
                'EmrManagedSlaveSecurityGroup': self.sg_slave,
                'ServiceAccessSecurityGroup': self.sg_service,
                'InstanceFleets': self.fleets,
                'KeepJobFlowAliveWhenNoSteps': self.keep_alive,
                'TerminationProtected': False
            },
            ManagedScalingPolicy=self.managed_scaling_policy,
            JobFlowRole=self.instance_profile,
            ServiceRole=self.service_role,
            StepConcurrencyLevel=self.concurrency,
            Steps=self.steps,
            Applications=self.__emr_applications(),
            VisibleToAllUsers=True,
            Tags=self.__emr_tags()
        )
        cluster_id = response['JobFlowId']
        steps = self.__get_steps(cluster_id)
        return {
            'id': cluster_id,
            'steps': steps
        }

    def __emr_tags(self):
        emr_tags = []
        for tag in self.tags:
            emr_tags.append({
                'Key': tag,
                'Value': self.__tags[tag]
            })
        return emr_tags

    def __emr_applications(self):
        emr_applications = []
        for app in self.applications:
            emr_applications.append({
                'Name': app
            })
        return emr_applications

    def __get_steps(self, cluster_id):
        response = self.__client.list_steps(ClusterId=cluster_id)
        steps = response['Steps']
        while response.get('Marker', None):
            response = self.__client.list_steps(
                ClusterId=cluster_id, Marker=response['Marker'])
            steps.extend(response['Steps'])

        output = []
        for step in steps:
            output.append({
                'id': step['Id'],
                'name': step['Name']
            })
        return output


class RunClusterException(Exception):
    '''Error when trying to run a cluster.
    Args:
        error (str): original error.
        query (str): Query that caused the error.
    '''
    msg = 'Cannot run the cluster. Error: {e}'

    def __init__(self, error):
        super(RunClusterException, self).__init__(
            self.msg.format(e=error))
