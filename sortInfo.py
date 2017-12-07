import hyperparameters
import sys
from math import sin, cos, sqrt, atan2, radians

def distance(lat1,lat2, lon1, lon2):
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    dlat = lat2-lat1
    dlon = lon1-lon2
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    return 6373.0 * 2 * atan2(sqrt(a),sqrt(1-a))

def fix_data(filename):
    # data.csv is 10 samples
    
    #
    # Had to change my filename to "data.csv" because
    # it is called that in repository
    #
    
    filename = "data.csv"
    #
    
    source = open(filename, "rb")
    destination = open(hyperparameters.edge_data,"w")
    fixed_data = open(hyperparameters.db_fixed,"w")    

    data = source.read().decode("utf-8").split("\n")
    labels = data[0].split(",")


    #for temp in data:
        #print(temp)

    #put only necessary labels in 
    fixed_data.write("x_location,y_location,time_frame\n")
    #erase headers in data.csv
    data = data[1:]
    #matrix of the data
    matrix = [i.split(",") for i in data]

    #calculate maxmin of latitude and longitude
    #index_lat/lon are indices of those columns in data.csv
    index_lat = labels.index("LATITUDE")
    index_lon = labels.index("LONGITUDE")
    
    #get indices of start/end term dates
    index_start = labels.index("LICENSE TERM START DATE")
    index_end   = labels.index("LICENSE TERM EXPIRATION DATE")
        
    #init matrix for fixed_data    

    matrix_fixed = []
    temp_matrix = []
    tempTime = ''

    max_latitude = float( matrix[0][index_lat] )
    min_latitude = float( max_latitude )
    
    max_longitude = float( matrix[0][index_lon] )
    min_longitude = float( max_longitude )


    min_time = "-1"
    for i in range( len( matrix ) ):
        lat = index_lat
        lon = index_lon
        tempStart = index_start
        tempEnd = index_end

        try:
            float(matrix[i][lat])
            
        #fix for some awesome dataponts
        #for that cool businesses that use comma in names
        #love them
        
        except:
            lat +=2
            lon +=2
            
            # if the lat/lon index is switched, so are the start/end dates
            tempStart +=2
            tempEnd+=2
            
        try:
            v_lat = float(matrix[i][lat])
            v_lon = float(matrix[i][lon])

            if v_lat > 44 or v_lat < 40 or v_lon > -85 or v_lon < -89:
                raise

            if max_latitude < v_lat:
                max_latitude = v_lat

            if min_latitude > v_lat:
                min_latitude = v_lat
                   
            if max_longitude < v_lon:
                max_longitude = v_lon

            if min_longitude > v_lon:
                min_longitude = v_lon
                
                        
            startframe = matrix[i][tempStart]
            endframe = matrix[i][tempEnd]
            timeframe = startframe + '-' + endframe

            tempTime = timeframe
            matrix_fixed.append([str(v_lat), str(v_lon), tempTime])

            #TODO RN
            if min_time == "-1":
                min_time =timeframe
            min_time = "update"

        except:
            "ignore that point"

    east_west = distance( 0,0, max_longitude, min_longitude )
    south_north = distance( max_latitude, min_latitude, 0,0 )

    for i in range( len( matrix_fixed) ):
        x = distance( min_latitude,matrix_fixed[i][0],min_longitude,min_longitude )
        y = distance( min_latitude,min_latitude,min_longitude,matrix_fixed[i][1] )

        #TODO RN CONVERT TO SOME INT VALUE THAT INDICATES THE TIME FRAME ##
        #IE. THE FIRST TIME FRAME HAS VALU1 1, ALL DATAPOINT AT THAT PERIOD WILL HAVE VALUE 1
        #THEN INCREMENT
        #THE SIZE OF THE FRAME IS 2 MONTHS
        fixed_time = "??"


        matrix_fixed[i][0] = str(x)
        matrix_fixed[i][1] = str(y)
        matrix_fixed[i][2] = str(fixedTime)

        labels = [ "max_latitude","min_latitude","max_longitude","min_longitude", "east_west","south_north" ]
        result = [ max_latitude, min_latitude, max_longitude, min_longitude, east_west, south_north ]

        destination.write( ",".join( labels ) + "\n" )
        destination.write( ",".join( [ str( x ) for x in result ] ) )

        fixed_data(",".join([x for x in matrix_fixed[i]]))

    print( matrix_fixed )


def read_and_convert_to_tensor(source):
    matrix = [x.split(',') for x in open(source,"r").read().split("\n")]

   # number of blocks that we have
    point_len = 9*1
    data = []
    for row in matrix:
        x = row[0]
        y = row[1]
        times = row[2]
        block = int(int(x)/2) + 3 * int(y)
        for frame in times.split(';'):
            id = int(frame)
            # expand if requires
            if len(data)<= id:
                for i in range(len(data), id+1):
                    data.append([0 for k in range(point_len)])
            data[id][block] += 1

    return data
######
#TEST RUN
######
