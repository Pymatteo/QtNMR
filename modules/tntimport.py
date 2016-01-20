import modules.utils as utils
import numpy as np
import struct
import re
from copy import deepcopy

def tntopen(filename):
        f = open(filename[0], "rb")
        f.seek(16)
        lenghttm1 = struct.unpack('=l', f.read(4))[0]
        #f.seek(52)
        f.seek(36)
        #print(f.tell())
        acq_points = np.zeros(2, dtype=np.int32)
        acq_points[0] = struct.unpack('=l', f.read(4))[0]  ###
        acq_points[1] = struct.unpack('=l', f.read(4))[0] ###
        #print(self.__acq_points[1])
        f.seek(72)
        scans = struct.unpack('=l', f.read(4))[0]
        actual_scans = struct.unpack('=l', f.read(4))[0]
        f.seek(292)
        dwell_time_bin = struct.unpack('d', f.read(8))[0]
        #print(dwell_time)
        dwell_time = dwell_time_bin #* (10**6)
        
        data = np.zeros((acq_points[1], acq_points[0]), dtype=np.complex64)  ###     

        f.seek(32+lenghttm1)     # Go to the 1056th byte in the file read data
        # prepare time array
        time = np.arange(acq_points[0]) * dwell_time  ###
		
        for jj in range(acq_points[1]):
           for ii in range(acq_points[0]):
                   data[jj,ii] = struct.unpack('=f', f.read(4))[0] 
                   data[jj,ii] += 1j * struct.unpack('=f', f.read(4))[0] 

        #end of data reading; start of delay table reading

        step_read = 32+lenghttm1+8*acq_points[0]*acq_points[1]+8
        f.seek(step_read)
        TMG2lenght = struct.unpack('=l', f.read(4))[0]
        step_read = step_read + TMG2lenght + 4 
        f.seek(step_read)
        search_region = f.read()
        delay_re = re.compile(b'de[0-9]+:[0-9]')

        delay_tables = {}  ###
        delay_tables_si = {}  ###
        for match in delay_re.finditer(search_region):
                offset = (match.start()-4 )
                delay_name = utils.read_string(search_region[offset:])
                offset = match.start() + len(delay_name)
                delay = utils.read_string(search_region[offset:])
                # Now check for delay tables of length one and discard them
                if len(delay) > 1:
                    delay = utils.make_str(delay)
                    delay = delay.split()   
                    delay_name = utils.make_str(delay_name)
                    #delay = convert_si(delay)
                    delay_tables[delay_name] = utils.make_str(delay)
                    #print(delay_tables)
                    delay_tables_si[delay_name] = utils.convert_si(deepcopy(delay))
                    #print(delay_tables_si[delay_name])
        
        f.close()    

        return acq_points, data, time, delay_tables, delay_tables_si, scans, actual_scans




