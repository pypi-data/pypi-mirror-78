from control import step_response as st, impulse_response, initial_response, forced_response
from matplotlib import pyplot as plt

def step(sys, T=None, X0=0.0, input=None, output=None, transpose=False, return_x=False, squeeze=True):
    """
    Step response of a linear system

    If the system has multiple inputs or outputs (MIMO), one input has
    to be selected for the simulation. Optionally, one output may be
    selected. The parameters `input` and `output` do this. All other
    inputs are set to 0, all other outputs are ignored.

    For information on the **shape** of parameters `T`, `X0` and
    return values `T`, `yout`, see :ref:`time-series-convention`.

    Parameters
    ----------
    sys: StateSpace, or TransferFunction
        LTI system to simulate

    T: array-like object, optional
        Time vector (argument is autocomputed if not given)

    X0: array-like or number, optional
        Initial condition (default = 0)

        Numbers are converted to constant arrays with the correct shape.

    input: int
        Index of the input that will be used in this simulation.

    output: int
        Index of the output that will be used in this simulation. Set to None
        to not trim outputs

    transpose: bool
        If True, transpose all input and output arrays (for backward
        compatibility with MATLAB and scipy.signal.lsim)

    return_x: bool
        If True, return the state vector (default = False).

    squeeze: bool, optional (default=True)
        If True, remove single-dimensional entries from the shape of
        the output.  For single output systems, this converts the
        output response to a 1D array.

    Returns
    -------
    T: array
        Time values of the output

    yout: array
        Response of the system

    xout: array
        Individual response of each x variable

    See Also
    --------
    forced, initial, impulse

    Notes
    -----
    This function uses the `forced` function with the input set to a
    unit step.

    Examples
    --------
    >>> T, yout = step(sys, T, X0)
    """
    yout, T = st(sys,T,X0,input,output,transpose,return_x,squeeze)
    plt.plot(yout,T)
    plt.title("Step response")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.axhline(y=yout[-1], color="black", linestyle="--")
    plt.show()

def impulse(sys, T=None, X0=0.0, input=0, output=None, transpose=False, return_x=False, squeeze=True):
    """
    Impulse response of a linear system

    If the system has multiple inputs or outputs (MIMO), one input has
    to be selected for the simulation. Optionally, one output may be
    selected. The parameters `input` and `output` do this. All other
    inputs are set to 0, all other outputs are ignored.

    For information on the **shape** of parameters `T`, `X0` and
    return values `T`, `yout`, see :ref:`time-series-convention`.

    Parameters
    ----------
    sys: StateSpace, TransferFunction
        LTI system to simulate

    T: array-like object, optional
        Time vector (argument is autocomputed if not given)

    X0: array-like object or number, optional
        Initial condition (default = 0)

        Numbers are converted to constant arrays with the correct shape.

    input: int
        Index of the input that will be used in this simulation.

    output: int
        Index of the output that will be used in this simulation. Set to None
        to not trim outputs

    transpose: bool
        If True, transpose all input and output arrays (for backward
        compatibility with MATLAB and scipy.signal.lsim)

    return_x: bool
        If True, return the state vector (default = False).

    squeeze: bool, optional (default=True)
        If True, remove single-dimensional entries from the shape of
        the output.  For single output systems, this converts the
        output response to a 1D array.

    Returns
    -------
    T: array
        Time values of the output
    yout: array
        Response of the system
    xout: array
        Individual response of each x variable

    See Also
    --------
    forced, initial, step

    Notes
    -----
    This function uses the `forced` function to compute the time
    response. For continuous time systems, the initial condition is altered to
    account for the initial impulse.

    Examples
    --------
    >>> T, yout = impulse(sys, T, X0)
    """
    yout, T = impulse_response(sys,T,X0,input,output,transpose,return_x,squeeze)
    plt.plot(yout,T)
    plt.title("Impulse response")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Response")
    plt.show()

