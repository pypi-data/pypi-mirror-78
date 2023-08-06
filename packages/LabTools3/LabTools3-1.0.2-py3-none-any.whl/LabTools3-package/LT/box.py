"""
The LT box contains an assortment of plotting, histogramming and fitting routines
used for data analysis. The plotting routines have been imported from the :ref:`plotting`
module and the fitting routines have been imported from the :ref:`LT_Fit`. For detailed
information about these functions check the :ref:`plotting` and the the :ref:`LT_Fit` documentation.

Normally all you should need to do is import the `box`_ and you have a *box of tools*.

Example::

    >>> import LT.box as B

-------------------------------------------

Imported functions:

   From LT.plotting:
        * :meth:`~LT.plotting.plot_exp`: plot experimental data points with or without error bar  
        * :meth:`~LT.plotting.plot_line`: plot a line through a set of data points
        * :meth:`~LT.plotting.plot_spline`: plot a spline curve through a set of data points
        
        * dplot_exp: (:meth:`~LT.plotting.datafile_plot_exp`) is like plot_exp but accesses the datafile variables directly via their names
        * dplot_line: (:meth:`~LT.plotting.datafile_plot_theory`) like plot_line for datafile variables
        * dplot_spline: (:meth:`~LT.plotting.datafile_spline_plot_theory`) like plot_spline for datafiles variables

   From LT_Fit:
        * :class:`~LT_Fit.linear_fit.linefit`: fit a straight line through a set of data points
        * :class:`~LT_Fit.linear_fit.polyfit`: fit a polynomial
        * :class:`~LT_Fit.linear_fit.gen_linfit`: general linear fit
        * :class:`~LT_Fit.gen_fit.genfit`: general, non-linear fit
        
-------------------------------------------

"""

import pdb
import numpy as np
import matplotlib.pyplot as pl
import LT

# include the version with parameters
from .pdatafile import pdfile

from .plotting import plot_exp
from .plotting import plot_line
from .plotting import plot_spline

from .plotting import datafile_plot_exp as dplot_exp

from .plotting import datafile_plot_theory as dplot_line
from .plotting import datafile_spline_plot_theory as dplot_spline

from LT_Fit.linear_fit import linefit
from LT_Fit.linear_fit import polyfit
from LT_Fit.linear_fit import gen_linfit

from LT_Fit.parameters import *

# general fitting
from LT_Fit.gen_fit import genfit

# this is done for general linear fitting

# for MCA spectra
from . import MCA as mcsp

def get_file(file, **kwargs):
    """ 
    Assume that  B is  the name of LT.box.
    
    Open and read the file::
    
    >>> md = B.get_file( 'file.data' )

    """
    return pdfile(file, **kwargs)

def get_data(D, var):
    """
    
    Assume that  B is  the name of LT.box.
    
    Get all the values of variable 'my_var' as a :func:`numpy.array`::
    
    >>> mv = B.get_data(md, 'my_var')
    
    """
    return np.array(D.get_data(var))

# window cuts
def in_between(xmin, xmax, val):
    return ( (xmin <= val) and (val <= xmax) )

in_window = np.vectorize(in_between)

# select data within a window
def select_data(xmin, a, xmax):
    """
    
    Assume that  B is  the name of LT.box.
    
    Find which values of an array A lie between 0.8 and 1.2
    
    >>> iw = B.select_data( 0.8, A, 1.2)

    iw now is an array of indices, A[iw] is an array with values
    between 0.8 and 1.2

    in general: B.select_data(xmin, a, xmax)
    
    """
    return np.where( in_window(xmin, xmax, a) )

# histogram class exception
class histoError(Exception):
    def __init__(self, comment, value):
        self.comment = comment
        self.value = value
    def __str__(self):
        return self.comment + repr(self.value)

