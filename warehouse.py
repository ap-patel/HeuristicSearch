#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
warehouse STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
import math
from copy import deepcopy

##################################################
# The search space class 'warehouse'             #
# This class is a sub-class of 'StateSpace'      #
##################################################

class warehouse(StateSpace):
    def __init__(self, action, gval, parent, product_list, packing_station, current_time, open_order, robot_status):
        """Initialize a warehouse search state object."""
        StateSpace.__init__(self, action, gval, parent)
        self.product_list = product_list
        self.packing_station = packing_station
        self.current_time = current_time
        self.open_order = open_order
        self.robot_status = robot_status
#IMPLEMENT
        

    def successors(self): 
#IMPLEMENT
        '''Return list of warehouse objects that are the successors of the current object'''
        Stateswarehouse = list()
        current_robot_status = deepcopy(self.robot_status)
       # current_idle = []
        current_on_delivery = list()
        for i in current_robot_status:
            if i[1] == "idle":
                for j in self.get_orders():
                    #new_warehouse = self.deliver(i[0], j[0], j[1])                    
                    Stateswarehouse.append(self.deliver(i[0], j[0], j[1]))
            else: #case where robot_status is "on_delivery"
                current_on_delivery.append(i)
        if len(current_on_delivery) > 0:
            min_time = current_on_delivery[0][-1]
            for i in current_on_delivery:
                if i[-1] < min_time:
                    min_time = i[-1]
            new_warehouse = self.move_forward(min_time)
            Stateswarehouse.append(new_warehouse)
        return Stateswarehouse
    
    def move_forward(self, min_time):
        action = "move_forward({})".format(min_time)
        new_gval = min_time - self.current_time + self.gval
        parent = self
        current_product_list = deepcopy(self.product_list)
        current_packing_station = deepcopy(self.packing_station)
        current_open_order = deepcopy(self.open_order)        
        current_robot_status = deepcopy(self.robot_status)
       # current_time = deepcopy(self.current_time)
        
        #for i in current_robot_status:
            #if i[1] == "on_delivery":
                #if i[-1] == min_time:
                    #i = i[:-1]
                    #i[1] = "idle"
        for robot in range(len(current_robot_status)):
            if current_robot_status[robot][1] == "on_delivery":
                if current_robot_status[robot][-1] == min_time:
                    current_robot_status[robot][1]= "idle"
                    current_robot_status[robot].remove( current_robot_status[robot][-1])
                
                
      #  current_time = min_time
        return warehouse(action, new_gval, self, current_product_list, current_packing_station, min_time,  current_open_order, current_robot_status)            
        
        
       
    def deliver(self, robot_name, product_name, packing_station):
        ''' Return a new warehouse object updating open_order and rovot_status
        '''
        current_product_list = deepcopy(self.product_list)
        current_packing_station = deepcopy(self.packing_station)
        current_open_order = deepcopy(self.open_order)
        robot_status_before_delivery = deepcopy(self.robot_status)
        g_value = self.gval
        action = "deliver({}, {}, {})".format(robot_name,product_name,packing_station)
        current_time = deepcopy(self.current_time)
        pack_station_pos = 0
        product_pos = 0
        new_f_val = 0
        
        #Finding the fval
        for i in current_packing_station:
            if i[0] == packing_station:
                pack_station_pos = i[1]
                break
        for prod in current_product_list:
            if prod[0] == product_name:
                product_pos = prod[1]
                break
        
        for i in range(len(robot_status_before_delivery)):
            
            if robot_status_before_delivery[i][0] == robot_name:
                robot_status_before_delivery[i][1] = "on_delivery"
                current_pos = robot_status_before_delivery[i][2]
                new_f_val = (abs(current_pos[0] - product_pos[0])) + (abs(current_pos[1] - product_pos[1])) + (
                            abs(product_pos[0] - pack_station_pos[0])) + (abs(product_pos[1] - pack_station_pos[1]))                
                robot_status_before_delivery[i].append(new_f_val)
                robot_status_before_delivery[i][2] = pack_station_pos
                break
                
        #remove the order
        for i in current_open_order:
            if (i[0] == product_name) and (i[1] == packing_station):
                current_open_order.remove(i)
                break
        return warehouse(action, g_value, self, current_product_list, current_packing_station, current_time, current_open_order, robot_status_before_delivery)
      


    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        tuple_status = tuple(deepcopy(self.robot_status))
        tuple_order = tuple(deepcopy(self.open_order))
        return (self.current_time,(tuple_status, tuple_order))
        
        
        
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("Time = {}".format(self.get_time()))
        print("Unfulfilled Orders")
        for o in self.get_orders():
            print("    {} ==> {}".format(o[0], o[1]))
        print("Robot Status")
        for rs in self.get_robot_status():
            print("    {} is {}".format(rs[0], rs[1]), end="")
            if rs[1] == 'idle':
                print(" at location {}".format(rs[2]))
            elif rs[1] == 'on_delivery':
                print(" will be at location {} at time {}".format(rs[2], rs[3]))

