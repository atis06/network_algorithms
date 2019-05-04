from typing import List
import constants

class NodeModel(object):
    """
	Node object
	"""

    def __init__(self, id: int, network_functions: List[str], is_virtual = False):
        self.__id = id
        self.__network_functions = network_functions
        self.__is_virtual = is_virtual
        self.__parent_id = -1
        self.__is_removed = False
        if self.__is_virtual:
            self.__parent_id = int(self.__id/(len(constants.REQUIRED_SERVICE_FUNCTIONS)+1))
        pass

    @property
    def id(self):
        return self.__id

    @property
    def is_virtual(self):
        return self.__is_virtual

    @property
    def parent_id(self):
        return self.__parent_id

    @property
    def network_functions(self):
        return self.__network_functions

    def set_id(self, id: int):
        self.__id = id
        pass

    def set_is_removed(self, removed: bool):
        self.__is_removed = removed
        pass

    @property
    def is_removed(self):
        return self.__is_removed

    pass
