from datetime import datetime

# Base class representing a generic vehicle.
# Demonstrates Encapsulation by using private variables for internal state.
class Vehicle:

    def __init__(self,number_plate):
        self.__number_plate = number_plate
        self.__duration = 0
    # Public getter method to access private vehicle number (Encapsulation).   
    def getVehicleNum(self):
        return self.__number_plate   
    # Setter method to set the values of entry and exit time.
    # User should not be able to access or modify the entry/exit time.
    def set_time(self, time_entry=0, time_exit=0):
        if(time_entry!=0):
            self.__entry_time = time_entry
        if(time_exit!=0):
            self.__exit_time = time_exit
    # To calculate the duration vehicle was parked, to be used during fare calculation.
    def duration(self):
        dur_diff= self.__exit_time-self.__entry_time
        self.__duration = float(format((dur_diff.total_seconds())/60, '.3f'))
        return self.__duration


# Subclasses of vehicle
# Inherits from Vehicle class and overrides the parking fee calculation.
# Demonstrates Inheritance and Polymorphism (method overriding).
class Bike(Vehicle):
    def get_Parking_fee(self):
        self.__fee_per_minute =10
        fare = self.duration()*self.__fee_per_minute
        return fare

class Car(Vehicle):
    def get_Parking_fee(self):
        self.__fee_per_minute =20
        fare = self.duration()*self.__fee_per_minute
        return fare
    
class Bus(Vehicle):    
    def get_Parking_fee(self):
        self.__fee_per_minute =50
        fare = self.duration()*self.__fee_per_minute
        return fare

# Represents an individual parking slot.    
class Slots:
    def __init__(self,id):
        self.__id = id
        self.__vn = None
        self.__is_occupied = False
    # Used to assign the parking slot to the vehicle during parking. 
    def assign_vehicle(self,vehicle):
        entry_time= datetime.now()
        vehicle.set_time(entry_time,0)
        self.__is_occupied=True
        self.__vn = vehicle.getVehicleNum()
        print("Parking done at " + self.__id)
    # Used to release the slot after unparking.
    def release(self):
        self.__is_occupied = False
        self.__vn = None  
        print("Unparked")
    # Public getter methods to know if the slot is occupied. 
    def isOccupied(self):
        return self.__is_occupied
    # Public getter method to know the vehicle's number plate if parked in the slot.
    def getVehicleNum(self):
        return self.__vn

# Represents the parking ticket, generated upon vehicle exit.
# Demonstrates: Abstraction
# Abstracts the details of duration and fare calculation.    
class Ticket:
    def __init__(self,vehicle):
        self.__fare=vehicle.get_Parking_fee()
        self.__dur=vehicle.duration()
        self.__vn = vehicle.getVehicleNum()
    
    def __str__(self):
         return (
            "----- Parking Ticket -----\n"
            f"Vehicle Number: {self.__vn}\n"
            f"Duration: {self.__dur} minutes\n"
            f"Fare: ₹{self.__fare}\n"
            "--------------------------"
        )

# Central class managing the overall parking lot logic.
# Encapsulates parking slots and coordinates vehicle entry/exit.          
class ParkingLot:
    # Uses a static method to initialize slots — abstraction of setup logic.  
    # Why static? because for a parking lot object, no of slots should be shared among vehicles using it. Class variable.
    __Parking_slots ={}
    __is_initialized = False
    @staticmethod
    def __initialize_parking_lot():
        if not ParkingLot.__is_initialized:
            ParkingLot.__Parking_slots = {
                'Car': [Slots('C1'), Slots('C2')],
                'Bike': [Slots('B1'), Slots('B2'),Slots('B3')],
                'Bus': [Slots('BUS1')]
            }
        ParkingLot.__is_initialized = True

    def __init__(self):
         ParkingLot.__initialize_parking_lot() 
         print("Welcome to the Parking lot!")

    def menu(self,vehicle):
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
            self.menu(vehicle)
        elif(user_input=='2'):
            print("Looking availability for parking the Vehicle")
            self.__park(vehicle)
            self.menu(vehicle)
        elif(user_input=='3'):
            print("Unparking the vehicle")
            self.__unpark(vehicle)
            print("Thank you for using the Parking lot!")
        else:
            print("EXIT")
    # To know no. of unoccupied slots for each category of vehicle.
    def __status(self):
        for k,v in ParkingLot.__Parking_slots.items():
            count=0
            for slot in v:
                if not slot.isOccupied():
                    count+=1
            print("No. of unoccupied slots for " + f"{k}" + ":" ,end=" ")
            print(count)
    # While parking and unparking, need to check if vehicle already exists in the parking.
    # If during parking, vehicle already exists, displays a message- can not park again!
    # If during unparking, vehicle does not exist, displays message that vehicle does not exist.    
    def __vehicle_already_in_parking(self,vehicle):
        vtype= type(vehicle).__name__
        for val in ParkingLot.__Parking_slots[vtype]:
            if(val.getVehicleNum()==vehicle.getVehicleNum()):
                return val
        return False
    # Method to park a vehicle if empty slots are there.
    def __park(self,vehicle):
        vtype= type(vehicle).__name__
        no_empty_slot_found = True
        if not self.__vehicle_already_in_parking(vehicle):
            for slot in ParkingLot.__Parking_slots[vtype]:
                if not slot.isOccupied():
                    slot.assign_vehicle(vehicle)
                    no_empty_slot_found = False 
                    break
            if no_empty_slot_found:
                print ("Empty slots not found for " + vtype)
        else:
            print("Vehicle already exists in the parking, can not park again")
        
    # Method to unpark the vehicle.
    def __unpark(self,vehicle):
        slot=self.__vehicle_already_in_parking(vehicle)
        if(slot==False):
            print("Vehicle does not exist in the parking")
        else:
            exit_time = datetime.now()
            vehicle.set_time(0,exit_time)
            slot.release()
            print(Ticket(vehicle))

            

# Entry point of the program demonstrating real-world interaction with the ParkingLot system.
def main():
# Testing the ParkingLot class
    vehicle_registry = {}

# Function to get or create a vehicle
# If the vehicle already exist, will return the already existed vehicle object
    def get_vehicle(vtype, number_plate):
        if number_plate not in vehicle_registry:
            if vtype == 'Car':
                vehicle_registry[number_plate] = Car(number_plate)
            elif vtype == 'Bike':
                vehicle_registry[number_plate] = Bike(number_plate)
            elif vtype == 'Bus':
                vehicle_registry[number_plate] = Bus(number_plate)
        return vehicle_registry[number_plate]

# Sample test simulation
    vehicles = [
        get_vehicle('Car', 'AB101'),
        get_vehicle('Bike', 'BK202'),
        get_vehicle('Bus', 'BUS303'),
        get_vehicle('Car', 'AB101')  # Reuses the same object
    ]
    lot = ParkingLot()
    for vehicle in vehicles:
        print("\n--- New Parking Session ---")
        lot.menu(vehicle)
     
if __name__ == "__main__":
    main()            