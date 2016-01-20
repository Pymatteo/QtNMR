self.select2d(1)
point2d = self.echo_find(True)
self.auto_phase(point2d)

self.setShifter(0.000256)
self.sqr_apodization()

self.setShifter(0.000053)
self.left_shift(True)
self.zerofill()

self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()
self.exp_apodization()


self.fourier(True)
self.export()


