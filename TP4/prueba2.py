import warnings
warnings.filterwarnings('ignore')
import scipy.signal as sig
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.io as sio

def vertical_flaten(a):
    
    return a.reshape(a.shape[0],1)

fig_sz_x = 5
fig_sz_y = 4
fig_dpi = 80 # dpi

fig_font_family = 'Ubuntu'
fig_font_size = 10

sio.whosmat('ECG_TP4.mat')
mat_struct = sio.loadmat('ECG_TP4.mat')

ecg_one_lead = mat_struct['ecg_lead']
ecg_one_lead = ecg_one_lead.flatten(1)
cant_muestras = len(ecg_one_lead)

fs = 1000 # Hz
nyq_frec = fs / 2


# filter design
ripple = 0.5 # dB
atenuacion = 40 # dB

ws1 = 1.0 #Hz
wp1 = 3.0 #Hz
wp2 = 15.0 #Hz
ws2 = 35.0 #Hz

frecs = np.array([0.0,         ws1,         wp1,     wp2,     ws2,         nyq_frec   ]) / nyq_frec
gains = np.array([-atenuacion, -atenuacion, -ripple, -ripple, -atenuacion, -atenuacion])
gains = 10**(gains/20)


bp_sos_butter = sig.iirdesign(wp=np.array([wp1, wp2]) / nyq_frec, ws=np.array([ws1, ws2]) / nyq_frec, gpass=0.5, gstop=40., analog=False, ftype='butter', output='sos')
bp_sos_cheby = sig.iirdesign(wp=np.array([wp1, wp2]) / nyq_frec, ws=np.array([ws1, ws2]) / nyq_frec, gpass=0.5, gstop=40., analog=False, ftype='cheby1', output='sos')
bp_sos_cauer = sig.iirdesign(wp=np.array([wp1, wp2]) / nyq_frec, ws=np.array([ws1, ws2]) / nyq_frec, gpass=0.5, gstop=40., analog=False, ftype='ellip', output='sos')

cant_coef = 501

num_firls = sig.firls(cant_coef, frecs, gains, fs=fs)
num_remez = sig.remez(cant_coef, frecs, gains[::2], fs=fs)
num_win =   sig.firwin2(cant_coef, frecs, gains , window='blackmanharris' )

den = 1.0

######################################################################################################

plt.rcParams.update({'font.size':fig_font_size})
plt.rcParams.update({'font.family':fig_font_family})

w, h_butter = sig.sosfreqz(bp_sos_butter)
_, h_cheby = sig.sosfreqz(bp_sos_cheby)
_, h_cauer = sig.sosfreqz(bp_sos_cauer)
_, hh_firls = sig.freqz(num_firls, den)
_, hh_remez = sig.freqz(num_remez, den)
_, hh_win = sig.freqz(num_win, den)

w = w / np.pi * nyq_frec


#plt.figure(figsize=(fig_sz_x, fig_sz_y), dpi= fig_dpi, facecolor='w', edgecolor='k')

#plt.plot(w, 20*np.log10(np.abs(h_butter)), label='IIR-Butter' )
#plt.plot(w, 20*np.log10(np.abs(h_cheby)), label='IIR-Cheby' )
#plt.plot(w, 20*np.log10(np.abs(h_cauer)), label='IIR-Cauer' )
#plt.plot(w, 20 * np.log10(abs(hh_firls)), label='FIR-ls')
#plt.plot(w, 20 * np.log10(abs(hh_remez)), label='FIR-remez')
#plt.plot(w, 20 * np.log10(abs(hh_win)), label='FIR-Win')
#plt.plot(frecs * nyq_frec, 20*np.log10(gains), 'rx', label='plantilla' )

#plt.title('FIR diseñado por métodos directos')
#plt.xlabel('Frequencia [Hz]')
#plt.ylabel('Modulo [dB]')
#plt.axis([0, nyq_frec, -60, 5 ]);

#plt.grid()

#axes_hdl = plt.gca()
#axes_hdl.legend()

#plt.show()

###############################################################################################

ECG_f_butt = sig.sosfiltfilt(bp_sos_butter, ecg_one_lead)
ECG_f_cheb = sig.sosfiltfilt(bp_sos_cheby, ecg_one_lead)
ECG_f_cauer = sig.sosfiltfilt(bp_sos_cauer, ecg_one_lead)

ECG_f_ls = sig.filtfilt(num_firls, den, ecg_one_lead)
ECG_f_remez = sig.filtfilt(num_remez, den, ecg_one_lead)
ECG_f_win = sig.filtfilt(num_win, den, ecg_one_lead)

# Segmentos de interés
regs_interes = ( 
        np.array([0, 1000]), # minutos a muestras
        )

for ii in regs_interes:
    
    # intervalo limitado de 0 a cant_muestras
    zoom_region = np.arange(np.max([0, ii[0]]), np.min([cant_muestras, ii[1]]), dtype='uint')
    
    plt.figure(figsize=(fig_sz_x, fig_sz_y), dpi= fig_dpi, facecolor='w', edgecolor='k')
    plt.plot(zoom_region, ecg_one_lead[zoom_region], label='ECG', lw=2)
    #plt.plot(zoom_region, ECG_f_butt[zoom_region], label='Butter')
    #plt.plot(zoom_region, ECG_f_cheb[zoom_region], label='Cheby')
    #plt.plot(zoom_region, ECG_f_cauer[zoom_region], label='Cauer')
    #plt.plot(zoom_region, ECG_f_remez[zoom_region], label='Remez')
    #plt.plot(zoom_region, ECG_f_ls[zoom_region], label='LS')
    #plt.plot(zoom_region, ECG_f_win[zoom_region], label='Win')
    
    plt.title('ECG filtering example from ' + str(ii[0]) + ' to ' + str(ii[1]) )
    plt.ylabel('Adimensional')
    plt.xlabel('Muestras (#)')
    
    axes_hdl = plt.gca()
    axes_hdl.legend()
    axes_hdl.set_yticks(())
            
    plt.show()















