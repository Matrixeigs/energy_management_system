# The configuration file of local databases and network databases


universal_database = \
    {
        "db_str" : 'mysql+pymysql://' + 'root' + ':' + 'Ntu@1003' + '@' + 'localhost' + '/' + 'universal_ems'
    }

local_database = \
    {
        "db_str" : 'mysql+pymysql://' + 'root' + ':' + 'Ntu@1003' + '@' + 'localhost' + '/' + 'local_ems'
    }

#IP address of local EMSs,
local_ems_ip_address = \
    {
        'module1':'192.168.1.150'
    }
