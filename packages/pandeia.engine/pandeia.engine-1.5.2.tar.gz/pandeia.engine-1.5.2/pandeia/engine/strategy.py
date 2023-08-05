# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import division, absolute_import

import os
import numpy as np
import scipy as sc

from . import coords
from . import io_utils as io
from . import config as cf

from .custom_exceptions import EngineInputError, UnsupportedError
from .config import DefaultConfig
from .utils import recursive_subclasses, merge_data
from .pandeia_warnings import strategy_warning_messages as warning_messages
from six.moves import range
from six.moves import zip

default_refdata_directory = cf.default_refdata_directory


class Strategy(DefaultConfig):

    """
    Parent class for all strategies.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    webapp: bool
        Toggle strict API checking
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters

    Attributes
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Observing mode (given the instrument).

    Methods
    -------
    set_values(section,**kwargs)
        Set parameter values for the strategy
    get_defaults()
        Get the default parameters for the instantiated strategy.
    extract(my_detector_signal,my_detector_noise)
        Applies the strategy to calculate an ETC product, given a detector signal and noise plane.
    reconstruct_cube(my_detector_signal, my_detector_noise)
        Constructs a reduced datacube from the detector plane. A classical application is to transform an IFU
        observation to an X,Y,WAVELENGTH cube.
    get_plane_grid(my_detector_signal)
        Returns an instance of the Grid() class containing the spatial grid information of the observation.
    get_cube_shape(my_detector_signal)
        Returns the shape tuple of the X,Y,WAVELENGTH cube.
    """

    def __init__(self, instrument=None, webapp=False, config={}, **kwargs):
        """
        How a strategy is instantiated depends on the instrument and mode it is used with.

        Parameters
        ----------
        instrument: Instrument subclass instance
            Instrument that was the basis of the calculation
        webapp: bool
            Determines whether strict API checks should be performed
        config: dict
            Extra configuration information in engine input API dict format
        **kwargs: keyword/value pairs
            Extra configuration information in kwargs format
        """
        if instrument is not None:
            self.instrument = instrument
            self.mode = self.instrument.mode
            self.disperser_key = instrument.instrument['disperser']

        if not hasattr(self, "api_parameters"):
            # API parameters common to all strategies
            self.api_parameters = ["method", "units", "target_xy", "aperture_size"]

        # parameters to configure photutils.geometry routines
        self.use_exact = 1

        # self.subsampling is only used for rectangular regions (i.e. SpecApPhot) currently and
        # only as a stop-gap until use_exact is supported for those cases. the value of 20 was determined
        # by running the same calculation with sub-pixel offsets of the source and aperture. the higher the value, the
        # better the convergence between the extracted SNR/flux values for each case. a value of 20 yields good convergence
        # without significantly impacting performance.
        self.subsampling = 20

        if hasattr(self, "api_ignore"):
            self.api_ignore.extend(["target_source", "target_type", "display_string", "calc_type"])
        else:
            self.api_ignore = ["target_source", "target_type", "display_string", "calc_type"]

        DefaultConfig.__init__(self, webapp=webapp, config=config, **kwargs)

        # do some sanity checks to make sure inputs make sense
        try:
            self._sanity_checks()
        except AttributeError as e:
            self.warnings['no_sanity_check'] = warning_messages['no_sanity_check'] % (self.__class__.__name__, e)

    def _get_config(self):
        """
        For strategies we need to merge instrument-specific defaults from the instrument configuration
        with the strategy-specific defaults from a defaults file.

        Returns
        -------
        config: dict
            Merged instrument and strategy-specific defaults
        """
        objname = self.__class__.__name__.lower()

        # pop the instrument-specific defaults out of self.instrument
        if self.mode is not None:
            inst_config = self.instrument.strategy_config[self.mode]
        else:
            inst_config = self.instrument.strategy_config

        # check to make sure this strategy is appropriate for instrument/mode
        if objname not in inst_config['permitted_methods']:
            msg = "%s is not permitted or implemented for instrument %s and mode %s." % (objname.capitalize(),
                                                                                         self.instrument,
                                                                                         self.mode)
            raise EngineInputError(value=msg)

        if 'aperture_key' in list(inst_config.keys()):
            if isinstance(inst_config['aperture_key'], dict):
                keys = inst_config.pop('aperture_key')
                key = keys[objname]
            else:
                key = inst_config.pop('aperture_key')

            if key:
                sizes = inst_config.pop('aperture_sizes')
                inst_config['aperture_size'] = sizes[self.instrument.instrument[key]]
                if "sky_annulus_sizes" in inst_config:
                    sky_sizes = inst_config.pop('sky_annulus_sizes')
                    inst_config['sky_annulus'] = sky_sizes[self.instrument.instrument[key]]

                if "contrast_azimuths" in inst_config:
                    options = inst_config.pop('contrast_azimuths')
                    inst_config['contrast_azimuth'] = options[self.instrument.instrument[key]]

                if "contrast_separations" in inst_config:
                    options = inst_config.pop('contrast_separations')
                    inst_config['contrast_separation'] = options[self.instrument.instrument[key]]

                if "unocculted_xys" in inst_config:
                    options = inst_config.pop('unocculted_xys')
                    inst_config['unocculted_xy'] = options[self.instrument.instrument[key]]

                if "ta_offset" in inst_config:
                    options = inst_config.pop('ta_offset')
                    inst_config['ta_offset'] = options[self.instrument.instrument[key]]

        # now get the strategy-specific config
        config_file = "%s.json" % objname
        config_path = os.path.join(default_refdata_directory, "strategy", config_file)

        strat_config = io.read_json(config_path, raise_except=True)

        # per-instrument defaults take precendence over per-strategy defaults
        config = merge_data(strat_config, inst_config)
        return config

    def _create_covariance_matrix(self, my_detector_signal, my_detector_noise, subscripts=None):
        """
        The covariance matrix. It no longer uses scipy sparse matrix functionality because it was found
        to be highly inefficient for the sizes of matrices encountered. Future strategies can overload
        this if they do require that functionality. Correlated noise can be passed as a correlation matrix
        that can be rearranged into off-diagonals.

        Parameters
        ----------
        my_detector_signal : DetectorSignal class
        my_detector_noise : DetectorNoise class
        subscripts : list of subscript tuples
                     Oftentimes, only a small number of pixels are considered for a single product
                     calculation. In this case, the caller can pass a list of subscripts so that the
                     eventual matrix product does not have to sum over a large amount of 0s.

        Returns
        -------
        c_ij : numpy.ndarray
               The pixel-to-pixel correlation matrix.
        """

        if subscripts is None:
            subscripts = np.indices(my_detector_noise.var_pix.shape)

        diagonal = my_detector_noise.var_pix[subscripts].ravel()
        diagonal_rn = my_detector_noise.var_rn_pix[subscripts].ravel()

        nn = diagonal.shape[0]

        if my_detector_signal.det_pars['rn_correlation']:
            c_ij = np.zeros((nn, nn))
            # handle correlated readnoise by arranging the correlation matrix into the
            # off-diagonals of the covariance matrix

            # Half of the correlation matrix size
            ncorr = int((my_detector_signal.read_noise_correlation_matrix.shape[0] - 1) / 2)

            for i in range(nn):
                correlation_subscripts = (subscripts[0] - subscripts[0][i] + ncorr,
                                          subscripts[1] - subscripts[1][i] + ncorr)
                # Correlated read noise is only ...emm... correlated with the read noise
                c_ij[i, :] = my_detector_signal.read_noise_correlation_matrix[correlation_subscripts] * diagonal_rn[i]

                # Then replace diagonal with the total variance
                c_ij[i, i] = diagonal[i]

        else:
            # no correlated read noise
            c_ij = np.diagflat(diagonal)

        return c_ij

    def extract(self, my_detector_signal_list, my_detector_noise_list):
        """
        It is the same for all strategies, so simply gets inherited.
        The strategy can return a list of products defined by a set of weight matrices.

        Parameters
        ----------
        my_detector_signal_list : List of DetectorSignal instances
        my_detector_noise_list : List of DetectorNoise instances

        Returns
        -------
        products : Dictionary of strategy products.
                    detector_signal - 2D image of pixel count rates on detector plane
                    detector_noise - 2D image of pixel count rate standard deviations on detector plane
                    wavelength - either a wavelength vector for spectroscopic modes or the effective wavelength
                                 for imaging modes.
                    extracted_flux - The flux extracted by the strategy from the input detector pixel plane(s). This is always
                                     background-subtracted either via a background extracted from another aperture or an
                                     ideal noiseless sky background.
                    extracted_noise - The noise extracted by the strategy from the input detector pixel plane(s).
                    extracted_flux_plus_bg - The flux extracted by the strategy from the input detector pixel plane(s) with
                                             sky background included in signal.  If background subtraction is done via an
                                             aperture, this will be the same as 'extracted_flux'.  If an ideal background is
                                             assumed, then this will include the flux from the sky background as well.
                    source_flux_in_fov - The total sum of all source flux within the scene field of view (no background).
                    source_flux_in_fov_plus_bg - The total sum of all flux within the scene, including the background.
                    reconstructed - Reconstructed detector plane product (relevant for dithered or IFU calculations)
        """

        # We calculate the weights for all the dithers first, because each dither may have different weights, depending
        # on the strategy. These differences between dithers are not known to the general extract method, but only to the
        # specific _createWeightMatrix methods, which are redefined for each strategy.
        a_ij_list, product_subscripts_list = self._create_weight_matrix(my_detector_signal_list, my_detector_noise_list)

        # ARR - FOR DEBUGGING ONLY
        self.weight_matrix = a_ij_list
        # Check whether there are multiple dithers or only one. If there is only one, there is no need to add
        # products from multiple exposures.
        if isinstance(a_ij_list, list):
            # It's a list of dithers.
            exposure_products_list = []
            warnings = {}
            for i in range(len(my_detector_signal_list)):
                exposure_products = self._error_sum(
                    a_ij_list[i],
                    product_subscripts_list[i],
                    my_detector_signal_list[i],
                    my_detector_noise_list[i]
                )
                exposure_products_list.append(exposure_products)

                # if we're not on-target, remove the warnings pertaining to scene size...
                if not self.on_target[i]:
                    if "scene_fov_too_small" in my_detector_signal_list[i].warnings:
                        my_detector_signal_list[i].warnings.pop("scene_fov_too_small")
                    if "max_scene_size_reached" in my_detector_signal_list[i].warnings:
                        my_detector_signal_list[i].warnings.pop("max_scene_size_reached")

                warnings.update(my_detector_signal_list[i].warnings)
                warnings.update(my_detector_noise_list[i].warnings)

            products = self._add_exposure_products(exposure_products_list)
            products['warnings'] = warnings
            products['warnings'].update(self.warnings)
            products = [products]
            self._filter_results(products, exposure_products_list)
        else:
            # There is only one.
            a_ij = a_ij_list
            product_subscripts = product_subscripts_list
            products = self._error_sum(a_ij, product_subscripts, my_detector_signal_list[0], my_detector_noise_list[0])
            products['warnings'] = my_detector_signal_list[0].warnings
            products['warnings'].update(my_detector_noise_list[0].warnings)
            products['warnings'].update(self.warnings)
            products = [products]

        return products

    def _error_sum(self, a_ij, product_subscripts, my_detector_signal, my_detector_noise):
        """
        This private method calculates the total flux from the weight matrix, a_ij*F_ij, and the noise from
        var = sum(a_ij C_ij a_ij^-1). See the self.extract docstring for public details.

        Parameters
        ----------
        a_ij : numpy matrix
        product_subscripts : list of subscript tuples
        my_detector_signal : DetectorSignal instance
        my_detector_noise : DetectorNoise instance

        Returns
        -------
        exposure_products : A single product dictionary
        """

        flux_products = []
        flux_plus_bg_products = []
        sigma_products = []
        bg_only_products = []
        bg_plus_contamination_products = []
        full_saturation_products = []
        partial_saturation_products = []

        # get the saturation mask
        saturation_mask = my_detector_signal.get_saturation_mask()

        # the covariance matrix is the same row-wise at every step, but scaled by the variance along
        # the diagonal. utilize this to initialize the matrix once and then simply scale it from there.
        init_var = my_detector_noise.var_pix[product_subscripts[0]].ravel()
        c_ij_init = self._create_covariance_matrix(
            my_detector_signal,
            my_detector_noise,
            subscripts=product_subscripts[0]
        )
        # create normalized covariance matrix
        c_ij_norm = c_ij_init / init_var.reshape(len(init_var), 1)
        for product_subscript in product_subscripts:
            a_ij_raveled = a_ij[product_subscript]

            # make weight map of only the background region for measuring background+contamination.
            # if self.background_subtraction is False, this will be all zeroes. But we need to make sure they're
            # floating point zeroes, not uint8.
            a_ij_bg_raveled = np.asarray(a_ij[product_subscript], dtype=np.float)
            a_ij_bg_raveled[a_ij_bg_raveled > 0] = 0
            a_ij_bg_raveled *= -1.0

            # scale the covariance matrix by the current variance
            diagonal = my_detector_noise.var_pix[product_subscript].ravel()

            # reshape diagonal to do row-wise scaling
            c_ij = c_ij_norm * diagonal.reshape(len(diagonal), 1)

            # this is equivalent to the matrix operation A_ij * C_ij * A_ij.T
            var_product = np.dot(np.dot(a_ij_raveled, c_ij), a_ij_raveled.transpose())

            # extract flux with and without sky background included
            flux_product = a_ij_raveled.dot(my_detector_signal.rate[product_subscript].transpose())
            flux_plus_bg_product = a_ij_raveled.dot(my_detector_signal.rate_plus_bg[product_subscript].transpose())

            # calculate the sky background rate for measuring contamination
            bg_rate = my_detector_signal.rate_plus_bg[product_subscript] - my_detector_signal.rate[product_subscript]

            # if self.background_subtraction is True, we need to use the background-only weight map otherwise
            # we'll subtract background from itself. if self.background_subtraction is False, then we use the normal
            # weight map to get the sky background flux within the extraction aperture. in that case, sky subtraction
            # is treated as ideal and noiseless.
            if self.background_subtraction:
                bg_only = a_ij_bg_raveled.dot(bg_rate.transpose())
                bg_plus_contamination = a_ij_bg_raveled.dot(
                    my_detector_signal.rate_plus_bg[product_subscript].transpose()
                )
            else:
                bg_only = a_ij_raveled.dot(bg_rate.transpose())
                bg_plus_contamination = bg_only

            # count how many pixels have full and partial saturation
            nsaturated_full = np.sum(saturation_mask[product_subscript] == 2)
            nsaturated_partial = np.sum(saturation_mask[product_subscript] == 1)

            sigma_products.append(np.sqrt(var_product.item()))
            flux_products.append(flux_product.item())
            flux_plus_bg_products.append(flux_plus_bg_product.item())
            bg_only_products.append(bg_only.item())
            bg_plus_contamination_products.append(bg_plus_contamination.item())
            full_saturation_products.append(nsaturated_full)
            partial_saturation_products.append(nsaturated_partial)

        # Image mode:
        if len(product_subscripts) == 1:
            flux_tots = np.array([my_detector_signal.rate.sum()])
            flux_plus_bg_tots = np.array([my_detector_signal.rate_plus_bg.sum()])
        else:
            if self.instrument.dispersion_axis() == 'x':
                flux_tots = my_detector_signal.rate.sum(axis=0)
                flux_plus_bg_tots = my_detector_signal.rate_plus_bg.sum(axis=0)
            else:
                # for dispersion axis along +Y need to sum along X axis and then reverse order since
                # we want spectrum to go blue to red
                flux_tots = my_detector_signal.rate.sum(axis=1)
                flux_plus_bg_tots = my_detector_signal.rate_plus_bg.sum(axis=1)

        # if projection_type is multiorder, then we need to use the configured order for the strategy to get the
        # right wavelength solution. Or if it's one of the slitless calculations that has background orders...
        if (self.disperser_key is None or not
                ('orders' in my_detector_signal.current_instrument.disperser_config[self.disperser_key] or
                'norders' in my_detector_signal.current_instrument.disperser_config[self.disperser_key])):
            wave_pix = my_detector_signal.wave_pix
        else:
            wave_pix = my_detector_signal.wave_pix_dict[self.order]

        exposure_products = {
            'detector_signal': my_detector_signal.rate_plus_bg,
            'detector_noise': my_detector_noise.stdev_pix,
            'detector_saturation': my_detector_signal.get_saturation_mask(),
            'detector_ngroups': my_detector_signal.ngroup_map,
            'wavelength': wave_pix,
            'extracted_flux_plus_bg': np.array(flux_plus_bg_products),
            'extracted_flux': np.array(flux_products),
            'extracted_bg_total': np.array(bg_plus_contamination_products),
            'extracted_bg_only': np.array(bg_only_products),
            'source_flux_in_fov': flux_tots,
            'source_flux_in_fov_plus_bg': flux_plus_bg_tots,
            'extracted_noise': np.array(sigma_products),
            'reconstructed': self.reconstruct_cube(my_detector_signal, my_detector_noise),
            'plane_grid': self.get_plane_grid(my_detector_signal),
            'extraction_area': self.extraction_area,
            'background_area': self.background_area,
            'weight_matrix': self.weight_matrix,  # ARR - FOR DEBUGGING ONLY
            'saturation_products': {
                'full':np.array(full_saturation_products),
                'partial':np.array(partial_saturation_products),
                'fraction_saturation': my_detector_signal.fraction_saturation
            }
        }
        return exposure_products

    def _add_exposure_products(self, exposure_products_list):
        """
        This private method adds products from multiple exposures/dithers in a sensible manner. The key
        assumption is that different exposures are *uncorrelated*, so errors are simply added in quadrature.
        Exposures are added according to self.dither_weights so that a negative weight yields subtraction (e.g.
        of background). A weight can be 0 in some special cases (e.g. coronagraphy) where the exposure has a special
        purpose, but its flux not included in the overall calculation.

        Parameters
        ----------
        exposure_products_list : A list of product dictionaries
                                 From multiple compatible exposures.

        Returns
        -------
        exposure_sum : A single product dictionary
                       Contains a sensible sum of signals (weighted by a_ij) and noise (added in quadrature).
        """

        ref_products = exposure_products_list[0]
        product_shape = ref_products['wavelength'].shape
        cube_shape = ref_products['reconstructed'][0].shape

        exposure_sum = {
            'wavelength': ref_products['wavelength'],
            'extracted_flux': np.zeros(product_shape),
            'extracted_flux_plus_bg': np.zeros(product_shape),
            'source_flux_in_fov': np.zeros(product_shape),
            'source_flux_in_fov_plus_bg': np.zeros(product_shape),
            'extracted_noise': np.zeros(product_shape),
            'extracted_bg_total': np.zeros(product_shape),
            'extracted_bg_only': np.zeros(product_shape),
            'extraction_area': ref_products['extraction_area'],
            'background_area': ref_products['background_area'],
            'saturation_products': {'full':np.zeros(product_shape),'partial':np.zeros(product_shape),'fraction_saturation': 0.0}

        }

        reconstructed_signal = np.zeros(cube_shape)
        reconstructed_noise = np.zeros(cube_shape)
        reconstructed_saturation = np.zeros(cube_shape)
        reconstructed_groups = np.zeros(cube_shape)

        exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups = self._add_exposures(
            exposure_products_list,
            exposure_sum,
            reconstructed_signal,
            reconstructed_noise,
            reconstructed_saturation,
            reconstructed_groups
        )

        exposure_sum['extracted_noise'] = np.sqrt(exposure_sum['extracted_noise'])
        reconstructed_noise = np.sqrt(reconstructed_noise)
        exposure_sum['reconstructed'] = (
            reconstructed_signal,
            reconstructed_noise,
            reconstructed_saturation,
            reconstructed_groups,
            ref_products['reconstructed'][4]
        )
        exposure_sum['detector_signal'] = self.on_detector(reconstructed_signal)
        exposure_sum['detector_noise'] = self.on_detector(reconstructed_noise)
        exposure_sum['detector_saturation'] = self.on_detector(reconstructed_saturation)
        exposure_sum['detector_ngroups'] = self.on_detector(reconstructed_groups)
        exposure_sum['plane_grid'] = ref_products['reconstructed'][4]
        # The number of dithers on-source is the sum of dithers with self.on_target is True
        exposure_sum['n_on_source'] = np.array(self.on_target).sum()
        # The total number of real dithers are those with non-zero dither weights. In some cases, the dither weight
        # is set to 0 because it is a "fictional" dither. A key example of a fictional dither is used for
        # coronagraphic contrasts (the ratio between an extracted source flux and that of an unocculted source).
        exposure_sum['n_total'] = np.count_nonzero(self.dither_weights)

        return exposure_sum

    def _add_exposures(self, exposure_list, exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups):
        """
        Perform actual building of exposure_sum reconstructed products.  IFUNodInScene in particular needs to overload
        this to deal with the way it handles each exposure.

        Parameters
        ----------
        exposure_list: list
            A list of exposure product dictionaries
        exposure_sum: dict
            Dict of exposure products to be updated and populated
        reconstructed_signal: 3D numpy.ndarray
            Initial reconstructed signal cube
        reconstructed_noise: 3D numpy.ndarray
            Initial reconstructed noise cube
        reconstructed_saturation: 3D numpy.ndarray
            Initial reconstructed saturation cube

        Returns
        -------
        exposure_sum: dict
            Contains a sensible sum of signals (weighted by dithers) and noise (added in quadrature).
        reconstructed_signal: 3D numpy.ndarray
            Combined reconstructed signal cube
        reconstructed_noise: 3D numpy.ndarray
            Combined reconstructed noise cube
        reconstructed_saturation: 3D numpy.ndarray
            Combined reconstructed saturation cube
        """
        reconstructed_saturation = exposure_list[0]['reconstructed'][2]
        reconstructed_groups = exposure_list[0]['reconstructed'][3]

        for i, exposure in enumerate(exposure_list):
            exposure_sum['extracted_flux'] += self.dither_weights[i] * exposure['extracted_flux']
            exposure_sum['extracted_flux_plus_bg'] += self.dither_weights[i] * exposure['extracted_flux_plus_bg']
            exposure_sum['source_flux_in_fov'] += self.dither_weights[i] * exposure['source_flux_in_fov']
            exposure_sum['source_flux_in_fov_plus_bg'] += self.dither_weights[i] * exposure['source_flux_in_fov_plus_bg']
            exposure_sum['extracted_noise'] += (self.dither_weights[i] * exposure['extracted_noise']) ** 2
            exposure_sum['saturation_products']['full'] += exposure['saturation_products']['full']
            exposure_sum['saturation_products']['partial'] += exposure['saturation_products']['partial']
            exposure_sum['saturation_products']['fraction_saturation'] = np.max([exposure_sum['saturation_products']['fraction_saturation'],
                                                                               exposure['saturation_products']['fraction_saturation']])

            # need to avoid cases with dither weight set to 0 because spurious saturation can creep in otherwise
            if np.abs(self.dither_weights[i]) > 0:
                reconstructed_signal += self.dither_weights[i] * exposure['reconstructed'][0]
                reconstructed_noise += (self.dither_weights[i] * exposure['reconstructed'][1]) ** 2
                reconstructed_saturation = np.maximum(reconstructed_saturation,exposure['reconstructed'][2])
                reconstructed_groups = np.minimum(reconstructed_groups,exposure['reconstructed'][3])

            # cases where the dither weight is less than 0 means we're subtracting background.
            # make the weight positive and add the extracted background quantities
            if self.dither_weights[i] < 0:
                w = -1.0 * self.dither_weights[i]
                exposure_sum['extracted_bg_total'] += w * exposure['extracted_bg_total']
                exposure_sum['extracted_bg_only'] += w * exposure['extracted_bg_only']


        return exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups

    def _filter_results(self, product, listobj):
        """
        Function to control which products are added to the output, for control over multi-pointing mode outputs.

        Parameters
        ----------
        product: list
            extracted products produced by the strategy
        listobj: list
            list of extracted products from individual pointings

        Returns
        -------
        product: list
            list of extracted products with the additional listobj products appended to the end
        """
        product.extend(listobj)
        return product

    def _fill_array(self, n, value):
        """
        Helper function that produces a one-dimensional array filled with a certain value.

        Parameters
        ----------
        n : integer
            Size of the array.
        value : float-like
            Every element in the array will be set to this value.

        Returns
        -------
        array : One-dimensional numpy.array
        """

        array = np.empty(n, dtype=np.dtype('i2'))
        array.fill(value)
        return array

    def reconstruct_cube(self, my_detector_signal, my_detector_noise):
        """
        This method creates an x,y,wavelength cube from the detector image.
        For images and single-slit spectra, this is trivial. For IFUs, this is a key step in the data
        reduction process.

        Parameters
        ----------
        my_detector_signal : DetectorSignal instance
        my_detector_noise : DetectorNoise instance

        Returns
        -------
        cube_signal : three-dimensional numpy.array
            The pixel rate plane, reshaped into an x,y,wavelength cube,
            sampled with spacings defined by the detector pixel scale.
        cube_noise : three-dimensional numpy.array
            As cube_signal, just for the noise.
        plane_grid : pandeia.engine.coords.Grid instance.
            The spatial grid.
        """

        cube_shape = self.get_cube_shape(my_detector_signal)
        cube_signal = np.zeros(cube_shape)
        cube_noise = np.zeros(cube_shape)
        cube_saturation = np.zeros(cube_shape)
        cube_ngroup_map = np.zeros(cube_shape)

        i = 0
        rates = my_detector_signal.rate_list
        stddevs = my_detector_noise.stdev_pix_list
        sats = my_detector_signal.saturation_list
        groups = my_detector_signal.groups_list
        for rate, stdev_pix, sat, group in zip(rates, stddevs, sats, groups):
            # The detector elements are not in the correct orientation. By using
            #  transpose, we rotate AND flip the array, such that the wavelength axis comes
            #  first (for easy slicing) and is in the correct order, AND the XY
            #  planes have the correct orientation (Issue #3167).
            cube_signal[:, :, i] = np.transpose(rate['fp_pix'])
            cube_noise[:, :, i] = np.transpose(stdev_pix)
            cube_saturation[:, :, i] = np.transpose(sat)
            cube_ngroup_map[:, :, i] = np.transpose(group)
            i += 1

        plane_grid = self.get_plane_grid(my_detector_signal)

        # For IFUs, the wavelength dimension has >1 element. For other modes, the wavelength dimension == 1, so we remove it here:
        if cube_signal.shape[1] == 1:
            cube_signal = cube_signal.squeeze()
            cube_noise = cube_noise.squeeze()

        return cube_signal, cube_noise, cube_saturation, cube_ngroup_map, plane_grid

    def get_plane_grid(self, my_detector_signal):
        """
        Create the spatial grid. A key application of this (general) method is to construct a spatial
        IFU grid (pixels-by-slices).

        Parameters
        ----------
        my_detector_signal : DetectorSignal instance

        Returns
        -------
        plane_grid : pandeia.engine.coords.Grid instance
            The spatial grid.
        """

        offsets = [aperture['offset'][1] for aperture in my_detector_signal.aperture_list]
        plane_grid = coords.IrregularGrid(my_detector_signal.grid.col, np.array(offsets))
        return plane_grid

    def get_cube_shape(self, my_detector_signal):
        """
        Returns the shape of the pixel-sampled cube (wavelength, number of slices, number of pixels).
        This is only used by spectroscopic modes.

        Parameters
        ----------
        my_detector_signal : DetectorSignal class

        Returns
        -------
        cube_shape : three-tuple
            The dimensions of the pixel-sampled cube.
        """

        aperture_sh = my_detector_signal.rate_list[0]['fp_pix'].shape
        n_apertures = len(my_detector_signal.rate_list)
        cube_shape = (aperture_sh[1], aperture_sh[0], n_apertures)
        return cube_shape

    def on_detector(self, image):
        """
        This helper method helps create a model detector plane from either an IFU cube or set of dithered
        images. In the case of IFU cubes, the detector plate scales are accurate, but the placement of slices
        on the detector is notional only. The output in that case is a computational convenience rather than
        something to be presented to a user. If the input data is not 3D, then apply appropriate image transforms
        to match the input coordinates. This way the same code can be used for dithered IFU and dithered
        imaging (e.g. coronagraphy).

        Parameters
        ----------
        image : two or three-dimensional numpy array.
            This contains the image or IFU cube data.

        Returns
        -------
        detector : two-dimensional numpy array.
            A "detector-like" product.
        """

        sh = image.shape
        if len(sh) == 3:
            # cubes come in with wavelength on the first axis for broadcasting purposes.
            # reshape it here to put dispersion along the X axis. we need to keep wavelength
            # first to keep the axes from getting scrambled by the reshape. do a transpose()
            # to get the 2D image into the desired orientation of +Y up and +wavelength to
            # the right.
            detector = np.reshape(image, (sh[0], sh[1] * sh[2]), order='F')
            detector = detector.transpose()
        else:
            # if we're not a cube, then the input image is already a detector plane image.
            detector = image
        return detector

    def _make_strip(self, grid, size, off=0., raise_except=False, name="Region"):
        """
        Make a mask image that defines a rectangular region of a given height and offset that
        extends along the entire dispersion axis. Perform bounds checking of the defined region.

        Parameters
        ----------
        grid: pandeia.engine.coords.Grid instance
            Grid that defines the coordinate system of the mask image
        size: float
            Size (height or width) of the region
        off: float
            Spatial offset to the center of the region
        except: bool
            If True, raise exception if region is outside of the field of view.  Otherwise create a warning.
        name: string
            Name to use for creating error/warning messages

        Returns
        -------
        region, reg_size: 2D np.ndarray, float
            'region' is the 2D image containing the mask that defines the region. Pixel values range from 0.0 to 1.0.
            'reg_size' is the 1D width of the region
        """
        if self.instrument.dispersion_axis() == "x":
            samp = grid.ysamp
            # SpecApPhot regions contain all wavelengths
            region = grid.rectangular_mask(height=size, yoff=off)
            reg_cut = region.sum(axis=1) / region.shape[1]
        else:
            samp = grid.xsamp
            # SpecApPhot regions contain all wavelengths
            region = grid.rectangular_mask(width=size, xoff=off)
            reg_cut = region.sum(axis=0) / region.shape[0]

        reg_size = reg_cut.sum() * samp
        reg_subs = np.where(reg_cut > 0)[0]

        # do some sanity and bounds checking
        if reg_subs.size == 0:
            msg = "%s outside of the field of view" % name
            if raise_except:
                raise EngineInputError(value=msg)
            else:
                key = '%s_missing' % name.lower().replace(' ', '_')
                self.warnings[key] = warning_messages[key]

        # if we have a pixel that's fully within the region at the edge of the image,
        # then the region is being truncated at the edge.
        if reg_cut[0] == 1.0 or reg_cut[-1] == 1.0:
            key = '%s_truncated' % name.lower().replace(' ', '_')
            loss_pct = 100.0 * (1.0 - reg_size / size)
            self.warnings[key] = warning_messages[key] % loss_pct

        return region, reg_size

    def _rotate_xy(self, vector):
        """
        Generic method for rotating coordinates in the scene (both real sources and strategy coordinates).
        Note that this will not spin extended sources; it only operates on a list of x and y coordinates and knows
        nothing about the geometry of a source.

        Parameters
        ----------
        vector: list
            A list of floats corresponding to the x and y coordinates of a scene element that needs to be rotated.

        Returns
        -------
        tx: float
        ty: float
               The x and y coordinates of the scene element after rotation.
        """
        angle = np.radians(self.scene_rotation)
        x = vector[0]
        y = vector[1]
        tx = x * np.cos(angle) - y * np.sin(angle)
        ty = x * np.sin(angle) + y * np.cos(angle)

        return tx,ty

    def rotate_sources(self,sources):
        """
        Wrapper for _rotate_xy to handle a list of sources dicts (that may be extended and need to be spun)

        Parameters
        ----------
        sources: list
            A list of source definition dictionaries, containing full source specifications.

        Returns
        -------
        sources: list
            A list of source definition dictionaries that have been rotated (and spun, if necessary)
        """
        for i, s in enumerate(sources):
            x = s.position['x_offset']
            y = s.position['y_offset']
            sources[i].position['x_offset'],sources[i].position['y_offset'] = self._rotate_xy([x,y])
            # if the sources are extended, they need to be rotated
            if s.shape['geometry'] != "point":
                sources[i].position['orientation'] = (sources[i].position['orientation'] + self.scene_rotation) % 360.0

        return sources

