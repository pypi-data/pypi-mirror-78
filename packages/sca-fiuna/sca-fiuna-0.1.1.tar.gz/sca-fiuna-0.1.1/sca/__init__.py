from control.xferfcn import tf, tfdata, ss2tf
from control.statesp import ss, drss, rss, tf2ss, ssdata
from control.frdata import frd
from control.bdalg import feedback, connect, series, parallel, append, negate
from control.ctrlutil import mag2db, db2mag, issys
from control.dtime import c2d
from control.lti import dcgain, pole, zero, damp, evalfr, freqresp, isctime as isct, isdtime as isdt, issiso, timebase
from control.pzmap import pzmap
from control.iosys import input_output_response as ioresponse, find_eqpt as findeqpt, linearize, ss2io, tf2io
from control.phaseplot import phase_plot as phaseplot
from control.freqplot import bode_plot as bode, nyquist_plot as nyquist, gangof4_plot as gangof4
from control.nichols import nichols_plot as nichols
from control.margins import margin, stability_margins as smargin
from control.sisotool import sisotool
from control.mateqn import care, dare, lyap, dlyap
from control.statefbk import ctrb, obsv, gram, acker, lqr, place, place_varga as varga
from control.robust import h2syn, hinfsyn, mixsyn, augw
from control.modelsimp import minreal, balred, hsvd, modred, era, markov
from control.canonical import canonical_form as canon, observable_form as obsvf, reachable_form
from control.delay import pade


from cmath import sqrt, phase, pi, tan
import matplotlib.pyplot as plt
from numpy import real, imag
import warnings
from numpy.linalg import matrix_rank as rank
warnings.filterwarnings("ignore")


from .rlocus import root_locus as rlocus
from .funclib import *
from .graph import *
