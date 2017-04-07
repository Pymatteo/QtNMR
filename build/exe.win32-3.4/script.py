import matplotlib
#matplotlib.use('qt5agg')
import matplotlib.pyplot as plt

plt.ion()
plt.clf()
x = np.linspace(0, 2, 100)
fig=plt.figure(1)
plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
       
plt.legend()
plt.ioff()
self.loadSaved()