class ImagingApPhot(Strategy):

    """
    Strategy for aperture photometry used for standard imaging modes (NIRCam, MIRI, NIRISS).

    Attributes
    ----------
    aperture_size : float, in the internal spatial unit
        The radius of the extraction aperture.
    sky_annulus : float list-like, in the internal spatial unit.
        The inner and outer radius of the sky annulus.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    webapp: bool
        Toggle strict API checking
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        """
        The aperture photometry class is instantiated with the default aperture size given in the instrument
        configuration file.  If sky annulus not provided, set it to reasonable default.
        """

        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["method", "units", "target_xy", "aperture_size",
                                   "background_subtraction"]

        # https://github.com/spacetelescope/pandeia/issues/1686
        # Add check for sky_annulus if background_subraction exists and is true
        if config.get("background_subtraction"):
            self.api_parameters.append("sky_annulus")

        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

    def _sanity_checks(self):
        """
        Check various configuration items to make sure they make sense and raise exception if not.
        """
        # check that the subsampling is >= 1
        if self.subsampling < 1:
            msg = "Subsampling factor for source extraction aperture creation must be >= 1: %d" % self.subsampling
            raise EngineInputError(value=msg)
        # check that the specified units are supported
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)

        # make sure aperture size is > 0
        if self.aperture_size <= 0.0:
            msg = "%s error: aperture radius must be > 0.0." % self.__class__.__name__
            raise EngineInputError(value=msg)

        if self.background_subtraction:
            # check source and background regions to make sure they don't overlap
            ap = self.aperture_size
            bk_inner = self.sky_annulus[0]
            bk_outer = self.sky_annulus[1]
            if bk_inner >= bk_outer:
                msg = "%s error: background region outer radius must be > inner radius." % self.__class__.__name__
                raise EngineInputError(value=msg)
            if bk_inner <= ap:
                msg = "%s error: background region inner radius must be > aperture size to avoid overlap." % self.__class__.__name__
                raise EngineInputError(value=msg)

        # imagingapphot doesn't yet fully support dithers, but will eventually.
        on_target = getattr(self, "on_target", None)
        dithers = getattr(self, "dithers", None)

        # use the 'on_target' configuration to set up weight matrices based on which images
        # are at the target position and which are considered background.
        if on_target is None and dithers is not None:
            # If no on_target designations are passed, it is assumed that the first one
            # will be on target and the rest background.
            self.on_target = [False] * len(self.dithers)
            self.on_target[0] = True
        elif on_target is not None and dithers is not None:
            # make sure on_target and dithers are the same length
            if len(self.on_target) != len(self.dithers):
                message = "Number of on_target designations must equal number of dithers for %s." % self.__class__.__name__
                raise EngineInputError(value=message)
        else:
            self.on_target = [True]
            self.dithers = [{"x": 0.0, "y": 0.0}]

    def _check_circular_aperture_limits(self, aper_region, sky_subs, grid, aperture, annulus):
        """
        Make sure a circular aperture and the background estimation region around it both lie within the FOV, are not
        truncated by the edge of the FOV, and are not badly undersampled.

        Parameters
        ----------
        aper_region: numpy.ndarray
            Weight mask of pixels used for source extraction
        sky_subs: numpy.ndarray
            Index values for pixels used for background estimation
        grid: pandeia.engine.coords.Grid instance
            Spatial grid for detector plane
        aperture: float
            Radius of source extraction region
        annulus: list-like of length 2
            Inner and outer radii of background estimation region
        """
        # do some sanity checks that should result in exceptions
        n_aper = aper_region.sum()
        aper_subs = np.where(aper_region > 0)

        if n_aper == 0:
            msg = "No valid pixels within extraction aperture. Aperture too small or placed outside of the usable field of view."
            raise EngineInputError(value=msg)

        self.background_area = None
        # if there's no sky region (e.g. dithered or nodded calculations), sky_subs will be None
        if self.background_subtraction and sky_subs is not None and annulus is not None:
            n_sky = len(sky_subs[0])
            if n_sky == 0:
                msg = "No valid pixels within background estimation region. "
                msg += "Region too small or placed outside of the usable field of view."
                raise EngineInputError(value=msg)

            # having smaller sky region than source region is sub-optimal for the SNR
            if n_sky < n_aper:
                key = "background_region_too_small"
                self.warnings[key] = warning_messages[key]

            # check if background region bumps up against the edges of the FOV
            bk_outside_fov = False
            bk_x_check = 0 in sky_subs[1] or grid.nx - 1 in sky_subs[1]
            bk_y_check = 0 in sky_subs[0] or grid.ny - 1 in sky_subs[0]
            if bk_x_check or bk_y_check:
                bk_outside_fov = True
                key = "background_region_truncated"
                self.warnings[key] = warning_messages[key]

            bkgd_area = np.pi * (annulus[1] ** 2 - annulus[0] ** 2)
            bkgd_area_pix = bkgd_area / (grid.xsamp * grid.ysamp)
            self.background_area = bkgd_area_pix
            # warn if the actual area in pixels is much less than the requested area
            if n_sky < 0.9 * bkgd_area_pix and bk_outside_fov is False:
                loss_pct = 100.0 * (1.0 - n_sky / bkgd_area_pix)
                key = 'background_region_undersampled'
                self.warnings[key] = warning_messages[key] % loss_pct

        # check if source region bumps up against an edge of the field of view
        ap_outside_fov = False
        ap_x_check = 0 in aper_subs[1] or grid.nx - 1 in aper_subs[1]
        ap_y_check = 0 in aper_subs[0] or grid.ny - 1 in aper_subs[0]
        if ap_x_check or ap_y_check:
            ap_outside_fov = True
            key = "extraction_aperture_truncated"
            self.warnings[key] = warning_messages[key]

        aper_area = np.pi * aperture ** 2
        aper_area_pix = aper_area / (grid.xsamp * grid.ysamp)
        self.extraction_area = aper_area_pix

        # partial pixels are not included so n_aper/n_sky will always be less than aper_area/bkgd_area.
        # report a warning if the difference is more than 10%...
        if n_aper < 0.9 * aper_area_pix and ap_outside_fov is False:
            loss_pct = 100.0 * (1.0 - n_aper / aper_area_pix)
            key = 'extraction_aperture_undersampled'
            self.warnings[key] = warning_messages[key] % loss_pct

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        This private method creates the weight matrix, a_ij, used for the strategy sum. It gets overridden
        in each strategy.

        Parameters
        ----------
        my_detector_signal_list: list of DetectorSignal instances
        my_detector_noise_list: list of DetectorNoise instances

        Returns
        -------
        weight_matrix: numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts: List of subscripts
            A single strategy can return multiple products. The subscripts list the pixels to be summed
            over for each product.
        """

        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for imaging is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]

        aperture = self.aperture_size
        annulus = self.sky_annulus

        # pass target_xy to Signal.grid.dist() to offset the target position
        dist = my_detector_signal.grid.dist(xcen=self.target_xy[0], ycen=self.target_xy[1])

        # sky_subs only takes into account whole pixels which is sufficient for the sky estimation
        # region and for the sanity checking we need to do. however, we need to be more exact for the source extraction
        # region. photutils.geometry provides routines to do this either via subsampling or exact geometric
        # calculation. the exact method is slower, but for the sizes of regions we deal with in the ETC it is not noticeable.
        sky_subs = np.where((dist > annulus[0]) & (dist <= annulus[1]))
        n_sky = len(sky_subs[0])

        # generate the source extraction region mask.
        src_region = my_detector_signal.grid.circular_mask(
            aperture,
            xoff=self.target_xy[0],
            yoff=self.target_xy[1],
            use_exact=self.use_exact,
            subsampling=self.subsampling
        )

        # the src_region mask values are the fraction of the pixel subtended by the aperture so
        # in the range 0.0 to 1.0 inclusive.  the effective number of pixels in the aperture is
        # then the sum of this mask.
        n_aper = src_region.sum()

        # do some more sanity checks to make sure the target and background regions are configured as expected
        self._check_circular_aperture_limits(src_region, sky_subs, my_detector_signal.grid, aperture, annulus)

        weight_matrix = src_region
        if self.background_subtraction:
            weight_matrix[sky_subs] = -1. * n_aper / n_sky

        # The method also returns a list of 'products': subscripts of the weight matrix that is non-zero.
        # This can also be a list if the strategy returns more than one product (such a spectrum over a
        # number of wavelengths).
        product_subscript = weight_matrix.nonzero()

        # The subscripts returned from a matrix contain a redundant dimension. This removes it.
        # Note that this is not how matrix indexing is formally constructed, but it enforces a rule
        # that product subscripts should always be tuples or regular ndarrays.
        product_subscript = (np.array(product_subscript[0]).flatten(), np.array(product_subscript[1]).flatten())
        return weight_matrix, [product_subscript]

    def set_aperture(self, aperture_size, sky_annulus=None):
        """
        Sets the aperture parameters.

        Parameters
        ----------
        aperture : float
            Radius of the aperture in internal spatial units.
        sky_aperture : list-like of floats
            Radii of the inner and outer radius of the sky annulus.
        """

        self.aperture_size = aperture_size
        if isinstance(sky_annulus, (list, tuple)) and len(sky_annulus) == 2:
            self.sky_annulus = sky_annulus
        else:
            self.sky_annulus = (2.0 * self.aper, 4.0 * self.aper)

    def set_dithers(self, dithers):
        """
        Sets a list of dither positions. Each dither is a dict of x,y spatial offsets in the internal angular units.
        This list of dither positions can be trivial (i.e., ==[{'x':0.0,'y':0.0}]). The trivial dither is the default.

        Parameters
        ----------
        dithers : list of dither dictionaries
        """

        if 'x' in dithers[0] and 'y' in dithers[0]:
            self.dithers = dithers
        else:
            message = "Dither offsets need to be a list of {'x':x,'y':y} dictionaries."
            raise EngineInputError(value=message)


