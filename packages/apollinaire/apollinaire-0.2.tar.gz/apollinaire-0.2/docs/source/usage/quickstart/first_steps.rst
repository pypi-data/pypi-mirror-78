Quickstart
**********

Let’s assume that you want to use *apollinaire* to fit p-mode parameters
for a given star. First we need to import the package :

.. code:: python

    import apollinaire as apn

The name of the stars we are going to work with is KIC6603624, also
known as Saxo. The package include a version of the lightcurves
calibrated following the KEPSEISMIC method (see García et al. 2014).

.. code:: python

    from astropy.io import fits
    from os import path
    import numpy as np
    import matplotlib.pyplot as plt
    
    modDir = path.abspath ('..')
    filename = path.join (modDir, 'timeseries/kplr006603624_52_COR_filt_inp.fits')
    hdu = fits.open (filename) [0]
    data = np.array (hdu.data)
    t = data[:,0]
    v = data[:,1]
    
    fig, ax = plt.subplots ()
    ax.plot (t-t[0], v, color='black')
    
    ax.set_xlabel ('Time (days)')
    ax.set_ylabel ('Luminosity variation (ppm)')


.. image:: output_3_1.png


Let’s compute the psd of this lightcurve with the dedicated function:

.. code:: python

    dt = np.median (t[1:] - t[:-1]) * 86400
    freq, psd = apn.psd.series_to_psd (v, dt=dt, correct_dc=True)
    freq = freq*1e6
    psd = psd*1e-6
    
    fig, ax = plt.subplots ()
    ax.plot (freq, psd, color='black')
    ax.set_xlabel (r'Frequency ($\mu$Hz)')
    ax.set_ylabel (r'PSD (ppm$^2$ / $\mu$Hz)')
    ax.set_yscale ('log')
    ax.set_xscale ('log')



.. image:: output_5_0.png


Here are the p-modes we want to fit :

.. code:: python

    fig, ax = plt.subplots ()
    cond = (freq>1500.)&(freq<3000.)
    ax.plot (freq[cond], psd[cond], color='black')
    ax.set_xlabel (r'Frequency ($\mu$Hz)')
    ax.set_ylabel (r'PSD (ppm$^2$ / $\mu$Hz)')


.. image:: output_7_1.png


We can also take a look at the echelle diagram of the modes. For this
purpose, we have to compute :math:`\Delta\nu`, the large separation,
through the scaling law, knowing mass and radius of the star. Mass and
radius values are taken from the DR25 *Kepler* catalog (see Mathur et
al. 2017).

.. code:: python

    r = 1.162
    m = 1.027
    dnu_sun = 135.
    dnu = dnu_sun * np.power (m, 0.5) * np.power (r, -1.5)
    apn.psd.echelle_diagram (freq[cond]*1e-6, psd[cond], dnu)


.. image:: output_9_0.png


The main peakbagging tool provided by *apollinaire* is the
``stellar_framework`` function. It will successively fit the background
of the star, the global pattern of the p-modes, and finally the
individual parameters of the modes. Radius, mass and effective
temperature are needed as input.

.. code:: python

    
    teff = 5671
    apn.peakbagging.stellar_framework (freq, psd, r, m, teff, n_harvey=2, low_cut=50., filename_back='background',
                           filemcmc_back=None, nsteps_mcmc_back=1000, n_order=5, filename_pattern='pattern',
                           filemcmc_pattern=None, nsteps_mcmc_pattern=1000, parallelise=True,
                           progress=True, a2z_file='modes_param.a2z', nsteps_mcmc_peakbagging=1000, filename_peakbagging='summary_peakbagging.pdf')

