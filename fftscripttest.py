import numpy as np

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

# This variable controll the streght of the exponential apodization #
## change it as needed, experiemnt before... (1000 is often good)####
LB=1000
#####################################################################
self.dat.setLB(LB)


def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False
    
def find_nearest(array,value,np):
    idx = np.abs(array-value).argmin()
    return idx
    

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

echo_center=(selection[1]-selection[0])/2+selection[0]

spectrum=np.zeros(self.dat.get1dpoints())
frequencies=np.zeros(self.dat.get1dpoints())

print('##############')
print('initilize fft sum')
print('##############')

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
      if (frequencies_temp[0] < np.amin(frequencies)) or (frequencies_temp[0] > np.amax(frequencies)):
       print('too wide data separation')
      else: 
#       print(find_nearest(frequencies,frequencies_temp[0],np))
#       print(frequencies_temp.size)
#       print(frequencies.size)
       trailing_zeros=find_nearest(frequencies,frequencies_temp[0],np)+frequencies_temp.size-frequencies.size
       leading_zeros=trailing_zeros-frequencies_temp.size+frequencies.size
       print(trailing_zeros)
       frequencies=np.append(frequencies,frequencies_temp[-trailing_zeros:])
       spectrum=np.append(spectrum,np.zeros(trailing_zeros))
       spectrum_temp=np.append(np.zeros(leading_zeros),spectrum_temp)
       spectrum=spectrum+spectrum_temp
       print(frequencies_temp.size)
       print(frequencies.size)
       print(spectrum.size)
    

spectrum=np.column_stack((frequencies,spectrum))

np.savetxt(folder+'/spectrum_fftsum_'+folder.rsplit('/',1)[1]+'.dat', spectrum, delimiter=' ')


plt.ion()
plt.clf()

fig=plt.figure(1)
plt.plot(spectrum[:,0], spectrum[:,1])

plt.xlabel('Frequency (MHz)')
plt.ylabel('Intensity')
plt.title("Spectrum "+folder.rsplit('/',1)[1])

plt.ioff()
