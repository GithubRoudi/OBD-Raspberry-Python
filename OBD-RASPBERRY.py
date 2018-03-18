import obd
import time
from db_connection import db_connection as dbc

#push time to DataBase to order the results
def push_time():
    LocalTime = time.strftime("%d %m %Y %X ", time.localtime())
    LocalTime = LocalTime[6:10]+LocalTime[3:5]+LocalTime[0:2]+LocalTime[11:13]+LocalTime[14:16]+LocalTime[17:19]
    return (LocalTime)
# OBD setup
obd.logger.setLevel(obd.logging.DEBUG)

# Connect to OBDII adapter
ports = obd.scan_serial()
print("Ports: ")
print(ports)

connection = obd.OBD(ports[0])
print("Connection status: ")
print(connection.status())

while (True):
	try:
# Send a command
		SpeedCmd = connection.query(obd.commands.SPEED)
		SpeedVal = str(SpeedCmd.value)
		
		RPMCmd = connection.query(obd.commands.RPM)
		RPMVal = str(RPMCmd.value)
		
		StatusCmd = connection.query(obd.commands.STATUS)
		StatusVal = str(StatusCmd.value)
		
		EngineLoadCmd = connection.query(obd.commands.ENGINE_LOAD)
		EngineLoadVal = str(EngineLoadCmd.value)
		
		BarometricPressureCmd = connection.query(obd.commands.BAROMETRIC_PRESSURE)
		BarometricPressureVal = str(BarometricPressureCmd.value)
		
		DistanceSinceDtcClearedCmd = connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEARED)
		DistanceSinceDtcClearedVal = str(DistanceSinceDtcClearedCmd.value)
		
		EvapVapPressureCmd = connection.query(obd.commands.EVAP_VAP_PRESSURE)
		EvapVapPressureVal = str(EvapVapPressureCmd.value)
		
		FuelTypeCmd = connection.query(obd.commands.FUEL_TYPE)
		FuelTypeVal = str(FuelTypeCmd.value)
		
		OilTempCmd = connection.query(obd.commands.OIL_TEMP)
		OilTempVal = str(OilTempCmd.value)
		
		HybridBatteryRemainingCmd = connection.query(obd.commands.HYBRID_BATTERY_REMAINING)
		HybridBatteryRemainingVal = str(HybridBatteryRemainingCmd.value)
		
		TimeSinceDtcClearedCmd = connection.query(obd.commands.TIME_SINCE_DTC_CLEARED)
		TimeSinceDtcClearedVal = str(TimeSinceDtcClearedCmd.value)
		
#the list can go on to take all commands
		print("Status: " + StatusVal + ", RPM: " + RPMVal + ", Speed: " + SpeedVal + ", 
		      Engine Load: " + EngineLoadVal + ", Barometric Pressure: " + BarmetricPressureVal)

#Request all Error Codes
		ErrorsCmd = connection.querry(obd.commands.GET_DTC)
		ErrorsVal = ErrorsCmd.value
#Print all Errors
		print(ErrorsVal)
#handle OBD connection exceptions		
	except Exception as ex:
		print("Error: " + str(ex))
#Post Data to DataBase
	dbc.push_to_db(BarmetricPressureVal, SpeedVal, RPMVal, OilTempVal, HybridBatteryRemainingVal, 
		       TimeSinceDtcClearedVal, FuelTypeVal,  EvapVapPressureVal, DistanceSinceDtcClearedVal, 
		       EngineLoadVal, ErrorsVal, Status, push_time())
#Request data every minute
	time.sleep(60) 
# Close the connection
connection.close()

