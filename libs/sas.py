from numpy import *
import scipy.optimize as opt
import copy as cp
import matplotlib.pyplot as plt
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
import matplotlib.figure as fig
import matplotlib.axes as maxes
import matplotlib.ticker as mticker
import tkFileDialog as tkfd
from matplotlib.backends.backend_agg import FigureCanvasAgg

class SasData(object):
    """Root class for data object for holding 1-d Q versus I SAS data.

    Class has a series of methods for initialising and
    doing basic operations on SAS data. The root class
    is very simple and only contains the Q and I lists
    providing simple addition, multiplication, length
    and string operations.
    """

    def __init__(self, q_vals, i_vals):
        """Initializing the SasData object.

        Just passes two lists to the initializing object which
        are then stored internally. Possibly an argument for 
        including the units of Q in the root object
        """

        assert type(q_vals) == list or type(q_vals) == ndarray
        assert type(i_vals) == list or type(i_vals) == ndarray
        assert len(q_vals) == len(i_vals), 'q and i not the same length'
        self.q = q_vals
        self.i = i_vals


    def __len__(self):
        return len(self.q)


    def __add__(self, other):
        """Test whether other is SasData or float/int and add together.

        The basic add operation covers two specific cases. The first is
        where two SasData objects are added together where the wish is
        for the intensities of both to be combined. The second cases is
        when adding (or more likely subtracting) a numeric value (float 
        or int) which is handled separately. Probably both of these could
        be written neater and faster.

        Inputs must required are a SasData object and either a SasData object or
        an int or float. Returns a new SasData object.
        """

        # addition of two SasData objects
        if isinstance(other, SasData):
            assert len(self) == len(other), 'datasets not the same length'
	    assert all(self.q) == all(other.q), 'q values not the same'

            # initialize a SasData object with zero for all intensities
	    out = SasData(self.q, ([0] * len(self)))
	    for j in range(len(self)):
                out.i[j] = self.i[j] + other.i[j]

	    return out

        # addition of a float or int to  SasData objects
        elif type(other) is int or type(other) is float:
            out = SasData(self.q, ([0]*len(self)))
	    for j in range(len(self)):
	        out.i[j] = self.i[j] + other

	    return out

        else:
            return NotImplemented

    def __sub__(self, other):
        """Subtraction method for SasData Objects.

        See documentation for __add__ which is essentially identical
        """

        # addition of two SasData objects
        if isinstance(other, SasData):
            assert len(self) == len(other), 'datasets not the same length'
	    assert all(self.q) == all(other.q), 'q values not the same'

            # initialize a SasData object with zero for all intensities
	    out = SasData(self.q, ([0] * len(self)))
	    for j in range(len(self)):
                out.i[j] = self.i[j] - other.i[j]

	    return out

        # addition of a float or int to  SasData objects
        elif type(other) is int or type(other) is float:
            out = SasData(self.q, ([0]*len(self)))
	    for j in range(len(self)):
	        out.i[j] = self.i[j] - other

	    return out

        else:
            return NotImplemented

    def __mul__(self, other):
        """Basic mutplication function for SasData objects.

        Requires a SasData object and an int or a float. Returns a new
        SasData object.
        """

        assert isinstance(self, SasData)
        try:
            assert type(other) is int or type(other) is float
        except:
            return NotImplemented

        # initialize a SasData object with zero for all intensities 
        out = SasData(self.q, (([0] * len(self)))) 
        for j in range(len(self)):
            out.i[j] = self.i[j] * other
	return out


