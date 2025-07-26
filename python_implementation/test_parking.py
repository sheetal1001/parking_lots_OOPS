import unittest
from datetime import datetime
from main import Car,Bus,Bike

class TestCarParking(unittest.TestCase):
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

class TestBikeParking(unittest.TestCase):
    def test_bike_parking_fee(self):
        bike = Bike("BK202")
        entry = datetime(2025, 7, 25, 10, 0, 0)
        exit = datetime(2025, 7, 25, 10, 45, 0)
        bike.set_time(entry, exit)
        self.assertEqual(bike.get_Parking_fee(), 450)  # 45 * 10

class TestBusParking(unittest.TestCase):
    def test_bus_parking_fee(self):
        bus = Bus("BS202")
        entry = datetime(2025, 7, 25, 10, 0, 0)
        exit = datetime(2025, 7, 25, 10, 10, 0)
        bus.set_time(entry, exit)
        self.assertEqual(bus.get_Parking_fee(), 500)  # 10 * 50

if __name__ == '__main__':
    unittest.main()

