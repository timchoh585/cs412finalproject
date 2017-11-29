import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

data = pd.read_csv( 'Business_Licenses.csv', usecols=[ "ACCOUNT NUMBER", "WARD", "LICENSE CODE", "LICENSE DESCRIPTION", "BUSINESS ACTIVITY",
                    "APPLICATION TYPE", "LICENSE TERM START DATE", "LICENSE TERM EXPIRATION DATE", "LICENSE APPROVED FOR ISSUANCE",
                    "DATE ISSUED", "POLICE DISTRICT" ] )

data.sort_values( [ 'WARD', 'LICENSE TERM START DATE' ], ascending = [ True, True ] )

data.groupby( [ 'WARD', 'LICENSE DESCRIPTION' ] ).nunique().to_csv( r'pandas.txt', sep = ' ', index = False, header = False, mode = 'a' )