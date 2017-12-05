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
    # filename = "data.csv"
    #
    
    source = open(filename, "rb")
    destination = open(hyperparameters.edge_data,"w")
    fixed_data = open(hyperparameters.db_fixed,"w")    

    data = source.read().decode("utf-8").split("\n")
    labels = data[0].split(",")


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
    
    #assign current max/min values for lat/lon
    max_latitude = float(matrix[0][index_lat])
    min_latitude = max_latitude
    
    max_longitude = float(matrix[0][index_lon])
    min_longitude = float(max_longitude)
    
    for i in range(len(matrix)):
        lat = index_lat
        lon = index_lon
        tempStart = index_start
        tempEnd = index_end
        
        
        #get long/lat values
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

            if v_lat > 43 or v_lat < 40 or v_lon > -85 or v_lon < -89:
                raise
            if max_latitude < v_lat:
                max_latitude = v_lat
            if min_latitude > v_lat:
                min_latitude = v_lat
                   
            if max_longitude < v_lon:
                max_longitude = v_lon
            if min_longitude > v_lon:
                min_longitude = v_lon
                
            matrix_fixed.append(matrix[i][lat] + ',')
            matrix_fixed.append(matrix[i][lon] + ',')
        except:
            "ignore that point"
            
        #get time frame values
        try:
            #
            # get start date and end date and combine them into one string
            #
            
            startframe = matrix[i][tempStart]
            endframe = matrix[i][tempEnd]
            timeframe = startframe + '-' + endframe

            #
            # append the final string
            #
            
            matrix_fixed.append(timeframe)
                    
        except:
            "ignore that point"


    #calculate range (overestimation)
    east_west = distance(0,0, max_longitude, min_longitude)
    south_north = distance(max_latitude, min_latitude, 0,0)

    #now put data back with only necessary info
    
    counter = 0
    for entry in matrix_fixed:
        fixed_data.write(entry)
        sys.stdout.write(entry)
        counter += 1

        if counter == 3:
            fixed_data.write("\n")
            print("\n")
            
            counter = 0
            
    
    #
    #TODO : sort by date and separate to chunks 
    #
    
    
    #for i in range(len(matrix_fixed)):
    #    lat = 0.0
    #    lon = 0.0
    #    try:
    #        lat = float(matrix_fixed[i][index_lat])
    #        lon = float(matrix_fixed[i][index_lon])
    #   except:
    #        lat = float(matrix_fixed[i][index_lat+2])
    #        lon = float(matrix_fixed[i][index_lon+2])

    #    x = distance(min_latitude,lat,min_longitude,min_longitude)
    #    y = distance(min_latitude,min_latitude,min_longitude,lon)
    #    matrix_fixed[i] += [str(x),str(y)]
    #   fixed_data.write("\n" + ",".join(matrix_fixed[i]))

    #output results
                  
    labels = ["max_latitude","min_latitude","max_longitude","min_longitude", "east_west","south_north"]
    result = [max_latitude, min_latitude, max_longitude, min_longitude, east_west, south_north]

    destination.write(",".join(labels) + "\n")
    destination.write(",".join([str(x) for x in result]))



######
#TEST RUN
######
fix_data(hyperparameters.test_db)
