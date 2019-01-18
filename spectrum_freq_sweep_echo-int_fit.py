import numpy as np

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

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

for ii in filelist:
   if isint(ii.split('/')[-1].split('.')[-2]):
    self.loadFile([ii,''])
    integral, magnitude_integral = self.dat.find_phcorr_int()
    print(integral, magnitude_integral)
    if magnitude_integral[0] >  signal_max[0]:
       signal_max=[magnitude_integral[0],ii]

#print('signalmax',signal_max)
self.loadFile([signal_max[1],''])
self.echo_find()

self.save_selection()

spectrum=[]

for ii in filelist:
   if isint(ii.split('/')[-1].split('.')[-2]):
    self.loadFile([ii,''])
    self.load_selection()
    integral, magnitude_integral = self.dat.bc_phcorr_int()
    spectrum.append([int(ii.split('/')[-1].split('.')[-2])/1000,integral.real[0]])


spectrum= np.array(spectrum)
spectrum[:,1]= spectrum[:,1]/np.amax(spectrum[:,1])  

spectrumtofit=spectrum

### A, mu, sigma offset #####
p0 = [1, (spectrumtofit[-1,0]-spectrumtofit[0,0])/2+spectrumtofit[0,0], 
      (spectrumtofit[-1,0]-spectrumtofit[0,0])/5, 0]
#############################

coeff, var_matrix = curve_fit(gauss, spectrumtofit[:,0], spectrumtofit[:,1], p0=p0)
fitted = gauss(np.arange(spectrumtofit[0,0],spectrumtofit[-1,0],0.001), *coeff)

print('paramsfit', coeff)

fitted_spectrum=np.column_stack((np.arange(spectrumtofit[0,0],spectrumtofit[-1,0],0.001),fitted))

np.savetxt(folder+'/spectrum_int_'+folder.rsplit('/',1)[1]+'.dat', spectrum, delimiter=' ')
np.savetxt(folder+'/spectrum_intfit_'+folder.rsplit('/',1)[1]+'.dat', fitted_spectrum, delimiter=' ')

plt.ion()
plt.clf()

fig=plt.figure(1)
plt.scatter(spectrum[:,0], spectrum[:,1], label='data')
plt.plot(np.arange(spectrumtofit[0,0],spectrumtofit[-1,0],0.001),fitted,'r-', label='fit')
plt.legend()
plt.xlabel('Frequency (MHz)')
plt.ylabel('Intensity')

plt.title("Spectrum "+folder.rsplit('/',1)[1]+' ; Fit Par (A, mu, sigma, offset): \n'+ str(coeff))

plt.ioff()


#############################
logfilename = folder.rsplit('/',1)[0]+'/linefitsint.dat'
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
              
              
              
