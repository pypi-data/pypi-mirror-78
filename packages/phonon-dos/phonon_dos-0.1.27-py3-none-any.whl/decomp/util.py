#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:33:25 2019

@author: gc4217
"""
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import numpy as np
import os

def repeat_masses(Masses, n_atom_conventional_cell, n_atom_primitive_cell, N1, N2, N3):
    repeated_masses = np.array([])
    repeated_masses_for_ani = np.array([])
    for i in range(len(Masses)):
        mass = Masses[i]

        n = n_atom_conventional_cell[i]
        nprim = n_atom_primitive_cell[i]
        
        m = np.repeat(mass, N1*N2*N3*3*n)
        m_ani = np.repeat(mass,nprim*3)
        
        repeated_masses = np.concatenate((repeated_masses,m))
        repeated_masses_for_ani = np.concatenate((repeated_masses_for_ani,m_ani))
        
    masses = np.array(repeated_masses).flatten()
    masses_for_animation = np.array(repeated_masses_for_ani).flatten()
    
    return masses, masses_for_animation

def corr(tall,X,Y,tau,mode):
    M = len(tall)
    dt = tall[1] - tall[0]
    tmax = M - tau
    N = np.size(X[0]) 
    X0 = X[0:tmax,:]
    X2 = 1/tmax*np.sum(X[0:tmax,:]*X[0:tmax,:])
    C = []
    for n in range(tau):
        print(n)
        Xjj = Y[n:n+tmax,:]
        a = np.multiply(np.conjugate(X0),Xjj)
        b = 1/(tmax) * np.sum(a,axis=0)#/X2
        if (mode=='projected'):
            c = b
        else:
            c = np.sum(b)
        C.append(c)
    C = np.array(C)
    t = np.arange(0,tau)*dt
    freq = np.fft.fftfreq(tau,d=dt)
    Z = np.fft.fft(C,axis=0)
    return t, C, freq, Z

def lorentzian(x, x0, A, gamma):
    y = 1/np.pi *  A * 1/2*gamma / ((x - x0)**2 + (1/2*gamma)**2)
    return y

def save(filename, data):
    filename2 = filename
    if os.path.isfile(filename):
        n_of_files = len([name for name in os.listdir('.') if (os.path.isfile(name) and name==filename)])
        filename2 = filename+'_'+str(n_of_files)
        print(filename, ' already present. Saving it as ', filename2)
    np.savetxt(filename2,data) 
    return

def save_append(filename, data1, data2):
    filename2 = filename
#    if os.path.isfile(filename):
#        n_of_files = len([name for name in os.listdir('.') if (os.path.isfile(name) and name==filename)])
#        filename2 = filename+'_'+str(n_of_files)
#        print(filename, ' already present. Saving it as ', filename2)
        
    file = open(filename2,'ab')
    np.savetxt(file,data1)
    np.savetxt(file,data2)
    file.close()
    return

def max_freq(dt_ps, tau):
    #you want the max frequency plotted be 25 Thz
    max_freq = 0.5*1/dt_ps
    if (max_freq < 25):
        meta = int(tau/2)
    else:
        meta = int(tau/2*25/max_freq)
    return meta

def fit_to_lorentzian(x_data, y_data, k, n):
    try:
        if(n in [0,1,2] and np.allclose(k, [0,0,0])): #if acoustic modes at Gamma, don't fit anything
                popt, pcov = np.array([0.0001, 0, 0.0001]), np.zeros((3,3))
        else:
            popt, pcov = curve_fit(lorentzian, x_data, y_data)
    except RuntimeError:
        print('\t\tWasnt able to fit to Lorentzian mode '+str(n)+'\n\n')
        x0 = x_data[np.argwhere(y_data==y_data.max())]
        y0 = y_data.max()
        popt, pcov = np.array([x0,y0,0.0001]), np.zeros((3,3))
    perr = np.sqrt(np.diag(pcov))
    return popt, perr

def odd_num_steps(Num_timesteps):
    if((Num_timesteps-1)%2 == 0): 
        Num_steps = Num_timesteps -1
    return Num_steps

def create_Tkt(Num_timesteps, tot_atoms_uc, N1N2N3, Vt, R0, k):
    N = tot_atoms_uc*N1N2N3
    Vcoll = np.zeros((Num_timesteps,tot_atoms_uc*3),dtype=complex)  
    for j,h,l in zip(range(tot_atoms_uc*3),np.repeat(range(0,N),3)*N1N2N3*3,np.tile(range(0,3),tot_atoms_uc)):
        vels = np.array(Vt[:,h+l:h+N1N2N3*3:3],dtype=complex)
        poss = R0[h:h+N1N2N3*3:3,:]
        x = np.multiply(vels,np.exp(-1j*np.dot(poss,k)))
        Vcoll[:,j] = np.sum(x,axis=1)
    Tkt = Vcoll  
    return Tkt


def pair_distr(file_initial_conf, Rt, Nsteps, dr):
    N = len(Rt[0,0::3])
    ang_to_bohr = 1.8897259886
    SCell = np.genfromtxt(file_initial_conf, skip_header=2, max_rows=3)*ang_to_bohr
    A1, A2, A3 = SCell[0,:], SCell[1,:], SCell[2,:]
    V = np.dot(A1, np.cross(A2, A3))
    L = V**(1/3)
#    dr = .01 #[B] 
    r = np.arange(0,L/2,dr)
    Nbins = len(r)-1
    
    HIST = np.zeros(Nbins)
    for t in range(Nsteps):
        print(t)
        hist = np.zeros(Nbins)
        Rx, Ry, Rz = Rt[t,0::3], Rt[t,1::3], Rt[t,2::3]
#        vtx, vty, vtz = Vt[t,0::3],  Vt[t,1::3], Vt[t,2::3]
    #    R0x, R0y, R0z = R0[::3,0], R0[::3,1], R0[::3,2]
    
        Rmatx, Rmaty, Rmatz = np.tile(Rx,(N,1)).T, np.tile(Ry,(N,1)).T, np.tile(Rz,(N,1)).T
        Rijx, Rijy, Rijz = Rmatx - Rx, Rmaty - Ry, Rmatz - Rz
    
    
        for i in range(N):
    #        vi = np.sqrt(vtx[i]**2+vty[i]**2+vtz[i]**2)
            for j in range(N):
    #            vj = np.sqrt(vtx[j]**2+vty[j]**2+vtz[j]**2) 
                if(i==j):
                    continue
                rijx, rijy, rijz = Rijx[i,j], Rijy[i,j], Rijz[i,j]
                rij = np.sqrt(rijx**2+rijy**2+rijz**2)
                BIN = int(rij/dr) 
                if (BIN < Nbins):
                    hist[BIN] = hist[BIN] + 3 #3*vi*vj 
        HIST = HIST + hist
                        
    const = 4/3 * np.pi* N/V  
    g = np.zeros(Nbins)
    for b in range(Nbins):
        rlower = b*dr
        rupper = (b+1)*dr
        nid = const*(rupper**3-rlower**3)
        g[b] = HIST[b]/N/Nsteps/nid
        
    return r[0:-1], g





def get_real_branches(freqs, eigvecs, masses, Hk, qpoints_scaled):
    num_ks = len(freqs[0,:])
    num_branches = len(freqs[:,0])    
    
    freqs_until_now = freqs[:,0]
    indexes = np.tile(np.arange(num_branches), (2,1))
    new_indexes = np.arange(num_branches)
    for k in range(1,num_ks-1):
        kpoint = np.dot(Hk, qpoints_scaled[k])
        kpoint = kpoint/np.linalg.norm(kpoint)
        next_kpoint = np.dot(Hk, qpoints_scaled[k+1])
        if(np.allclose(next_kpoint,[0,0,0])):
            next_kpoint = [0,0,0]
        else:
            next_kpoint = next_kpoint/np.linalg.norm(next_kpoint)
#        print(k,qpoints_scaled[k], np.round(next_kpoint,2))

        this_eigvecs = eigvecs[k].T/np.sqrt(masses)*10
        next_eigvecs = eigvecs[k+1].T/np.sqrt(masses)*10
        next_eigvecs = next_eigvecs/np.linalg.norm(next_eigvecs, axis=0)

#        print(np.round(next_eigvecs[0::],2))

        temp = new_indexes#np.arange(num_branches)
        for j,l in zip(range(num_branches), new_indexes):
            eig = this_eigvecs[l,:]
            eig = eig/np.linalg.norm(eig)
#            print(l,np.round(eig,2), freqs[l,k])
            dot_prod = np.abs(np.dot(next_eigvecs,eig))
#            print(np.round(dot_prod,2))


            new_index = np.argwhere([dot_prod.max()-0.0000000000001 <= dd <= dot_prod.max() for dd in dot_prod])
            degenerate = len(new_index)
#            print(new_index)
            if (len(new_index) > 1):
#                print('two are degenerate')
#                next_eigvecs_deg = next_eigvecs[new_index,:]
#                dot_nexteigvecs_nextk = np.dot(next_eigvecs_deg.reshape(degenerate*2,3), next_kpoint)
#                dot_nexteigvecs_nextk = np.abs(dot_nexteigvecs_nextk.reshape(degenerate,2))
#                dot_nexteigvecs_nextk = dot_nexteigvecs_nextk/np.linalg.norm(dot_nexteigvecs_nextk)
#                dot_thiseig_nextk = np.abs(np.dot(eig.reshape(1*2,3), next_kpoint))
#                dot_thiseig_nextk = dot_thiseig_nextk/np.linalg.norm(dot_thiseig_nextk)
#                diff = np.abs(dot_thiseig_nextk - dot_nexteigvecs_nextk)
#                diff_sum = np.sum(diff, axis=1)
#                print(np.round(dot_nexteigvecs_nextk,2))
#                print(np.round(dot_thiseig_nextk,2))
#                print('diffsum', np.round(diff_sum,2))
                a=0
                if(a==10):#(np.isclose(dot_nexteigvecs_nextk, 1,  rtol=0.2, atol=0.2).any()):
                    #you have a longitudinal branch
                    print('theres a longitudinal')
#                    isclose = np.isclose(dot_nexteigvecs_nextk, dot_thiseig_nextk, rtol=0.2, atol=.2)
#                    true_long = np.all(isclose, axis=1)
#                    arg_long = np.argwhere(true_long)
#                    new_index = new_index[arg_long]
#                    print(new_index)
#                    
                else:
#                    c = np.argwhere(diff_sum==diff_sum.min())
                    new_index = l#new_index[c]
                    print(new_index)

                
                
            if (new_index in temp[0:j]): #it happens at Gamma where TA modes are degenerate
#                print('aaaa')
                new_index = l

            temp[j] = new_index
#            print()
        new_indexes = temp.astype(int)
#        print(new_indexes)
#        print()



        indexes = np.vstack((indexes,new_indexes))
        
    indexes = indexes.astype(int)
#    print(indexes)
    freqs_sorted = []
    for j in range(num_ks):
        freqs_sorted.append(freqs[indexes[j],j])   
        
    return indexes, np.array(freqs_sorted).T


#fig,ax = plt.subplots()
#    
#masses = np.array([24.305 ,  24.305  , 24.305 ,  15.9994 , 15.9994  ,15.9994])
#xd = np.copy(freqs_disp.T)
#s=get_real_branches(xd, eigvecs_phonopy, masses, Hk,  qpoints_scaled)
#print(np.shape(freqs_disp))
#
#kk = np.arange(len(freqs_disp[:,2]))
#for i in range(6):
#    ax.scatter(kk,freqs_disp[:,i], c='black')
##
##ax.plot(np.arange(len(s[0,:])),s[0,:].flatten())
##ax.plot(np.arange(len(s[0,:])),s[1,:].flatten())
##ax.plot(np.arange(len(s[0,:])),s[2,:].flatten())
#
#ax.plot(np.arange(len(s[0,:])),s[3,:].flatten())
#ax.plot(np.arange(len(s[0,:])),s[4,:].flatten())
#ax.plot(np.arange(len(s[0,:])),s[5,:].flatten())
    
def freqs_spectrum(freq,ZQS):
    num_modes = len(ZQS[0,:,0])
    num_ks = len(ZQS[0,0,:])
#    fig,ax = plt.subplots()
    freqs_from_spectrum = np.zeros((num_modes, num_ks))
    for i in range(num_ks):
        for j in range(num_modes):
            phonon = ZQS[:,j,i]
            if (-.001<phonon.max()<.001):
                continue
#            ax.plot(freq, phonon)
            freq_max = freq[np.argwhere(phonon==phonon.max())]
            
            freqs_from_spectrum[j,i] = freq_max
#    ax.plot(np.arange(2540), ZQS[:,0,1])
#    ax.plot(np.arange(2540), ZQS[:,0,2])
#    ax.plot(np.arange(2540), ZQS[:,0,3])
    return freqs_from_spectrum.T

def find_Gammas(ks_path):
    ks_path = np.array(ks_path)
    num_ks = len(ks_path)
    kk = np.linspace(0,1,num_ks)
    indexes_Gammas = np.argwhere(np.all(np.isclose(ks_path,[0,0,0]), axis=1)).flatten()
    if(indexes_Gammas[-1]==len(kk)):
        indexes_Gammas_withboundaries = indexes_Gammas
    else:
        indexes_Gammas_withboundaries = indexes_Gammas
        indexes_Gammas_withboundaries = np.concatenate((indexes_Gammas_withboundaries,[len(kk)-1]))
    num_Gammas = len(indexes_Gammas)
    return num_Gammas, indexes_Gammas, indexes_Gammas_withboundaries

def gaussian(x,A, B, c):
#    y = 1/(sig*np.sqrt(2*np.pi)) * np.exp(-.5*((x-mi)/sig)**2)
    y = A * np.exp(-B*(x-c)**2) 
    return y

def get_Force_Constants(eigvecs, freqs_spectrum, ks, R0):
    num_ks = len(freqs_spectrum[0,:])
    num_modes = len(freqs_spectrum[:,0])
    tot_atoms_uc = int(num_modes/3)
    N = len(R0[:,0])
    N1N2N3 = int(N/tot_atoms_uc)
    Dyna_matrixes = np.zeros((num_modes,num_modes, num_ks))
    K = np.zeros((num_modes,N*3))
    summa = 0
    print(np.shape(ks))
    for k in range(1):
        this_k = ks[k,:]
        this_eig = eigvecs[k]
        lamda = np.diag(freqs_spectrum[:,k])
        D = np.dot(np.dot(this_eig,lamda),this_eig.T)
        Dyna_matrixes[:,:,k] = D
    
    for a in range(tot_atoms_uc):
        R_origin = R0[a*N1N2N3,:]
        for b in range(tot_atoms_uc):
            somma = np.zeros((3,3))
            for k in range(num_ks):
                j = k + N1N2N3*a
                R_next = R0[j,:]
                diffR = R_next - R_origin
                kdotr = np.dot(this_k, diffR)
                D = Dyna_matrixes[:,:,k]
                Da = D[a*3:a*3+3, b*3:b*3+3]
                
                somma = somma + Da*np.exp(1j*kdotr)
  
        
    return

def all_kpoints(N1,N2,N3, Hk):
    N1N2N3 = N1*N2*N3
    #Compute all possible k points
    x1 = np.arange(0,N1)/N1
    x2 = np.arange(0,N2)/N2
    x3 = np.arange(0,N3)/N3
    comb = np.array(np.meshgrid(x1,x2,x3)).T.reshape(-1,3)
    allkpoints_scaled = comb.T
    allkpoints = np.dot(Hk,allkpoints_scaled)
    return allkpoints_scaled.T, allkpoints.T

def R_matrix(N1,N2,N3,tot_atoms_uc,R0):
    """
    returns the R matrix
    """
    N1N2N3 = N1 * N2 * N3
    N = len(R0[:,0])
    
    R_matrix = np.zeros((tot_atoms_uc*3,N*3))
    count = 0
    for i in range(tot_atoms_uc):
        atom_origin = R0[i*N1N2N3]
        row = (R0[:,:]-atom_origin).flatten()
        repeated_row = np.tile(row,(3,1))
        R_matrix[count:count+3,:] = repeated_row
        count =  count + 3
        
    return R_matrix#*0.529177249

def D(k, K,N1,N2,N3,R0,masses,tot_atoms_uc):
    """
    builds the dynamical matrix
    """
    N1N2N3 = N1 * N2 * N3
    N = N1N2N3*tot_atoms_uc
    
    R = R_matrix(N1,N2,N3,tot_atoms_uc, R0)
    #prepare kdotr
    kdotr = np.zeros((tot_atoms_uc*3,N*3))
    for i in range(tot_atoms_uc*3):
        for j in range(0,N*3,3):
            kdotr[i,j] = np.dot(k,R[i,j:j+3])
            kdotr[i,j+1] = np.dot(k,R[i,j:j+3])
            kdotr[i,j+2] = np.dot(k,R[i,j:j+3])
    
    D = np.zeros((tot_atoms_uc*3,tot_atoms_uc*3),dtype=complex)
    for i in range(tot_atoms_uc*3):
        for j,h in zip(range(tot_atoms_uc*3),np.repeat(range(0,N),3)):
            mass_coeff = complex(1/(masses[i]*masses[j])**(0.5))
            exp = 0*1j
            #h = 0
            for l in range(j+h*3*(N1N2N3-1),j+h*3*(N1N2N3-1)+(N1N2N3)*3,3):
                #print(np.exp(1j*kdotr[i,l]),K[i,l])
                exp = exp + K[i,l]*np.exp(1j*kdotr[i,l])
            #print()
            D[i,j] = mass_coeff*exp
    return D*0.964*10**(4)#, kdotr, R



def voigt_eq(n, k, freq, convolution, sig):
    if(n in [0,1,2] and np.allclose(k, [0,0,0])): #if acoustic modes at Gamma, don't fit anything
        popt, pcov = np.array([0, 0, 0]), np.zeros((3,3))
        return popt[0], popt[-1]
                
    f_max = int(np.argwhere(convolution==convolution.max()))
    conv_sx, conv_dx = convolution[0:f_max], convolution[f_max::]
    sx, dx = np.argwhere(conv_sx < convolution.max()/2)[-1], np.argwhere(conv_dx < convolution.max()/2)[0] + f_max
    fv = (freq[dx] - freq[sx])[0]
    fg = 2*sig*np.sqrt(2*np.log(2))
    a, b, c = 0.0692, -1.0692*fv, -fg**2+fv**2
    fl = (-b/2-np.sqrt((b/2)**2-a*c))/a 
#   www = (-fv**2+fg**2)/(-fv)
    return freq[f_max], fl






def all_freqs(N1,N2,N3, Hk, Num_timesteps, tot_atoms_uc, Vt):
    N1N2N3 = N1*N2*N3
    meta = int(len(freq)/2)
    freq_meta = freq[0:meta]
    #Compute all possible k points
    x1 = np.arange(0,N1+1)/N1
    x2 = np.arange(0,N2+1)/N2
    x3 = np.arange(0,N3+1)/N3
    comb = np.array(np.meshgrid(x1,x2,x3)).T.reshape(-1,3)
    #a1 = np.multiply(comb,b1)
    #a2 = np.multiply(comb,b2)
    #a3 = np.multiply(comb,b3)
    #kpoints = a1+a2+a3
    allkpoints_scaled = comb.T
    allkpoints = np.dot(Hk,allkpoints_scaled)
    
    import matplotlib.pyplot as plt
    from scipy import signal
    for k in range(1,2):
        fig,ax = plt.subplots()
        #Creating the collective variable based on the k point
        kpoint = allkpoints[:,k]
        Tkt = create_Tkt(Num_timesteps-1, tot_atoms_uc, N1N2N3, Vt, R0, kpoint)
        Tkw = np.fft.fft(Tkt, axis=0)
        Sq = (np.sum(np.conjugate(Tkw)*Tkw, axis=1)).real*cev/(kbev*T)/Num_timesteps*dt_ps
        sig, mi = .1/2, freq[int(meta/2)]
        gaussian = 1/(sig*np.sqrt(2*np.pi)) * np.exp(-.5*((freq_meta-mi)/sig)**2)
        convolution = signal.fftconvolve(Sq[0:meta],gaussian, mode='same') / sum( gaussian)
        print(convolution)
        ax.plot(freq_meta,Sq[0:meta], freq_meta, convolution)
        area_q = np.trapz(Sq, freq[0:meta])
        print('\t DOS for this kpoint: ', area_q)
    return allkpoints_scaled

#SSS= all_freqs(10,10,10, Hk, Num_timesteps, tot_atoms_uc, Vt)
#R = R0[0::3,:]
#get_Force_Constants(eigvecs_phonopy, freqs_from_spectrum.T, ks, R)


def interpol_spectrum(ks_path, freq, freqs_from_spectrum, eigvecs, modes, ZQS, new_ks_in_between):
    num_ks = len(ks_path)
    num_modes = len(freqs_from_spectrum[0,:])
    num_freqs = len(ZQS[:,0,0])
    kk = np.linspace(0,1,num_ks)
    num_Gammas, indexes_Gammas, indexes_Gammas_withboundaries = find_Gammas(ks_path)
    df = freq[1] - freq[0]
    X, Y = np.meshgrid(kk,freq)
    
#    get_Force_Constants(eigvecs, freqs_from_spectrum.T)
    interp_freq = []
    INTERP = []
    for j in range(len(modes)):
        interp_freq_interm = np.array([])
        for m in range(len(indexes_Gammas)):
            this_G = indexes_Gammas_withboundaries[m]
            next_G = indexes_Gammas_withboundaries[m+1]+1
            kk_i = kk[this_G:next_G]
            f_i = freqs_from_spectrum[this_G:next_G,j]
            interp = interp1d(kk_i, f_i, 'cubic')
#            x_i = np.arange(kk_i[0], kk_i[-1], 0.001)
            INTERP.append(interp)
#            interp_freq_interm = np.concatenate((interp_freq_interm, interp(x_i)))
#        interp_freq_interm = np.array(interp_freq_interm)
#        interp_freq.append(interp_freq_interm)
#    interp_freq = np.array(interp_freq)

    ZQS_interp = np.zeros((num_freqs,num_modes, new_ks_in_between*(num_ks-1)+num_ks))
    
    
    ktot = 0
    for k in range(num_ks-1):
        sector = 0
        for l in indexes_Gammas_withboundaries[1::]:
            if(k >= l):
                sector = sector + 1
        count_k_in_between = 0
        for j in range(num_modes):  
            this_gaussian = ZQS[:,j,k]
            next_gaussian = ZQS[:,j,k+1]
            
#            import matplotlib.pyplot as plt
#            fig,ax = plt.subplots()
#            #to comment
#            popt_this, pcov_this = curve_fit(gaussian, freq, this_gaussian)
#            popt_next, pcov_next = curve_fit(gaussian, freq, next_gaussian)
            
            this_max = freqs_from_spectrum[k,j]
            next_max = freqs_from_spectrum[k+1,j]
            diff_maxima = next_max - this_max
            
            if(diff_maxima >= 0):
                this_gaussian_interp = interp1d(freq, this_gaussian, bounds_error=False, fill_value=0)
                next_gaussian_interp = interp1d(freq, next_gaussian, bounds_error=False, fill_value=0)
                this_gaussian_fit = this_gaussian_interp(freq-diff_maxima)
                next_gaussian_fit = next_gaussian_interp(freq)
                shift_interp = -next_max
            else:
                this_gaussian_interp = interp1d(freq, this_gaussian, bounds_error=False, fill_value=0)
                next_gaussian_interp = interp1d(freq, next_gaussian, bounds_error=False, fill_value=0)
                this_gaussian_fit = this_gaussian_interp(freq)
                next_gaussian_fit = next_gaussian_interp(freq+diff_maxima)
                shift_interp = -this_max
            
#            area_this_gaussian = np.trapz(this_gaussian_fit, freq)
#            area_next_gaussian = np.trapz(next_gaussian_fit, freq)

            this_k = kk[k]
            next_k = kk[k+1]
            interm_k = np.linspace(this_k, next_k, new_ks_in_between+2)[0:-1]

            interp = INTERP[sector+j*num_Gammas]
            intermediate_maxima = interp(interm_k)
            
            count_k_in_between = 0
            for m in range(new_ks_in_between+1):
                mi = intermediate_maxima[m]
                x = (interm_k[m] - interm_k[0])/(next_k-interm_k[0])
#                area_factor = area_this_gaussian+(area_next_gaussian-area_this_gaussian)*x
                interp_gaussian = this_gaussian_fit+(next_gaussian_fit-this_gaussian_fit)*x
                interp_gaussian_interp = interp1d(freq, interp_gaussian,bounds_error=False, fill_value=0)
                interp_gaussian_fit = interp_gaussian_interp(freq-(shift_interp+mi))
                ZQS_interp[:,j,ktot+count_k_in_between] = interp_gaussian_fit
                count_k_in_between = count_k_in_between + 1
                

#                popt = popt_this + (popt_next-popt_this)*x
#                interp_gaussian_fit = gaussian(freq, *popt)#1/(sig*np.sqrt(2*np.pi)) * np.exp(-.5*((freq-mi)/sig)**2) *area_factor

#                ax.plot(freq, interp_gaussian_fit, label='interp')
#            ax.plot(freq, this_gaussian, label='real this')
#            ax.plot(freq,next_gaussian, label='real next')
##            ax.plot(freq, this_gaussian_fit, label='real this fit')
##            ax.plot(freq,next_gaussian_fit, label='real next fit')
#            ax.legend()
            
        ktot = ktot + count_k_in_between
    ZQS_interp[:,:,-1] = ZQS[:,:,-1]
    return ZQS_interp



def get_nac_wrong(kpoint,Vuc, BORN, eps_inf, masses):
    const = 1.18*1e+07
    num = np.outer(np.dot(kpoint,BORN.T) , np.dot(BORN,kpoint))
    den = np.dot(kpoint.T,np.dot(eps_inf,kpoint))
    Cna_k = 4*np.pi/Vuc * num/den #* const
    
#                    thisq_eigvec = eigvecs_phonopy[j]
#                    M = masses_for_animation[0]*masses_for_animation[3]/(masses_for_animation[0]+masses_for_animation[3])
#                    omega_l = np.sqrt(freqs_from_disp[0][5]**2 + 4*np.pi*BORN[0,0]/(M*eps_inf[0,0]*Vuc))   
#                    nac_q = np.zeros((tot_atoms_uc, tot_atoms_uc, 3, 3), dtype='double', order='C')
#                    born = BORN.reshape((2,3,3))
#                    A = np.dot(kpoint, born)
#                    CC = np.zeros((6,6))
#                    for i in range(tot_atoms_uc):
#                        for j in range(tot_atoms_uc):
#                            nac_q[i, j] = np.outer(A[i], A[j])
#                            CC[i*3:(i+1)*3, j*3:(j+1)*3] = 4*np.pi/Vuc *nac_q[i,j] /den
##                            print(i,j, 4*np.pi/Vuc *nac_q[i,j])
#                    AB = CC
#                    eigvna, eigvecna = np.linalg.eigh(AB)
#                    print(np.sqrt(eigvna))              
#                    lamdas = np.diag(freqs_from_disp[0]**2)
#                    Dq = np.dot(thisq_eigvec, np.dot(lamdas, np.linalg.inv(thisq_eigvec)))
    M1, M2 = np.meshgrid(np.sqrt(masses), np.sqrt(masses))
    Mij = np.multiply(M1,M2)
    D = 1/Mij*Cna_k*const/1000 #+Dq
    eigvals, eigvecs = np.linalg.eigh(D)
    omegas_nac = np.sqrt(eigvals)
    return omegas_nac, D



#interpol_spectrum(ks_path, freq, freqs_from_spectrum, eigvecs_phonopy, modes, ZQS_proj_reshaped, 1)


#def get_real_branches(freqs):
#    num_ks = len(freqs[0,:])
#    num_branches = len(freqs[:,0])
#    indexes0 = np.arange(num_branches)
#    freqs_until_now = freqs[:,0:2]
#    
#    
#    for k in range(1,8):
#        deriv = np.diff(freqs[:,k-1:k+2], axis=1)
#        next_freqs = freqs[:,k+1]
#        this_deriv = deriv[:,1]
#        prev_deriv = deriv[:,0]
#        actual_diff = this_deriv-prev_deriv
#        print(this_deriv[2])
#        print(prev_deriv[2])
#        
#        sopra, sotto = np.ones(num_branches)*100, np.ones(num_branches)*100
#        two_sopra, two_sotto = np.ones(num_branches)*100, np.ones(num_branches)*100
#        
#        for j in range(num_branches-1):
#            down_freq = freqs[j-1,k+1]
#            up_freq = freqs[j+1,k+1]
#            diff_down = down_freq - freqs[j,k] 
#            diff_up = up_freq - freqs[j,k] 
#            sopra[j] = diff_up
#            sotto[j+1] = diff_down
#            
#        for j,l in zip(range(num_branches-2),range(2,num_branches)):
#            two_down_freq = freqs[l-2,k+1]
#            two_up_freq = freqs[j+2,k+1]
#            two_diff_down = two_down_freq - freqs[j,k] 
#            two_diff_up = two_up_freq - freqs[j,k] 
#            two_sopra[j] = two_diff_up
#            two_sotto[j+1] = two_diff_down
#
#        sopra, sotto = np.array(sopra), np.array(sotto)
#        diff_deriv_up = sopra - prev_deriv
#        diff_deriv_down = sotto - prev_deriv
#        gain_up = np.abs(diff_deriv_up)-np.abs(actual_diff)
#        gain_down = np.abs(diff_deriv_down)-np.abs(actual_diff)
#        
#        two_sopra, two_sotto = np.array(two_sopra), np.array(two_sotto)
#        two_diff_deriv_up = two_sopra - prev_deriv
#        two_diff_deriv_down = two_sotto - prev_deriv
#        two_gain_up = np.abs(two_diff_deriv_up)-np.abs(actual_diff)
#        two_gain_down = np.abs(two_diff_deriv_down)-np.abs(actual_diff)
#        
#        print(k)
#        print(np.shape(next_freqs))
#        print(np.round(np.hstack((freqs_until_now[:,-2::],next_freqs.reshape(6,1))),4))
#        print(np.round(next_freqs,4))
##        print()
##        print(np.round(diff_deriv_down,2))
#        print('gaindown',np.round(gain_down,2))
#        print('gainup',np.round(gain_up,2))
#        print('actualdiff', np.round(actual_diff,2))
#        print()
#        for j in range(num_branches-1):
#
#            if(gain_down[j+1] <0 and gain_up[j] <0):
#                print('aaa',j)
#                temp = next_freqs[j]
#                next_freqs[j] = next_freqs[j+1]
#                next_freqs[j+1] = temp
#               
##            elif(two_gain_up[j]<0 and two_gain_down[j+2]<0 and np.abs(next_freqs[j]-next_freqs[j+1])<0.05):
##                print('aaa2',j)
##                temp = next_freqs[j]
##                next_freqs[j] = next_freqs[j+2]
##                next_freqs[j+2] = temp
#        print(next_freqs)
#        freqs_sorted = np.hstack((freqs_until_now,next_freqs.reshape(num_branches,1)))
#        freqs_until_now = freqs_sorted
#        
#        print()
#    return freqs_sorted








