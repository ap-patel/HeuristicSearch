from warehouse import *

#class person:
    #def __init__(self, name, lastname):
        #self.name = name
        #self.lastname = lastname
        #self.number = self.add(1,3)
        
    #def add(self,a,b):
        #print(self.name )
        #return a + b
#if __name__ == "__main__":
    #abhi = person("abhishek", "patel")
    #print(abhi.name)
    #print(abhi.lastname)
    #print(abhi.number)
    
#a = [[13,3], [14,5], [1,2]]
#for i in a:
    #if i[0] == 1:
        #a.remove(i)
#print(a)

#a = "deliver({}, {}, {})".format(1,2,3)
#print(a)

#a = [1]
#b = tuple(a)
#print(b)
#print(not a)
#a_len = len(a)
#boolean = True
#print(boolean and (a_len == 0))
product_list = [["prod1", (0,5)], ["prod2", (1,5)], ["prod3", (2,5)]]
pack_list =  [["pack1", (0,0)], ["pack2", (1,0)]]
open_order = [[ "prod3", "pack1"], ["prod2", "pack2"],
[ "prod3", "pack1"]]
robot_status = [["r1", 'idle', (0,0)], ['r2', 'on_delivery', (1,0), 8]]
ware_house_1 = warehouse("Start", 0, None, product_list, pack_list, 0, open_order, robot_status )
#a = ware_house_1.successors()
#print(ware_house_1.successors())

#for i in range(0,9):
    #print("problem here")
    #print("this is i" , i)
    #for items in ware_house_1.successors()[i].get_orders():
        #print(items)
        
#print(ware_house_1.successors()[0].get_orders())   
#print(ware_house_1.successors()[1].get_orders()) 

print(ware_house_1.successors())
print(ware_house_1.successors()) 
for i in ware_house_1.successors():
    print("This is the robot_status", i.get_robot_status())
    print("This is the order", i.get_orders()) 
#print(a)
  
#for i in a:
    #a.remove(i)
    
#k = a
#for i in k:
    #print (i)