class Coronagraphy(ImagingApPhot):
    """
    Strategy for carrying out and analyzing coronagraphic observations.

    Attributes
    ----------
    target_xy: two-element list-like (float, float)
        Position of extraction aperture
    aperture_size: float
        Radius of extraction aperture in 'units'
    sky_annulus: two-element list-like (float, float)
        Inner and outer radii of sky background estimation region
    contrast_azimuth: float
        Azimuth at which to calculate contrast curve
    contrast_separation: float
        Single contrast separation for returning a scalar reference contrast value
        obtained from the contrast curve
    pointing_error: two-element list-like (float, float)
        Amount to shift occulted source to emulate imperfect pointing
    delta_opd: float
        Change in system OPD
    scene_rotation: float
        Rotation angle to apply to scene
    psf_subtraction_source: Source dict in engine API format
        Definition of source to use for PSF subtraction
    psf_subtraction_xy: two-element list-like (float, float)
        Offset to apply to psf_subtraction_source
    unocculted_xy: two-element list-like (float, float)
        Offset to apply to source to measure contrast between occulted and unocculted observation
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        """
        Parameters
        ----------
        instrument: Instrument subclass instance
            Instrument that was the basis of the calculation
        webapp: bool
            Determines whether strict API checks should be performed
        config: dict
            Extra configuration information in engine input API dict format
        **kwargs: keyword/value pairs
            Extra configuration information in kwargs format
        """

        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["method", "units", "aperture_size", "sky_annulus", "psf_subtraction",
                                   "contrast_azimuth", "scene_rotation", "contrast_separation",
                                   "psf_subtraction_source", "target_xy", "annulus_shape", "background_subtraction"]
            self.api_ignore = ["pointing_error", "psf_subtraction_xy", "ncontrast", "delta_opd", "unocculted_xy", "do_weighted_dithers"]

        # set the initial dither to the source position. the dither positions for psf subtraction
        # and contrast measurement will be appended to this automatically.
        self.dithers = [{'x': 0.0, 'y': 0.0}]

        # an optional switch for engine scripts to turn the dither weighting off.
        if not webapp:
            try:
                if config["do_weighted_dithers"]:
                    config["psf_subtraction"] = "optimal"
                else:
                    config["psf_subtraction"] = "no_autoscale"
            except KeyError:
                pass

        ImagingApPhot.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        # We are not running _make_dither_weights() here as it requires knowledge of the sources that won't
        # be available until we are actually extracting fluxes.

    def _sanity_checks(self):
        """
        Check various configuration items to make sure they make sense and raise exception/warning if not.
        """
        # check that the subsampling is >= 1
        if self.subsampling < 1:
            msg = "Subsampling factor for source extraction aperture creation must be >= 1: %d" % self.subsampling
            raise EngineInputError(value=msg)
        # check that the specified units are supported
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)

        # make sure aperture size is > 0
        if self.aperture_size <= 0.0:
            msg = "%s error: aperture radius must be > 0.0." % self.__class__.__name__
            raise EngineInputError(value=msg)

        if self.background_subtraction:
            # check source and background regions to make sure they don't overlap
            ap = self.aperture_size
            bk_inner = self.sky_annulus[0]
            bk_outer = self.sky_annulus[1]
            if bk_inner >= bk_outer:
                msg = "%s error: background region outer radius must be > inner radius." % self.__class__.__name__
                raise EngineInputError(value=msg)
            if bk_inner <= ap:
                msg = "%s error: background region inner radius must be > aperture size to avoid overlap." % self.__class__.__name__
                raise EngineInputError(value=msg)

        on_target = getattr(self, "on_target", None)
        # use the 'on_target' configuration to set up weight matrices based on which images
        # are at the target position and which are considered background.
        if on_target is None:
            # If no on_target designations are passed, it is assumed that the first one
            # will be on target and the rest background.
            self.on_target = [False] * len(self.dithers)
            self.on_target[0] = True
        else:
            # make sure on_target and dithers are the same length
            if len(self.on_target) != len(self.dithers):
                message = "Number of on_target designations must equal number of dithers for %s." % self.__class__.__name__
                raise EngineInputError(value=message)

        # check for bar obscuration when using masklwb or maskswb
        if self.instrument.instrument['aperture'] in ('masklwb', 'maskswb'):
            bar_width = self.instrument.bar_width(self.target_xy[0])
            if np.abs(self.target_xy[1]) < bar_width / 2.0:
                key = "target_occulted"
                self.warnings[key] = warning_messages[key]

        if self.delta_opd != 0.0:
            message = "Variable system OPD is not yet implemented %s." % self.__class__.__name__
            raise NotImplementedError(message)

        #if self.psf_subtraction == "none":
        #    message = "Coronagraphy with no PSF subtraction is not currently implemented."
        #    raise NotImplementedError(message)
        if self.psf_subtraction == "realistic":
            message = "Coronagraphy with realistic PSF subtraction (including pointing errors, etc) is not currently implemented."
            raise NotImplementedError(message)
        elif self.psf_subtraction not in ["optimal", "no_autoscale", "target_only", "psf_only"]:
            message = "Invalid PSF subtraction method, %s" % self.psf_subtraction
            raise EngineInputError(value=message)


    def _filter_results(self, product, listobj):
        """
        This function does two things:

        1.) Add in other planes if all are requested (an 'optimal' or 'no_autoscale' PSF subtraction type. It does
            nothing in target_only or psf_only modes, limiting the results to just be from those specific pointings.
        2.) Blank out contrast plane saturation array in a.) complete case, b.) when contrast IS the product. When a
            source is offset to unocculted_xy, it can be bright enough to cause saturation flags to be raised.
            However, since this is an "artifactual" offset, those saturation flags are bogus. The hackish fix is to
            replace this bogus saturation map with a new one filled with zeros.

        Parameters
        ----------
        product: list
            extracted products produced by the strategy
        listobj: list
            list of extracted products from individual pointings

        Returns
        -------
        product: list
            list of extracted products with the additional listobj products appended to the end
        """
        if self.do_contrast:
            # if this IS the contrast case, blank out the product saturation array.
            product[0]['detector_saturation'] = np.zeros(product[0]['detector_saturation'].shape)
        if self.psf_subtraction in ['optimal', 'no_autoscale']:
            # if we're going to add all three raw planes, blank out the saturation array on the third (contrast) one
            listobj[2]['detector_saturation'] = np.zeros(listobj[2]['detector_saturation'].shape)
            product.extend(listobj)
        return product

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        This private method creates the weight matrix, a_ij, used for the strategy sum. It gets overridden
        in each strategy.

        Parameters
        ----------
        my_detector_signal_list: list of DetectorSignal instances
        my_detector_noise_list: list of DetectorNoise instances

        Returns
        -------
        weight_matrix: numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts: List of subscripts
            A single strategy can return multiple products. The subscripts list the pixels to be summed
            over for each product.
        """

        if len(my_detector_signal_list) != 3:
            message = 'Coronagraphic observations require three dithers (one on target, \
                       one on a PSF subtraction star and one of the unocculted target star)'
            raise UnsupportedError(value=message)

        max_central = 0.1
        min_psf = my_detector_signal_list[0].fov_size/2.0
        psf_idx = my_detector_signal_list[0].scene.psf_subtraction_idx

        # min_snr = 0.1  # the inner working angle will depend upon the mask and filter combination, and will need a more
        # rigorous computation to determine.  (See commented-out item 3, below)
        # 1. Check for existence of a central source:
        central = [k for k in range(len(my_detector_signal_list[0].scene.sources)) if
               np.sqrt(my_detector_signal_list[0].scene.sources[k].position['x_offset'] ** 2
               + my_detector_signal_list[0].scene.sources[k].position['y_offset'] ** 2) < max_central]
        if len(central) < 1:
            key = "coronagraphy_central_source"
            self.warnings[key] = warning_messages[key].format(max_central)
        # 2. Check the location of the PSF subtraction source:
        psfdist = np.sqrt(my_detector_signal_list[0].scene.sources[psf_idx].position['x_offset'] ** 2 +
                          my_detector_signal_list[0].scene.sources[psf_idx].position['y_offset'] ** 2)
        if psfdist < min_psf:
            key = "coronagraphy_psf_source"
            self.warnings[key] = warning_messages[key].format(min_psf, psfdist)
        # 3. Check that the target is unobscured (not implemented as of 2017.0920)

        weight_matrix_list = []
        product_subscripts_list = []

        for my_detector_signal in my_detector_signal_list:
            grid = my_detector_signal_list[0].grid

            aperture = self.aperture_size
            annulus = self.sky_annulus

            # pass target_xy to Signal.grid.dist() to offset the target position
            dist = grid.dist(xcen=self.target_xy[0], ycen=self.target_xy[1])

            # sky_subs only takes into account whole pixels which is sufficient for the sky estimation
            # region and for the sanity checking we need to do. however, we need to be more exact for the source extraction
            # region. photutils.geometry provides routines to do this either via subsampling or exact geometric
            # calculation. the exact method is slower, but for the sizes of regions we deal with in the ETC it is not noticeable.
            sky_subs = np.where((dist > annulus[0]) & (dist <= annulus[1]))
            n_sky = len(sky_subs[0])

            # generate the source extraction region mask.
            src_region = grid.circular_mask(
                aperture,
                xoff=self.target_xy[0],
                yoff=self.target_xy[1],
                use_exact=self.use_exact,
                subsampling=self.subsampling
            )

            # the src_region mask values are the fraction of the pixel subtended by the aperture so
            # in the range 0.0 to 1.0 inclusive.  the effective number of pixels in the aperture is
            # then the sum of this mask.
            n_aper = src_region.sum()

            # do some more sanity checks to make sure the target and background regions are configured as expected
            self._check_circular_aperture_limits(src_region, sky_subs, grid, aperture, annulus)

            weight_matrix = src_region
            if self.background_subtraction:
                weight_matrix[sky_subs] = -1. * n_aper / n_sky

            # The method also returns a list of 'products': subscripts of the weight matrix that is non-zero.
            # This can also be a list if the strategy returns more than one product (such a spectrum over a
            # number of wavelengths).
            product_subscript = weight_matrix.nonzero()

            # The subscripts returned from a matrix contain a redundant dimension. This removes it.
            # Note that this is not how matrix indexing is formally constructed, but it enforces a rule
            # that product subscripts should always be tuples or regular ndarrays.
            product_subscript = (np.array(product_subscript[0]).flatten(), np.array(product_subscript[1]).flatten())

            weight_matrix_list.append(weight_matrix)
            product_subscripts_list.append([product_subscript])

        return weight_matrix_list, product_subscripts_list


    def _add_exposures(self, exposure_list, exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups):
        """
        For Coronagraphy, the PSF subtraction source may be fainter, brighter, or simply a
        different spectral type from the central source. Thus, the dither weights can't be
        determined beforehand. This method overrides the default _add_exposures to pass
        Coronagraphy's _make_dither_weights the exposure fluxes.

        Parameters
        ----------
        exposure_list: list
            A list of exposure product dictionaries
        exposure_sum: dict
            Dict of exposure products to be updated and populated
        reconstructed_signal: 3D numpy.ndarray
            Initial reconstructed signal cube
        reconstructed_noise: 3D numpy.ndarray
            Initial reconstructed noise cube
        reconstructed_saturation: 3D numpy.ndarray
            Initial reconstructed saturation cube

        Returns
        -------
        exposure_sum: dict
            Contains a sensible sum of signals (weighted by dithers) and noise (added in quadrature).
        reconstructed_signal: 3D numpy.ndarray
            Combined reconstructed signal cube
        reconstructed_noise: 3D numpy.ndarray
            Combined reconstructed noise cube
        reconstructed_saturation: 3D numpy.ndarray
            Combined reconstructed saturation cube
        """
        exposure_list = self._make_dither_weights(exposure_list)

        exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups = Strategy._add_exposures(self, exposure_list, exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups)

        return exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups

    def _make_dither_weights(self, exposure_list):
        """
        Coronagraphy uses three dithers: The first dither is the main scene, the second is the appropriately-scaled
        PSF subtraction source, and the third is used to determine the contrast (its flux is neither added
        nor subtracted).

        We cannot use the extracted flux scalar for this, because the extracted flux is the flux of the entire scene.
        If we have more than one bright source in this scene, we would scale the PSF subtraction source to too high a
        flux and over-subtract the central source.

        We sample the arrays at multiple 3x3 regions because any one of them (but probably not more than two) may be
        contaminated with flux from another source - a nearby bright source, or the SNR source itself.

        We are removing the unused exposures from the exposure_list for each scenario. Setting the unused dither's
        weights to zero doesn't work: The unocculted dither (particularly) may be so bright it saturates, such that the
        noise array ends up full of NaNs. In that case, because 0*NaN = NaN, and any integer + NaN = NaN, it WOULD fill
        the results with NaNs even though it's weighted to zero.

        Parameters
        ----------
        exposure_list: list
            A list of exposure product dictionaries
        """

        # If self.do_contrast is set to True, set the unocculted dither for the contrast calculation (independent of psf_subtraction)
        if self.do_contrast:
            self.dither_weights = [1]
            exposure_list = [exposure_list[2]]
        else:
            # this is the default Optimal option with PSF Autoscaling, called "Optimal (PSF Autoscaling)" in the client.
            if self.psf_subtraction == "optimal":
                ditherpos = np.sum(exposure_list[0]['reconstructed'][0],axis=2)
                ditherneg = np.sum(exposure_list[1]['reconstructed'][0],axis=2)

                sizea,sizeb = ditherpos.shape
                sizea = np.int(np.round(sizea/2.0))
                sizeb = np.int(np.round(sizeb/2.0))

                # a series of grid positions, selected so that the 3x3 grids placed at those locations would not overlap.
                # These do not assume anything particularly about the scene size or pixel scale such that they would need to
                # change; they are simply there to measure the PSF ratio at 25 different points.
                positions = [-7, -4, 0, 4, 7]

                ratio = []
                for x in positions:
                    for y in positions:
                        # Grab a box
                        pos = np.median(ditherpos[sizea+x-1:sizea+x+2,sizeb+y-1:sizeb+y+2])
                        neg = np.median(ditherneg[sizea+x-1:sizea+x+2,sizeb+y-1:sizeb+y+2])
                        ratio.append(pos/neg)

                # All of the potential contaminants that would make the flux at 0,0 NOT representative of the flux of the
                # central source are things that would make the central source appear to be BRIGHTER. Thus, by looking for the
                # minimum value, we come closest to completely removing the central source.
                self.dither_weights = [1, -1*np.min(ratio)]
                exposure_list = exposure_list[:2]
            # this option has no autoscaling, and was the default behavior in v1.1.1 and previous. Called
            # "Optimal (No PSF Autoscaling)" in the client.
            elif self.psf_subtraction == "no_autoscale":
                self.dither_weights = [1, -1]
                exposure_list = exposure_list[:2]
            # this option returns only the first subreport (the scene w/central source and snr target), called
            # "Unsubtracted Science Scene" in the client.
            elif self.psf_subtraction == "target_only":
                self.dither_weights = [1]
                exposure_list = [exposure_list[0]]
            # this option returns only the second subreport (just the PSF subtraction source), called "PSF
            # Subtraction Source Only" in the client.
            elif self.psf_subtraction == "psf_only":
                self.dither_weights = [1]
                exposure_list = [exposure_list[1]]
            else:
                # this should already have been triggered by __init__, but just to cover the bases...
                message = "Invalid PSF subtraction method, %s" % self.psf_subtraction
                raise EngineInputError(value=message)


        return exposure_list


    def set_dithers(self, dithers):
        """
        Sets a list of dither positions. Each dither is a dict of x,y spatial offsets in the internal angular units.
        This list of dither positions can be trivial (i.e., ==[{'x': 0.0, 'y': 0.0}]). The trivial dither is the default.

        Parameters
        ----------
        dithers : list of dither dictionaries
        """

        if 'x' in dithers[0] and 'y' in dithers[0]:
            self.dithers = dithers
        else:
            message = "Dither offsets need to be a list of {'x': x, 'y': y} dictionaries."
            raise EngineInputError(value=message)

    def rotate(self,sources):
        """
        Rotate a Coronagraphy strategy calculation

        Parameters
        ----------
        sources: list
            A list of source dictionaries containing full souce definitions

        Returns
        -------
        sources: list
               The list of source dictionaries, with its sources rotated (and extended sources spun)
        """
        # rotating sources requires a few more steps and needs to use this wrapper
        sources = self.rotate_sources(sources)

        # rotate Coronagraphy strategy inputs
        self.psf_subtraction_xy = self._rotate_xy(self.psf_subtraction_xy)
        self.pointing_error = self._rotate_xy(self.pointing_error)
        self.unocculted_dither = self._rotate_xy(self.unocculted_xy)
        self.target_xy = self._rotate_xy(self.target_xy)

        return sources

