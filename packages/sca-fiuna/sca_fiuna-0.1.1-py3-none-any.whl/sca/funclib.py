import cmath
from control.matlab import TransferFunction
from control.xferfcn import tf

def phase(V):
    """
    function phase:

    receive one or vector of complex numbers and return the vector of phase
    angle respect the origin on radian

    num: complex single or vector of complex

    def: single number or vector of phases
    """
    if not type(V) == type([]): V = [V]
    fases = [cmath.phase(Poriginal) for Poriginal in V]
    if len(fases) == 1: return fases[0]
    return fases

def phased(V):
    """
    function phased:

    receive one or vector of complex numbers and return the vector of phase
    angle respect the origin on deg

    num: complex single or vector of complex

    def: single number or vector of phases
    """
    fases = phase(V)
    if not type(fases) == type([]): fases = [fases]
    fases = [fase*180/cmath.pi for fase in fases]
    if len(fases) == 1: return fases[0]
    return fases

def evals(G, Pole):
    """
    function evals:

    Receive a TransferFunction and one complex number s and evaluate in

    G: TransferFunction
    Pole: complex number

    return the complex number of result

    """
    return G.horner(Pole)[0][0]

def zpk(zeros, poles, gain):
    """
    zero pole gain function

    Create a Transfer Function with the zero, pole and gain


    Inputs:

    zeros: zero list of the system
    poles: pole list of the system
    gain: gain of the system


    Output:

    G: the transfer function


    Example:

    G = zpk([0],[3,2],10)

            10*s
    G =  -----------
          s^2-5*s+6

    """

    s = tf("s")
    G = 1
    for i in zeros:
        z = s-i
        G = G*z
    for i in poles:
        p = s-i
        G = G/p
    return G*gain