#Data accessor routines.

    def get_robot_status(self):
#IMPLEMENT
        '''Return list containing status of each robot
           This list has to be in the format: [rs_1, rs_2, ..., rs_k]
           with one status list for each robot in the state. 
           Each robot status item rs_i is itself a list in the format [<name>, <status>, <loc>, <ftime>]
           Where <name> is the name of the robot (a string)
                 <status> is either the string "idle" or the string "on_delivery"
                 <loc> is a location (a pair (x,y)) 
                       if <status> == "idle" then loc is the robot's current location
                       if <status> == "on_delivery" then loc is the robot's future location
                <ftime> 
                       if <status> == "idle" this item is missing (i.e., the list is of 
                                      length 3)
                       if <status> == "on_delivery" then this is a number that is the 
                                      time that the robot will complete its current delivery
        '''
        b = deepcopy(self.robot_status)
        return b

    def get_time(self):
#IMPLEMENT
        '''Return the current time of this state (a number)'''
        return self.current_time

    def get_orders(self):
#IMPLEMENT
        '''Return list of unfulfilled orders of this state
           This list is in the format [o1, o2, ..., om]
           one item for each unfulfilled order. 
           Each oi is itself a list [<product_name>, <packing_station_name>]
           where <product_name> is the name of the product to be delivered
           and  <packing_station_name> is the name of the packing station it is to be delivered to'''
        temp_order = deepcopy(self.open_order)
        return temp_order


#############################################
# heuristics                                #
#############################################
    
def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_min_completion_time(state):
#IMPLEMENT
    '''warehouse heuristic'''
    #We want an admissible heuristic. Since the aim is to delivery all
    #of the products to their packing station in as short as a time as
    #possible. 
    #NOTE that we want an estimate of the ADDED time beyond the current
    #     state time.
    #Consider all of the possible delays in moving from this state to
    #a final delivery of all orders.
    # 1. All robots have to finish any current delivery they are on.
    #    So the earliest we could finish is the 
    #    maximum over all robots on delivery of 
    #       (robot's finish time - the current state time)
    #    we subtract the current state time because we want time
    #    beyond the current time required to complete the delivery
    #    Let this maximum be TIME1.
    #    Clearly we cannot finish before TIME1
    #
    # 2. For all unfulfilled orders we need to pick up the product of
    #    that order with some robot, and then move it to the right
    #    packing station. However, we could do many of these
    #    deliveries in parallel. So to get an *admissible* heuristic
    #    we take the MAXIMUM of a MINUMUM time any unfulfilled order
    #    can be completed. There are many different minimum times that
    #    could be computed...of varying complexity. For simplicity we
    #    ignore the time required to get a robot to package, and
    #    instead take the time to move the package from its location
    #    to the packing station location as being a suitable minimum.
    #    So we compute these minimums, then take the maximum of these
    #    minimums Call this max TIME2
    #    Clearly we cannot finish before TIME2
    #
    # Finally we return as a the heuristic value the MAXIMUM of ITEM1 and ITEM2
    list_1 = []
    TIME1 = 0
    current_robot_status = deepcopy(state.robot_status)
    current_time = state.current_time
    for i in current_robot_status:
        if i[1] == "on_delivery":
            i_finish_time = i[-1]
            list_1.append(i_finish_time - current_time)
 #   print(list_1)
    if(list_1):
        TIME1 = max(list_1)
    
    list_2 = []
    current_open_orders = deepcopy(state.open_order)
    current_product_list = deepcopy(state.product_list)
    current_packing_staion = deepcopy(state.packing_station)
    pack_pos = 0
    prod_pos = 0
    TIME2 = 0
    for order in current_open_orders:
        product_name = order[0]
        packing_station = order[1]
        for product in current_product_list:
            if product[0] == product_name:
                prod_pos = product[-1]
                break
        for packing in current_packing_staion:
            if packing[0] == packing_station:
                pack_pos = packing[-1]
                break
        distance = abs(pack_pos[0] - prod_pos[0]) + abs(pack_pos[1] - prod_pos[1])
        list_2.append(distance)
        if (list_2):
            TIME2 = max(list_2)
    return max(TIME1, TIME2)