class SpecApPhot(ImagingApPhot):

    """
    Strategy for aperture spectroscopy. This strategy applies, at least, to all slitted spectroscopic modes,
    including NIRSpec MSA, NIRSpec fixed slit and MIRI LRS. It is not applicable to IFUs.

    Attributes
    ----------
    aperture_size : float, in the internal spatial unit, optional.
        The radius of the extraction aperture.
    sky_annulus : float tuple, in the internal spatial unit., optional.
        The inner and outer radius of the sky annulus.
    target_xy: list-like of format (float, float)
        X and Y center position of the aperture and sky annulus.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Instrument mode.
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """
    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["method", "units", "target_xy", "aperture_size",
                                   "background_subtraction", "reference_wavelength"]

        ImagingApPhot.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)
        # getting backgrounds from other orders for slitless modes requires treating them as multiorder modes.
        # Thus, we need to set the order (to the one listed in the disperser configuration `orders` attribute)
        # to pull the correct information out. For SpecApPhot modes that do not have background-only orders, `order`
        # will be unused.
        self.order=instrument.disperser_config[self.disperser_key].get("orders", [None])[0]

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        The weight matrix for the spectroscopic modes creates a separate strategy
        product for each spectral wavelength column. That is, the full weight matrix is
        created for the full (y,wavelength) grid, but each product will only use one column.

        Parameters
        ----------
        my_detector_signal : DetectorSignal instance
        my_detector_noise : DetectorNoise instance

        Returns
        -------
        weight_matrix : numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts : List of subscripts
            The product list has the same number of elements as there are wavelength columns.
        """
        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for slit spectroscopy is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]
        my_detector_noise = my_detector_noise_list[0]
        pix_grid = my_detector_signal.pixgrid_list[0]
        aperture = self.aperture_size
        annulus = self.sky_annulus

        # dispersion can be along +X or +Y axis.  set up the spatial and wavelength offsets accordingly to
        # account for dispersion being rotated w.r.t. the scene coordinates
        if self.instrument.dispersion_axis() == 'x':
            self.spatial_off = self.target_xy[1]
            self.wave_off = self.target_xy[0]
            wave_off_pix = self.wave_off / pix_grid.xsamp
        else:
            self.spatial_off = self.target_xy[0]
            self.wave_off = -self.target_xy[1]
            wave_off_pix = self.wave_off / pix_grid.ysamp

        src_region, src_region_size = self._make_strip(
            grid=pix_grid,
            size=2.0 * aperture,
            off=self.spatial_off,
            raise_except=True,
            name="Extraction aperture"
        )

        if self.background_subtraction:
            # now define the sky subtraction region as 2 swathes above and below the source aperture
            sky_size = annulus[1] - annulus[0]
            sky_offset = (annulus[1] + annulus[0]) / 2.0

            upper_sky_region, upper_sky_region_size = self._make_strip(
                grid=pix_grid,
                size=sky_size,
                off=self.spatial_off + sky_offset,
                raise_except=False,
                name="Upper background region"
            )

            lower_sky_region, lower_sky_region_size = self._make_strip(
                grid=pix_grid,
                size=sky_size,
                off=self.spatial_off - sky_offset,
                raise_except=False,
                name="Lower background region"
            )

            sky_region = upper_sky_region + lower_sky_region
            sky_region_size = upper_sky_region_size + lower_sky_region_size

            # make sure background region is larger than the source region
            if sky_region_size < src_region_size:
                key = 'background_region_too_small'
                self.warnings[key] = warning_messages[key]

            if sky_region_size == 0.0:
                msg = "No valid background region specified."
                raise EngineInputError(value=msg)

            bk_weight = -src_region_size / sky_region_size
            sky_region *= bk_weight
            weight_matrix = src_region + sky_region
        else:
            self.background_area = None
            weight_matrix = src_region

        # need to handle dispersion direction here to rotate the weight matrix
        # and set up the product_subscripts

        # if this is a slitless calculation with multiple background orders, my_detector_signal is actually a
        # CombinedSignal instance with a whole LIST of wave_pix values rather than just one.
        if 'orders' in my_detector_signal.current_instrument.disperser_config[self.disperser_key]:
            nw = my_detector_signal.wave_pix_dict[self.order].shape[0]
            wave_pix = my_detector_signal.wave_pix_dict[self.order]
        else:
            nw = my_detector_signal.wave_pix.shape[0]
            wave_pix = my_detector_signal.wave_pix
        nx = my_detector_noise.var_pix.shape[1]
        ny = my_detector_noise.var_pix.shape[0]

        # only compute subpixel wavelength offsets for slitless-type projections (JETC-646)
        if my_detector_signal.current_instrument.projection_type in ["slitless", "multiorder"]:
            # correct wave_pix for subpixel placement (JETC-646). Given a subpixel shift of x, the
            # wavelength array will too low by x wavelength elements.
            # 1. Get fractional part of wave_off_pix - this is the fraction of wavelength elements
            #    the array will be off by.
            wave_off_subpix = wave_off_pix % 1
            if wave_off_subpix != 0.0:
                # 2. Set up the wavelength grid in wavelength elements
                wave_elements = np.arange(nw)
                # bounds_error=False fills pixels outside of the interpolation range with np.NaN, rather than crashing
                interpolator = sc.interpolate.interp1d(wave_elements, wave_pix, bounds_error=False)
                # 3. Now find the offset wavelength elements.
                wave_off_elements = wave_elements-wave_off_subpix
                wave_pix = interpolator(wave_off_elements)

                # trim the wavelength array and shorten it
                nw = nw - 1
                # save the revised wavelength array back to the correct place
                if 'orders' in my_detector_signal.current_instrument.disperser_config[self.disperser_key]:
                    my_detector_signal.wave_pix_dict[self.order] = wave_pix[1:]
                else:
                    my_detector_signal.wave_pix = wave_pix[1:]

        if self.instrument.dispersion_axis() == 'x':
            # Are there more detector columns than wavelength channels?
            excess = nx - nw
            waves = np.arange(nw)
            if excess > 0:
                # only add in a wavelength offset if there's excess
                if wave_off_subpix != 0.0: # only do this if the spectrum doesn't line up exactly
                    waves = np.arange(nw) + 1
                waves = waves + int((excess - 1) / 2) + wave_off_pix
            if excess < 0:
                raise NotImplementedError
            waves = waves[waves < nx]
            waves = waves[waves >= 0]
            colsubs = np.arange(ny, dtype=np.dtype('i4'))
            product_subscripts = [(colsubs, self._fill_array(ny, i)) for i in waves]
            self.extraction_area = src_region_size / pix_grid.ysamp
            if self.background_subtraction:
                self.background_area = sky_region_size / pix_grid.ysamp
        else:
            # Are there more detector rows than wavelength channels?
            excess = ny - nw
            waves = np.arange(nw)
            # only apply wavelength offsets if there IS excess (JETC-646)
            if excess > 0:
                # only add in a wavelength offset if there's excess
                if wave_off_subpix != 0.0: # only do this if the spectrum doesn't line up exactly
                    waves = np.arange(nw) + 1
                # Fixes JETC-762 bug
                waves = waves + int((excess - 1) / 2) - wave_off_pix + 1
            if excess < 0:
                raise NotImplementedError
            waves = waves[waves < ny]
            waves = waves[waves >= 0]
            rowsubs = np.arange(nx, dtype=np.dtype('i4'))
            product_subscripts = [(self._fill_array(nx, i), rowsubs) for i in waves]
            self.extraction_area = src_region_size / pix_grid.xsamp
            if self.background_subtraction:
                self.background_area = sky_region_size / pix_grid.xsamp

        # if the wavelength subscripts are truncated compared to wave_pix, this means that the
        # center of the extraction aperture is out of the range of the reference data or field of view.
        # it should be possible to support the truncated case where the spectrum lies partially outside
        # the FOV, but it would require refactoring how wave_pix is handled here and returned.
        if len(waves) < nw:
            msg = "Extraction aperture out of range in dispersion direction."
            raise EngineInputError(value=msg)

        return weight_matrix, product_subscripts


class MSAApPhot(ImagingApPhot):

    """
    Strategy for imaging aperture photometry on the AllOpen MSA shutters. A
    slight variation on ImagingApPhot, with the addition of allowing the
    the target to be centered relative to the shutters and offset from there.

    Attributes
    ----------
    aperture_size : float, in the internal spatial unit
        The radius of the extraction aperture.
    sky_annulus : float list-like, in the internal spatial unit.
        The inner and outer radius of the sky annulus.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    webapp: bool
        Toggle strict API checking
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        """
        The aperture photometry class is instantiated with the default aperture size given in the instrument
        configuration file.  If sky annulus not provided, set it to reasonable default.
        """

        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["method", "units", "shutter_offset", "aperture_size",
                                   "target_xy", "dithers", "background_subtraction"]

        # https://github.com/spacetelescope/pandeia/issues/1686
        # Add check for sky_annulus if background_subraction exists and is true
        if config.get("background_subtraction"):
            self.api_parameters.append("sky_annulus")

        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        # apply shutter_offset to self.dithers
        for dither in self.dithers:
            dither['x'] = -self.target_xy[0] + self.shutter_offset[0]
            dither['y'] = -self.target_xy[1] + self.shutter_offset[1]

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        This private method creates the weight matrix, a_ij, used for the strategy sum. It gets overridden
        in each strategy.

        Parameters
        ----------
        my_detector_signal_list: list of DetectorSignal instances
        my_detector_noise_list: list of DetectorNoise instances

        Returns
        -------
        weight_matrix: numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts: List of subscripts
            A single strategy can return multiple products. The subscripts list the pixels to be summed
            over for each product.
        """

        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for imaging is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]

        aperture = self.aperture_size
        annulus = self.sky_annulus

        # pass target_xy to Signal.grid.dist() to offset to the offset position
        dist = my_detector_signal.grid.dist(xcen=self.shutter_offset[0], ycen=self.shutter_offset[1])

        # sky_subs only takes into account whole pixels which is sufficient for the sky estimation
        # region and for the sanity checking we need to do. however, we need to be more exact for the source extraction
        # region. photutils.geometry provides routines to do this either via subsampling or exact geometric
        # calculation. the exact method is slower, but for the sizes of regions we deal with in the ETC it is not noticeable.
        sky_subs = np.where((dist > annulus[0]) & (dist <= annulus[1]))
        n_sky = len(sky_subs[0])

        # generate the source extraction region mask.
        # because we're moving the source to the center, we only need to account for the shutter offset.
        src_region = my_detector_signal.grid.circular_mask(
            aperture,
            xoff=self.shutter_offset[0],
            yoff=self.shutter_offset[1],
            use_exact=self.use_exact,
            subsampling=self.subsampling
        )

        # the src_region mask values are the fraction of the pixel subtended by the aperture so
        # in the range 0.0 to 1.0 inclusive.  the effective number of pixels in the aperture is
        # then the sum of this mask.
        n_aper = src_region.sum()

        # do some more sanity checks to make sure the target and background regions are configured as expected
        self._check_circular_aperture_limits(src_region, sky_subs, my_detector_signal.grid, aperture, annulus)

        weight_matrix = src_region
        if self.background_subtraction:
            weight_matrix[sky_subs] = -1. * n_aper / n_sky

        # The method also returns a list of 'products': subscripts of the weight matrix that is non-zero.
        # This can also be a list if the strategy returns more than one product (such a spectrum over a
        # number of wavelengths).
        product_subscript = weight_matrix.nonzero()

        # The subscripts returned from a matrix contain a redundant dimension. This removes it.
        # Note that this is not how matrix indexing is formally constructed, but it enforces a rule
        # that product subscripts should always be tuples or regular ndarrays.
        product_subscript = (np.array(product_subscript[0]).flatten(), np.array(product_subscript[1]).flatten())
        return weight_matrix, [product_subscript]

class MSAFullApPhot(Strategy):
    """
    Strategy for full aperture extraction for multi-shutter instruments. This strategy is designed for use with the
    NIRSpec multi-shutter array. The MSA full aperture extraction only needs to know which shutters are
    designated background and which are sky. The spectra are then extracted from the full height of one or more shutters.
    The strategy can handle any combination of source and sky shutters, except for the case where there is no source shutter.

    Attributes
    ----------
    dithers: List of dictionaries.
        Each dither dict contains 'x' and 'y' offsets (floats) and 'on_source', a list of booleans indicating if a shutter
        should be extracted as the source (True) or sky (False).
    shutter_offset: two-element list-like
        X, Y offset pair by which the shutter array is offset w.r.t. the scene

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Instrument mode.
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["shutter_offset", "dithers", "units", "method",
                                   "background_subtraction", "reference_wavelength"]

        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        # apply shutter_offset to self.dithers
        # This offsetting process is currently broken (JETC-405) and needs to be fixed (JETC-429)
        for dither in self.dithers:
            dither['x'] += self.shutter_offset[0]
            dither['y'] += self.shutter_offset[1]

    def _sanity_checks(self):
        """
        Check various configuration items to make sure they make sense and raise exception if not.
        """
        # check that the subsampling is >= 1
        if self.subsampling < 1:
            msg = "Subsampling factor for source extraction aperture creation must be >= 1: %d" % self.subsampling
            raise EngineInputError(value=msg)
        # check that the specified units are supported
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)
        # check that the on_source arrays sent with the dithers are the correct length
        for d in self.dithers:
            if len(d['on_source']) != len(self.instrument.get_aperture_pars()['multishutter']):
                msg = "Each dither must provide a boolean for each shutter denoting whether it is on-source or on-sky."
                raise EngineInputError(value=msg)

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        The weight matrix for the spectroscopic modes creates a separate strategy
        product for each spectral wavelength column. That is, the full weight matrix is
        created for the full (y,wavelength) grid, but each product will only use one column.

        Parameters
        ----------
        my_detector_signal : DetectorSignal instance
        my_detector_noise : DetectorNoise instance

        Returns
        -------
        weight_matrix : numpy matrix
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts : List of subscripts
            The product list has the same number of elements as there are wavelength columns.
        """

        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for slit spectroscopy is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]
        pix_grid = my_detector_signal.pixgrid_list[0]
        samp = (pix_grid.xsamp + pix_grid.ysamp) / 2.0
        dither = self.dithers[0]

        height = self.instrument.get_aperture_pars()['xdisp']
        shutter_locations = self.instrument.get_aperture_pars()['multishutter']

        src_region_size = 0.
        sky_region_size = 0.
        src_region = np.zeros(pix_grid.shape)
        sky_region = np.zeros(pix_grid.shape)

        """
        We still need to implement the dithers, but eventually that should be done as a loop here.
        """
        for on_source, offset in zip(dither['on_source'], shutter_locations):
            region, region_size = self._make_strip(
                grid=pix_grid,
                size=height,
                off=offset[1],
                raise_except=True,
                name="Shutter region"
            )
            if on_source:
                src_region_size += region_size
                src_region = np.maximum(src_region, region)
            else:
                sky_region_size += region_size
                sky_region = np.maximum(sky_region, region)

        if sky_region_size > 0.0:
            if self.background_subtraction:
                bk_weight = -src_region_size / sky_region_size
            else:
                bk_weight = 0.0
            sky_region *= bk_weight

        weight_matrix = src_region + sky_region

        self.extraction_area = src_region_size / samp
        self.background_area = sky_region_size / samp

        ny = pix_grid.shape[0]
        nw = pix_grid.shape[1]
        colsubs = np.arange(ny, dtype=np.dtype('i4'))
        product_subscripts = [(colsubs, self._fill_array(ny, i))
                              for i in np.arange(nw)]

        return weight_matrix, product_subscripts


class MSAShutterApPhot(Strategy):
    """
    Strategy for full aperture extraction for multi-shutter instruments. This strategy is designed for use with the
    NIRSpec multi-shutter array. The MSA full aperture extraction only needs to know which shutters are
    designated background and which are sky. The spectra are then extracted from the full height of one or more shutters.
    The strategy can handle any combination of source and sky shutters, except for the case where there is no source shutter.

    Attributes
    ----------
    dithers: List of dictionaries.
        Each dither dict contains 'x' and 'y' offsets (floats) and 'on_source', a list of booleans indicating if a shutter
        should be extracted as the source (True) or sky (False).
    shutter_offset: two-element list-like
        X, Y offset pair by which the shutter array is offset w.r.t. the scene

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Instrument mode.
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["shutter_offset", "dithers", "units",
                                   "method", "background_subtraction"]

        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        # apply shutter_offset to self.dithers.
        # This offsetting process is currently broken (JETC-405) and needs to be fixed (JETC-429)
        for dither in self.dithers:
            dither['x'] += self.shutter_offset[0]
            dither['y'] += self.shutter_offset[1]

    def _sanity_checks(self):
        """
        Check various configuration items to make sure they make sense and raise exception if not.
        """
        # check that the subsampling is >= 1
        if self.subsampling < 1:
            msg = "Subsampling factor for source extraction aperture creation must be >= 1: %d" % self.subsampling
            raise EngineInputError(value=msg)
        # check that the specified units are supported
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)
        # check that the on_source arrays sent with the dithers are the correct length
        for d in self.dithers:
            if len(d['on_source']) != len(self.instrument.get_aperture_pars()['multishutter']):
                msg = "Each dither must provide a boolean for each shutter denoting whether it is on-source or on-sky."
                raise EngineInputError(value=msg)

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        The weight matrix for the spectroscopic modes creates a separate strategy
        product for each spectral wavelength column. That is, the full weight matrix is
        created for the full (y,wavelength) grid, but each product will only use one column.

        Parameters
        ----------
        my_detector_signal : DetectorSignal instance
        my_detector_noise : DetectorNoise instance

        Returns
        -------
        weight_matrix : numpy matrix
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts : List of subscripts
            The product list has the same number of elements as there are wavelength columns.
        """

        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for slitlet photometry is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]
        pix_grid = my_detector_signal.pixgrid_list[0]
        samp = (pix_grid.xsamp + pix_grid.ysamp) / 2.0
        dither = self.dithers[0]

        height = self.instrument.get_aperture_pars()['xdisp']
        width = self.instrument.get_aperture_pars()['disp']
        shutter_locations = self.instrument.get_aperture_pars()['multishutter']

        src_region_size = 0.
        sky_region_size = 0.
        src_region = np.zeros(pix_grid.shape)
        sky_region = np.zeros(pix_grid.shape)

        """
        We still need to implement the dithers, but eventually that should be done as a loop here.
        """
        for on_source, offset in zip(dither['on_source'], shutter_locations):
            region = pix_grid.rectangular_mask(
                width=width,
                height=height,
                xoff=offset[0],
                yoff=offset[1],
            )
            region_size = np.sum(region) * (pix_grid.xsamp * pix_grid.ysamp)
            if on_source:
                src_region_size += region_size
                src_region = np.maximum(src_region, region)
            else:
                sky_region_size += region_size
                sky_region = np.maximum(sky_region, region)

        if sky_region_size > 0.0:
            if self.background_subtraction:
                bk_weight = -src_region_size / sky_region_size
            else:
                bk_weight = 0.0
            sky_region *= bk_weight

        weight_matrix = src_region + sky_region

        self.extraction_area = src_region_size / samp
        self.background_area = sky_region_size / samp

        # The method also returns a list of 'products': subscripts of the weight matrix that is non-zero.
        # This can also be a list if the strategy returns more than one product (such a spectrum over a
        # number of wavelengths).
        product_subscript = weight_matrix.nonzero()

        # The subscripts returned from a matrix contain a redundant dimension. This removes it.
        # Note that this is not how matrix indexing is formally constructed, but it enforces a rule
        # that product subscripts should always be tuples or regular ndarrays.
        product_subscript = (np.array(product_subscript[0]).flatten(), np.array(product_subscript[1]).flatten())
        return weight_matrix, [product_subscript]


class IFUApPhot(ImagingApPhot):

    """
    Strategy for IFU spectroscopy. This strategy applies to the NIRSpec and MIRI IFUs. It operates as
    the imaging modes for each imaging plane. The wavelength-dependent IFU spectral product is then calculated
    by looping over all the wavelength planes.

    Attributes
    ----------
    aperture_size : float, in the internal spatial unit, optional.
        The radius of the extraction aperture.
    target_xy: list-like of format (float, float)
            X and Y center position of the aperture and sky annulus.
    sky_annulus : float tuple, in the internal spatial unit., optional.
        The inner and outer radius of the sky annulus.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Instrument mode.
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """
    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["method", "units", "target_xy", "aperture_size",
                                   "sky_annulus", "background_subtraction", "reference_wavelength"]

        ImagingApPhot.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        For the IFUs, the conceptually easiest approach is to initially create the
        apertures and weights in cube-space, and then reshape into detector-space.
        For PSF-dependent aperture sizes, this will have to be done for each wavelength.

        Parameters
        ----------
        my_detector_signal : DetectorSignal instance
        my_detector_noise : DetectorNoise instance

        Returns
        -------
        weight_matrix : numpy matrix
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts : List of subscripts
            For an IFU, each product represents a single image plane. Each image plane is treated
            as an image aperture photometry strategy.
            The product list has the same number of elements as there are wavelength planes.
        """

        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for regular IFU spectroscopy is not yet supported.'
            message += 'Consider using the IFUNodApPhot strategy instead.'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]

        aperture = self.aperture_size
        annulus = self.sky_annulus

        cube_shape = self.get_cube_shape(my_detector_signal)
        plane_grid = self.get_plane_grid(my_detector_signal)
        dist = plane_grid.dist(xcen=self.target_xy[0], ycen=self.target_xy[1])

        weight_cube = np.zeros(cube_shape)

        # sky_subs only takes into account whole pixels which is sufficient for the sky estimation
        # region and for the sanity checking we need to do. however, we need to be more exact for the source extraction
        # region. photutils.geometry provides routines to do this either via subsampling or exact geometric
        # calculation. the exact method is slower, but for the sizes of regions we deal with in the ETC it is not noticeable.
        sky_subs = np.where((dist > annulus[0]) & (dist <= annulus[1]))
        n_sky = len(sky_subs[0])

        # generate the source extraction region mask.
        src_region = plane_grid.circular_mask(
            aperture,
            xoff=self.target_xy[0],
            yoff=self.target_xy[1],
            use_exact=self.use_exact,
            subsampling=self.subsampling
        )

        # the src_region mask values are the fraction of the pixel subtended by the aperture so
        # in the range 0.0 to 1.0 inclusive.  the effective number of pixels in the aperture is
        # then the sum of this mask.
        n_aper = src_region.sum()

        # do some more sanity checks to make sure the target and background regions are configured as expected
        self._check_circular_aperture_limits(src_region, sky_subs, plane_grid, aperture, annulus)

        # build the weight cube plane by plane
        for i in range(cube_shape[0]):
            weight_cube[i, :, :] = src_region
            if self.background_subtraction:
                weight_cube[i, :, :][sky_subs] = -1. * n_aper / n_sky

        weight_matrix = self.on_detector(weight_cube)

        ny = weight_matrix.shape[0]
        nw = weight_matrix.shape[1]

        colsubs = np.arange(ny, dtype=np.dtype('i4'))
        product_subscripts = [(colsubs, self._fill_array(ny, i))
                              for i in np.arange(nw)]

        return weight_matrix, product_subscripts