class ExpSasData(SasData):
    """Derived class for experimental SAS data obects.

    The ExpSasData class is derived from the SasDatq class. The ExpSasData
    class adds support for masks over the data to remove parts of the
    experimental pattern. The mask and the masked data can be stored with
    the experimental data. 
    """

    def __init__(self, q, i):
        """Initialization routine adds additional SasData object for the 
        masked data at self.masked"""

        SasData.__init__(self, q, i)
        self.id = ''
        self.instrument = ''
        self.mask = []
        self.masked = SasData([],[])

    def set_id(self, id):
        try:
            assert (type(id) == float) or (type(id) == str)
        except AssertionError:
            raise TypeError

        self.id = str(id)

    def get_id(self):
        return self.id

    def set_instrument(self, instrument):
        try:
            assert type(instrument) == str
            assert instrument in ['loq', 'sans2d', 'i22', 'I22']
        except AssertionError:
            raise TypeError

        self.instrument = instrument

    def get_instrument(self):
        return self.instrument

    #################################################
    #
    # SasTrim Routines for Trimming and Masking ExpSasData
    #
    #################################################

    def make_mask(self, mask_ranges):
        """Generates a mask list of 0's and 1's to remove data in mask_ranges

        Takes a SasData object and creates a list with a 1 to 1 mapping with
        SasData.q containing only zeros and ones based on the q-values in
        mask_ranges. Mask_ranges takes the form of a list of length N of
        lists of length two containing data to exclude. May expand in the future
        to allow both positive and negative mask generation.
        """

    # need to make an assertion that mask ranges is a N x 2 set of lists
    # not immediately sure how to do this at the moment

    # make a copy of the q list because we are going to change it
        mask = cp.deepcopy(self.q)
        
        for j in range(0, len(mask)):

            #for each pair of values in mask_ranges
            for low, high in mask_ranges:
                # check whether q values are within mask_ranges
                if self.q[j] >= low and self.q[j] <= high:
                    mask[j] = 0
                    break
                else:
                    mask[j] = 1

        self.mask = mask

    def apply_mask(self):
        """Applies a pre-calculated mask to a SasData object.

        Takes the pre-calculated mask from make_mask and creates a new
        SasData object with the masked data points (those corresponding
        to zeros in the mask) removed. The new object is then placed in
        self.masked. In principle this should allow nested masking operations.
        Whether this is a good idea remains to be seen.
        """

        assert type(self.mask) is list, 'Mask needs to be a list'
        assert self.mask != None, 'Mask appears not to have been setup'
        assert len(self.mask) != 0, 'Mask is zero length?'
        assert len(self.mask
                     ) == len(self.q), 'Mask not same length as data?'

        q_masked = extract(self.mask, self.q)
        i_masked = extract(self.mask, self.i)

        self.masked =  SasData(q_masked, i_masked)
        return self.masked


##################################################
#
# Loaders for various SAS data formats to SasData objects
#
##################################################

def load_file():
    """A generic loader that will call specific loaders.

    The function will call tkFileDialog.askopenfilename() to 
    get a file and then will attempt to match it against known file
    types and call the correct one.
    """

    # Use tkfd to open an OS specific file dialog and get the path to the file
    path = tkfd.askopenfilename()

    DLS_I22_recogniser = 'Created at DLS-I22'
    sasxml_recogniser = 'cansas1d/1.0'

    file = open(path, 'r').readlines()

    for j in range(0,5):
        if DLS_I22_recogniser in file[j]:
            sas_data_object = load_two_column_data(path, 3)
            break
        elif sasxml_recogniser in file[j]:
            sas_data_object = loadsasxml(path)
            break

        else:
            pass

    sas_data_object = load_two_column_data(path,0)

    return sas_data_object
    

def load_two_column_data(file, rows_to_skip=0):
    """Loader for i22 two column data files.

    i22 files currently have two columns with three lines of text
    at the top. This just does a quick and dirty load of a the file
    into a SasData object. Currently setup to be called in the form
    data = load_two_column_data('file')
    """

    data = loadtxt(file, skiprows = rows_to_skip)



    data_q = data[:,0]
    data_i = data[:,1]
    return ExpSasData(data_q, data_i)

import xml.etree.ElementTree as ET

def loadsasxml(file):
    """Loaded for SASxml 1.0 format data.

    The loader uses xml.etree.ElementTree to parse the xml file and
    then searches through the file to find the {cansas1d/1.0}Q and
    {cansas1d/1,0}I tags and then extract the text attribute from each 
    of these. The list is then converted from text to floats and the Q
    and I lists passed to a new SasData object. Currently nothing else
    from the sas xml folder is loaded.
    """

    # Check that file is a sasxml file
    # assert (first line of file is what it should be) is True

    # Parse the xml file and find the root element
    tree = ET.parse('xmltest.xml')
    elem = tree.getroot()

    # return a list of all the <Q> tags and get the Q values
    q_tags = elem.getiterator("{cansas1d/1.0}Q")

    q_list = []

    for elements in q_tags:
        q_list.append(float(elements.text)) # need to convert text to float

    # then do the same for the <I> tags and values
    i_tags = elem.getiterator("{cansas1d/1.0}I")
    i_list = []

    for elements in i_tags:
        i_list.append(float(elements.text))

    # check everything is ok with q_list and i_list
    assert len(q_list) == len(i_list), 'different number of q and i values?'
    assert len(q_list) != 0, 'appear to be no q values'
    assert len(i_list) != 0, 'appear to be no i values'
    assert q_list[0] < q_list[-1], 'q values not in order?'

    # generate and return a SasData object
    return ExpSasData(q_list, i_list)


    

