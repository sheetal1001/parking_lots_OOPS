class Vehicle:
    def __init__(self,number_plate):
        self.__number_plate=number_plate
        
    def getVehicleNum(self):
        return self.__number_plate
    def set_time(self, time_entry=0, time_exit=0):
        if(time_entry!=0):
            self.__entry_time = time_entry
        if(time_exit!=0):
            self.__exit_time = time_exit

class Bus(Vehicle):
    
    def fare_calculation(self):
        pass

class Bike(Vehicle):
    pass

class Car(Vehicle):
    pass

class Slots:
    def __init__(self,id, vehicle):
        self.__id = id
        self.__vn = None
        self.__is_occupied = False
    
    def assign_vehicle(self,vehicle):
        entry_time= input("Enter the entry time in 00:00 24hrs format ")
        h1,m1= map(int, entry_time.split(":"))
        if((h1<0 or h1>24) or (m1<0 or m1>60)):
            print("Entry time not correct")
        else:
            vehicle.set_time(entry_time,0)
            self.__is_occupied=True
            self.__vn = vehicle.getVehicleNum()
            print("Parking done at " + self.__id)

    def release(self):
        self.__is_occupied = False
        self.__vn = None  
        print("Unparked")

    def isOccupied(self):
        return self.__is_occupied
    def getVehicleNum(self):
        return self.__vn
    
class Ticket:
    def __init__(self,vehicle):
        pass


    
class ParkingLot:

    __slots ={}
    __is_initialized = False
    @staticmethod
    def __initialize_parking_lot():
        if not ParkingLot.__is_initialized:
            ParkingLot.__slots = {
                'Car': [Slots('C1', 'car'), Slots('C2','car')],
                'Bike': [Slots('B1', 'bike'), Slots('B2','bike'),Slots('B3','bike')],
                'Bus': [Slots('BUS1', 'bus')]
            }
        ParkingLot.__is_initialized = True


    def __init__(self,vehicle):
         ParkingLot.__initialize_parking_lot() 
         print("Welcome to the Parking lot of ABC mall!")
         self.__menu(vehicle)

    def __menu(self,vehicle):
        user_input= input("""
    Please choose one of the options to proceed:
    1. Choose 1 to view status of unoccupied slots
    2. Choose 2 to park
    3. Choose 3 to unpark
    4. Choose 4 to exit    
""")
        
        if(user_input=='1'):
            print("The status of parking lot is as follows:")
            self.__status() 
            self.__menu(vehicle)
        elif(user_input=='2'):
            print("Looking availability for parking the Vehicle")
            self.__park(vehicle)
            self.__menu(vehicle)
        elif(user_input=='3'):
            print("Unparking the vehicle")
            self.__unpark(vehicle)
            self.__menu(vehicle)
        else:
            print("Thank you for using the Parking lot!")
    
    def __status(self):
        for k,v in ParkingLot.__slots.items():
            count=0
            for slot in v:
                if not slot.isOccupied():
                    count+=1
            print("No of unoccupied slots for " + f"{k}" + ":" ,end=" ")
            print(count)
        
    def __valid_parking(self,vehicle):
        vtype= type(vehicle).__name__
        for val in ParkingLot.__slots[vtype]:
            if(val.getVehicleNum()==vehicle.getVehicleNum()):
                return val
        return False

    def __park(self,vehicle):
        vtype= type(vehicle).__name__
        no_empty_slot_found = True
        if not self.__valid_parking(vehicle):
            for slot in ParkingLot.__slots[vtype]:
                if not slot.isOccupied():
                    s1= slot.assign_vehicle(vehicle)
                    no_empty_slot_found = False 
                    break
            if no_empty_slot_found:
                print ("Empty slots not found for " + vtype)
        else:
            print("Vehicle already exist in the parking, can not park again")
        

    def __unpark(self,vehicle):
        slot=self.__valid_parking(vehicle)
        if(slot==False):
            print("Vehicle does not exist in the parking")
        else:
            exit_time = input("Enter the exit time of the vehicle in 00:00 24hrs format ")
            h1,m1= map(int, exit_time.split(":"))
            if((h1<0 or h1>24) or (m1<0 or m1>60)):
                print("Exit time not correct")
            else:
                vehicle.set_time(0,exit_time)
                slot.release()

            


a=Car('AB101') 
b=ParkingLot(a) 
     
             