class IFUNodOffScene(IFUApPhot):

    """
    Strategy for IFU spectroscopy that uses a nod away from the scene to determine the background to subtract. This
    strategy applies to all supported IFUs. It functions like the regular IFUApPhot (and is derived from it),
    but implements an off-scene nod to subtract background rather than a sky annulus. In particular, sky_annulus is
    not a valid keyword (as opposed to IFUApPhot). The size of the off-scene offset is arbitrary as long as it's larger
    than the scene. It will be defined in the configuration file for this strategy and perhaps on a per-instrument
    basis.

    Attributes
    ----------
    aperture_size : float, in the internal spatial unit.
        The radius of the extraction aperture.
    target_xy: list-like of format (float, float)
        X and Y center position of the aperture and sky annulus.
    dithers : 2-element list of dither dictionaries
        A list of dither offsets in internal angular coordinates. The first element is the on-scene position which
        will apply no offset (i.e. x=0,y=0). The second element will be the off-scene position and should have
        x and/or y be large enough offsets to prevent any overlap with the scene.
    on_target : list of booleans
        This list indicates which dithers are intended for background (False) and which are on target (True).
        In this case, the first is assumed to be on-scene and the 2nd to be off so this will always be [True, False].
        Because this is hard-coded into the strategy, it cannot be overriden by input configurations.
    dither_weights : list of floats
        Global weights by which each dither is multiplied by to create the weight matrices.  In this case it should
        always be [1.0, -1.0] to give each nod position equal, but opposite, weighting so that the background (negative weight)
        is fully subtracted. Because this is hard-coded into the strategy, it cannot be overriden by input configurations.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Instrument mode.
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        # Add API parameters specific to this strategy
        self.api_parameters = ["method", "units", "target_xy", "aperture_size", "reference_wavelength"]
        self.api_ignore = ["dithers"]

        IFUApPhot.__init__(self, instrument=instrument, webapp=webapp, config=config, **kwargs)

        # This strategy will use a combination of two exposures: one on the scene and one off.
        # Hardcode self.on_target accordingly.
        self.on_target = [True, False]
        self.dither_weights = [1.0, -1.0]

        # hard-code this so various sanity checks can be shared. the entire point of this strategy is to safely subtract
        # background with no interference from contaminating source flux so it would never make sense to have this be False.
        self.background_subtraction = True

    def _sanity_checks(self):
        """
        Check that the configured units are in the list of supported ones.
        """
        # make sure aperture size is > 0
        if self.aperture_size <= 0.0:
            msg = "%s error: aperture radius must be > 0.0." % self.__class__.__name__
            raise EngineInputError(value=msg)

        # check that the specified units are supported
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        For the IFUs, the conceptually easiest approach is to initially create the
        apertures and weights in cube-space, and then reshape into detector-space.
        For PSF-dependent aperture sizes, this will have to be done for each wavelength.

        Parameters
        ----------
        my_detector_signal_list : List of DetectorSignal instances
        my_detector_noise_list : List of DetectorNoise instances

        Returns
        -------
        weight_matrix_list : list of numpy arrays
            This contains the weights, a_ij, of each pixel for the strategy product.
        product_subscripts_list : List of subscripts
            For an IFU, each product represents a single image plane. Each image plane is treated
            as an image aperture photometry strategy.
            The product list has the same number of elements as there are wavelength planes.

        """

        weight_matrix_list = []
        product_subscripts_list = []

        for my_detector_signal, dither_weight in zip(my_detector_signal_list, self.dither_weights):
            cube_shape = self.get_cube_shape(my_detector_signal)
            plane_grid = self.get_plane_grid(my_detector_signal)

            weight_cube = np.zeros(cube_shape)

            # generate the source extraction region mask.
            src_region = plane_grid.circular_mask(
                self.aperture_size,
                xoff=self.target_xy[0],
                yoff=self.target_xy[1],
                use_exact=self.use_exact,
                subsampling=self.subsampling
            )

            # do some more sanity checks to make sure the target and background regions are configured as expected
            self._check_circular_aperture_limits(src_region, None, plane_grid, self.aperture_size, None)

            for i in range(cube_shape[0]):
                weight_cube[i, :, :] = dither_weight * src_region

            weight_matrix = self.on_detector(weight_cube)

            ny = weight_matrix.shape[0]
            nw = weight_matrix.shape[1]

            colsubs = np.arange(ny, dtype=np.dtype('i4'))
            product_subscripts = [(colsubs, self._fill_array(ny, i))
                                  for i in np.arange(nw)]

            weight_matrix_list.append(weight_matrix)
            product_subscripts_list.append(product_subscripts)

        return weight_matrix_list, product_subscripts_list


