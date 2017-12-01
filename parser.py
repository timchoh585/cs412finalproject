import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

data = pd.read_csv( 'data.csv', usecols=[ "ACCOUNT NUMBER", "DOING BUSINESS AS NAME", "WARD", "LICENSE CODE", "LICENSE DESCRIPTION", "BUSINESS ACTIVITY",
                    "APPLICATION TYPE", "LICENSE TERM START DATE", "LICENSE TERM EXPIRATION DATE", "LICENSE APPROVED FOR ISSUANCE",
                    "DATE ISSUED", "POLICE DISTRICT", "LATITUDE", "LONGITUDE" ] )

fixedData = data.dropna( subset=['WARD', 'LICENSE CODE', 'LATITUDE', 'LONGITUDE', 'DOING BUSINESS AS NAME', 'LICENSE DESCRIPTION', 'LICENSE TERM START DATE', 'LICENSE TERM EXPIRED DATE' ] )

fixedData.sort_values( [ 'WARD', 'LICENSE TERM START DATE' ], ascending = [ True, True ] ).to_csv( r'map.csv', sep = ',', index = False, header = True, mode = 'a' )

fixedData.sort_values( [ 'WARD', 'LICENSE TERM START DATE' ], ascending = [ True, True ] ).to_csv( r'testing.csv', sep = ',', index = False, header = True, mode = 'a' )