def initial(sys, T=None, X0=0.0, input=0, output=None, transpose=False, return_x=False, squeeze=True):
    """
    Initial condition response of a linear system

    If the system has multiple outputs (MIMO), optionally, one output
    may be selected. If no selection is made for the output, all
    outputs are given.

    For information on the **shape** of parameters `T`, `X0` and
    return values `T`, `yout`, see :ref:`time-series-convention`.

    Parameters
    ----------
    sys: StateSpace, or TransferFunction
        LTI system to simulate

    T: array-like object, optional
        Time vector (argument is autocomputed if not given)

    X0: array-like object or number, optional
        Initial condition (default = 0)

        Numbers are converted to constant arrays with the correct shape.

    input: int
        Ignored, has no meaning in initial condition calculation. Parameter
        ensures compatibility with step_response and impulse_response

    output: int
        Index of the output that will be used in this simulation. Set to None
        to not trim outputs

    transpose: bool
        If True, transpose all input and output arrays (for backward
        compatibility with MATLAB and scipy.signal.lsim)

    return_x: bool
        If True, return the state vector (default = False).

    squeeze: bool, optional (default=True)
        If True, remove single-dimensional entries from the shape of
        the output.  For single output systems, this converts the
        output response to a 1D array.

    Returns
    -------
    T: array
        Time values of the output
    yout: array
        Response of the system
    xout: array
        Individual response of each x variable

    See Also
    --------
    forced, impulse, step

    Notes
    -----
    This function uses the `forced` function with the input set to
    zero.

    Examples
    --------
    >>> T, yout = initial(sys, T, X0)
    """
    yout, T = initial_response(sys,T,X0,input,output,transpose, return_x, squeeze)
    plt.plot(yout,T)
    plt.title("Response to Initial Conditions")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.show()

def forced(sys, T=None, U=0.0, X0=0.0, transpose=False, interpolate=False, squeeze=True):
    """
    Simulate the output of a linear system.

    As a convenience for parameters `U`, `X0`:
    Numbers (scalars) are converted to constant arrays with the correct shape.
    The correct shape is inferred from arguments `sys` and `T`.

    For information on the **shape** of parameters `U`, `T`, `X0` and
    return values `T`, `yout`, `xout`, see :ref:`time-series-convention`.

    Parameters
    ----------
    sys: LTI (StateSpace, or TransferFunction)
        LTI system to simulate

    T: array-like, optional for discrete LTI `sys`
        Time steps at which the input is defined; values must be evenly spaced.

    U: array-like or number, optional
        Input array giving input at each time `T` (default = 0).

        If `U` is ``None`` or ``0``, a special algorithm is used. This special
        algorithm is faster than the general algorithm, which is used
        otherwise.

    X0: array-like or number, optional
        Initial condition (default = 0).

    transpose: bool, optional (default=False)
        If True, transpose all input and output arrays (for backward
        compatibility with MATLAB and scipy.signal.lsim)

    interpolate: bool, optional (default=False)
        If True and system is a discrete time system, the input will
        be interpolated between the given time steps and the output
        will be given at system sampling rate.  Otherwise, only return
        the output at the times given in `T`.  No effect on continuous
        time simulations (default = False).

    squeeze: bool, optional (default=True)
        If True, remove single-dimensional entries from the shape of
        the output.  For single output systems, this converts the
        output response to a 1D array.

    Returns
    -------
    T: array
        Time values of the output.
    yout: array
        Response of the system.
    xout: array
        Time evolution of the state vector.

    See Also
    --------
    step, initial, impulse

    Notes
    -----
    For discrete time systems, the input/output response is computed using the
    :scipy-signal:ref:`scipy.signal.dlsim` function.

    For continuous time systems, the output is computed using the matrix
    exponential `exp(A t)` and assuming linear interpolation of the inputs
    between time points.

    Examples
    --------
    >>> T, yout, xout = forced(sys, T, u, X0)

    See :ref:`time-series-convention`.
    """
    yout, T,xout = forced_response(sys, T, U, X0, transpose, interpolate, squeeze)
    plt.plot(yout,T)
    plt.title("Response to Forced Conditions")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.show()