class IFUNodInScene(IFUApPhot):

    """
    Strategy for IFU spectroscopy that uses a nod within the scene to determine the background to subtract. This
    strategy applies to all supported IFUs. It functions like the regular IFUApPhot (and is derived from it),
    but implements a nod within the scene to subtract background rather than a sky annulus. In particular, sky_annulus is
    not a valid keyword (as opposed to IFUApPhot). The advantage of this strategy over IFUNodOffScene is that source flux
    is extracted from both nod positions rather than just the first one. The disadvantage is that the background regions
    will contain some amount of contaminating flux from sources in the scene. This strategy will be preferred in cases where
    the source of interest is much smaller than the FOV and there are few or no other sources in the scene so that contamination
    is minimized. In cases where the source is a significant fraction of the size of the scene or if there is a lot of crowding
    within the scene, IFUNodOffScene will be preferred so that contamination is avoided at the expense of doubling the amount of
    exposure time required. Default nod offsets will be defined in the configuration file for this strategy and also on a
    per-instrument basis.

    Attributes
    ----------
    aperture_size : float, in the internal spatial unit.
        The radius of the extraction aperture.
    target_xy: list-like of format (float, float)
        X and Y center position of the aperture and sky annulus.
    dithers : 2-element list of dither dictionaries
        A list of dither offsets in internal angular coordinates. Defaults are specified in the configuration file.
        The user is expected to modify the second offset to define the nod position, though it's also possible to
        modify both in special cases.
    on_target : list of booleans
        This list indicates which dithers are intended for background (False) and which are on target (True).
        In this case, this is hard-coded to be [True, True] to indicate that target flux is being collected in both
        exposures. This is then used in the accounting of on-source integration time vs. total integration time.
        Because this is hard-coded into the strategy, it cannot be overriden by input configurations.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    mode: string
        Instrument mode.
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """

    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        # Add API parameters specific to this strategy
        self.api_parameters = ["method", "units", "target_xy", "aperture_size", "dithers", "reference_wavelength"]

        IFUApPhot.__init__(self, instrument=instrument, webapp=webapp, config=config, **kwargs)

        # This strategy will use a combination of two exposures, both of which will contain target flux.
        # Hardcode self.on_target accordingly.
        self.on_target = [True, True]
        self.dither_weights = [1.0, 1.0]

        # hard-code this so various sanity checks can be shared. no point in doing this strategy unless you're subtracting
        # background.
        self.background_subtraction = True

    def _sanity_checks(self):
        """
        Check that the configured units are in the list of supported ones.
        """
        # make sure aperture size is > 0
        if self.aperture_size <= 0.0:
            msg = "%s error: aperture radius must be > 0.0." % self.__class__.__name__
            raise EngineInputError(value=msg)

        # check that the specified units are supported
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        For the IFUs, the conceptually easiest approach is to initially create the
        apertures and weights in cube-space, and then reshape into detector-space.
        For PSF-dependent aperture sizes, this will have to be done for each wavelength.

        Parameters
        ----------
        my_detector_signal_list : List of DetectorSignal instances
        my_detector_noise_list : List of DetectorNoise instances

        Returns
        -------
        weight_matrix : numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts : List of subscripts
            For an IFU, each product represents a single image plane. Each image plane is treated
            as an image aperture photometry strategy.
            The product list has the same number of elements as there are wavelength planes.

        """

        weight_matrix_list = []
        product_subscripts_list = []

        # This strategy will have two nod positions defined in self.dithers. In each case, the source extraction
        # region will be at one dither position and the background extraction region at the other. target_xy is used
        # to place the regions relative to the dither positions.

        # the cube shape and plane_grid will be the same for both
        cube_shape = self.get_cube_shape(my_detector_signal_list[0])
        plane_grid = self.get_plane_grid(my_detector_signal_list[0])
        weight_cubes = [np.zeros(cube_shape), np.zeros(cube_shape)]

        apertures = []
        apertures.append(
            plane_grid.circular_mask(
                self.aperture_size,
                xoff=self.target_xy[0] + self.dithers[0]['x'],
                yoff=self.target_xy[1] + self.dithers[0]['y'],
                use_exact=self.use_exact,
                subsampling=self.subsampling
            )
        )
        apertures.append(
            plane_grid.circular_mask(
                self.aperture_size,
                xoff=self.target_xy[0] + self.dithers[1]['x'],
                yoff=self.target_xy[1] + self.dithers[1]['y'],
                use_exact=self.use_exact,
                subsampling=self.subsampling
            )
        )
        # do some more sanity checks to make sure the target and background regions are configured as expected
        for ap in apertures:
            self._check_circular_aperture_limits(ap, None, plane_grid, self.aperture_size, None)

        src_regions = apertures
        bkg_regions = []
        bkg_regions.append(-1.0 * apertures[1])
        bkg_regions.append(-1.0 * apertures[0])

        # same apertures are used for background and source and swapped between exposures
        self.background_area = self.extraction_area

        for j in [0, 1]:
            for i in range(cube_shape[0]):
                weight_cubes[j][i, :, :] = src_regions[j] + bkg_regions[j]

            weight_matrix = self.on_detector(weight_cubes[j])
            weight_matrix_list.append(weight_matrix)

            ny = weight_matrix.shape[0]
            nw = weight_matrix.shape[1]

            colsubs = np.arange(ny, dtype=np.dtype('i4'))
            product_subscripts = [(colsubs, self._fill_array(ny, i))
                                  for i in np.arange(nw)]
            product_subscripts_list.append(product_subscripts)

        return weight_matrix_list, product_subscripts_list

    def _add_exposures(self, exposure_list, exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups):
        """
        We overload this private method here because this strategy is a special case of extracting both sky and
        source flux from each dither position.  Thus dither weights will always be positive so co-adding background
        components will need to change.  Likewise the construction of the reconstructed cubes needs to be done differently.

        Parameters
        ----------
        exposure_list: list
            A list of exposure product dictionaries
        exposure_sum: dict
            Dict of exposure products to be updated and populated
        reconstructed_signal: 3D numpy.ndarray
            Initial reconstructed signal cube
        reconstructed_noise: 3D numpy.ndarray
            Initial reconstructed noise cube
        reconstructed_saturation: 3D numpy.ndarray
            Initial reconstructed saturation cube

        Returns
        -------
        exposure_sum: dict
            Contains a sensible sum of signals (weighted by dithers) and noise (added in quadrature).
        reconstructed_signal: 3D numpy.ndarray
            Combined reconstructed signal cube
        reconstructed_noise: 3D numpy.ndarray
            Combined reconstructed noise cube
        reconstructed_saturation: 3D numpy.ndarray
            Combined reconstructed saturation cube
        """
        # for this strategy there are only two exposures, equally weighted.
        for exposure in exposure_list:
            exposure_sum['extracted_flux'] += exposure['extracted_flux']
            exposure_sum['extracted_flux_plus_bg'] += exposure['extracted_flux_plus_bg']
            exposure_sum['source_flux_in_fov'] += exposure['source_flux_in_fov']
            exposure_sum['source_flux_in_fov_plus_bg'] += exposure['source_flux_in_fov_plus_bg']
            exposure_sum['extracted_noise'] += exposure['extracted_noise'] ** 2

            # each exposure has a sky region from which the background is extracted
            exposure_sum['extracted_bg_total'] += exposure['extracted_bg_total']
            exposure_sum['extracted_bg_only'] += exposure['extracted_bg_only']

        reconstructed_grid = exposure_list[0]['reconstructed'][4]
        cube_shape = exposure_list[0]['reconstructed'][0].shape

        # Reconstruct the signal by subtracting one pointing from the other; then reconstruct the noise by
        # adding the noise from both pointings in quadrature.
        reconstructed_signal = exposure_list[0]['reconstructed'][0] - exposure_list[1]['reconstructed'][0]
        reconstructed_noise = np.zeros(cube_shape)
        reconstructed_noise += exposure_list[0]['reconstructed'][1] ** 2
        reconstructed_noise += exposure_list[1]['reconstructed'][1] ** 2

        sat1 = exposure_list[0]['reconstructed'][2]
        sat2 = exposure_list[1]['reconstructed'][2]
        reconstructed_saturation = np.maximum(sat1, sat2)
        reconstructed_groups = np.minimum(exposure_list[0]['reconstructed'][3],exposure_list[1]['reconstructed'][3])

        return exposure_sum, reconstructed_signal, reconstructed_noise, reconstructed_saturation, reconstructed_groups


class SOSS(Strategy):
    """
    Strategy for extracting spectra from a NIRISS SOSS observation.

    Attributes
    ----------
    order: int
        Which of the orders of the spectrum to extract (1, 2, or 3 for NIRISS)
    reference_wavelength: float (in PANDEIA_WAVEUNITS)
        Wavelength to use for determining scalar outputs
    background_subtraction: bool
        Toggle whether background should be estimated and subtracted from spectrum

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    webapp: bool
        Toggle strict API checking
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """
    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["method", "order", "reference_wavelength", "background_subtraction"]

        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        disperser = instrument.instrument['disperser']
        # we're not doing background subtraction yet
        self.background_area = None
        # the shape of the extraction mask is complicated and may not even be constant spatial at some point.
        # right now we're only using 35 pixel wide masks so we'll punt and hardcode that here for not.
        self.extraction_area = 35.0

    def _sanity_checks(self):
        """
        Sanity checking for SOSS configuration.
        """
        # if we're subtracting background, we use all pixels not included in configured masks
        # and weight those pixels accordingly.
        if self.background_subtraction:
            msg = "Background subtraction not yet implemented for SOSS."
            self.warnings["strategy_unsupported_soss_bknd"] = msg

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        This private method creates the weight matrix, a_ij, used for the strategy sum. It gets overridden
        in each strategy. In this case it creates the weight matrix from extraction masks defined by the
        instrument configuration.

        Parameters
        ----------
        my_detector_signal_list: list of DetectorSignal or CombinedSignal instances
        my_detector_noise_list: list of DetectorNoise instances

        Returns
        -------
        weight_matrix: numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts: List of subscripts
            A single strategy can return multiple products. The subscripts list the pixels to be summed
            over for each product.
        """
        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers or aperture slices is not yet supported for SOSS'
            raise UnsupportedError(value=message)

        signal = my_detector_signal_list[0]
        inst = signal.current_instrument

        weight_matrix = inst.get_extraction_mask(order=self.order)

        # the detector signal will be larger than the mask images because of how slitless rates are calculated.
        # need to pad/trim the masks to match.  SOSS is dispersed along the Y axis so that axis will be extended
        # by half a FOV on each end.
        y_excess = signal.spatial_grid.ny / 2.0
        ly = int(np.floor(y_excess))
        uy = int(np.ceil(y_excess))
        x_excess = (signal.rate.shape[1] - weight_matrix.shape[1]) / 2.0
        lx = int(np.floor(x_excess))
        ux = int(np.ceil(x_excess))

        if x_excess < 0.0:
            weight_matrix = weight_matrix[:, lx:-ux]
            weight_matrix = np.pad(weight_matrix, ([ly, uy], [0, 0]))
        else:
            weight_matrix = np.pad(weight_matrix, ([ly, uy], [lx, ux]), mode='constant')

        # get the detector pixel offset from the first wavelength in the first order
        wave_off_pix = signal.detector_pixel_list[self.order-1][0] - signal.detector_pixel_list[0][0]
        wave_pix = signal.wave_pix_dict[self.order]
        nw = len(wave_pix)

        nx = weight_matrix.shape[1]
        rowsubs = np.arange(nx, dtype=np.dtype('i4'))
        product_subscripts = [(self._fill_array(nx, i), rowsubs) for i in np.arange(nw) + ly + wave_off_pix]

        return weight_matrix, product_subscripts

