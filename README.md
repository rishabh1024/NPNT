# NPNT

MAVProxy is the main program handling all the Pre-Arm Checks
1. Date and Time Check using: func ParseXML()
2. Verifying Permission Artifact Signature using : func VerifySig()
3. GeoFenceCheck using : func picket.fence()

After Successful Pre-Arm Checks Drone is Armed.
Once the flight starts func Telemetry_data_json is called
 periodically using mavutil periodic function.
The telemetry_data_json file creates a json formated file which
contains all telemetry log information.
After the flight is over the sign_log() is called to sign the json file.
