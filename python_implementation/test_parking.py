import unittest
from datetime import datetime,timedelta
from main import Car,Bus,Bike,Slots,Ticket, ParkingLot


class TestVehicle(unittest.TestCase):
    def test_car_parking_fee(self):
        car = Car('AB123')
        entry_time = datetime(2025,7,26,10,0,0)
        exit_time = datetime(2025,7,26,10,5,0)
        car.set_time(entry_time,exit_time)
        self.assertAlmostEqual(car.duration(),5.000, places=3)
        self.assertEqual(car.get_Parking_fee(),100) # 5 * 20

    def test_car_zero_duration(self):
        car = Car('UP123')
        entry_exit = datetime(2025,7,26,12,52,0)
        car.set_time(entry_exit,entry_exit)
        self.assertEqual(car.get_Parking_fee(),0)

    def test_bike_parking_fee(self):
        bike = Bike("BK202")
        entry = datetime(2025, 7, 25, 10, 0, 0)
        exit = datetime(2025, 7, 25, 10, 45, 0)
        bike.set_time(entry, exit)
        self.assertEqual(bike.get_Parking_fee(), 450)  # 45 * 10

    def test_bus_parking_fee(self):
        bus = Bus("BS202")
        entry = datetime(2025, 7, 25, 10, 0, 0)
        exit = datetime(2025, 7, 25, 10, 10, 0)
        bus.set_time(entry, exit)
        self.assertEqual(bus.get_Parking_fee(), 500)  # 10 * 50

class TestSlots(unittest.TestCase):
    def test_assign_and_release(self):
        slot= Slots('C1')
        vehicle = Car('AB101')
        # Vehicle not yet assigned to the slot
        self.assertFalse(slot.isOccupied())
        # Assigned vehicle
        slot.assign_vehicle(vehicle)
        self.assertTrue(slot.isOccupied())
        self.assertEqual(slot.getVehicleNum(),vehicle.getVehicleNum())
        # Released the slot
        slot.release()
        self.assertFalse(slot.isOccupied())
        self.assertIsNone(slot.getVehicleNum())
    
class TestTicket(unittest.TestCase):
    def test_ticket(self):
        vehicle = Bike('BK101')
        entry = datetime(2025,7,26,1,0)
        exit = entry + timedelta(minutes=15)
        vehicle.set_time(entry,exit)
        ticket = Ticket(vehicle)
        # To check if the ticket is being printed correctly
        self.assertIn("Vehicle Number: BK101", str(ticket))
        self.assertIn("Duration: 15.0 minutes", str(ticket))
        self.assertIn("Fare: ₹150", str(ticket))

class testParking(unittest.TestCase):

    def setUp(self):
        # Created a ParkingLot and a Car Object
        self.parking_lot = ParkingLot()
        self.car = Car("CAR123")
    
    def test_park_and_unpark(self):
        # Not yet parked the car, vehicle does not exist in the parking
        self.assertFalse(self.parking_lot._ParkingLot__vehicle_already_in_parking(self.car))

        # Parked, slot occupied
        self.parking_lot._ParkingLot__park(self.car)
        slot = self.parking_lot._ParkingLot__vehicle_already_in_parking(self.car)
        self.assertIsNot(slot, False)
        self.assertTrue(slot.isOccupied())

        # Unparked-->slot unoccupied
        self.parking_lot._ParkingLot__unpark(self.car)
        slot = self.parking_lot._ParkingLot__vehicle_already_in_parking(self.car)
        self.assertFalse(slot)
    # Check the number of unoccupied slots
    def test_status(self):
        car_slots_before = sum(not slot.isOccupied() for slot in self.parking_lot._ParkingLot__Parking_slots['Car'])
        self.parking_lot._ParkingLot__park(self.car)
        car_slots_after = sum(not slot.isOccupied() for slot in self.parking_lot._ParkingLot__Parking_slots['Car'])
        self.assertEqual(car_slots_before - 1, car_slots_after)



if __name__ == '__main__':
    unittest.main()

