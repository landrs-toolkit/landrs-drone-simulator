'''
Flight Class for simple drone emulator that,
1) takes GCS mission file
2) gathers user data for a flight
2) creates class instances that are required
3) store data
4) provide access to the stored data

Chris Sweet 08/02/2020
University of Notre Dame, IN
LANDRS project https://www.landrs.org

This code provides py_drone_flight, the class for enabling data acquisition
using the LANDRS ontology.

Workflow,
1. Select mission name/description for Flight
2. Select wp file from missions, defines sosa:procedure and location
3. Generate sosa:Procedure based on the current drone, points to flight controller 
   as actuator/output, wp file as input
4. Select observable property/properties, linked to sensors, Create ObservableProperty
5. Create Place/Geometry from wp file (bounding polygon)
6. Create Feature of interest with bounding polygon and ObservableProperty. (Prop. time too)
7. Create ObservationCollection (Flight), includes ssn:startTime, ssn:endTime
8. Go fly drone, interface presents instructions, create observations
    i. Start time
    ii. Create sosa:opservations
    iii. End time
9. Create ObservationDataset
10. Download data, query etc.
'''

# Imports ######################################################################
import logging
import os

# setup logging ################################################################
logger = logging.getLogger(__name__)

################################################################################
# Class to house flight/mission functions for drone
################################################################################


class py_drone_flight():
    '''
    '''

    #######################
    # class initialization
    #######################
    def __init__(self, flight_dict):
        '''
        Args:
            flight_dict (dict):    dictionary for flight config
        '''
        self.mission_files = flight_dict.get('mission_files', './')
        self.default_file = flight_dict.get('default_file', 'Dalby-OBC2016.txt')
        print("Mission files", self.mission_files, self.default_file)

    def get_mission_files(self):
        # create a list
        missions = []
        # get the list of files
        files_in_graph_folder = os.walk(self.mission_files)
        print("Folder provided for import.")
        # loop
        for (dirpath, dirnames, filenames) in files_in_graph_folder:
            for file in filenames:
                file_path = os.path.join(dirpath, file)
                # each file if turtle
                if os.path.splitext(file_path)[-1].lower() == ".txt":
                    if os.path.isfile(file_path):
                        print("file", file_path)
                        missions.append({"path": file_path, "name": os.path.basename(file_path)})
        
        #return info
        return missions, self.default_file

    def process_mission_file(self, request_dict):
        # get lat long, guarenteed file from get_mission_files
        f=open(request_dict['missions'],"r")
        lines=f.readlines()
        #result=[]

        # find bounding box
        max_lat = 0
        max_long = 0
        min_lat = 10000
        min_long = 10000
        # split lines to get lat/long
        for x in lines:
            cols = x.split()
            # go if no data or zeros
            if len(cols) < 10 or (float(cols[8]) == 0 and float(cols[9]) == 0):
                continue
            #print("Res", cols[8], cols[9])

            latf = float(cols[8])
            longf = float(cols[9])

            # min
            if min_lat > latf:
                min_lat = latf
            if min_long > latf:
                min_long = latf

            # max
            if max_lat < longf:
                max_lat = longf
            if max_long < longf:
                max_long = longf

        f.close()

        # bounding box
        geosparql_geometry_data = {"lat": {"min": min_lat, "max": max_lat}, "long": {"min": min_long, "max": max_long}}
        print("geo", geosparql_geometry_data)
        
        return {"status": "hi info " + request_dict['missions']}

###########################################
# end of py_drone_flight class
###########################################