# histogram class
#
# fitting of a gaussian on a quadratic back ground is built in
# 
class histo:
    """
    
    Define a histogram based on the np.histogram class.

    The various ways of defining one are:

       *  If *a* is a 1D ( :func:`numpy.array`) containing the data to be histogrammed
    
          >>> h = histo( a )

       *  If *his* is the output of the :func:`numpy.histogram` function
          
          >>> h = histo(histogram = his) 

       *  If ``bc`` is a 1D array with bin center values, and ``bcont``
          contains bin content values then:

          >>> h = histo(bin_center = bc, bin_content = bcont)
             
       *  A filename for a stored histogram is given

          >>> h = histo(filename), where filename contains the pdatafile

          Usually the result of a histo.save operation
          
    Important keywords:
        
    ============   =====================================================
    Keyword        Meaning
    ============   ===================================================== 
    values         Array of values to be histogrammed (:func:`numpy.array`)
    range          Lower and upper limits  of binning ( e.g. ``range = (10.,20.)`` )
    bins           Number of bins
    histogram      Result of :func:`numpy.histogram` function
    bin_error      Array of errors for each bin content (:func:`numpy.array`)
    bin_center     Array of bin-center values (:func:`numpy.array`)
    bin_content    Array of bin-content values (:func:`numpy.array`)
    file           Load data from file
    window         Set a window (a zoom window)
    title          Set the title
    xlabel         Set the x-label
    ylabel         Set the y-label
    ============   =====================================================
    
    Additional keyword arguments are passed to the :func:`numpy.histogram` function
    
    """
    def __init__(self,\
                 values = None, \
                 range = None, \
                 bins = None, \
                 histogram = None, \
                 bin_error = None, \
                 bin_center = None, \
                 bin_content = None, \
                 file = None, \
                 window = None, \
                 title = 'my histogram', \
                 xlabel = 'x-bin', \
                 ylabel = 'content', \
                 **kwargs):
        self.res = None
        self.fit_dict = {}
        # initialize fitting
        self.b0 = Parameter(0., 'b0')
        self.b1 = Parameter(0., 'b1')
        self.b2 = Parameter(0., 'b2')
        self.mean =  Parameter(1.,'mean')
        self.sigma =  Parameter(1., 'sigma')
        self.A = Parameter(1., 'A') 
        # create a dictionary for vairable fitting
        self.fit_par = {
        "b0" : self.b0, \
        "b1" : self.b1, \
        "b2" : self.b2, \
        "mean" :  self.mean, \
        "sigma":  self.sigma, \
        "A" : self.A}
        # setup fitting list
        self.set_fit_list()
        self.window_set = False
        if values is not None:
            # values have been given for filling
            if (range is None) and (bins is None):
                self.fill(values, **kwargs)
            elif (range is not None) and (bins is None):
                self.fill(values, range = range, **kwargs)
            elif (range is None) and (bins is not None):
                self.fill(values, bins = bins, **kwargs)
            else:
                self.fill(values, bins = bins, range = range, **kwargs)
        elif file is not None:
            # create from file
            self.load(file)
            return
        elif histogram is not None:
            # the output of the numpy histogram function has been given
            self.res = histogram
        elif (bin_center is not None) and (bin_content is not None):
            # the histogram content is given direectly
            self.bin_center = np.copy(bin_center)
            self.bin_content = np.copy(bin_content)
            self.bin_width = np.diff(self.bin_center)[0]
            self.__get_histogram()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.__setup_bins(error = bin_error)
        self.nbins = self.bin_center.shape[0]
        if window is None:
            self.clear_window()
        else:
            self.set_window( xmin = window[0], xmax = window[1])
            
    def save_index(self, i):
        # make sure i is always within the allowed range
        return min(len(self.bin_content)-1, i)

    def fill(self, y, add = False, **kwargs):
        """
        
        Fill the histogram with the values stored in the :func:`numpy.array` y.

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        add            if True add the results to the existing content
        ============   =====================================================

        Additional keyword arguments are passed to the :func:`numpy.histogram` function

        """
        if not add:
            # a new filling
            try:
                self.res = np.histogram(y, new = None, **kwargs)
            except:
                self.res = np.histogram(y, **kwargs)
            self.__setup_bins(error = None)
        else:
            # the bins have already been defined continue
            # to accumulate statistics
            if self.res is None:
                print("no binning information: try fill with add = False ")
                return
            try:
                res = np.histogram(y, new = True, bins = self.res[1], **kwargs)
            except:
                res = np.histogram(y, bins = self.res[1], **kwargs)
            # add the new bin content to the old one
            self.res = (self.res[0] + res[0], self.res[1])
            # update the histogram information
            self.__setup_bins(error = None)
        # end of fill

    def clear(self):
        """
        
        Set the content and errors to 0.
        
        """
        self.bin_content = np.zeros_like(self.bin_content)
        self.bin_error = np.zeros_like(self.bin_content)
        self.res = (np.zeros_like(self.res[0]), self.res[1])
        self.__prepare_histo_plot()

    def sum(self, xmin = None, xmax = None):
        """
        
        Return the sum of all bins. If the limits are given, calculate the sum of all bins between the bins that contain
        the values xmin and xmax.

        Example::

           >>> s0 = h.sum() # add all bins
           >>> s1 = h.sum(0.5, 1.1) # add the bins between 0.5 and 1.1
           >>> s2 = h.sum(xmin = 0.5, xmax = 1.1) # add the bins between 0.5 and 1.1

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        xmin           lower limit of sum of bin content
        xmax           upper limit of sum
        ============   =====================================================

        The errors are also calculated.
        
        """
        if (xmin is None) and (xmax is None):
            sum = self.bin_content.sum()
            sum_err = np.sqrt( (self.bin_error**2).sum())
        elif (xmin is None):
            sel = (self.bin_center <= xmax)
            sum = self.bin_content[sel].sum()
            sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
        elif (xmax is None):
            sel = (xmin <= self.bin_center)
            sum = (self.bin_content[sel]).sum()
            sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
        else:
            sel = (xmin <= self.bin_center) & (self.bin_center <= xmax)
            sum = (self.bin_content[sel]).sum()
            sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
        return (sum, sum_err)

    def copy(self):
        """
        
        Create a copy of the histogram::

           >>>hc = h.copy()

        Only the histogram values are copied, no lables and titles etc.
        """
        res = (np.copy(self.res[0]), np.copy(self.res[1]) )
        err = np.copy( self.bin_error )
        return histo(histogram = res, bin_error = err)

    def rebin(self, n, scale = False):
        """
        
        rebin the histogram by a factor n::
        
           >>>hc = h.rebin(2)
           
        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        scale          True: the original bin number is not a multiple of n 
                             and the last bin content will be scaled
        ============   =====================================================
        

        """
        divisible = (np.mod(self.bin_center.shape[0], n) != 0)
        # change bin content
        bco_sl, mean_sl, sl, fact_sl =  self.__rebin_array(self.bin_content, n)
        be2_sl, mean_sl, sl, fact_sl =  self.__rebin_array(self.bin_error**2, n)
        sum_sl, bc_sl, sl, fact_sl =  self.__rebin_array(self.bin_center, n)
        # adjust the bin center of last bin if necessary
        if not divisible:
            bc_sl[-1] = bc_sl[-2]+ np.diff(bc_sl)[0]
        if scale:
            bco_sl *= fact_sl
        # store new histogram parameters and update histogram
        self.bin_content = np.copy(bco_sl)
        self.bin_error = np.copy(np.sqrt(be2_sl))
        self.bin_center = np.copy(bc_sl)
        self.bin_width = np.diff(self.bin_center)[0]
        self.__get_histogram()
        self.bins = self.res[1]
        # prepare for plotting
        self.__prepare_histo_plot()
        
        
    def plot(self,filled = 'True', ymin = 0.,  axes = None, ignore_zeros = False,  **kwargs):
        """

        Plot the histogram content:

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        filled         if True draw a filled histogram
        ymin           lower limit where fill starts (horizontal line)
        ignore_zeros   do not plot channels with  bin content 0 (default = False)
        ============   =====================================================

        """
        if axes is None:
            axes = pl.gca()
        if ymin is None:
            ymin = self.cont_min
        # prepare histo plot if axes have changed
        self.__prepare_histo_plot()
        if filled :
            xx = self.xpl
            yy = self.ypl
            if ignore_zeros:
                sel = yy != 0.
            else:
                sel = np.ones_like(yy).astype('bool')            
            axes.fill_between( xx[sel], yy[sel], y2=ymin, **kwargs)
        else:
            xx = np.concatenate([self.xpl[:1], self.xpl, self.xpl[-1:]])
            yy = np.concatenate([np.array([ymin]), self.ypl, np.array([ymin])])
            if ignore_zeros:
                sel = yy != 0.
            else:
                sel = np.ones_like(yy).astype('bool')
            axes.plot(xx[sel],yy[sel], **kwargs)
        if self.window_set:
            axes.set_xlim( (self.win_min, self.win_max) )
            # prepare y scale
            sel = (self.win_min <= self.xpl) & (self.xpl <= self.win_max)
            ymin = self.ypl[sel].min()
            ymax = self.ypl[sel].max()
            axes.set_ylim( (ymin, ymax) )
        axes.set_xlabel(self.xlabel)
        axes.set_ylabel(self.ylabel)
        axes.set_title(self.title)

    def set_window(self, xmin =  None, xmax = None):
        """

        Define a window into the histogram. This is similar to a zoom or a
        region of interest (ROI)

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        xmin           lower limit for plotting or fitting
        xmax           upper limit
        ============   =====================================================

        """
        # a call to __setup_bins MUST preced usage of this call
        self.window_set = True
        if xmin is None:
            self.win_min = self.xpl.min()
        else:
            self.win_min = xmin
        if xmax is None:
            self.win_max = self.xpl.max()
        else:
            self.win_max = xmax
        return
    def set_window_view(self):
        """
        
        Like set_windows but uses the current display limits. This is only
        useful if the histogram has been plotted.
        
        """
        xmin,xmax = pl.xlim()
        self.set_window(xmin,xmax)
        
    def clear_window(self):
        """

        Reset (Clear) the defined window

        """
        # a call to __setup_bins MUST preced usage of this call
        self.window_set = False
        self.win_min = self.xpl.min()
        self.win_max = self.xpl.max()

    def plot_exp(self, ignore_zeros = False, **kwargs):
        """

        Plot histogram content and errors like experimental data.
        
        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        ignore_zeros   do not plot channels with  bin content 0 (default = False)
        ============   =====================================================
        

        """
        xx = self.bin_center
        yy = self.bin_content
        dyy = self.bin_error
        if ignore_zeros:
            sel = yy != 0.
        else:
            sel = np.ones_like(yy).astype('bool')            
        
        plot_exp(xx[sel], yy[sel], dyy[sel],\
                 x_label = self.xlabel, \
                 y_label = self.ylabel, \
                 plot_title = self.title, \
                 **kwargs)

    def save(self, filename = 'histo.data'):
        """

        Save the histogram in :mod:`~LT.pdatafile` format

        """
        of = open(filename, 'w')
        of.write('#\ title = %s\n'%(self.title))
        of.write('#\ xlabel = %s\n'%(self.xlabel))
        of.write('#\ ylabel = %s\n'%(self.ylabel))
        # now write the current fit parameters
        for key in self.fit_par:
            name = key + ' = %r'
            err_name = '; d_'+name
            fmt = '#\ '+name+err_name+'\n'
            l =  fmt%( self.fit_par[key].value, self.fit_par[key].err)
            of.write(l)
        of.write('# \n')
        of.write('#! bin_center[f, 0]/ bin_content[f,1]/ bin_error[f, 2]/ \n')
        for i,bc in enumerate(self.bin_center):
            of.write ("%r %r %r \n"%( bc, self.bin_content[i], self.bin_error[i])  )
        of.close()

    def load(self, file='histo.data'):
        """
        
        read the histogram data from :mod:`~LT.pdatafile`

        If the file does not result from a save function make sure that
        all the necessary data are present.
        
        """
        data = get_file(file)
        # first the data 
        self.bin_center = np.array(data.get_data('bin_center') )
        self.bin_content = np.array(data.get_data('bin_content') )
        self.bin_error =  np.array(data.get_data('bin_error') )
        # now the parameters
        self.title = data.par.get_value('title', str)
        self.xlabel = data.par.get_value('xlabel', str)
        self.ylabel = data.par.get_value('ylabel', str)
        # now the fit parameters
        for key in self.fit_par:
            name = key
            dname = 'd_'+key
            self.fit_par[key].set(data.par.get_value(name, float), \
                                      err = data.par.get_value(dname, float))
        self.bin_width = np.diff(self.bin_center)[0]
        self.__get_histogram()
        self.bins = self.res[1]
        self.__prepare_histo_plot()
        # plot the fit
        x = np.linspace(self.bins[0], self.bins[-1:][0], 100)
        self.fit_dict['xpl'] = x
        self.fit_dict['ypl'] = self.fit_func(x)

    def find_bin(self, x):
        """
        
        Find the bin that would contain the value x

        """
        # self.bins contains the bin edged
        if (x < self.bins[0]):
            print('searched value {0} < lowest bin = {1} '.format(x, self.bins[0]))  
            return 0
        elif (x > self.bins[-1:][0]):
            print('searched value {0} > highest bin = {1} '.format(x, self.bins[-1:][0]))
            return len(self.bins) - 1
        elif (x == self.bins[0]):
            return 0
        else:
            return (np.searchsorted(self.bins, x) - 1 )

    def set_fit_list(self, fit = [ 'A', 'mean', 'sigma'] ):
        """

        Define which parameters are to be fitted.

        The default list is ::
        
           fit = [ 'A', 'mean', 'sigma']

        to use all parameters::

           h.set_fit_list( fit = [ 'A', 'mean', 'sigma', 'b0', 'b1, 'b2'])
           
        """
        if fit==[]:
            # empty list show possibilities
            print('possible fit parameters:')
            print(list(self.fit_par.keys()))
            return
        self.fit_names = fit
        self.fit_list = []
        for key in self.fit_names:
            try:
                curr_par_name = self.fit_par[key]
            except:
                print('cannot use parameter :', key, ' (does not exist ?!)')
                continue
            self.fit_list.append(curr_par_name)
        # end of fitting list

    def fit(self, xmin = None, xmax = None, init = True, ignore_zeros = True):
        """
        
        Fit a gaussian on a quadratic background. You can also just
        fit a background or just a gaussian. All this is controlled by which
        parameters you want to fit. Another important part of non-linear
        fitting is that you need to provide reasonable guesses for the fit
        parameters. The parameters in :class:`~LT.box.histo` are not just
        numbers but objects with their own properties and functions (see
        :class:`~LT_Fit.parameters.Parameter` ).  The full fit function is as
        follows:
    
        :math:`$ f(x) = b_0 + b_1x + b_2x^2  + A exp(-(x - \mu)^2/\sigma^2)$` 

        The (:class:`LT.box.histo`) parameters are:

        =================== ================================================
        Parameter           Histo Class Member
        =================== ================================================
        :math:`$b_o $`      b0
        :math:`$b_1 $`      b1
        :math:`$b_2 $`      b2
        :math:`$A $`        A
        :math:`$\mu  $`     mean
        :math:`$\sigma  $`  sigma
        =================== ================================================

        Which parameters are fitted is defined in :meth:`~LT.box.histo.set_fit_list`
        
        Keyword arguments are:

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================          
        xmin           lower fit limit        
        xmax           upper fit limit
        init           True/False (default = True) estimate initial fit parameters automatically
        ignore_zeros   True/False (default = True) ignore channels with bin content zero
        ============   =====================================================
        
                 

        """
        # is there a range given, or is a window set
        sel_all = np.ones_like(self.bin_center, dtype = 'bool')
        if init:
            self.init_gauss(xmin, xmax)
        if (xmin is None) and (xmax is None):
            # check if a window is set
            if self.window_set:
                # if so use the set window limits
                sel = (self.win_min <= self.bin_center) & (self.bin_center <= self.win_max)
                self.fit_indx, = np.where ( sel )
            else:
                # if not use all data
                self.fit_indx, = np.where(sel_all)
        elif (xmin is None):
            sel = (self.bin_center <= xmax)
            if self.window_set:
                # if so check which is smaller
                sel_w = (self.bin_center <= self.win_max) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel) 
        elif (xmax is None):
            sel = (xmin <= self.bin_center)
            if self.window_set:
                # if so check which is larger
                sel_w = (self.win_min <= self.bin_center) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        else:
            sel = (xmin <= self.bin_center) & ( self.bin_center <= xmax)
            if self.window_set:
                # if so check the set window limits
                sel_w = (self.win_min <= self.bin_center) & ( self.bin_center <= self.win_max) & sel
                # use the tighter limits
                self.fit_indx, = np.where(sel_w) 
            else:
                self.fit_indx, = np.where(sel)
        # set minimal error to 1
        is_zero = np.where(self.bin_error == 0.)
        self.bin_error[is_zero] = 1.
        # do the fit
        if ignore_zeros:
            # ignore bins with content of 0
            sel = self.bin_content[self.fit_indx] != 0.
            bin_content = self.bin_content[self.fit_indx][sel]
            bin_center = self.bin_center[self.fit_indx][sel]
            bin_error = self.bin_error[self.fit_indx][sel]
        else:
            bin_content = self.bin_content[self.fit_indx]
            bin_center = self.bin_center[self.fit_indx]
            bin_error = self.bin_error[self.fit_indx]
            
        # do the fit using the new version
        self.F = genfit( self.fit_func, self.fit_list, \
                                   x = bin_center, \
                                   y = bin_content, \
                                   y_err = bin_error, \
                                   full_output=1, \
                                   ftol = 0.001, \
                                   print_results = False)
        self.fit_dict = self.F.stat
        self.fit_dict['xpl'] = self.F.xpl
        self.fit_dict['ypl'] = self.F.ypl
        # get the covariance matrix
        if self.fit_dict == {}:
            print("Problem with fit: no result, check parameters !")
            return
        self.cov = self.F.covar
        # print the result
        print('----------------------------------------------------------------------')
        print('Fit results:')
        for key in self.fit_names:
            print(key, ' = ', self.fit_par[key].value,' +/- ', self.fit_par[key].err)
        print('Chi square = ', self.F.chi2)
        print('Chi sq./DoF = ', self.F.chi2_red)
        print('----------------------------------------------------------------------')
        self.calc_fit_plot()

    def fit_view(self, init = True):
        """
        
        Fit histogram using the current display limits as fit range. This is only
        useful if the histogram has been plotted.
        
        """
        xmin,xmax = pl.xlim()
        self.fit(xmin,xmax, init = init)
        

    def init_gauss(self, xmin = None, xmax = None):
        """
        
        Calculate the initial parameter guess for a gaussian. These parameters
        can them be used in the call to :class:`~LT.box.histo.fit`

        """
        # is there a range given, or is a window set
        sel_all = np.ones_like(self.bin_center, dtype = 'bool')
        if (xmin is None) and (xmax is None):
            # check if a window is set
            if self.window_set:
                # if so use the set window limits
                sel = (self.win_min <= self.bin_center) & (self.bin_center <= self.win_max)
                self.fit_indx, = np.where ( sel )
            else:
                # if not use all data
                self.fit_indx, = np.where(sel_all)
        elif (xmin is None):
            sel = (self.bin_center <= xmax)
            if self.window_set:
                # if so check which is smaller
                sel_w = (self.bin_center <= self.win_max) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel) 
        elif (xmax is None):
            sel = (xmin <= self.bin_center)
            if self.window_set:
                # if so check which is larger
                sel_w = (self.win_min <= self.bin_center) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        else:
            sel = (xmin <= self.bin_center) & ( self.bin_center <= xmax)
            if self.window_set:
                # if so check the set window limits
                sel_w = (self.win_min <= self.bin_center) & ( self.bin_center <= self.win_max) & sel
                # use the tighter limits
                self.fit_indx, = np.where(sel_w) 
            else:
                self.fit_indx, = np.where(sel)
        # set minimal error to 1
        is_zero = np.where(self.bin_error == 0.)
        self.bin_error[is_zero] = 1.
        # do the fit
        bin_content = self.bin_content[self.fit_indx]
        bin_center = self.bin_center[self.fit_indx]
        # bin_error = self.bin_error[self.fit_indx]
        # calculate initial parameters
        mean = np.sum(bin_center*bin_content)/bin_content.sum()
        sigma = np.sqrt( np.sum(bin_content*(bin_center - mean)**2)/bin_content.sum())
        A = bin_content.max()
        # store the parameters
        self.A.set(A)
        self.mean.set(mean)
        self.sigma.set(sigma)
        
    def calc_fit_plot(self):
        # plot the fit
        imax = min(len(self.bins)-1, self.fit_indx[-1:][0] + 1)
        xmin = self.bins[self.fit_indx][0]
        xmax = self.bins[imax]
        x = np.linspace(xmin, xmax, 100)
        self.fit_dict['xpl'] = x
        self.fit_dict['ypl'] = self.fit_func(x)

    def plot_fit(self, color = 'r', axes = None, **kwargs):
        """

        Plot the fitted curve

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        color          color of the fitted line
        ============   =====================================================

        """
        if axes is None:
            axes = pl.gca()
        if self.fit_dict == {}:
            print('no fit, nothing to plot !')
        else:
            plot_line(self.fit_dict['xpl'], self.fit_dict['ypl'], color = color, axes = axes, **kwargs)
            if self.window_set:
                axes.set_xlim( (self.win_min, self.win_max) )

                
    def fit_func(self, x):
        """
        
        The function fitted to the histogram data

        """
        fit_val = (self.b2()*x + self.b1())*x + self.b0() + \
            self.A()*np.exp(-0.5*((x-self.mean())/self.sigma() )**2)
        return fit_val
    def apply_calibration(self, cal):
        """
        
        apply x-axis calibration, new axis values are cal(xaxis)
        
        """
        self.bin_center = cal(self.bin_center)
        self.bin_width = np.diff(self.bin_center)[0]
        self.bins = cal(self.bins)
        # prepare histo plot if axes have changed
        self.__prepare_histo_plot()
                
