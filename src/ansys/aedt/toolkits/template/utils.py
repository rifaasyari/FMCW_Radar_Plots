# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:01:31 2020

@author: asligar
"""

# import numpy as np
# from numpy.fft import fft
import glob
# from pyargus import directionEstimation as de
# import time as walltime
# from skimage.feature import peak_local_max
# from copy import deepcopy

def get_results_files(path, wildcard=''):
    """
    wildcard is if we want to seperate different results folder
    different solution setups would be named something like
    DV551_S17_V518_Data.transient
    where the wild card could be "s17_V518" to indicate that specific setup
    """
    results_files = []
    all_paths = glob.glob(path + '\\*' + wildcard + '_Data.transient')
    index_num = []
    for filename in all_paths:
        index_num.append( int(filename.split('\\DV')[1].split('_')[0]))
    
    all_paths_sorted = sorted(zip(index_num, all_paths))
    #all_paths = sorted(all_paths)
    for each in all_paths_sorted:
        results_files.append(each[1]+'\\RxSignal.frtm')
    return results_files

# def range_profile(data, window=False, size=1024):
#     """
#     range profile calculation
#
#     input: 1D array [freq_samples]
#
#     returns: 1D array in original_lenth * upsample
#
#     """
#
#     nfreq = int(np.shape(np.squeeze(data))[0])
#     #scale factors used for windowing function
#     if window:
#         win_range = np.hanning(nfreq)
#         win_range_sum = np.sum(win_range)
#         sf_rng = nfreq/win_range_sum
#         win_range = win_range*sf_rng
#         pulse_f = np.multiply(data, win_range) #apply windowing
#     else:
#         pulse_f = data
#
#
#     sf_upsample = size/nfreq
#
#     #should probaby upsample to closest power of 2 for faster processing, but not going to for now
#     pulse_t_win_up = (sf_upsample*np.fft.ifft(pulse_f, n=size))
#
#
#     return pulse_t_win_up
# def convert_freqpulse_to_rangepulse(data,output_size = 256, pulse=None):
#     '''
#     input: 3D array [channel][freq_samples][pulses], size is desired output in (ndoppler,nrange)
#             output_size is up/down samping in range dimensions
#             pulse=None, this is the pulse to use, if set to none it will extract from center pulse
#     returns: 3D array in [channel][range]
#     '''
#
#
#     rPixels = output_size
#     #input shape
#     rng_dims = np.shape(data)[1]
#     dop_dims = np.shape(data)[2]
#
#     if pulse == None:
#         pulse = int(dop_dims/2)
#     else:
#         pulse = int(pulse)
#
#     freq_ch = np.swapaxes(data, 0, 2)
#     freq_ch = freq_ch[pulse] #only extract this pulse
#     ch_freq = np.swapaxes(freq_ch, 0, 1)
#
#     #window
#     h_rng = np.hanning(rng_dims)
#     sf_rng = len(h_rng)/np.sum(h_rng)
#     sf_upsample_rng = rPixels/rng_dims
#     h_rng = h_rng*sf_rng
#
#     #apply windowing
#     ch_freq_win = sf_upsample_rng* np.multiply(ch_freq, h_rng)
#
#     #take fft
#     ch_rng_win = np.fft.ifft(ch_freq_win, n=rPixels) #[ch][range][dop]fft across dop dimenions
#     ch_rng_win = np.fliplr(ch_rng_win)
#
#     return ch_rng_win
#
# def range_doppler_map(data, window=False, size=(256,256)):
#     """
#     range doppler calculation
#
#     input: 2D array [freq_samples][pulses], size is desired output in (ndoppler,nrange)
#
#     returns: 2D array in [range][doppler]
#
#     """
#
#     time_before = walltime.time()
#     #I think something is wrong with data being returned as opposte, freq and pulse are swaped
#     nfreq = int(np.shape(data)[0])
#     ntime = int(np.shape(data)[1])
#
#     rPixels = size[0]
#     dPixels = size[1]
#
#     h_dop = np.hanning(ntime)
#     sf_dop = len(h_dop)/np.sum(h_dop)
#     sf_upsample_dop = dPixels/ntime
#
#     h_rng = np.hanning(nfreq)
#     sf_rng = len(h_rng)/np.sum(h_rng)
#     sf_upsample_rng = rPixels/nfreq
#
#
#     h_dop = h_dop*sf_rng
#     h_rng = h_rng*sf_dop
#
#
#     fp_win = sf_upsample_dop * np.multiply(data, h_dop)
#     s1 = np.fft.ifft(fp_win, n=dPixels)
#     s1 = np.rot90(s1)
#
#     s1_win = sf_upsample_rng*np.multiply(h_rng, s1)
#     s2 = np.fft.ifft(s1_win, n=rPixels)
#     s2 = np.rot90(s2)
#     s2_shift = np.fft.fftshift(s2, axes=1)
#     #range_doppler = np.flipud(s2_shift)
#     range_doppler = np.flipud(s2_shift)
#     #range_doppler=s2_shift
#     time_after = walltime.time()
#     duration_time = time_after-time_before
#     if duration_time == 0:
#         duration_time = 1
#     duration_fps = 1/duration_time
#
#     rp = 0
#     return range_doppler, rp, duration_fps
#
# def range_angle_map(data,antenna_spacing_wl=0.5, source_data = 'RangeDoppler', DoA_method='fft', fov = [-90,90], out_size=(256,256), range_bin_idx=-1):
#     """
#     range calculationg calculation
#
#     input: 3D array [channel][freq_samples][pulses], in case of FreqPulse mode
#                 or
#            3D array [channel][range][doppler], in case of RangeDoppler mode
#            source_data = 'RangeDoppler' or 'FreqPulse'
#
#            DoA_method, 'fft', Bartlett, Capon, MEM, MUSIC
#
#            out_size, output size in [range][xrange]
#            range_bin=-1 do all range bins, or if specified do only specific range bin index
#
#     returns: 2D array of size [range][xrange]
#
#     """
#     time_before = walltime.time()
#
#
#     rPixels = out_size[0]
#     xrPixels = out_size[1]
#
#     xrng_dims = np.shape(data)[0]
#     nchannel = xrng_dims
#
#     DoA_method = DoA_method.lower()
#
#     if source_data == 'FreqPulse':
#         ch_range = convert_freqpulse_to_rangepulse(data, output_size=rPixels)
#         if DoA_method == "fft":
#             h_xrng = np.hanning(xrng_dims)
#             sf_xrng = len(h_xrng)/np.sum(h_xrng)
#             sf_upsample_xrng = xrPixels/xrng_dims
#
#             h_xrng = np.atleast_2d(h_xrng*sf_xrng)
#
#             rng_ch_win = sf_upsample_xrng* np.multiply(ch_range, h_xrng.T)
#             rng_ch_win = rng_ch_win.T #correct order after multiplication (same as swapaxes)
#             rng_xrng = np.fft.ifft(rng_ch_win, n=xrPixels)
#             rng_xrng = np.fft.fftshift(rng_xrng, axes=1)
#
#         else: #for DoA_method = bartlett, capon mem and music
#             ang_stop = fov[1]+90 #offset fov because beam serach is from 0 to 180
#             ang_start = fov[0]+90
#             range_ch = np.swapaxes(ch_range, 0, 1)
#             array_alignment = np.arange(0, nchannel, 1) * antenna_spacing_wl
#             incident_angles=np.linspace(ang_start, ang_stop, num=xrPixels)
#             ula_scanning_vectors = de.gen_ula_scanning_vectors(array_alignment, incident_angles)
#             sf = len(incident_angles)/xrng_dims
#             if range_bin_idx != -1: #do only specific range bin
#                 rPixels = 1
#                 range_ch = np.atleast_2d(range_ch[range_bin_idx])
#
#             rng_xrng = np.zeros((rPixels,xrPixels), dtype=complex) #(pulse,range)
#             for n, rb in enumerate(range_ch): #if range bin is speficied it will only go once
#                 ## R matrix calculation
#                 rb = np.reshape(rb, (1, nchannel))
#                 #R = de.corr_matrix_estimate(rb, imp="fast")
#                 R = np.outer(rb, rb.conj()) # Correlation matrix(?)
#                 #R = de.forward_backward_avg(R)
#                 if DoA_method == "bartlett":
#                     range_bin = de.DOA_Bartlett(R, ula_scanning_vectors)
#                 elif DoA_method == "capon":
#                     range_bin = de.DOA_Capon(R, ula_scanning_vectors)
#                 elif DoA_method == "mem":
#                     range_bin = de.DOA_MEM(R, ula_scanning_vectors, column_select=0)
#                 elif DoA_method == "music":
#                     range_bin = de.DOA_MUSIC(R, ula_scanning_vectors, signal_dimension=1)
#                 rng_xrng[n] = range_bin*sf
#
#
#     elif source_data == 'RangeDoppler':
#         if DoA_method == 'fft':
#             #fft to get to range vs pulse
#             ch_rng_pulse = np.fft.fft(data)
#             ch_rng_pulse = np.fft.fftshift(ch_rng_pulse, axes=2)
#             ch_rng_pulse = np.fliplr(ch_rng_pulse)
#
#             rng_dims = np.shape(ch_rng_pulse)[1]
#             dop_dims = np.shape(ch_rng_pulse)[2]
#
#             range_ch = np.swapaxes(data, 2, 0)
#             range_ch = np.fliplr(range_ch)
#             range_ch = range_ch[int(dop_dims/2)]
#
#             ch_range = np.swapaxes(range_ch, 0, 1)
#
#             h_xrng = np.hanning(xrng_dims)
#             sf_xrng = len(h_xrng)/np.sum(h_xrng)
#             sf_upsample_xrng = xrPixels/xrng_dims
#
#             h_xrng = np.atleast_2d(h_xrng*sf_xrng)
#
#             rng_ch_win = np.multiply(ch_range, h_xrng.T)
#             rng_ch_win = rng_ch_win.T #correct order after multiplication (same as swapaxes)
#             rng_xrng = np.fft.ifft(rng_ch_win, n=xrPixels)
#
#             rng_xrng  = np.fft.fftshift(rng_xrng, axes=1)
#         else: #for DoA_method = bartlett, capon mem and music
#             rng_dims = np.shape(data)[1]
#             dop_dims = np.shape(data)[2]
#             xrng_dims = np.shape(data)[0]
#
#             ch_rng_pulse = np.fft.fft(data)
#             ch_rng_pulse = np.fft.fftshift(ch_rng_pulse, axes=2)
#             ch_rng_pulse = np.fliplr(ch_rng_pulse)
#
#             range_ch = np.swapaxes(ch_rng_pulse,2,0)
#             range_ch = range_ch[int(dop_dims/2)]
#
#             ang_stop = fov[1]+90 #offset fov because beam serach is from 0 to 180
#             ang_start = fov[0]+90
#             array_alignment = np.arange(0, nchannel, 1) * antenna_spacing_wl
#             incident_angles = np.linspace(ang_start, ang_stop, num=xrPixels)
#             ula_scanning_vectors = de.gen_ula_scanning_vectors(array_alignment, incident_angles)
#
#             sf = len(incident_angles)/xrng_dims
#             if range_bin_idx != -1: #do only specific range bin
#                 rng_dims = 1
#                 range_ch = np.atleast_2d(range_ch[range_bin_idx])
#             rng_xrng = np.zeros((rng_dims, xrPixels), dtype=complex) #(pulse,range)
#             for n, rb in enumerate(range_ch):
#                 ## R matrix calculation
#                 rb = np.reshape(rb, (1, nchannel))
#                 #R = de.corr_matrix_estimate(rb, imp="fast")
#                 R = np.outer(rb, rb.conj())
#                 #R = de.forward_backward_avg(R)
#                 if DoA_method == "bartlett":
#                     range_bin = de.DOA_Bartlett(R, ula_scanning_vectors)
#                 elif DoA_method == "capon":
#                     range_bin = de.DOA_Capon(R, ula_scanning_vectors)
#                 elif DoA_method == "mem":
#                     range_bin = de.DOA_MEM(R, ula_scanning_vectors, column_select=0)
#                 elif DoA_method == "music":
#                     range_bin = de.DOA_MUSIC(R, ula_scanning_vectors, signal_dimension=1)
#                 rng_xrng[n] = range_bin*sf
#
#     rng_xrng = np.flipud(rng_xrng)
#
#     time_after = walltime.time()
#     duration_time = time_after-time_before
#     if duration_time == 0:
#         duration_time = 1
#     duration_fps = 1/duration_time
#
#     return rng_xrng, duration_fps
# def peak_detector2(data,max_detections = 20, threshold_rel=1e-5):
#     '''
#     passing data in as linear, but converting to dB seems to work
#     '''
#     time_before = walltime.time()
#     size = np.shape(data)
#     if len(size) > 2:
#         data = data[0]
#
#     data = np.abs(data)
#     #data = 20*np.log10(np.abs(data))
#     #threshold_rel*max_val of plot is the minimum threshold returned
#
#
#     coordinates = peak_local_max(data, min_distance=2, threshold_rel=threshold_rel, num_peaks=max_detections, exclude_border=False)
#
#     peak_mask = np.zeros_like(data, dtype=bool)
#     peak_mask[tuple(coordinates.T)] = True
#
#     time_after = walltime.time()
#     duration_time = time_after-time_before
#     if duration_time == 0:
#         duration_time = 1
#     duration_fps = 1/duration_time
#
#     #return as 1 or zero to be consistent with CFAR processing below
#     return peak_mask.astype(int), duration_fps
#
# def peak_detector(data, max_detections = 20):
#     '''
#     passing data in as linear, but converting to dB seems to work
#     '''
#     time_before = walltime.time()
#     size = np.shape(data)
#     if len(size) > 2:
#         data = data[0]
#     data = np.abs(data)
#     #data = 20*np.log10(np.abs(data))
#     data[data > 1e-7] = 1
#     data[data < 1e-7] = 0
#
#     time_after = walltime.time()
#     duration_time = time_after-time_before
#     if duration_time == 0:
#         duration_time = 1
#     duration_fps = 1/duration_time
#
#     #return as 1 or zero to be consistent with CFAR processing below
#     return data, duration_fps
#
# ######################################################################
# """
#
#                              Python based Advanced Passive Radar Library (pyAPRiL)
#
#                                           Hit Processor Module
#
#
#      Description:
#      ------------
#          Contains the implementation of the most common hit processing algorithms.
#
#              - CA-CFAR processor: Implements an automatic detection with (Cell Averaging - Constant False Alarm Rate) detection.
#              - Target DOA estimator: Estimates direction of arrival for the target reflection from the range-Doppler
#                                      maps of the surveillance channels using phased array techniques.
#
#      Notes:
#      ------------
#
#      Features:
#      ------------
#
#      Project: pyAPRIL
#      Authors: Tamás Pető
#      License: GNU General Public License v3 (GPLv3)
#
#      Changelog :
#          - Ver 1.0.0    : Initial version (2017 11 02)
#          - Ver 1.0.1    : Faster CFAR implementation(2019 02 15)
#          - Ver 1.1.0    : Target DOA estimation (2019 04 11)
#
#  """
#
# def CA_CFAR(rd_matrix, win_len=50, win_width=50, guard_len=10, guard_width=10, threshold=20):
#     """
#     Description:
#     ------------
#         Cell Averaging - Constant False Alarm Rate algorithm
#
#         Performs an automatic detection on the input range-Doppler matrix with an adaptive thresholding.
#         The threshold level is determined for each cell in the range-Doppler map with the estimation
#         of the power level of its surrounding noise. The average power of the noise is estimated on a
#         rectangular window, that is defined around the CUT (Cell Under Test). In order the mitigate the effect
#         of the target reflection energy spreading some cells are left out from the calculation in the immediate
#         vicinity of the CUT. These cells are the guard cells.
#         The size of the estimation window and guard window can be set with the win_param parameter.
#
#     Implementation notes:
#     ---------------------
#
#     Parameters:
#     -----------
#
#     :param rd_matrix: Range-Doppler map on which the automatic detection should be performed
#     :param win_param: Parameters of the noise power estimation window
#                       [Est. window length, Est. window width, Guard window length, Guard window width]
#     :param threshold: Threshold level above the estimated average noise power
#
#     :type rd_matrix: R x D complex numpy array
#     :type win_param: python list with 4 elements
#     :type threshold: float
#
#     Return values:
#     --------------
#
#     :return hit_matrix: Calculated hit matrix
#
#     """
#
#
#     time_before = walltime.time()
#
#     norc = np.size(rd_matrix, 1)  # number of range cells
#     noDc = np.size(rd_matrix, 0)  # number of Doppler cells
#     hit_matrix = np.zeros((noDc, norc), dtype=float)
#
#     # Convert range-Doppler map values to power
#     rd_matrix = np.abs(rd_matrix) ** 2
#
#     # Generate window mask
#     rd_block = np.zeros((2 * win_width + 1, 2 * win_len + 1), dtype=float)
#     mask = np.ones((2 * win_width + 1, 2 * win_len + 1))
#     mask[win_width - guard_width:win_width + 1 + guard_width, win_len - guard_len:win_len + 1 + guard_len] = np.zeros(
#         (guard_width * 2 + 1, guard_len * 2 + 1))
#
#     cell_counter = np.sum(mask)
#
#     # Convert threshold value
#     threshold = 10 ** (threshold / 10)
#     threshold /= cell_counter
#
#     # -- Perform automatic detection --
#     for j in np.arange(win_width, noDc - win_width, 1):  # Range loop
#         for i in np.arange(win_len, norc - win_len, 1):  # Doppler loop
#             rd_block = rd_matrix[j - win_width:j + win_width + 1, i - win_len:i + win_len + 1]
#             rd_block = np.multiply(rd_block, mask)
#             cell_SINR = rd_matrix[j, i] / np.sum(rd_block) # esimtate CUT SINR
#
#             # Hard decision
#             if cell_SINR > threshold:
#                 hit_matrix[j, i] = 1
#     time_after = walltime.time()
#     duration_time = time_after-time_before
#     duration_fps = 1/duration_time
#     return hit_matrix, duration_fps
# def target_DOA_estimation(data, xrPixels, range_idx, doppler_idx, fov=[-90, 90], antenna_spacing_wl=0.48, DOA_method="Bartlett"):
#     """
#         Performs DOA (Direction of Arrival) estimation for the given hits. To speed up the calculation for multiple
#         hits this function requires the calculated range-Doppler maps from all the surveillance channels.
#
#     Parameters:
#     -----------
#         :param: rd_maps: range-Doppler matrices from which the azimuth vector can be extracted
#         :param: hit_list: Contains the delay and Doppler coordinates of the targets.
#         :param: DOA_method: Name of the required algorithm to use for the estimation
#         :param: array_alignment: One dimensional array, which describes the active antenna positions
#
#         :type : rd_maps: complex valued numpy array with the size of  Μ x D x R , where R is equal to
#                                 the number of range cells, and D denotes the number of Doppler cells.
#         :type: hit_list: Python list [[delay1, Doppler1],[delay2, Doppler2]...].
#         :type: DOA_method: string
#         :type: array_alignment: real valued numpy array with size of 1 x M, where M is the number of
#                             surveillance antenna channels.
#
#     Return values:
#     --------------
#         target_doa : Measured incident angles of the targets
#
#     TODO: Extend with decorrelation support
#     """
#     size = np.shape(data)
#     doa_list = []  # This list will contains the measured DOA values
#     nchannel= int(size[0])
#
#     ang_stop = fov[1]+90 #offset fov because beam serach is from 0 to 180
#     ang_start = fov[0]+90
#
#     array_alignment = np.arange(0, nchannel, 1) * antenna_spacing_wl
#
#     incident_angles = np.linspace(ang_start, ang_stop, num=xrPixels)
#     ula_scanning_vectors = de.gen_ula_scanning_vectors(array_alignment, incident_angles)
#     DOA_method = DOA_method.lower()
#     azimuth_vector = data[:, range_idx, doppler_idx]
#     R = np.outer(azimuth_vector, azimuth_vector.conj())
#     if DOA_method == "bartlett":
#         doa_res = de.DOA_Bartlett(R, ula_scanning_vectors)
#     elif DOA_method == "capon":
#         doa_res = de.DOA_Capon(R, ula_scanning_vectors)
#     elif DOA_method == "mem":
#         doa_res = de.DOA_MEM(R, ula_scanning_vectors, column_select=0)
#     elif DOA_method == "music":
#         doa_res = de.DOA_MUSIC(R, ula_scanning_vectors, signal_dimension=1)
#
#
#     doa_res_abs = np.abs(doa_res)
#     max_location = np.argmax(doa_res_abs)
#     ########################
#     # #this is slowing down post processing and is not currently used
#     # #commenting out for now
#     # max_value = np.max(doa_res_abs)
#     # peaks_indices = find_peaks(doa_res_abs)
#     # peaks_indices = peaks_indices[0]
#     # peaks_values = doa_res_abs[peaks_indices]
#     # #find_peaks does not indentify peaks and start or end of data set. I'll
#     # #check if the max value is not in the peak dataset, if it isn't add it
#     # if max_location not in peaks_indices:
#     #     peaks_indices = np.append(peaks_indices,max_location)
#     #     peaks_values = np.append(peaks_values,max_value)
#     # peaks = list(zip(peaks_indices, peaks_values))
#     # peaks = np.array(peaks)
#
#     # threshold = 0.9 * max_value
#
#     # filtered_peaks_indices = [int(index) for index, value in peaks if value > threshold]
#
#
#
#     #minus 90 because orginal scan was 0 to 180,
#     #coordinate sys for osi would mean these angles are reversed
#     #assumes the Y axis is to the left if the vehicke is looking forward
#     hit_doa = (incident_angles[max_location]-90)
#     #hit_doa_all = -1*(incident_angles[filtered_peaks_indices]-90)
#     hit_doa_all = []
#     return hit_doa, hit_doa_all
#
# def create_target_list(rd_all_channels_az=None, rd_all_channels_el=None, rngDomain=None, velDomain=None, azPixels=256,elPixels=256, antenna_spacing_wl=0.5, radar_fov=[-90,90], centerFreq=76.5e9, rcs_min_detect=0, min_detect_range=7.5, rel_peak_threshold = 1e-3, max_detections=10, return_cfar=False, All_R_Data=None, GTR=12.7):
#
#     if rd_all_channels_el is None:
#         includes_elevation = False
#     else:
#         includes_elevation = True
#
#     time_before_target_list = walltime.time()
#     target_list = {}
#     #this CA_CFAR is too slow, doing to just use local peak detection instead
#     #rd_cfar, cfar_fps = pp.CA_CFAR(rd, win_len=50,win_width=50,guard_len=10,guard_width=10, threshold=20)
#     # Calculate the max at each point of the range for all values and send to the detector.
#     rd_cfar, fps_cfar = peak_detector2(rd_all_channels_az.mean(axis=0), max_detections=max_detections, threshold_rel=rel_peak_threshold)
#     target_index = np.where(rd_cfar == 1) #any where there is a hit, get the index of tha tlocation
#     num_targets = len(target_index[0])
#     if num_targets == 0:
#         print('no targets')
#         target_list = None
#
#     hit_idx = 0 #some hit targest may generate multiple hits (ie, multiple at same range, but different azimuth)
#     for hit in range(num_targets):
#         loc_dict = {}
#         ddim_idx = target_index[1][hit] #index  in doopper dimension
#         rdim_idx = target_index[0][hit] #index  in range dimension
#         doa_az, all_doa_az_bins = target_DOA_estimation(rd_all_channels_az, azPixels, rdim_idx, ddim_idx, antenna_spacing_wl=antenna_spacing_wl, fov=radar_fov, DOA_method="music")
#         print(all_doa_az_bins)
#         if includes_elevation==False:
#             doa_el = 0
#             all_doa_el_bins = [0]
#         elif len(rd_all_channels_el) < 2: #needs to have at least 2 channel to get elevation
#             doa_el = 0
#             all_doa_el_bins = [0]
#         else:
#             doa_el, all_doa_el_bins = target_DOA_estimation(rd_all_channels_el, elPixels, rdim_idx,ddim_idx, antenna_spacing_wl=antenna_spacing_wl, fov=[radar_fov[0],0], DOA_method="bartlett")   #Bartlett
#
#         R_dist = rngDomain[rdim_idx] #get range at index where peak/hit was detected
#         loc_dict['range'] = R_dist
#         #ignore hits that are closer than this distance and futher than 90%of max range
#         # for doa_az_peak in all_doa_az_bins:
#         #     for doa_el_peak in all_doa_el_bins:
#         if ((loc_dict['range']>min_detect_range) and (loc_dict['range']<np.max(rngDomain)*.9)):
#             loc_dict['azimuth'] = doa_az #in degrees
#             loc_dict['elevation'] = doa_el
#             loc_dict['cross_range_dist'] = rngDomain[rdim_idx]*np.sin(doa_az*np.pi/180)
#             loc_dict['xpos'] = R_dist*np.cos(doa_az*np.pi/180) #this is distnace as defined in +x in front of sensor
#             loc_dict['ypos'] = R_dist*np.sin(doa_az*np.pi/180) #+y and -y is cross range dimenionson,
#             loc_dict['zpos'] = R_dist*np.sin(doa_el*np.pi/180)
#             loc_dict['velocity'] = velDomain[ddim_idx]
#             #Pr= np.abs(rd_all_channels_az[0][rdim_idx][ddim_idx])
#             # Power recieved in all channesl
#             Pr = np.max(np.abs(rd_all_channels_az[:,rdim_idx,ddim_idx]))
#             #Pr = np.max(np.abs(rd_all_channels_az[:,rdim_idx,ddim_idx]))
#             Pr_dB = 20*np.log10(Pr)
#             print(Pr_dB)
#             loc_dict['p_received'] = Pr
#             # TODO get transmit power from API
#             Pt = 1 #1Watt, input power, 0dBw is source power
#             Pt_dB = 10*np.log10(Pt)
#
#             #user radar range equation to scale results by range to get relative rcs
#             #is there a better way to do this? This will not work for objects in near field
#             #gain used in dB, should probably use the actual antenna pattern gain, but this will be used for testing
#             # This is from actual antenna gain
#             #print(int(doa_az))
#             Gt = GTR[int(doa_az)+90]
#             Gr = GTR[int(doa_az)+90]
#             #print("#==============R_dist,doa,Gt,Gr,Pr_dB,Pt_dB")
#             #print(R_dist,int(doa_az),Gt,Gr,Pr_dB,Pt_dB)
#
#             #radar range equation in dB
#             rcs_scaled_dB = Pr_dB+30*np.log10(4*np.pi)+40*np.log10(R_dist)-(Pt_dB+Gt+Gr+20*np.log10(3e8/(centerFreq)))
#             #print("#$#$#$#$#$#$#$#$")
#             #print(np.size(Pr_dB))
#             if rcs_scaled_dB> rcs_min_detect: #only add if peak rcs is above min value specified
#                 loc_dict['rcs'] = rcs_scaled_dB
#                 loc_dict['G_Ant'] = Gt
#                 target_list[hit_idx] = deepcopy(loc_dict)
#                 hit_idx += 1
#                         #target_list['original_time_index'] = time
#     #if target recorded, add it to the list
#
#     time_after_target_list = walltime.time()
#     time_target_list = time_after_target_list-time_before_target_list
#     if time_target_list == 0:
#         time_target_list = 1
#     fps_target_list = 1/time_target_list
#
#     if return_cfar:
#         return target_list, fps_target_list, rd_cfar
#     else:
#         return target_list, fps_target_list
