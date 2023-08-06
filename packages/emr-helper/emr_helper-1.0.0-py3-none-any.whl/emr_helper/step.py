import boto3
import logging


class Step:
    '''Generic class to include different step types.'''

    def get_step(self):
        '''Return dictionary with EMR format.'''
        raise NotImplementedError()


class CommandRunnerStep(Step):

    @ property
    def name(self):
        '''Step name'''
        return self.__name

    @ property
    def action_on_failure(self):
        '''Define what action has to take when the step fails.'''
        return self._action_on_failure

    @ action_on_failure.setter
    def action_on_failure(self, value):
        types = ['TERMINATE_CLUSTER', 'CANCEL_AND_WAIT', 'CONTINUE']
        if value in types:
            self._action_on_failure = value
        else:
            raise AttributeError('aaction_on_failure must be {}'.format(types))

    @ property
    def args(self):
        '''Step arguments for CommandRunner.'''
        return self.__args

    def __init__(self,
                 name, args, action_on_failure='TERMINATE_CLUSTER',
                 client=None):
        self.__name = name
        self.action_on_failure = (action_on_failure)
        self.__args = args
        if client is None:
            self.__client = boto3.client('emr')
        else:
            self.__client = client

    def get_step(self):
        '''Return dictionary with EMR format.'''
        return {
            'Name': self.name,
            'ActionOnFailure': self.action_on_failure,
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': self.args
            }
        }

    def run_on_cluster(self, cluster_id=None):
        ''' Adds step to an existing cluster.

            Args:
                - cluster_id (str): AWS Cluster ID. If None, finds any cluster.
            Return (dict):
                {
                    'id': (str),
                    'steps': [{
                        'id': (str),
                        'name': (str)
                    }]
                }
        '''

        if cluster_id is None:
            logging.debug('AUTO cluster selected. Finding cluster')
            cluster_id = self.__find_cluster()

        logging.debug('Adding step to cluster {}'.format(cluster_id))

        response = self.__client.add_job_flow_steps(
            JobFlowId=cluster_id,
            Steps=[self.get_step()]
        )

        return {
            'id': cluster_id,
            'steps': [{
                'id': response['StepIds'][0],
                'name': self.name
            }]
        }

    def __find_cluster(self):

        response = self.__client.list_clusters(
            ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING']
        )
        if response['Clusters']:
            return response['Clusters'][0]['Id']
        else:
            raise FindClusterException()


class FindClusterException(Exception):
    '''Error when trying to find a running cluster.
    '''
    msg = 'Cannot find a correct cluster.'

    def __init__(self):
        super(FindClusterException, self).__init__(
            self.msg.format())