###################################################
#
# Definition of plotting routines
#
###################################################

class SasPlot(fig.Figure):
    """Class for generating and handling data plots.

    Uses the pylab module of matplotlib to generate and
    manipulate plots and provide some easy routines for
    modifying them, adding data, etc.
    """

    def __init__(self, data, format='ro'):
        """__init__ routine creates a plot with default features.

        """

        fig.Figure.__init__(self)

        self.ax = self.add_subplot(111)
        self.ax.plot(data.q, data.i, format)
        self.ax.set_ylabel('I')
        self.ax.set_xlabel('Q')
        # plt.title(name of data_to_plot) - how do I do this?
        self.canvas = FigureCanvasAgg(self)
        # setup a list for holding the data for this plot
        # self.data.append(name of data_to_plot)


    

    def guinier_plot(self):
        """Routine to convert to a Guinier plot.

        Converts plot to show data on the coordinates of ln(I)
        versus Q^2. First we need to get the correct figure
        number and then change the axes. The routine sets the axes
        to base e log and a squared scale on y and x axes respectively.
        """

        self.ax.set_yscale('log', basey=e)
        self.ax.set_xscale('q_squared')



class SquaredScale(mscale.ScaleBase):
    """ScaleBase class for generating x axis of Guinier plots.

    Uses the built in scalebase to generate a transformed axis type
    called SquaredScale which can be called using ax.set_xscale('q_squared').
    Currently uses the default ticker and scale setup which will need
    to be changed in the future.

    The class requires the import of pylab (AutoLocator, ScalarFormatter
    NullLocator and NullFormatter) matplotlib.transforms (imported as
    mtransforms, required for the mtransforms.Transform class) and
    matplotlib.scale (imported as mscale, required for the mscale.ScaleBase
    class for inheritance of the scale).
    """

    name = 'q_squared'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)
        thresh = kwargs.pop("thresh", 0)
        if thresh < 0:
            raise ValueError("thresh must be greater than 0")
        self.thresh = thresh

    def get_transform(self):
        """Set the actual transform for the axis coordinates.

        """
        return self.SquaredTransform(self.thresh)

    def set_default_locators_and_formatters(self, axis):
        """
        Set the locators and formatters to reasonable defaults for
        scaling. Not really too sure what these do at the moment.
        """
        axis.set_major_locator(mticker.AutoLocator())
        axis.set_major_formatter(mticker.ScalarFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return  0, vmax

    class SquaredTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a): return a**2

        def inverted(self):
            return SquaredScale.InvertedSquaredTransform()

    class InvertedSquaredTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a): 
            return sqrt(a)    

        def inverted(self):
            return SquaredScale.SquaredTransform()



mscale.register_scale(SquaredScale)

        

              

###################################################
#
# Definition of data fitting models
#
###################################################

def guinier(q,param):
    """Function that returns a Guinier model

    The parameter set list should contain i0, Rg, and background in that
    order. There is currently no option to hold any parameter.
    """

    assert len(param) == 3, 'Guinier fit requires three parameters'
    assert len(q) != 0, 'No Q values to evaluate'
      
    return param[0]*exp((-1/3)*(param[1]**2)*(q**2)) + param[2]

#calculate the residuals for a fit
def guinier_residuals(param, i, q):

    err = i-guinier(q, param)
    return err


def fit_guinier(data):
    """Function for calling to get a Guinier fit to a dataset

    This currently takes a dataset and sets some plausible initial values
    for a Guinier fit before calling guinier_residuals using leastsq.
    """

    assert isinstance(data, SasData) 

    param_0 = [1.,1.,0.] # Set reasonable initial values for Guinier fit
           
    least_squares_fit = opt.leastsq(
            guinier_residuals, param_0, args=(data.i, data.q))

    return least_squares_fit

    
