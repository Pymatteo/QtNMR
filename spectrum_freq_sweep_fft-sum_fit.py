
# This variable controll the streght of the exponential apodization #
## change it as needed, experiemnt before... (1000 is often good)####
LB=9000
#####################################################################

#  number of points to be cutted at the tail of the spectra (try...)
cutted=950
#####################################################################

#  threshold for echo find (TEST IT!!!!)
threshold=15
#####################################################################


import numpy as np

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path


self.dat.setLB(LB)
self.dat.setThreshold(threshold)

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False
    
def find_nearest(array,value,np=np):
    idx = np.abs(array-value).argmin()
    return idx
    

def gauss(x, *p,np=np):
    A, mu, sigma, offset = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2)) + offset
##    return (A/(w*numpy.sqrt(numpy.pi/2)))*numpy.exp(- 2 * ((x-mu)/w**2/(2.*sigma**2)) + offset

np.set_printoptions(precision=5)

filelist = utils.filelist(self.dat.getFilename()[0])
#print(filelist)

folder = self.dat.getFilename()[0].rsplit('/',1)[0]
folder = folder.replace("\\", "/")

signal_max=[0,'']

spectra_list=[]

for ii in filelist:
   if isint(ii.split('/')[-1].split('.')[-2]):
      print(ii)
      spectra_list = spectra_list + [ii]
      
print(spectra_list)      

for ii in spectra_list:
    self.loadFile((ii,'*.tnt'))
    integral, magnitude_integral = self.dat.find_phcorr_int()
#    print(integral, magnitude_integral)
    if magnitude_integral[0] >  signal_max[0]:
       signal_max=[magnitude_integral[0],ii]

#print('signalmax',signal_max)
self.loadFile((signal_max[1],'*.tnt'))
self.echo_find()

selection=self.dat.getSelection()

self.save_selection()

#################################
echo_center=(selection[1]-selection[0])/2+selection[0]

# you can also set it manually!##
#echo_center=0.000020
##################################

spectrum=np.zeros(self.dat.get1dpoints())
frequencies=np.zeros(self.dat.get1dpoints())

print('##################')
print('initilize fft sum')
print('##################')

for ii in spectra_list:
    print(ii)
    self.loadFile((ii,'*.tnt'))
    self.load_selection()
    self.dat.auto_phase()
    self.dat.setShifter(echo_center)
    self.dat.left_shift(True)
    self.dat.zerofill()
    self.exp_apodization()
    self.dat.fourier(True)
    spectrum_temp=self.dat.getData()[0].real
    frequencies_temp=(self.dat.getXaxis()+int(ii.split('/')[-1].split('.')[-2])*1e3)/1e6
    if ii == spectra_list[0]:
      frequencies=frequencies_temp
      spectrum=spectrum_temp
    else:
#      if (frequencies_temp[0] < np.amin(frequencies)) or (frequencies_temp[0] > np.amax(frequencies)):
      if (frequencies_temp[0] > np.amax(frequencies)):
       print('too wide data separation')
      else: 
       trailing_zeros=find_nearest(frequencies,frequencies_temp[0])+frequencies_temp.size-frequencies.size
       leading_zeros=find_nearest(frequencies,frequencies_temp[0])
#       print(trailing_zeros)
       frequencies=np.append(frequencies,frequencies_temp[-trailing_zeros:])
       spectrum=np.append(spectrum,np.zeros(trailing_zeros))
       spectrum_temp=np.append(np.zeros(leading_zeros),spectrum_temp)
       spectrum=spectrum+spectrum_temp
       print(frequencies_temp.size)
       print(frequencies.size)
       print(spectrum.size)
    
# plot...    

spectrum=np.column_stack((frequencies,spectrum))

spectrum[:,1]= spectrum[:,1]/np.amax(spectrum[:,1])

spectrumtofit=spectrum[cutted:-cutted,:]

### A, mu, sigma offset #####
p0 = [1, (spectrumtofit[-1,0]-spectrumtofit[0,0])/2+spectrumtofit[0,0], 
      (spectrumtofit[-1,0]-spectrumtofit[0,0])/5, 0]
#############################

coeff, var_matrix = curve_fit(gauss, spectrumtofit[:,0], spectrumtofit[:,1], p0=p0)
fitted = gauss(spectrumtofit[:,0], *coeff)

print('paramsfit', coeff)

plt.ion()
plt.clf()

fig=plt.figure(1)
plt.plot(spectrum[cutted:-cutted,0], spectrum[cutted:-cutted,1],'b-', label='data')
plt.plot(spectrum[cutted:-cutted,0],fitted,'r-', label='fit')

plt.xlabel('Frequency (MHz)')
plt.ylabel('Intensity')
plt.legend()
plt.title("Spectrum "+folder.rsplit('/',1)[1]+' ; Fit Par (A, mu, sigma, offset): \n'+ str(coeff))

plt.ioff()

printed_spectrum=np.column_stack((spectrum[cutted:-cutted,:],fitted))

np.savetxt(folder+'/spectrum_fftsum_'+folder.rsplit('/',1)[1]+'.dat', 
           printed_spectrum, delimiter=' ')


#############################
logfilename = folder.rsplit('/',1)[0]+'/linefits.dat'
#############################
temperature=folder.rsplit('/',1)[1][:-1]

test_file = Path(logfilename)

perr = np.sqrt(np.diag(var_matrix))

print('perr',perr)

if test_file.is_file():
   with open(logfilename,'a') as logfile:
            logfile.write(temperature+' '+str(coeff[0])+' '+str(perr[0])+' '+str(coeff[1])
              +' '+str(perr[1])+' '+str(coeff[2])+' '+str(perr[2])+' '+str(coeff[3])+' '+
              str(perr[3])+' '+str(coeff[2]*2.35482)+' '+str(perr[2]*2.35482)+' '+'\n')
             
else:
   with open(logfilename,'w') as logfile:
            logfile.write('Temperature A e mu e sigma e offset e FWHM e'+'\n')
            logfile.write(temperature+' '+str(coeff[0])+' '+str(perr[0])+' '+str(coeff[1])
              +' '+str(perr[1])+' '+str(coeff[2])+' '+str(perr[2])+' '+str(coeff[3])+' '+
              str(perr[3])+' '+str(coeff[2]*2.35482)+' '+str(perr[2]*2.35482)+' '+'\n')


