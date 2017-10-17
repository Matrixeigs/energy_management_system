# The root configuration of energy internet
#

default_operation_mode=\
    {
        "Operation_serve_mode" : 1, # The EMS is a server or a client, 1=the ems is a server,0=the ems is a client
        "Grid_connnected" : 1,#The system is connected to the main grid ?
        "Micro_grid_connected": 0, #The MG is conncted to external grid or not ?
    }
#When the ems works as the server, the ems is a universal energy management system.
#When the ems works as the client, the ems is a local energy management system.

#When the grid is conncted, the MG needs to estilish the information model relating the eternal power systems.
#When the MG is connected to other MGs, the information relating to neighboring MGs should be estibilished.
