import numpy as np

import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

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

print(spectrum)

np.savetxt(folder+'/spectrum_'+folder.rsplit('/',1)[1]+'.dat', spectrum, delimiter=' ')


plt.ion()
plt.clf()

fig=plt.figure(1)
plt.scatter(spectrum[:,0], spectrum[:,1])

plt.xlabel('Frequency (MHz)')
plt.ylabel('Intensity')
plt.title("Spectrum "+folder.rsplit('/',1)[1])

plt.ioff()
