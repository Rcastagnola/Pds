import numpy as np
import matplotlib.pylab as plt
import scipy.signal as signal

def Rectangular (N,x):
    
    ventana = signal.boxcar(N)
    
    salida = np.multiply(x,ventana)

    return salida

def Bartlett (N,x):
    
    ventana = signal.bartlett(N)
    
    salida = np.multiply(x,ventana)

    return salida

def Hann (N,x):
    
    ventana = signal.windows.hann(N)
    
    salida = np.multiply(x,ventana)

    return salida

def Blackman (N,x):
    
    ventana = signal.blackman(N)
    
    salida = np.multiply(x,ventana)

    return salida

def Flattop (N,x):
    
    ventana = signal.flattop(N)
    
    salida = np.multiply(x,ventana)

    return salida

N = 1000
fs = 1000
a0 = 2
f0 = 10

señal = 1

rectangular = Rectangular(N,señal)
bartlett = Bartlett(N,señal)
hann     = Hann(N,señal)
blackman = Blackman(N,señal)
flattop  = Flattop(N,señal)

sp0 = np.fft.fft(rectangular,2048)/25.5
sp1 = np.fft.fft(bartlett,2048)/25.5
sp2 = np.fft.fft(hann,2048)/25.5
sp3 = np.fft.fft(blackman,2048)/25.5
sp4 = np.fft.fft(flattop,2048)/25.5

freq = np.linspace(0, 1, 100)

plt.title('Ventana Rectangular' )
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.plot(rectangular)
plt.show()
plt.title('Espectro' )
plt.ylabel("Magnitud [dB]")
plt.xlabel("Frequencia")
plt.plot(freq, 20*np.log10(np.absolute(sp0)[0:100]))
plt.show()

plt.title('Ventana Bartlett' )
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.plot(bartlett)
plt.show()
plt.title('Espectro' )
plt.ylabel("Magnitud [dB]")
plt.xlabel("Frequencia")
plt.plot(freq, 20*np.log10(np.absolute(sp1)[0:100]))
plt.show()

plt.title('Ventana Hann' )
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.plot(hann)
plt.show()
plt.title('Espectro' )
plt.ylabel("Magnitud [dB]")
plt.xlabel("Frequencia")
plt.plot(freq, 20*np.log10(np.absolute(sp2)[0:100]))
plt.show()

plt.title('Ventana Blackman' )
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.plot(blackman)
plt.show()
plt.title('Espectro' )
plt.ylabel("Magnitud [dB]")
plt.xlabel("Frequencia")
plt.plot(freq, 20*np.log10(np.absolute(sp3)[0:100]))
plt.show()

plt.title('Ventana Flat-top' )
plt.ylabel("Amplitude")
plt.xlabel("Sample")
plt.plot(flattop)
plt.show()
plt.title('Espectro' )
plt.ylabel("Magnitud [dB]")
plt.xlabel("Frequencia")
plt.plot(freq, 20*np.log10(np.absolute(sp4)[0:100]))
plt.show()



