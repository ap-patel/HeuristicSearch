from warehouse import *
product_list = [["prod1", (0,5)], ["prod2", (1,5)], ["prod3", (2,5)]]
pack_list =  [["pack1", (0,0)], ["pack2", (1,0)]]
open_order = [[ "prod3", "pack1"], ["prod2", "pack2"],
[ "prod3", "pack1"]]
robot_status = [["r1", 'idle', (0,0)], ['r2', 'on_delivery', (1,0), 8]]
ware_house_1 = warehouse("Start", 0, None, product_list, pack_list, 0, open_order, robot_status )

a = ware_house_1.successors()
for i in a:
    print(i.get_orders(), i.get_time())
    
    
#untitles 1 output
    #['prod2', 'pack2']
    #['prod3', 'pack1']    
    
#original output
#[['prod2', 'pack2'], ['prod3', 'pack1']]
#[['prod3', 'pack1'], ['prod3', 'pack1']]
#[['prod2', 'pack2'], ['prod3', 'pack1']]
#[['prod3', 'pack1'], ['prod2', 'pack2'], ['prod3', 'pack1']]
