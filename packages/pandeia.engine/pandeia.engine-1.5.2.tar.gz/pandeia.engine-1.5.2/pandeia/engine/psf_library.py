# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import division, absolute_import

import os
import copy

import astropy.io.fits as fits
import numpy as np

from .custom_exceptions import DataError


class PSFLibrary:

    """
    Class for encapsulating a hard PSF library, typically one generated
    by WebbPSF or its derivatives.

    Parameters
    ----------
    path : string, optional
        the path to the PSF library root (any .fits files in the
        path root will be assumed to be a valid PSF file in the WebbPSF format.
        If it is none, the PSF library from the package distribution will be used.
    aperture : string, optional
        restrict psfs to a specific mode with the name matching the keyword string.
        Strictly, the reader will look for psf file names with a substring matching the aperture
        string. 'all' reads all psfs in the path. This is the default. The aperture string in the filename
        should match the .fits keyword APERTURE.

    Methods
    -------
    read_library
    get_values
    get_good_psfs
    get_psf

    """

    def __init__(self, path=None, aperture='all'):
        if path is None:
            path = os.path.join(os.path.dirname(__file__), 'refdata', 'psfs')
        self.read_library(path, aperture)

    def read_library(self, path, aperture, wave_unit='m'):
        """
        Read in a library of PSFs stored in FITS files. The filenames contain information about each PSF. The fields are
        separated by _'s with the resulting list entries corresponding to:
            0 - instrument name
            1 - apertures for which PSF is used. this is a - separated string that is split() into a list of apertures
            2 - wavelength at which PSF is calculated
            3, 4 (optional) - x,y rectangular coordinates in FOV at which at which PSF is calculated

        Parameters
        ----------
        path: string
            Path containing the PSF FITS images

        wave_unit: string
            Wavelength unit used by PSF library (default: m)
        """
        files = os.listdir(path)
        files = [x for x in files if x.endswith(".fits") ] # Filter to just .fits files

        psf_files = []
        for file in files:
            filename, ext = os.path.splitext(file)
            filename_split = filename.split('_')
            filename_instrument = filename_split[0]
            filename_apertures = filename_split[1].split('-')
            filename_wave = filename_split[2]
            # If the psf is on-axis, the offset coordinates may not exist

            if aperture is 'all':
                if ext == '.fits':
                    psf_files.append(file)
            elif ext == '.fits' and aperture in filename_apertures:
                    psf_files.append(file)
            # If the aperture has a string with an underscore in it, try to use only the first part.
            elif ext == '.fits' and (aperture.split('_'))[0] in filename_apertures:
                    psf_files.append(file)
            else:
                pass

        self._psfs = []

        for psf_file in psf_files:
            hdulist = fits.open(path + '/' + psf_file, memmap=False)

            psf_int = copy.deepcopy(hdulist[0].data)

            ins = hdulist[0].header['INSTRUME'].lower()
            nwaves = hdulist[0].header['NWAVES']
            if nwaves != 1:
                raise ValueError("Input PSF must be monochromatic (nwaves = #r)" % nwaves)

            wave_scl = self._get_unit_scl(wave_unit)
            wave = hdulist[0].header['WAVE0'] * wave_scl

            pix_scl = hdulist[0].header['PIXELSCL']
            diff_limit = hdulist[0].header['DIFFLMT']
            aperture_name = hdulist[0].header['APERTURE'].lower()
            pup_thru = hdulist[0].header['PUP_THRU']
            # offset_x/offset_y is the offset from the optical center in webbpsf.  However, for NIRCam masklwb
            # and maskswb, this includes the offset from the optical center to the optimal position along the bar.
            # what we need for source association is instead the offset from that optimal position. this is stored in the
            # optoff_x/optoff_y keywords which need to be provided in these cases. aperture_name here will have these
            # aperture and filter names concatenated, so do a string compare to look for aperture.
            try:
                offset_x = hdulist[0].header['OPTOFF_X']
                offset_y = hdulist[0].header['OPTOFF_Y']
            except KeyError:
                offset_x = 0.0
                offset_y = 0.0

            upsamp = hdulist[0].header['DET_SAMP']

            psf = {
                'int': psf_int,
                'wave': wave,
                'pix_scl': pix_scl,
                'diff_limit': diff_limit,
                'upsamp': upsamp,
                'instrument': ins,
                'aperture_name': aperture_name,
                'source_offset': (offset_x, offset_y),
                'pupil_throughput': pup_thru
            }

            self._psfs.append(psf)
            hdulist.close()

    def get_values(self, key, instrument, aperture_name, source_offset=(0, 0)):
        """
        Returns the available values of a given key for a given instrument and aperture name.

        Parameters
        ----------
        key: string
            Desired key. One of 'int', 'wave', 'pix_scl', 'diff_limit', 'upsamp', 'instrument',
            'aperture_name', 'source_offset_x', or 'source_offset_y'

        Returns
        -------
        result: tuple of format (list, list)
            Lists of index id's and values
        """
        # any part of the aperture name after a double underscore should be ignored when dealing with the PSF library
        aperture_name = aperture_name.split("__")[0]
        values = [psf[key] for psf in self._psfs
                  if (instrument == psf['instrument'] and
                      aperture_name in psf['aperture_name']) and
                      source_offset == psf['source_offset']]
        ids = [i for i, psf in enumerate(self._psfs)
               if (instrument == psf['instrument'] and
                   aperture_name in psf['aperture_name']) and
                   source_offset == psf['source_offset']]
        result = ids, values
        return result

    def get_psf(self, wave, instrument, aperture_name, source_offset=(0, 0)):
        """
        Get PSF given wavelength, instrument, instrument aperture, and optionally source xy offset coordinates.
        Values are interpolated linearly between the two PSF library entries that bracket the given wavelength.

        Parameters
        ----------
        wave: float
            Desired wavelength for the PSF
        instrument: str
            Instrument name
        aperture_name: str
            Name of the instrument aperture

        Returns
        -------
        psf: dict
            Dict containing the PSF and associated information
        """
        wids, psf_waves = self.get_values('wave', instrument, aperture_name, source_offset=source_offset)
        nids, nearest_waves = self._find_two_nearest(psf_waves, wave)

        # if wave is not in psf_waves then the two closest will be returned
        if len(nids) == 2:
            ids = [wids[nids[0]], wids[nids[1]]]

            pix_scl0 = self._psfs[ids[0]]['pix_scl']
            pix_scl1 = self._psfs[ids[1]]['pix_scl']
            if pix_scl0 != pix_scl1:
                raise ValueError("Pixel scales in the library must be the same for a single instrument aperture.")

            psf_int0 = self._psfs[ids[0]]['int']
            psf_int1 = self._psfs[ids[1]]['int']
            wave0 = self._psfs[ids[0]]['wave']
            wave1 = self._psfs[ids[1]]['wave']
            diff_limit0 = self._psfs[ids[0]]['diff_limit']
            diff_limit1 = self._psfs[ids[1]]['diff_limit']

            upsamp0 = self._psfs[ids[0]]['upsamp']
            upsamp1 = self._psfs[ids[1]]['upsamp']
            if upsamp0 != upsamp1:
                raise ValueError("Upsampling factors in the library must be the same for a single instrument aperture.")

            psf_int = psf_int0 + (psf_int1 - psf_int0) * (wave - wave0) / (wave1 - wave0)
            diff_limit = diff_limit0 + (diff_limit1 - diff_limit0) * (wave - wave0) / (wave1 - wave0)

        # if wave is one of the values in psf_waves then only it will be returned and
        # no interpolation is necessary
        else:
            ids = nids

            psf_int = self._psfs[ids[0]]['int']
            diff_limit =  self._psfs[ids[0]]['diff_limit']
            pix_scl0 = self._psfs[ids[0]]['pix_scl']
            upsamp0 = self._psfs[ids[0]]['upsamp']

        psf = {
            'int': psf_int,
            'wave': wave,
            'pix_scl': pix_scl0,
            'diff_limit': diff_limit,
            'upsamp': upsamp0,
            'instrument': self._psfs[ids[0]]['instrument'],
            'aperture_name': self._psfs[ids[0]]['aperture_name'],
            'source_offset': self._psfs[ids[0]]['source_offset'],
            'pupil_throughput': self._psfs[ids[0]]['pupil_throughput']
        }
        return psf

    def get_pix_scale(self, instrument, aperture_name):
        """
        Get PSF pixel scale for given instrument/aperture

        Parameters
        ----------
        instrument: str
            Instrument name
        aperture_name: str
            Name of instrument aperture

        Returns
        -------
        pix_scl: float
            Pixel scale of the PSF in arcsec/pixel
        """
        wids, psf_waves = self.get_values('wave', instrument, aperture_name)
        pix_scl = self._psfs[wids[0]]['pix_scl']
        return pix_scl

    def get_shape(self, instrument, aperture_name):
        """
        Get PSF shape for given instrument/aperture

        Parameters
        ----------
        instrument: str
            Instrument name
        aperture_name: str
            Name of instrument aperture

        Returns
        -------
        sh: tuple (int, int)
            Shape of the PSF kernel image
        """
        wids, psf_waves = self.get_values('wave', instrument, aperture_name)
        sh = self._psfs[wids[0]]['int'].shape
        return sh

    def get_upsamp(self, instrument, aperture_name):
        """
        Get PSF upsampling for given instrument/aperture

        Parameters
        ----------
        instrument: str
            Instrument name
        aperture_name: str
            Name of instrument aperture

        Returns
        -------
        upsamp: int
            PSF upsampling factor
        """
        wids, psf_waves = self.get_values('wave', instrument, aperture_name)
        upsamp = self._psfs[wids[0]]['upsamp']
        return upsamp

    def get_offsets(self, instrument, aperture_name):
        """
        Get available PSF offset positions. PSF libraries supporting position-dependent
        PSFs will have multiple. Libraries that do not support position-dependent PSFs will
        only have one position.

        Parameters
        ----------
        list: list-like
            List of values to search
        value: float
            Input value to be bracketed

        Returns
        -------
        psf_positions: list of tuples (source_offset_x, source_offset_y)
            Polar coordinates of PSF offsets.

        """
        aperture_name = aperture_name.split("__")[0]
        offsets = [psf['source_offset'] for psf in self._psfs if instrument ==
                   psf['instrument'] and aperture_name in psf['aperture_name']]
        unique_offsets = list(set(offsets))
        return unique_offsets

    def get_pupil_throughput(self, wave, instrument, aperture_name):
        """
        Get the pupil throughput for a given instrument and aperture. Throughputs are
        calculated for the shortest wavelength in the set, and are given in the headers
        of every fits file.

        Parameters
        ----------
        wave: float
            Wavelength of interest
        instrument: string
            Name of the instrument
        aperture_name: string
            String used to select the PSFs. Nominally, this is the aperture, but in certain cases it's not.

        Returns
        -------
        pupil_thru: float
            Pupil throughput fraction
        """
        # get pupil losses from the PSF pupil_throughput keyword
        psf_offsets = self.get_offsets(instrument, aperture_name)
        unique_positions = np.unique([psf_offset[0] for psf_offset in psf_offsets])
        # if there's only one PSF offset per wavelength, just grab the one associated with the first wavelength (they're
        # all the same)
        if unique_positions.size == 1:
            pupil_thru = self.get_psf(wave,instrument,aperture_name)['pupil_throughput']
        # if there are multiple PSF offsets, find the one for the unocculted PSF.
        else:
            offsets_x = np.asarray(list(zip(*psf_offsets))[0])
            offsets_y = np.asarray(list(zip(*psf_offsets))[1])
            # we need to select the maximum y for the maximum x; for NIRCam MASKLWB the maximum x is at the smallest
            # part of the wedge.
            x_off = np.asarray([k for k in range(len(offsets_x)) if offsets_x[k] == np.max(offsets_x)])
            psf_offset_x = np.max(offsets_x)
            psf_offset_y = np.max(offsets_y[x_off])
            pupil_thru = self.get_psf(wave, instrument, aperture_name, source_offset=(psf_offset_x,psf_offset_y))['pupil_throughput']
        return pupil_thru

    def _calculate_distances(self, psf_offsets, source):
        """
        Compute the distances between a source and the possible PSF offsets.

        Parameters
        ----------
        psf_offsets: np.array
            The possible PSF offsets for this instrument and aperture combination.
        source: list
            The x and y coordinates of the source to be matched.

        Returns
        -------
        distances: np.array
            The distances between the source and the psf_offsets
        """
        distances = [np.sqrt((source[0] - psf_offset[0]) ** 2 + \
                             (source[1] - psf_offset[1]) ** 2) \
                     for psf_offset in psf_offsets]
        return distances

    def associate_offset_to_source(self, sources, instrument, aperture_name):
        """
        Pandeia does not interpolate spatially between PSFs; it merely picks the closest offset to the source.
        This is the function that makes that selection.

        Parameters
        ----------
        sources: list
            A list of Source objects
        instrument: string
            The name of the instrument
        aperture_name:
            String used to select the PSFs. Nominally this is the aperture, but in certain cases, it is changed in the
            _loadpsfs functions in jwst.py and wfirst.py.

        Returns
        -------
        psf_associations: list
            The X and Y coordinates of the associated PSF.
        """

        psf_offsets = self.get_offsets(instrument, aperture_name)

        # Make sure there are offsets given the instrument and aperture
        if len(psf_offsets) == 0:
            raise DataError("No psf offsets found for instrument {} and aperture {}".format(instrument, aperture_name))

        unique_positions = np.unique([psf_offset[0] for psf_offset in psf_offsets])

        psf_associations = []
        for source in sources:
            if unique_positions.size == 1:
                # if there is only one x position, we will assume azimuthal symmetry, and only use the y positions
                source_radius = np.sqrt(source.position['x_offset'] ** 2 + source.position['y_offset'] ** 2)
                distances = [np.abs(psf_offset[1] - source_radius) for psf_offset in psf_offsets]
            else:
                # multiple x positions indicate that we'd expect the full 2D field
                # to be appropriately sampled by the PSF library.
                if 'masklwb' in aperture_name or 'maskswb' in aperture_name:
                    offset_y = np.abs(source.position['y_offset'])
                    offset_x = source.position['x_offset']
                if 'fqpm' in aperture_name:
                    # first, the FQPM masks (and their PSF library) are rotated by 5 degrees cw relative to the
                    #  detector axes. Therefore, we need to rotate 5 degrees ccw to get the real positions relative to
                    #  THAT grid.
                    off_x = source.position['x_offset'] * np.cos(5.0 * np.pi / 180.0) - source.position['y_offset'] * np.sin(5.0 * np.pi / 180.0)
                    off_y = source.position['x_offset'] * np.sin(5.0 * np.pi / 180.0) + source.position['y_offset'] * np.cos(5.0 * np.pi / 180.0)
                    # second, we take the absolute value of both rotated coordinates, AND reflect across the x=y axis
                    if np.abs(off_y) < np.abs(off_x):
                        offset_x = np.abs(off_x)
                        offset_y = np.abs(off_y)
                    else:
                        offset_x = np.abs(off_y)
                        offset_y = np.abs(off_x)

                distances = self._calculate_distances(psf_offsets, [offset_x,offset_y])

            closest_index = np.argmin(distances)
            psf_associations.append(psf_offsets[closest_index])

        return psf_associations

    def _find_two_nearest(self, values, value):
        """
        Find the subscripts of the two neighboring values in list relative to
        an input value.

        Parameters
        ----------
        values: list-like
            List of values to search
        value: float
            Input value to be bracketed

        Returns
        -------
        vals: tuple (list, np.ndarray)
            Bracketing indices in both list and numpy array format
        """
        nplist = np.array(values)

        # ensure that value is not outside the range of list.
        # rounding value of 6 exceeds the highest number of decimal places that actually 
        # exists in the data directories (5, as of 2017-09-25)
        if value < np.round(nplist.min(),6) or value > np.round(nplist.max(),6):
            raise ValueError("Value must be within range of list.")

        # This function is called from get_psf(), which can handle getting only one PSF 
        # back in the case that we don't need interpolation because an actual PSF exists 
        # at that wavelength.
        if np.round(nplist.min(),6) == np.round(value,6):
            vals = [nplist.argmin()],[nplist.min()]
        elif np.round(nplist.max(),6) == np.round(value,6):
            vals = [nplist.argmax()], [nplist.max()]
        # This code will not work if we're requesting exactly the highest wavelength or 
        # lowest wavelength that has actually been generated.
        else:
            diff = nplist - value
            diff_sorted = np.sort(diff)

            smaller = np.max(diff_sorted[diff_sorted<=0])
            larger = np.min(diff_sorted[diff_sorted>=0])

            ids = [i for i, v in enumerate(diff) if diff[i] == smaller or diff[i] == larger]

            vals = ids, nplist[ids]

        return vals

    def _get_unit_scl(self, unit):
        """
        Get unit scale factor for given unit string: m, micron, nm, or Angstrom.
        This should get replaced with real astropy.units support eventually.

        Parameters
        ----------
        unit: str
            Unit string

        Returns
        -------
        scale: float
            Scale factor corresponding to unit string
        """
        scales = {'m': 1.0e6, 'micron': 1.0, 'nm': 1.0e-3, 'Angstrom': 1.0e-4}
        try:
            scale = scales[unit]
            return scale
        except KeyError:
            raise KeyError('Unknown wavelength unit')
