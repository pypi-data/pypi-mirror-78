#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:11:33 2019

@author: Gabriele Coiana
"""
import numpy as np
from scipy import signal
from decomp import  read,  util#,  plot 
import sys

## =============================================================================
## Parameters
input_file = sys.argv[1]
a = read.read_parameters(input_file)[0]
Masses = read.read_parameters(input_file)[1]
n_atom_unit_cell = read.read_parameters(input_file)[2]
n_atom_conventional_cell = read.read_parameters(input_file)[3]
N1,N2,N3 = read.read_parameters(input_file)[4:7]
kinput = read.read_parameters(input_file)[7::][0]
file_eigenvectors = read.read_parameters(input_file)[8]
file_trajectory = read.read_parameters(input_file)[9]
file_initial_conf = read.read_parameters(input_file)[10]
system = read.read_parameters(input_file)[11]
DT = read.read_parameters(input_file)[12]



tot_atoms_uc = int(np.sum(n_atom_unit_cell)) 
tot_atoms_conventional_cell = int(np.sum(n_atom_conventional_cell)) 
N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*tot_atoms_uc    # Number of atoms
cH = 1.066*1e-6 # to [H]
cev = 2.902*1e-05 # to [ev]
kbH = 3.1668085639379003*1e-06# a.u. [H/K]
kbev = 8.617333262*1e-05 # [ev/K]
#### =============================================================================

print('\nHello, lets start!\n')
print('Getting input parameters...')
print(' System: ', system)
print(' Masses: ', Masses)
print(' Number of atoms per unit cell', n_atom_unit_cell)
print(' Supercell: ', N1, N2, N3)
print(' k path: ', [x.tolist() for x in kinput])
print(' Extent of timestep [ps]: ', DT*2.418884254*1e-05)
print()
print('Now calculating velocities...')

Nqpoints, qpoints_scaled, ks, freqs, eigvecs, distances, Hk = read.read_phonopy(file_eigenvectors, tot_atoms_uc)
Scell, Ruc, R0, masses, masses_for_animation = read.read_SPOSCAR_and_masses(file_initial_conf, n_atom_conventional_cell, n_atom_unit_cell, Masses)                       #rhombo or avg R0

Rt = np.loadtxt(file_trajectory)[:,1:]
Num_timesteps = int(len(Rt[:,0]))
print(' Number of timesteps of simulation: ', Num_timesteps)
tall = np.arange(Num_timesteps)*DT*2.418884254*1e-05 #conversion to picoseconds
dt_ps = tall[1]-tall[0]
Vt = np.diff(Rt,axis=0)/dt_ps*np.sqrt(masses)/np.sqrt(3*(N))
T = np.sum(np.average(Vt**2*cev/kbev, axis=0))
print(' Temperature: ',T, ' K')

meta = util.max_freq(dt_ps, Num_timesteps) #you want the max frequency plotted be 25 Thz
ZS, Zqs = np.zeros((meta,1+Nqpoints+1)), np.zeros((meta,tot_atoms_uc*3+1))


Vw, freq = np.fft.fft(Vt, axis=0), np.fft.fftfreq(Num_timesteps-1, dt_ps)
S = np.sum(np.conjugate(Vw)*Vw, axis=1).real*cev/(kbev*T)/Num_timesteps*dt_ps
tot_area = np.trapz(S,freq)
print(' The total DOS is ', tot_area*N)
print(' You are losing ',N - tot_area*N, ' kBT')
ZS[:,0], ZS[:,1] = freq[0:meta], S[0:meta]

Ctot = np.fft.ifft(S)
for t in range(int(len(Ctot)/2)):
    Ctot[t] = Ctot[t]*Num_timesteps/(Num_timesteps-t)
C = Ctot[0:int(len(Ctot)/2)].real



print('\nDone. Performing decomposition...\n')
#anis = list(range(tot_atoms_uc*3))
#namedir = plot.create_folder(system)
#every_tot = int(tot_atoms_conventional_cell/tot_atoms_uc)
Num_steps = util.odd_num_steps(Num_timesteps) #this is very stupid: it is to have a odd number of steps 

for i in range(Nqpoints):
    eigvec = eigvecs[i]
    eigvecH = np.conjugate(eigvec.T)
    freq_disp = freqs[i]
    k = ks[i]
    k_scal = qpoints_scaled[i]
    print('\t kpoint scaled: ', k_scal)
    print('\t kpoint:        ',np.round(k,3))
    
    #Creating the collective variable based on the k point
    Tkt = util.create_Tkt(Num_timesteps-1, tot_atoms_uc, N1N2N3, Vt, R0, k)
    Qkt = np.dot(eigvecH,Tkt.T).T
    
##   this was to convert conventional into primitive
#    Tkt = np.zeros((Num_timesteps-1,tot_atoms_uc*3), dtype=complex)
#    for l,m in zip(range(0,tot_atoms_conventional_cell*3, every_tot*3),range(0,tot_atoms_uc*3,3)):
#        Tkt[:,m:m+3] = Vcoll[:,l:l+3]
    
    Tkw = np.fft.fft(Tkt, axis=0)
    Sq = (np.sum(np.conjugate(Tkw)*Tkw, axis=1)).real*cev/(kbev*T)/Num_timesteps*dt_ps
    area_q = np.trapz(Sq, freq)
    print('\t DOS for this kpoint: ', area_q)
    
    
    Qkw = np.fft.fft(Qkt, axis=0)
    Sq_proj = (np.conjugate(Qkw)*Qkw).real*cev/(kbev*T)/Num_timesteps*dt_ps

    ZS[:,i+2] = Sq[0:meta]
    Zqs[:,0] = Sq[0:meta]
    Zqs[:,1:] = Sq_proj[0:meta,:]
    
    Params = np.zeros((3,tot_atoms_uc*3))
    for n in range(tot_atoms_uc*3):
        x_data, y_data = freq[0:int((Num_steps-1)/2)], Sq_proj[0:int((Num_steps-1)/2),n]
        popt, perr = util.fit_to_lorentzian(x_data, y_data, k, n)
        
        #now you go apply to Voigt equation for the sigmas
        sig, mi = popt[-1]/(2*np.sqrt(2*np.log(2))),  x_data[int(len(x_data)/2)]
        gaussian = 1/(sig*np.sqrt(2*np.pi)) * np.exp(-.5*((x_data-mi)/sig)**2)                
        convolution = signal.fftconvolve(y_data,gaussian, mode='same') / sum( gaussian)
        omega_l, FWHM_l = util.voigt_eq(n, k, freq, convolution, sig)
        
        print()
        print('\t\tFitting to Lorentzian, mode '+str(n)+'...')
        print('\t\tResonant frequency Lorentzian =',np.round(popt[0],2),' +-',np.round(perr[0],3))
        print('\t\tResonant frequency Convolution =',np.round(omega_l,2))
        print('\t\tLinewidth gamma =',np.round(popt[2],2),' +-',np.round(perr[2],3))
        print('\t\tFWHM Convolution =',np.round(FWHM_l,2))
        print()
        Params[:,n] = [omega_l, popt[1], FWHM_l]

#        anis[n] = plot.plot_with_ani(freq[0:meta],Z[0:meta,n],Z_q[0:meta], k, eigvec[:,n],freq_disp[n],n,Ruc,file_eigenvectors,masses_for_animation)
#        plot.save_proj(ff[0:meta*2],Sq_proj[0:meta*2,n],Sq[0:meta*2], qpoints_scaled[i], Ruc, eigvec[:,n],freq_disp[n],n,namedir,masses_for_animation, popt, -1)  
   
    util.save_append('Zqs', k_scal.reshape(1,3), Zqs)
    util.save_append('quasiparticles', k_scal.reshape(1,3), Params)  
    print()


util.save('C_t', np.vstack((tall[0:len(C)],C)).T)
util.save('ZS', ZS)
    