class TAPhot(Strategy):

    """
    Photometry strategy for JWST target acquisition modes.

    Attributes
    ----------
    aperture_size : integer, in pixels
        The width of a square aperture.
    target_xy : list of 2 numbers
        Distance to offset the target position.

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    webapp: bool
        Toggle strict API checking
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """
    def __init__(self, instrument, webapp=False, config={}, **kwargs):
        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["background_subtraction", "target_xy",
                                   "units"]
        self.api_ignore = ["method", "aperture_size", "ta_offset"]
        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        # If there is an offset (e.g., for coronagraphic TA), implement that as a dither here
        self.dithers = [{'x': self.ta_offset[0], 'y': self.ta_offset[1]}]

    def _sanity_checks(self):
        """
        Sanity checking for TAPhot configuration.
        """

        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)

    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        This private method creates the weight matrix, a_ij, used for the strategy sum. It gets overridden
        in each strategy. In this case it creates the weight matrix from extraction masks defined by the
        instrument configuration.

        Parameters
        ----------
        my_detector_signal_list: list of DetectorSignal or CombinedSignal instances
        my_detector_noise_list: list of DetectorNoise instances

        Returns
        -------
        weight_matrix: numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts: List of subscripts
            A single strategy can return multiple products. The subscripts list the pixels to be summed
            over for each product.
        """
        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for target acquisition is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]

        aperture = self.aperture_size
        aper_area = aperture ** 2
        aper_area_pix = aper_area / (my_detector_signal.grid.xsamp * my_detector_signal.grid.ysamp)
        self.extraction_area = aper_area_pix
        # For now, we do not have a background subtraction
        self.background_area = 0.0
        # generate the rectangular source extraction region mask. Make sure a dither is taken into account.
        # This is important for coronagraphic TAs.
        weight_matrix = my_detector_signal.grid.rectangular_mask(
            width = aperture,
            height = aperture,
            xoff=self.target_xy[0]+self.ta_offset[0],
            yoff=self.target_xy[1]+self.ta_offset[1]
        )
        # the src_region mask values are the fraction of the pixel subtended by the aperture so
        # in the range 0.0 to 1.0 inclusive.  the effective number of pixels in the aperture is
        # then the sum of this mask.
        n_aper = weight_matrix.sum()

        # do some more sanity checks to make sure the target and background regions are configured as expected
        #self._check_circular_aperture_limits(src_region, sky_subs, my_detector_signal.grid, aperture, annulus)

        # We can just use one of the directions to calculate the product subscripts (they have to be the same)
        product_subscript = weight_matrix.nonzero()

        # The subscripts returned from a matrix contain a redundant dimension. This removes it.
        # Note that this is not how matrix indexing is formally constructed, but it enforces a rule
        # that product subscripts should always be tuples or regular ndarrays.
        product_subscript = (np.array(product_subscript[0]).flatten(), np.array(product_subscript[1]).flatten())

        return weight_matrix, [product_subscript]

class TACentroid(Strategy):

    """
    Centroid strategy for JWST target acquisition. Note that, while the on-board algorithm typically
    subtracts the background, this does adds minimal noise to the centroid since the background level is eliminated
    in the weighted average of the centroid (in the ETC formulation anyway). We still report the background area.


    Attributes
    ----------
    aperture_size : integer, in pixels
        The width of a square aperture.
    target_xy : list of 2 numbers
        Distance to offset the target position.
    axis : string, "x" or "y"
        Which direction the centroid is calculated

    Parameters
    ----------
    instrument: string
        The instrument used for the strategy.
    webapp: bool
        Toggle strict API checking
    config: dict
        Strategy configuration parameters in the form of a engine API dict
    **kwargs: list of keyword/value pairs
        Additional strategy configuration parameters
    """
    def __init__(self, instrument, webapp=False, config={}, **kwargs):

        if not hasattr(self, "api_parameters"):
            # Add the API parameters specific to this strategy
            self.api_parameters = ["background_subtraction", "target_xy",
                                   "units", "axis"]

        self.api_ignore = ['method', "aperture_size","ta_offset"]

        Strategy.__init__(self, instrument=instrument, config=config, webapp=webapp, **kwargs)

        # If there is an offset (e.g., for coronagraphic TA), implement that as a dither here
        self.dithers = [{'x': self.ta_offset[0], 'y': self.ta_offset[1]}]

    def _sanity_checks(self):
        """
        Sanity checking for TAPhot configuration.
        """
        if self.units not in self.permitted_units:
            msg = "Unsupported unit type, %s, in strategy %s" % (self.units, self.__class__.__name__)
            raise EngineInputError(value=msg)


    def _create_weight_matrix(self, my_detector_signal_list, my_detector_noise_list):
        """
        This private method creates the weight matrix, a_ij, used for the strategy sum. It gets overridden
        in each strategy. In this case it creates the weight matrix from extraction masks defined by the
        instrument configuration.

        Parameters
        ----------
        my_detector_signal_list: list of DetectorSignal or CombinedSignal instances
        my_detector_noise_list: list of DetectorNoise instances

        Returns
        -------
        weight_matrix: numpy array
            This contains the weights, a_ij, of each pixel for the strategy matrix product.
        product_subscripts: List of subscripts
            A single strategy can return multiple products. The subscripts list the pixels to be summed
            over for each product.
        """
        if len(my_detector_signal_list) > 1:
            message = 'Multiple dithers for target acquisition is not yet supported'
            raise UnsupportedError(value=message)

        my_detector_signal = my_detector_signal_list[0]
        aperture = self.aperture_size
        aper_area = aperture ** 2
        aper_area_pix = aper_area / (my_detector_signal.grid.xsamp * my_detector_signal.grid.ysamp)
        self.extraction_area = aper_area_pix

        # pass target_xy to Signal.grid.dist() to offset the target position
        dist_x,dist_y = my_detector_signal.grid.dist_xy(xcen=self.target_xy[0], ycen=self.target_xy[1])

        # generate the rectangular source extraction region mask. Make sure a dither is taken into account.
        # This is important for coronagraphic TAs.
        src_region = my_detector_signal.grid.rectangular_mask(
            width = aperture,
            height = aperture,
            xoff=self.target_xy[0]+self.ta_offset[0],
            yoff=self.target_xy[1]+self.ta_offset[1]
        )

        # This is an approximation. A Taylor expansion shows that the weights should be:
        # w_x_i ~ (dist_x_i*sum(F_i) - sum(d_x_i * F_i))/sum(F_i)^2. So if we assume that the centroid
        # is symmetric around 0 (sum*(x_i * F_i)=0), then we recover the fully linear formula below.
        weight_matrix_x = dist_x*src_region/np.sum(my_detector_signal.rate*src_region)
        weight_matrix_y = dist_y*src_region/np.sum(my_detector_signal.rate*src_region)

        self.background_area = None

        # We can just use one of the directions to calculate the product subscripts (they have to be the same)
        product_subscript = weight_matrix_x.nonzero()

        # The subscripts returned from a matrix contain a redundant dimension. This removes it.
        # Note that this is not how matrix indexing is formally constructed, but it enforces a rule
        # that product subscripts should always be tuples or regular ndarrays.
        product_subscript = (np.array(product_subscript[0]).flatten(), np.array(product_subscript[1]).flatten())

        if self.axis == "x":
            return weight_matrix_x, [product_subscript]
        elif self.axis == "y":
            return weight_matrix_y, [product_subscript]


def StrategyFactory(instrument, webapp=False, config={}, **kwargs):
    """
    Function to take an Instrument instance and configuration data and build/return an appropriately
    configured instance of the desired or default Strategy class.

    Parameters
    ----------
    instrument: Instrument instance
        Need an Instrument instance to find out about instrument-specific strategy defaults/parameters.
    webapp: bool
        Switch to toggle strict API checking
    config: dict
        Configuration data in engine API dict format
    **kwargs: keyword/value pairs
        Additional configuration data
    """
    method = None
    all_config = merge_data(config, dict(**kwargs))
    mode = instrument.mode
    types = recursive_subclasses(Strategy)
    methods = [t.__name__.lower() for t in types]
    type_map = dict(list(zip(methods, types)))

    try:
        # first pop the default method out of the instrument
        if mode in instrument.strategy_config:
            method = instrument.strategy_config[mode]['method']
        else:
            method = instrument.strategy_config['method']
    except KeyError as e:
        msg = "Strategy configuration for mode=%s missing from %s configuration. (%s)" % (mode, instrument.__name__, e)
        raise EngineInputError(value=msg)

    # now pop the method out of the passed config, if it's there.
    if 'method' in all_config:
        method = all_config.pop('method')

    # raise exception if we haven't figured out method by now
    if method is None:
        msg = "No Strategy specified in either the input configuration or instrument defaults."
        raise EngineInputError(value=msg)

    # now make sure method is supported and build the appropriate instance if so
    if method not in methods:
        msg = "Unsupported or not yet implemented strategy: %s" % method
        raise EngineInputError(value=msg)
    else:
        cls = type_map[method](instrument=instrument, webapp=webapp, config=config, **kwargs)
        return cls
