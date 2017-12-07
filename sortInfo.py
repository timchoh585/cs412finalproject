import hyperparameters
import sys
from math import sin, cos, sqrt, atan2, radians
import time
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

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


    min_time = "01/01/2020"
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
                
                        
            startFrame = matrix[i][tempStart]
            endFrame = matrix[i][tempEnd]
            if endFrame == "":
                endFrame = "12/7/2017"
            timeFrame = startFrame + '-' + endFrame

            tempTime = timeFrame

            cur_min = [int(x) for x in startFrame.split('/')]
            old_min = [int(x) for x in min_time.split('/')]

            if old_min[2] > cur_min[2]:
                min_time = startFrame
            elif old_min[2] == cur_min[2]:
                if old_min[0] > cur_min[0]:
                    min_time = startFrame
                elif old_min[0] == cur_min[0] and old_min[1] > cur_min[1]:
                    min_time = startFrame

            matrix_fixed.append( [ str(v_lat), str(v_lon), str( tempTime ) ] )

        except:
            "ignore that point"

    east_west = distance( 0,0, max_longitude, min_longitude )
    south_north = distance( max_latitude, min_latitude, 0,0 )

    for i in range( len( matrix_fixed ) ):
        x = distance( min_latitude, float( matrix_fixed[i][0] ), min_longitude, min_longitude )
        y = distance( min_latitude, min_latitude, min_longitude, float( matrix_fixed[i][1] ) )

        frameCounter = 0

        frame = matrix_fixed[i][2].split( "-" )
        startDate = frame[0]
        endDate = frame[1]

        minDate = min_time

        minimum = datetime.strptime( minDate, '%m/%d/%Y' ).date()
        start = datetime.strptime( startDate, '%m/%d/%Y' ).date()
        end = datetime.strptime( endDate, '%m/%d/%Y' ).date()



        startSpread = minimum
        endSpread = minimum

        minToStart = []
        startCounter = 0

        while startSpread < start:
            minToStart.append( str( startCounter ) )
            startSpread += relativedelta( months=2 )
            startCounter += 1

        difference = []
        while start < end:
            difference.append(str(startCounter))
            startCounter += 1
            start += relativedelta(months= 2)

        matrix_fixed[i][0] = str( x )
        matrix_fixed[i][1] = str( y )
        matrix_fixed[i][2] = ";".join( difference )

        labels = [ "max_latitude","min_latitude","max_longitude","min_longitude", "east_west","south_north" ]
        result = [ max_latitude, min_latitude, max_longitude, min_longitude, east_west, south_north ]

        destination.write( ",".join( labels ) + "\n" )
        destination.write( ",".join( [ str( x ) for x in result ] ) )

        fixed_data.write( ",".join( [ x for x in matrix_fixed[i] ] ) )
 
    print( matrix_fixed )


######
#TEST RUN
######
fix_data( hyperparameters.test_db )
