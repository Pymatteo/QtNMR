#self.select2d(0)


#self.select2d(0)
point2d = self.echo_find(True)
self.auto_phase()

#self.setShifter(0.000256)
#self.sqr_apodization()

self.setShifter(0.000042)
self.left_shift(True)
self.zerofill()

self.exp_apodization()



self.fourier(True)
#self.auto_phase()
self.export()


