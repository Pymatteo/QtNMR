#self.select2d(0)


#self.select2d(0)
point2d = self.dat.echo_find(True)
self.dat.auto_phase()

#self.setShifter(0.000256)
#self.sqr_apodization()

self.dat.setShifter(0.000042)
self.dat.left_shift(True)
self.dat.zerofill()

self.dat.exp_apodization()



self.dat.fourier(True)
#self.auto_phase()
self.dat.export()