# private functions

    def __setup_bins(self, error = None ):
        self.bin_width = np.diff(self.res[1])[0]
        self.bin_center = self.res[1][:-1] + self.bin_width/2.
        self.bin_content = self.res[0]
        self.bins = self.res[1]
        if error is None:
            self.bin_error = np.sqrt(self.bin_content)
        else:
            self.bin_error = error
        self.__prepare_histo_plot()

    def __get_histogram(self):
        # create the histogram arrays from bin_width, bin_center, bin_content and bin_error
        res1 = np.concatenate( [self.bin_center - self.bin_width/2., self.bin_center[-1:] + self.bin_width/2.])
        res0 = self.bin_content
        self.res = ([res0,res1])

    def __prepare_histo_plot(self):
        # prepare data for plotting as steps
        self.cont_min = self.res[0].min()
        iv = self.bin_width / 2.
        self.xpl = np.array(list(zip( self.bin_center - iv, self.bin_center + iv))).ravel()
        self.ypl = np.array(list(zip( self.bin_content, self.bin_content))).ravel()
        
        
    def __rebin_array(self, x, n):
        # rebin 1d  array, useful for histograms
        # start array for slices
        i_s = np.arange(0, x.shape[0]+n, n, dtype=int)
        # end array for slices
        # i_e = np.roll(i_s, -1)
        i_e = np.arange(n, x.shape[0]+2*n, n, dtype=int)
        # create the slices
        slices = [ slice(s, e) for s, e in zip(i_s,i_e)]
        # sum over the slices
        sum_sl = np.array([np.sum(x[sl]) for sl in slices[:-1]])
        # mean value of the slices
        mean_sl = np.array([np.mean(x[sl]) for sl in slices[:-1]])
        # factor to correct the sum for slices that are shorter than n
        fact = np.array([np.float(n)/len(x[sl]) for sl in slices[:-1]])
        # return the values
        return sum_sl, mean_sl, slices[:-1], fact


    def __add__(self, v):
        # add 2 histograms and take care of the errors
        if np.array(self.bin_center == v.bin_center).min():
            # this is the content
            res0 = self.res[0] + v.res[0]
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        else:
            print('bin centers do not match-> cannot add, sorry !')
            return None
    def __sub__(self, v):
        # subtract 2 histograms and take care of the errors
        if np.array(self.bin_center == v.bin_center).min():
            res0 = self.res[0] - v.res[0]
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        else:
            print('bin centers do not match-> cannot subtract, sorry !')
            return None

    def __mul__(self, c):
        # scale a histogram multiply from left
        res0 = c*self.res[0]
        err = c*self.bin_error
        res1 = np.copy(self.res[1])
        res = ([res0, res1 ])
        return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))

    def __rmul__(self, c):
        # scale a histogram multiply from right
        res0 = c*self.res[0]
        err = c*self.bin_error
        res1 = np.copy(self.res[1])
        res = ([res0, res1 ])
        return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))

# end of histo class

# get an MCA spectrum as histogram
def get_spectrum(file, calibration = None):
    """

    Read an MCA spectrum and convert it to a histogram.

    Example::

       >>> h = B.get_spectrum('co60.spe')  # read the spectrum
       >>> h.plot()                        # plot the spectrum

    """
    sp = mcsp.MCA(file)
    sp_title = sp.spectrum['$DATE_MEA'] + \
        " live time = %6.1f s, total time = %6.1f s"%(sp.spectrum['$MEAS_TIM'][0],\
                                                           sp.spectrum['$MEAS_TIM'][1])
    # create histogram
    if calibration is None:
        h = histo(bin_center=sp.chn, bin_content = sp.cont, title = sp_title)
        h.xlabel = 'Channels'
    elif calibration == 'internal':
        h = histo(bin_center=sp.energy, bin_content = sp.cont, title = sp_title)
        h.xlabel = 'Energy'
    else:
        chan_values = calibration( sp.chn )
        h = histo(bin_center=chan_values, bin_content = sp.cont, title = sp_title)
        h.xlabel = 'User Calibration'
    # set the titles
    h.ylabel = 'Counts'
    return(h)
