
class Fleet:
    '''Generic class to include different fleet types.'''

    def get_fleet(self):
        '''Return dictionary with EMR format.'''
        raise NotImplementedError()


class SpotFleet(Fleet):

    @ property
    def name(self):
        '''Fleet name'''
        return self.__name

    @ property
    def fleet_type(self):
        '''Fleet type. It can be MASTER, CORE or TASK.'''
        return self._fleet_type

    @ fleet_type.setter
    def fleet_type(self, value):
        types = ['MASTER', 'CORE', 'TASK']
        if value in types:
            self._fleet_type = value
        else:
            raise AttributeError('fleet_type must be {}'.format(types))

    @ property
    def capacity(self):
        '''Fleet capacity.'''
        return self.__capacity

    @ capacity.setter
    def capacity(self, value):
        if isinstance(value, int) and value >= 1:
            self.__capacity = value
        else:
            raise AttributeError('CAPACITY must be a positive integer.')

    @ property
    def timeout(self):
        '''Launch specifications timeout.'''
        return self.__timeout

    @ timeout.setter
    def timeout(self, value):
        if isinstance(value, int) and value >= 5 and value <= 1440:
            self.__timeout = value
        else:
            raise AttributeError(
                'TIMEOUT must be an integer between 5 and 1440')

    @ property
    def timeout_action(self):
        '''Launch specifications timeout action.'''
        return self._timeout_action

    @ timeout_action.setter
    def timeout_action(self, value):
        types = ['TERMINATE_CLUSTER', 'SWITCH_TO_ON_DEMAND']
        if value in types:
            self._timeout_action = value
        else:
            raise AttributeError('timeout_action must be {}'.format(types))

    def __init__(self, name, capacity=1, fleet_type='MASTER',
                 timeout=5, timeout_action='SWITCH_TO_ON_DEMAND'):
        self.__name = name
        self.capacity = (capacity)
        self.fleet_type = (fleet_type)
        self.__instanceconfigs = []
        self.timeout = (timeout)
        self.timeout_action = (timeout_action)

    def add_instance_config(self,
                            instance_type, capacity=1,
                            bid_price_as_percent=None, bid_price=None):
        '''Add instance config to fleet.

        Args:
            instance_type (str): EC2 instance type.
            capacity (int): instance capacity.
            bid_price_as_percent (int): Bid price as percent. If none and
            bid_price is none, bid_price_as_percent is 100.0.
            bid_price (int). Bid price as int.
        '''
        if bid_price is None and bid_price_as_percent is None:
            bid_price_as_percent = 100.0

        config = {
            'InstanceType': instance_type,
            'WeightedCapacity': capacity,
        }
        if bid_price:
            config['BidPrice'] = bid_price
        else:
            config[
                'BidPriceAsPercentageOfOnDemandPrice'] = bid_price_as_percent

        self.__instanceconfigs.append(config)

    def get_fleet(self):
        '''Return dictionary with EMR format.'''
        return {
            'Name': self.name,
            'InstanceFleetType': self.fleet_type,
            'TargetSpotCapacity': self.capacity,
            'InstanceTypeConfigs': self.__instanceconfigs,
            'LaunchSpecifications': {
                'SpotSpecification': {
                    'TimeoutDurationMinutes': self.timeout,
                    'TimeoutAction': self.timeout_action
                }
            }
        }


class OnDemandFleet(Fleet):

    @ property
    def name(self):
        '''Fleet name'''
        return self.__name

    @ property
    def fleet_type(self):
        '''Fleet type. It can be MASTER, CORE or TASK.'''
        return self._fleet_type

    @ fleet_type.setter
    def fleet_type(self, value):
        types = ['MASTER', 'CORE', 'TASK']
        if value in types:
            self._fleet_type = value
        else:
            raise AttributeError('fleet_type must be {}'.format(types))

    @ property
    def capacity(self):
        '''Fleet capacity.'''
        return self.__capacity

    @ capacity.setter
    def capacity(self, value):
        if isinstance(value, int) and value >= 1:
            self.__capacity = value
        else:
            raise AttributeError('CAPACITY must be a positive integer.')

    def __init__(self, name, capacity=1, fleet_type='MASTER'):
        self.__name = name
        self.capacity = (capacity)
        self.fleet_type = (fleet_type)
        self.__instanceconfigs = []
        self.__allocation_strategy = 'lowest-price'

    def add_instance_config(self,
                            instance_type, capacity=1, ebsConfiguration=None):
        '''Add instance config to fleet.

        Args:
            instance_type (str): EC2 instance type.
            capacity (int): instance capacity.
            ebsConfiguration (dict): EBS Configuration.
        '''

        config = {
            'InstanceType': instance_type,
            'WeightedCapacity': capacity
        }
        if ebsConfiguration:
            config['EbsConfiguration'] = ebsConfiguration

        self.__instanceconfigs.append(config)

    def get_fleet(self):
        '''Return dictionary with EMR format.'''
        return {
            'Name': self.name,
            'InstanceFleetType': self.fleet_type,
            'TargetOnDemandCapacity': self.capacity,
            'InstanceTypeConfigs': self.__instanceconfigs,
            'LaunchSpecifications': {
                'OnDemandSpecification': {
                    'AllocationStrategy': self.__allocation_strategy
                }
            }
        }