def warehouse_goal_fn(state):
#IMPLEMENT
    '''Return a boolean.Have we reached the goal when all orders have been delivered'''
    all_robots_idle = True
    len_order_list = len(state.open_order)
    if len_order_list > 0:
        return False
    current_robot_status = deepcopy(state.robot_status)
    for i in current_robot_status:
        if i[1] == "on_delivery":
            return False
    return all_robots_idle and (len_order_list == 0)
    
    

def make_init_state(product_list, packing_station_list, current_time, open_orders, robot_status):
#IMPLEMENT
    '''Input the following items which specify a state and return a warehouse object 
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       product_list = [p1, p2, ..., pk]
          a list of products. Each product pi is itself a list
          pi = [product_name, (x,y)] where 
              product_name is the name of the product (a string) and (x,y) is the
              location of that product.
       packing_station = [ps1, ps2, ..., psn]
          a list of packing stations. Each packing station ps is itself a list
          pi = [packing_station_name, (x,y)] where 
              packing_station_name is the name of the packing station (a string) and (x,y) is the
              location of that station.
       current_time = an integer >= 0
          The state's current time.
       open_orders = [o1, o2, ..., om] 
          a list of unfulfilled (open) orders. Each order is itself a list
          oi = [product_name, packing_station_name] where
               product_name is the name of the product (a string) and
               packing_station_name is the name of the packing station (a string)
               The order is to move the product to the packing station
        robot_status = [rs1, rs2, ..., rsk]
          a list of robot and their status. Each item is itself a list  
          rsi = ['name', 'idle'|'on_delivery', (x, y), <finish_time>]   
            rsi[0] robot name---a string 
            rsi[1] robot status, either the string "idle" or the string
                  "on_delivery"
            rsi[2] robot's location--if "idle" this is the current robot's
                   location, if "on_delivery" this is the robots final future location
                   after it has completed the delivery
            rsi[3] the finish time of the delivery if the "on_delivery" 
                   this element of the list is absent if robot is "idle" 

   NOTE: for simplicity you may assume that 
         (a) no name (robot, product, or packing station is repeated)
         (b) all orders contain known products and packing stations
         (c) all locations are integers (x,y) where both x and y are >= 0
         (d) the robot status items are correctly formatted
         (e) the future time for any robot on_delivery is >= to the current time
         (f) the current time is >= 0
    '''
    return warehouse("START", 0, None, product_list, packing_station_list, current_time, open_orders, robot_status)

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_init_state(nprods, npacks, norders, nrobots):
    '''Generate a random initial state containing 
       nprods = number of products
       npacks = number of packing stations
       norders = number of unfulfilled orders
       nrobots = number of robots in domain'''

    prods = []
    for i in range(nprods):
        ii = int(i)
        prods.append(["product{}".format(ii), (randint(0,50), randint(0,50))])
    packs = []
    for i in range(npacks):
        ii = int(i)
        packs.append(["packing{}".format(ii), (randint(0,50), randint(0,50))])
    orders = []
    for i in range(norders):
        orders.append([prods[randint(0,nprods-1)][0], packs[randint(0,npacks-1)][0]])
    robotStatus = []
    for i in range(nrobots):
        ii = int(i)
        robotStatus.append(["robot{}".format(ii), "idle", (randint(0,50), randint(0,50))])
    return make_init_state(prods, packs, 0, orders, robotStatus)


def test(nprods, npacks, norders, nrobots):
    s0 = make_rand_init_state(nprods, npacks, norders, nrobots)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, warehouse_goal_fn, heur_min_completion_time)