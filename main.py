from controller import Controller
import constants
import sys


if __name__ == '__main__':
    start_node = sys.argv[1]
    end_node = sys.argv[2]
    print("Shortest path between node: " + str(sys.argv[1]) + " and " + str(sys.argv[2]))
    print("Required service functions are: ", constants.REQUIRED_SERVICE_FUNCTIONS)
    ctrl = Controller(int(start_node), int(end_node), render=True)
    ctrl.run()
    pass

pass
