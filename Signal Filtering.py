#!/usr/bin/env python
# coding: utf-8

# # PHYS 3203L FINAL EXAMINATION
# ## BITOON, GIL GARRETH L.

# In[25]:


#importing libraries and defining functions#

import pandas as pd
import numpy as np
from scipy import fftpack as fft
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
import wave
import sounddevice as sd
import time

def butter_lowpass(cutOff, fs, order=5):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low', analog = False)
    return b, a

def butter_lowpass_filter(data, cutOff, fs, order=5):
    b, a = butter_lowpass(cutOff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# ### 1. Store the signal from the excel file in an array (use the pd function from pandas and convert it to an array), then plot the magnitude of the spectrum of the noisy signal (with normalized frequency as the x-axis) and generate a sound from this noisy signal using the play function.

# In[26]:


data = pd.read_csv(r"C:\Users\caobg\Desktop\3203\speech2.csv")
data_list = data['VALUES'][:]
data_arr = data['VALUES'].to_numpy()
data.head()


# In[59]:


plt.title('Magnitude of the Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.magnitude_spectrum(data_list, Fs = 2*np.pi, scale='dB')
plt.show()


# #### Playing the signal 

# In[56]:


fs = 8000 #sampling rate

sd.play(data_list, fs)
time.sleep(5)
sd.stop()


# ### What did you hear?
#  "If you can hear this clearly, you've filtered the signal correctly". But in this instance, it is noisy.

# ### 2. From the spectrum of the noisy signal you will see that the high frequency component from the background noise covers the range |w| > 2.2, while the low frequency signal component covers the range |w| < 1.8. Now design a low pass filter with cut-off frequency of 2.0 using the butter function, and then plot the filter frequency response with as the x-axis.

# In[29]:


fs = 2*np.pi
cut_off = 2
order = 5

b, a = butter_lowpass(cut_off, fs, order)
w, h = freqz(b, a, worN = 8000)


# In[42]:


norm_freq = 0.5*fs*(w/np.pi) #normalized frequency

plt.title('Low-Pass Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.plot(norm_freq, abs(h), color='b')
plt.plot(cut_off, 0.5*np.sqrt(2), 'ko')
plt.axvline(cut_off, color='k')
plt.grid(True)
plt.show()


# ### 5. Now filter the noisy signal using the designed low pass filter you have made by utilizing the lfilter  function in python. Then plot the magnitude of the spectrum of the filtered signal and and generate a sound from this filtered signal.

# In[46]:


data_filter = butter_lowpass_filter(data_arr, cut_off, fs, order)
t = np.linspace(0, 10, len(y))


# In[54]:


plt.title('Filtered vs Unfiltered Signal')
plt.plot(t, data_list, color='blue', label='data')
plt.plot(t, data_filter, color='green', label='filtered data')
plt.legend(loc='best')
plt.xlabel('Time (s)')
plt.grid(True)
plt.show()


# In[60]:


plt.title('Magnitude of the Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Magnitude (dB)')
plt.magnitude_spectrum(data_filter, Fs = 2*np.pi, scale='dB')
plt.grid(True)
plt.show()


# #### Playing the filtered signal

# In[57]:


sd.play(data_filter, fs)
time.sleep(5)
sd.stop()


# ### What did you observe on the spectrum plot?

# The frequencies above the cut-off frequency were filtered out while frequencies below the threshold remain, thus it results into a smoother and cleaner magnitude spectrum plot.

# ### What is the message of the filtered signal?

# "If you can hear this clearly, you've filtered the signal correctly" but with less noise.
