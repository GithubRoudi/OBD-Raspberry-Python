import obd

# OBD setup
obd.logger.setLevel(obd.logging.DEBUG)

# Connect to OBDII adapter
ports = obd.scan_serial()
print("Ports: ")
print(ports)

connection = obd.OBD(ports[0])
print("Connection status: ")
print(connection.status())

# Send a command
try:
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
#the list can go on to take all commands
    print("Status: " + StatusVal + ", RPM: " + RPMVal + ", Speed: " + SpeedVal + ", Engine Load: " + EngineLoadVal + ", Barometric Pressure: " + BarmetricPressureVal)

#Request all Error Codes
    ErrorsCmd = connection.querry(obd.commands.GET_DTC)
    ErrorsVal = ErrorsCmd.value
#Print all Errors
    print(ErrorsVal)
except Exception as ex:
    print("Error: " + str(ex))
    
# Close the connection
connection.close()
