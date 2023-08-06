This repertory contains a library of tools useful for Solar-SONG data reduction. 

#Solar-SONG data structure. 

SONG is a spectrographe echelle network originally designed for asteroseismology.
The SONG prototype has been operating at the Observatorio del Teide since 2014.  
The idea was emitted in 2017 to use it also for helioseismology.
A high cadence test run was performed during the summer 2018.

The spectrum acquired with Solar-SONG have been reduced using the 'chunk' methodology
presented in Butler et al. (1996). Spectrums acquired with the iodine cell are divided 
into 24 echelle, themselves divided into 22 thin chunks (about 2 Å). 

For each measurements, matrix of dimension 24x22x27 (each chunk possesses 27 tags with diverse
information) are stored into 'siod' files (saved with the sav IDL file). I provide here two 
IDL routines designed for an efficient processing of siod files into daily velocity matrix saved
as hdf5 files :
- extract_velocity.pro
- extract_velocity_global.pro

The Python library provides functions to read and save (time-velocity) files under 
the hdf5 format.  

Here is a short example :

>>> import apollinaire as apn
>>> filename = '***'
>>> stamps, velocity = apn.songlib.read_hdf5 (filename)

To save a file :

>>> import apollinaire as apn
>>> fileout = '***'
>>> apn.songlib.save_hdf5 (fileout, stamps, velocity)





