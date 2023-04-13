# cython: boundscheck=False
# cython: initializedcheck=False
# cython: wraparound=False

cdef int where_to_insert(
        np.float_t* arr,
        np.float_t number,
        int size) nogil:
    cdef:
        int idx
        np.float_t current
    for idx in range(size - 1, -1, -1):
        current = arr[idx]
        if number >= current:
            return idx + 1

    return 0


cdef void cumsum(
        np.float_t* arr_in,
        np.float_t* arr_out,
        int N) nogil:
    cdef:
        int i = 0
        np.float_t csum = 0
    for i in range(N):
        csum += arr_in[i]
        arr_out[i] = csum


cdef void copy_point(
        double * a,
        double * b) nogil:
    cdef:
        int i = 0
    for i in range(3):
        b[i] = a[i]


cdef void scalar_muliplication_point(
        double * a,
        double scalar) nogil:
    cdef:
        int i = 0
    for i in range(3):
        a[i] *= scalar


cpdef double random() nogil:
    """Sample a random number between 0 and 1.

    Returns
    -------
    _ : double
        random number
    """
    return rand() / float(RAND_MAX)


cpdef double norm(double[:] v) nogil:
    """Compute the vector norm.

    Parameters
    ----------
    v : double[3]
        input vector.

    Returns
    -------
    _ : double
        norm of the input vector.
    """
    return sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


cpdef double dot(double[:] v1, double[:] v2) nogil:
    """Compute vectors dot product.

    Parameters
    ----------
    v1 : double[3]
        input vector 1.
    v2 : double[3]
        input vector 2.

    Returns
    -------
    _ : double
        dot product of input vectors.
    """
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]


cpdef void normalize(double[:] v) nogil:
    """Normalize the vector.

    Parameters
    ----------
    v : double[3]
        input vector

    Notes
    -----
    Overwrites the first argument.

    """
    cdef double scale = 1.0 / norm(v)
    v[0] = v[0] * scale
    v[1] = v[1] * scale
    v[2] = v[2] * scale


cpdef void cross(double[:] out, double[:] v1, double[:] v2) nogil:
    """Compute vectors cross product.

    Parameters
    ----------
    out : double[3]
        output vector.
    v1 : double[3]
        input vector 1.
    v2 : double[3]
        input vector 2.

    Notes
    -----
    Overwrites the first argument.

    """
    out[0] = v1[1] * v2[2] - v1[2] * v2[1]
    out[1] = v1[2] * v2[0] - v1[0] * v2[2]
    out[2] = v1[0] * v2[1] - v1[1] * v2[0]


cpdef void random_vector(double[:] out):
    """Generate a unit random vector

    Parameters
    ----------
    out : double[3]
        output vector

    Notes
    -----
    Overwrites the input
    """
    out[0] = 2.0 * random() - 1.0
    out[1] = 2.0 * random() - 1.0
    out[2] = 2.0 * random() - 1.0
    normalize(out)


cpdef void random_perpendicular_vector(double[:] out,double[:] v):
    """Generate a random perpendicular vector

    Parameters
    ----------
    out : double[3]
        output vector

    v : double[3]
        input vector

    Notes
    -----
    Overwrites the first argument
    """
    cdef double[3] tmp

    random_vector(tmp)
    cross(out, v, tmp)
    normalize(out)


cpdef (double, double) random_point_within_circle(double r):
    """Generate a random point within a circle

    Parameters
    ----------
    r : double
        The radius of the circle

    Returns
    -------
    x : double
        x coordinate of the random point

    y : double
        y coordinate of the random point

    """
    cdef double x = 1.0
    cdef double y = 1.0

    while (x * x + y * y) > 1:
        x = 2.0 * random() - 1.0
        y = 2.0 * random() - 1.0
    return (r * x, r * y)

