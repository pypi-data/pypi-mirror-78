# distutils: language=c++
# cython: embedsignature=True
cimport cython
cimport numpy as np
from libc.math cimport sqrt, abs, cbrt
from libc.stdlib cimport malloc, free
from libcpp.vector cimport vector
from numpy.math cimport INFINITY
import warnings

from tree cimport int_t, Tree as c_Tree, PyWrapper, Node, Edge, Face, Cell as c_Cell

import scipy.sparse as sp
from scipy.spatial import Delaunay, cKDTree
from six import integer_types
import numpy as np

from .utils.interputils_cython cimport _bisect_left, _bisect_right

from discretize.utils.codeutils import requires
# matplotlib is a soft dependencies for discretize
try:
    import matplotlib
    import matplotlib.cm as cmx
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.collections import PatchCollection
except ImportError:
    matplotlib = False


cdef class TreeCell:
    """A Cell of the `TreeMesh`

    This cannot be created in python, it can only be accessed by indexing the
    `TreeMesh` object.

    This is also the object that is passed to the user defined refine function
    when calling TreeMesh.refine(func).

    Notes
    -----
    When called as part of the `refine` function, only the x0, center, and h
    properties are valid.
    """
    cdef double _x, _y, _z, _x0, _y0, _z0, _wx, _wy, _wz
    cdef int_t _dim
    cdef c_Cell* _cell
    cdef void _set(self, c_Cell* cell):
        self._cell = cell
        self._dim = cell.n_dim
        self._x = cell.location[0]
        self._x0 = cell.points[0].location[0]

        self._y = cell.location[1]
        self._y0 = cell.points[0].location[1]

        self._wx = cell.points[3].location[0] - self._x0
        self._wy = cell.points[3].location[1] - self._y0
        if(self._dim > 2):
            self._z = cell.location[2]
            self._z0 = cell.points[0].location[2]
            self._wz = cell.points[7].location[2] - self._z0

    @property
    def nodes(self):
        """indexes of this cell's nodes

        Returns
        -------
        list of ints
        """
        cdef Node *points[8]
        points = self._cell.points
        if self._dim == 3:
            return [points[0].index, points[1].index,
                    points[2].index, points[3].index,
                    points[4].index, points[5].index,
                    points[6].index, points[7].index]
        return [points[0].index, points[1].index,
                points[2].index, points[3].index]

    @property
    def edges(self):
        """indexes of this cell's edges

        Returns
        -------
        list of ints
        """
        cdef Edge *edges[12]
        edges = self._cell.edges
        if self._dim == 2:
            return [edges[0].index, edges[1].index,
                    edges[2].index, edges[3].index]
        return [
            edges[0].index, edges[1].index, edges[2].index, edges[3].index,
            edges[4].index, edges[5].index, edges[6].index, edges[7].index,
            edges[8].index, edges[9].index, edges[10].index, edges[11].index,
        ]
    @property
    def faces(self):
        """indexes of this cell's faces
        Returns
        -------
        list of ints
        """
        cdef Face *faces[6]
        faces = self._cell.faces
        if self._ == 3:
            return [
                faces[0].index, faces[1].index,
                faces[2].index, faces[3].index,
                faces[4].index, faces[5].index
            ]
        cdef Edge *edges[12]
        edges = self._cell.edges
        return [edges[2].index, edges[3].index,
                edges[0].index, edges[1].index]

    @property
    def center(self):
        """numpy.array of length dim"""
        if self._dim == 2: return np.array([self._x, self._y])
        return np.array([self._x, self._y, self._z])

    @property
    def x0(self):
        """numpy.array of length dim"""
        if self._dim == 2: return np.array([self._x0, self._y0])
        return np.array([self._x0, self._y0, self._z0])

    @property
    def h(self):
        """ numpy.array of length dim
        width of this cell
        """
        if self._dim == 2: return np.array([self._wx, self._wy])
        return np.array([self._wx, self._wy, self._wz])

    @property
    def dim(self):
        """"int dimension of cell"""
        return self._dim

    @property
    def index(self):
        """integer index of this cell"""
        return self._cell.index

    @property
    def neighbors(self):
        """ The indexes of this cell's neighbors

        Indexes of this cell's neighbors. If a cell has more than one neighbor
        in a certain direction (i.e. when a level changes between adjacent cells),
        then that entry will also be a list of all of those neighbor indices.
        The list is order -x, +x, -y, +y, -z, +z. If a cell has no neighbor in
        that direction, the value will be -1.

        Returns
        -------
        list of ints or list of ints
        """
        neighbors = [-1]*self._dim*2

        for i in range(self._dim*2):
            if self._cell.neighbors[i] is NULL:
                continue
            elif self._cell.neighbors[i].is_leaf():
                neighbors[i] = self._cell.neighbors[i].index
            else:
                if self._dim==2:
                    if i==0:
                        neighbors[i] = [self._cell.neighbors[i].children[1].index,
                                        self._cell.neighbors[i].children[3].index]
                    elif i==1:
                        neighbors[i] = [self._cell.neighbors[i].children[0].index,
                                        self._cell.neighbors[i].children[2].index]
                    elif i==2:
                        neighbors[i] = [self._cell.neighbors[i].children[2].index,
                                        self._cell.neighbors[i].children[3].index]
                    else:
                        neighbors[i] = [self._cell.neighbors[i].children[0].index,
                                        self._cell.neighbors[i].children[1].index]
                else:
                    if i==0:
                        neighbors[i] = [self._cell.neighbors[i].children[1].index,
                                        self._cell.neighbors[i].children[3].index,
                                        self._cell.neighbors[i].children[5].index,
                                        self._cell.neighbors[i].children[7].index]
                    elif i==1:
                        neighbors[i] = [self._cell.neighbors[i].children[0].index,
                                        self._cell.neighbors[i].children[2].index,
                                        self._cell.neighbors[i].children[4].index,
                                        self._cell.neighbors[i].children[6].index]
                    elif i==2:
                        neighbors[i] = [self._cell.neighbors[i].children[2].index,
                                        self._cell.neighbors[i].children[3].index,
                                        self._cell.neighbors[i].children[6].index,
                                        self._cell.neighbors[i].children[7].index]
                    elif i==3:
                        neighbors[i] = [self._cell.neighbors[i].children[0].index,
                                        self._cell.neighbors[i].children[1].index,
                                        self._cell.neighbors[i].children[4].index,
                                        self._cell.neighbors[i].children[5].index]
                    elif i==4:
                        neighbors[i] = [self._cell.neighbors[i].children[4].index,
                                        self._cell.neighbors[i].children[5].index,
                                        self._cell.neighbors[i].children[6].index,
                                        self._cell.neighbors[i].children[7].index]
                    else:
                        neighbors[i] = [self._cell.neighbors[i].children[0].index,
                                        self._cell.neighbors[i].children[1].index,
                                        self._cell.neighbors[i].children[2].index,
                                        self._cell.neighbors[i].children[3].index]
        return neighbors

    @property
    def _index_loc(self):
        if self._dim == 2:
            return tuple((self._cell.location_ind[0], self._cell.location_ind[1]))
        return tuple((self._cell.location_ind[0], self._cell.location_ind[1],
                      self._cell.location_ind[2]))
    @property
    def _level(self):
        return self._cell.level

cdef int_t _evaluate_func(void* function, c_Cell* cell) with gil:
    # Wraps a function to be called in C++
    func = <object> function
    pycell = TreeCell()
    pycell._set(cell)
    return <int_t> func(pycell)

cdef class _TreeMesh:
    cdef c_Tree *tree
    cdef PyWrapper *wrapper
    cdef int_t _dim
    cdef int_t[3] ls
    cdef int _finalized

    cdef double[:] _xs, _ys, _zs
    cdef double[:] _x0

    cdef object _gridCC, _gridN, _gridhN
    cdef object _gridEx, _gridEy, _gridEz, _gridhEx, _gridhEy, _gridhEz
    cdef object _gridFx, _gridFy, _gridFz, _gridhFx, _gridhFy, _gridhFz

    cdef object _h_gridded
    cdef object _vol, _area, _edge
    cdef object _aveFx2CC, _aveFy2CC, _aveFz2CC, _aveF2CC, _aveF2CCV,
    cdef object _aveN2CC, _aveN2E, _aveN2Ex, _aveN2Ey, _aveN2Ez
    cdef object _aveN2F, _aveN2Fx, _aveN2Fy, _aveN2Fz
    cdef object _aveEx2CC, _aveEy2CC, _aveEz2CC,_aveE2CC,_aveE2CCV
    cdef object _aveCC2F, _aveCCV2F, _aveCC2Fx, _aveCC2Fy, _aveCC2Fz
    cdef object _faceDiv
    cdef object _edgeCurl, _nodalGrad

    cdef object __ubc_order, __ubc_indArr

    def __cinit__(self, *args, **kwargs):
        self.wrapper = new PyWrapper()
        self.tree = new c_Tree()

    def __init__(self, h, x0):
        nx2 = 2*len(h[0])
        ny2 = 2*len(h[1])
        self._dim = len(x0)
        self._x0 = x0

        xs = np.empty(nx2 + 1, dtype=float)
        xs[::2] = np.cumsum(np.r_[x0[0], h[0]])
        xs[1::2] = (xs[:-1:2] + xs[2::2])/2
        self._xs = xs
        self.ls[0] = int(np.log2(len(h[0])))

        ys = np.empty(ny2 + 1, dtype=float)
        ys[::2] = np.cumsum(np.r_[x0[1],h[1]])
        ys[1::2] = (ys[:-1:2] + ys[2::2])/2
        self._ys = ys
        self.ls[1] = int(np.log2(len(h[1])))

        if self._dim > 2:
            nz2 = 2*len(h[2])

            zs = np.empty(nz2 + 1, dtype=float)
            zs[::2] = np.cumsum(np.r_[x0[2],h[2]])
            zs[1::2] = (zs[:-1:2] + zs[2::2])/2
            self._zs = zs
            self.ls[2] = int(np.log2(len(h[2])))
        else:
            self._zs = np.zeros(1, dtype=float)
            self.ls[2] = 1

        self.tree.set_dimension(self._dim)
        self.tree.set_levels(self.ls[0], self.ls[1], self.ls[2])
        self.tree.set_xs(&self._xs[0], &self._ys[0], &self._zs[0])
        self.tree.initialize_roots()
        self._finalized = False
        self._clear_cache()

    def _clear_cache(self):
        self._gridCC = None
        self._gridN = None
        self._gridhN = None
        self._h_gridded = None

        self._gridEx = None
        self._gridEy = None
        self._gridEz = None
        self._gridhEx = None
        self._gridhEy = None
        self._gridhEz = None

        self._gridFx = None
        self._gridFy = None
        self._gridFz = None
        self._gridhFx = None
        self._gridhFy = None
        self._gridhFz = None

        self._vol = None
        self._area = None
        self._edge = None

        self._aveCC2F = None
        self._aveCC2Fx = None
        self._aveCC2Fy = None
        self._aveCC2Fz = None

        self._aveFx2CC = None
        self._aveFy2CC = None
        self._aveFz2CC = None
        self._aveF2CC = None
        self._aveF2CCV = None

        self._aveEx2CC = None
        self._aveEy2CC = None
        self._aveEz2CC = None
        self._aveE2CC = None
        self._aveE2CCV = None

        self._aveN2CC = None
        self._aveN2E = None
        self._aveN2F = None
        self._aveN2Ex = None
        self._aveN2Ey = None
        self._aveN2Ez = None
        self._aveN2Fx = None
        self._aveN2Fy = None
        self._aveN2Fz = None

        self._faceDiv = None
        self._nodalGrad = None
        self._edgeCurl = None

        self.__ubc_order = None
        self.__ubc_indArr = None

    def refine(self, function, finalize=True):
        """ Refine a TreeMesh using a user supplied function.

        Refines the TreeMesh using a function that is recursively called on each
        cell of the mesh. It must accept an object of type `discretize.TreeMesh.Cell`
        and return an integer like object defining the desired level.
        The function can also simply be an integer, which will then cause all
        cells to be at least that level.

        Parameters
        ----------
        function : callable | int
            a function describing the desired level,
            or an integer to refine all cells to at least that level.
        finalize : bool, optional
            Whether to finalize the mesh

        Examples
        --------
        >>> from discretize import TreeMesh
        >>> mesh = TreeMesh([32,32])
        >>> def func(cell):
        >>>     r = np.linalg.norm(cell.center-0.5)
        >>>     return mesh.max_level if r<0.2 else mesh.max_level-1
        >>> mesh.refine(func)
        >>> mesh
        ---- QuadTreeMesh ----
         x0: 0.00
         y0: 0.00
         hx: 32*0.03,
         hy: 32*0.03,
        nC: 352
        Fill: 34.38%

        See Also
        --------
        discretize.TreeMesh.TreeCell : a description of the TreeCell object
        """
        if type(function) in integer_types:
            level = function
            function = lambda cell: level

        #Wrapping function so it can be called in c++
        cdef void * func_ptr = <void *> function
        self.wrapper.set(func_ptr, _evaluate_func)
        #Then tell c++ to build the tree
        self.tree.build_tree_from_function(self.wrapper)
        if finalize:
            self.finalize()

    def insert_cells(self, points, levels, finalize=True):
        """Insert cells into the TreeMesh that contain given points

        Insert cell(s) into the TreeMesh that contain the given point(s) at the
        assigned level(s).

        Parameters
        ----------
        points : array_like with shape (N, dim)
        levels : array_like of integers with shape (N)
        finalize : bool, optional
            Whether to finalize after inserting point(s)

        Examples
        --------
        >>> from discretize import TreeMesh
        >>> mesh = TreeMesh([32,32])
        >>> mesh.insert_cells([0.5, 0.5], mesh.max_level)
        >>> print(mesh)
        ---- QuadTreeMesh ----
         x0: 0.00
         y0: 0.00
         hx: 32*0.03,
         hy: 32*0.03,
        nC: 40
        Fill: 3.91%
        """
        points = np.require(np.atleast_2d(points), dtype=np.float64,
                            requirements='C')
        cdef double[:, :] cs = points
        cdef int[:] ls = np.require(np.atleast_1d(levels), dtype=np.int32,
                                    requirements='C')
        cdef int_t i
        for i in range(ls.shape[0]):
            self.tree.insert_cell(&cs[i, 0], ls[i])
        if finalize:
            self.finalize()

    def finalize(self):
        """Finalize the TreeMesh
        Called after finished cronstruction of the mesh. Can only be called once.
        After finalize is called, all other attributes and functions are valid.
        """
        if not self._finalized:
            self.tree.finalize_lists()
            self.tree.number()
            self._finalized=True

    def number(self):
        """Number the cells, nodes, faces, and edges of the TreeMesh"""
        self.tree.number()

    def _set_x0(self, x0):
        if not isinstance(x0, (list, tuple, np.ndarray)):
            raise ValueError('x0 must be a list, tuple or numpy array')
        self._x0 = np.asarray(x0, dtype=np.float64)
        cdef int_t dim = self._x0.shape[0]
        cdef double[:] shift
        #cdef c_Cell *cell
        cdef Node *node
        cdef Edge *edge
        cdef Face *face
        if self.tree.n_dim > 0: # Will only happen if __init__ has been called
            shift = np.empty(dim, dtype=np.float64)

            shift[0] = self._x0[0] - self._xs[0]
            shift[1] = self._x0[1] - self._ys[0]
            if dim == 3:
                shift[2] = self._x0[2] - self._zs[0]

            for i in range(self._xs.shape[0]):
                self._xs[i] += shift[0]
            for i in range(self._ys.shape[0]):
                self._ys[i] += shift[1]
            if dim == 3:
                for i in range(self._zs.shape[0]):
                    self._zs[i] += shift[2]

            #update the locations of all of the items
            self.tree.shift_cell_centers(&shift[0])

            for itN in self.tree.nodes:
                node = itN.second
                for i in range(dim):
                    node.location[i] += shift[i]

            for itE in self.tree.edges_x:
                edge = itE.second
                for i in range(dim):
                    edge.location[i] += shift[i]

            for itE in self.tree.edges_y:
                edge = itE.second
                for i in range(dim):
                    edge.location[i] += shift[i]

            if dim == 3:
                for itE in self.tree.edges_z:
                    edge = itE.second
                    for i in range(dim):
                        edge.location[i] += shift[i]

                for itF in self.tree.faces_x:
                    face = itF.second
                    for i in range(dim):
                        face.location[i] += shift[i]

                for itF in self.tree.faces_y:
                    face = itF.second
                    for i in range(dim):
                        face.location[i] += shift[i]

                for itF in self.tree.faces_z:
                    face = itF.second
                    for i in range(dim):
                        face.location[i] += shift[i]
            #clear out all cached grids
            self._gridCC = None
            self._gridN = None
            self._gridhN = None
            self._gridEx = None
            self._gridhEx = None
            self._gridEy = None
            self._gridhEy = None
            self._gridEz = None
            self._gridhEz = None
            self._gridFx = None
            self._gridhFx = None
            self._gridFy = None
            self._gridhFy = None
            self._gridFz = None
            self._gridhFz = None

    @property
    def fill(self):
        """
        How filled is the mesh compared to a TensorMesh?
        As a fraction: [0, 1].
        """
        #Tensor mesh cells:
        cdef int_t nxc, nyc, nzc;
        nxc = (self._xs.shape[0]-1)//2
        nyc = (self._ys.shape[0]-1)//2
        nzc = (self._zs.shape[0]-1)//2 if self._dim==3 else 1
        return float(self.nC)/(nxc * nyc * nzc)

    @property
    def maxLevel(self):
        """
        The maximum level used, which may be
        less than `levels` or `max_level`.
        """
        cdef int level = 0
        for cell in self.tree.cells:
            level = max(level, cell.level)
        return level

    @property
    def max_level(self):
        """The maximum possible level for a cell on this mesh"""
        return self.tree.max_level

    @property
    def nC(self):
        """Number of cells"""
        return self.tree.cells.size()

    @property
    def nN(self):
        """Number of non-hanging nodes"""
        return self.ntN - self.nhN

    @property
    def ntN(self):
        """Number of non-hanging and hanging nodes"""
        return self.tree.nodes.size()

    @property
    def nhN(self):
        """Number of hanging nodes"""
        return self.tree.hanging_nodes.size()

    @property
    def nE(self):
        """Total number of non-hanging edges amongst all dimensions"""
        return self.nEx + self.nEy + self.nEz

    @property
    def nhE(self):
        """Total number of hanging edges amongst all dimensions"""
        return self.nhEx + self.nhEy + self.nhEz

    @property
    def ntE(self):
        """Total number of non-hanging and hanging edges amongst all dimensions"""
        return self.nE + self.nhE

    @property
    def nEx(self):
        """Number of non-hanging edges oriented along the first dimension"""
        return self.ntEx - self.nhEx

    @property
    def nEy(self):
        """Number of non-hanging edges oriented along the second dimension"""
        return self.ntEy - self.nhEy

    @property
    def nEz(self):
        """Number of non-hanging edges oriented along the third dimension"""
        return self.ntEz - self.nhEz

    @property
    def ntEx(self):
        """Number of non-hanging and hanging edges oriented along the first dimension"""
        return self.tree.edges_x.size()

    @property
    def ntEy(self):
        """Number of non-hanging and hanging edges oriented along the second dimension"""
        return self.tree.edges_y.size()

    @property
    def ntEz(self):
        """Number of non-hanging and hanging edges oriented along the third dimension"""
        return self.tree.edges_z.size()

    @property
    def nhEx(self):
        """Number of hanging edges oriented along the first dimension"""
        return self.tree.hanging_edges_x.size()

    @property
    def nhEy(self):
        """Number of hanging edges oriented along the second dimension"""
        return self.tree.hanging_edges_y.size()

    @property
    def nhEz(self):
        """Number of hanging edges oriented along the third dimension"""
        return self.tree.hanging_edges_z.size()

    @property
    def nF(self):
        """Total number of non-hanging faces amongst all dimensions"""
        return self.nFx + self.nFy + self.nFz

    @property
    def nhF(self):
        """Total number of hanging faces amongst all dimensions"""
        return self.nhFx + self.nhFy + self.nhFz

    @property
    def ntF(self):
        """Total number of hanging and non-hanging faces amongst all dimensions"""
        return self.nF + self.nhF

    @property
    def nFx(self):
        """Number of non-hanging faces oriented along the first dimension"""
        return self.ntFx - self.nhFx

    @property
    def nFy(self):
        """Number of non-hanging faces oriented along the second dimension"""
        return self.ntFy - self.nhFy

    @property
    def nFz(self):
        """Number of non-hanging faces oriented along the third dimension"""
        return self.ntFz - self.nhFz

    @property
    def ntFx(self):
        """Number of non-hanging and hanging faces oriented along the first dimension"""
        if(self._dim == 2): return self.ntEy
        return self.tree.faces_x.size()

    @property
    def ntFy(self):
        """Number of non-hanging and hanging faces oriented along the second dimension"""
        if(self._dim == 2): return self.ntEx
        return self.tree.faces_y.size()

    @property
    def ntFz(self):
        """Number of non-hanging and hanging faces oriented along the third dimension"""
        if(self._dim == 2): return 0
        return self.tree.faces_z.size()

    @property
    def nhFx(self):
        """Number of hanging faces oriented along the first dimension"""
        if(self._dim == 2): return self.nhEy
        return self.tree.hanging_faces_x.size()

    @property
    def nhFy(self):
        """Number of hanging faces oriented along the second dimension"""
        if(self._dim == 2): return self.nhEx
        return self.tree.hanging_faces_y.size()

    @property
    def nhFz(self):
        """Number of hanging faces oriented along the third dimension"""
        if(self._dim == 2): return 0
        return self.tree.hanging_faces_z.size()

    @property
    def gridCC(self):
        """
        Returns a numpy arrayof shape (nC, dim) with the center locations of all cells
        in order.
        """
        cdef np.float64_t[:, :] gridCC
        cdef np.int64_t ii, ind, dim
        if self._gridCC is None:
            dim = self._dim
            self._gridCC = np.empty((self.nC, self._dim), dtype=np.float64)
            gridCC = self._gridCC
            for cell in self.tree.cells:
                ind = cell.index
                for ii in range(dim):
                    gridCC[ind, ii] = cell.location[ii]
        return self._gridCC

    @property
    def gridN(self):
        """
        Returns a numpy array of shape (nN, dim) with the locations of all
        non-hanging nodes in order.
        """
        cdef np.float64_t[:, :] gridN
        cdef Node *node
        cdef np.int64_t ii, ind, dim
        if self._gridN is None:
            dim = self._dim
            self._gridN = np.empty((self.nN, dim) ,dtype=np.float64)
            gridN = self._gridN
            for it in self.tree.nodes:
                node = it.second
                if not node.hanging:
                    ind = node.index
                    for ii in range(dim):
                        gridN[ind, ii] = node.location[ii]
        return self._gridN

    @property
    def gridhN(self):
        """
        Returns a numpy array of shape (nN, dim) with the locations of all
        hanging nodes in order.
        """
        cdef np.float64_t[:, :] gridN
        cdef Node *node
        cdef np.int64_t ii, ind, dim
        if self._gridhN is None:
            dim = self._dim
            self._gridhN = np.empty((self.nhN, dim), dtype=np.float64)
            gridhN = self._gridhN
            for node in self.tree.hanging_nodes:
                ind = node.index-self.nN
                for ii in range(dim):
                    gridhN[ind, ii] = node.location[ii]
        return self._gridhN

    @property
    def h_gridded(self):
        """
        Returns an (nC, dim) numpy array with the widths of all cells in order
        """
        if self._h_gridded is not None:
            return self._h_gridded
        cdef np.float64_t[:, :] gridCH
        cdef np.int64_t ii, ind, dim
        cdef np.float64_t len
        cdef int epc = 4 if self._dim==3 else 2
        dim = self._dim
        self._h_gridded = np.empty((self.nC, dim), dtype=np.float64)
        gridCH = self._h_gridded
        for cell in self.tree.cells:
            ind = cell.index
            for ii in range(dim):
                gridCH[ind, ii] = cell.edges[ii*epc].length

        return self._h_gridded

    @property
    def gridEx(self):
        """
        Returns a numpy array of shape (nEx, dim) with the centers of all
        non-hanging edges along the first dimension in order.
        """
        cdef np.float64_t[:, :] gridEx
        cdef Edge *edge
        cdef np.int64_t ii, ind, dim
        if self._gridEx is None:
            dim = self._dim
            self._gridEx = np.empty((self.nEx, dim), dtype=np.float64)
            gridEx = self._gridEx
            for it in self.tree.edges_x:
                edge = it.second
                if not edge.hanging:
                    ind = edge.index
                    for ii in range(dim):
                        gridEx[ind, ii] = edge.location[ii]
        return self._gridEx

    @property
    def gridhEx(self):
        """
        Returns a numpy array of shape (nhEx, dim) with the centers of all
        hanging edges along the first dimension in order.
        """
        cdef np.float64_t[:, :] gridhEx
        cdef Edge *edge
        cdef np.int64_t ii, ind, dim
        if self._gridhEx is None:
            dim = self._dim
            self._gridhEx = np.empty((self.nhEx, dim), dtype=np.float64)
            gridhEx = self._gridhEx
            for edge in self.tree.hanging_edges_x:
                ind = edge.index-self.nEx
                for ii in range(dim):
                    gridhEx[ind, ii] = edge.location[ii]
        return self._gridhEx

    @property
    def gridEy(self):
        """
        Returns a numpy array of shape (nEy, dim) with the centers of all
        non-hanging edges along the second dimension in order.
        """
        cdef np.float64_t[:, :] gridEy
        cdef Edge *edge
        cdef np.int64_t ii, ind, dim
        if self._gridEy is None:
            dim = self._dim
            self._gridEy = np.empty((self.nEy, dim), dtype=np.float64)
            gridEy = self._gridEy
            for it in self.tree.edges_y:
                edge = it.second
                if not edge.hanging:
                    ind = edge.index
                    for ii in range(dim):
                        gridEy[ind, ii] = edge.location[ii]
        return self._gridEy

    @property
    def gridhEy(self):
        """
        Returns a numpy array of shape (nhEy, dim) with the centers of all
        hanging edges along the second dimension in order.
        """
        cdef np.float64_t[:, :] gridhEy
        cdef Edge *edge
        cdef np.int64_t ii, ind, dim
        if self._gridhEy is None:
            dim = self._dim
            self._gridhEy = np.empty((self.nhEy, dim), dtype=np.float64)
            gridhEy = self._gridhEy
            for edge in self.tree.hanging_edges_y:
                ind = edge.index-self.nEy
                for ii in range(dim):
                    gridhEy[ind, ii] = edge.location[ii]
        return self._gridhEy

    @property
    def gridEz(self):
        """
        Returns a numpy array of shape (nEz, dim) with the centers of all
        non-hanging edges along the third dimension in order.
        """
        cdef np.float64_t[:, :] gridEz
        cdef Edge *edge
        cdef np.int64_t ii, ind, dim
        if self._gridEz is None:
            dim = self._dim
            self._gridEz = np.empty((self.nEz, dim), dtype=np.float64)
            gridEz = self._gridEz
            for it in self.tree.edges_z:
                edge = it.second
                if not edge.hanging:
                    ind = edge.index
                    for ii in range(dim):
                        gridEz[ind, ii] = edge.location[ii]
        return self._gridEz

    @property
    def gridhEz(self):
        """
        Returns a numpy array of shape (nhEz, dim) with the centers of all
        hanging edges along the third dimension in order.
        """
        cdef np.float64_t[:, :] gridhEz
        cdef Edge *edge
        cdef np.int64_t ii, ind, dim
        if self._gridhEz is None:
            dim = self._dim
            self._gridhEz = np.empty((self.nhEz, dim), dtype=np.float64)
            gridhEz = self._gridhEz
            for edge in self.tree.hanging_edges_z:
                ind = edge.index-self.nEz
                for ii in range(dim):
                    gridhEz[ind, ii] = edge.location[ii]
        return self._gridhEz

    @property
    def gridFx(self):
        """
        Returns a numpy array of shape (nFx, dim) with the centers of all
        non-hanging faces along the first dimension in order.
        """
        if(self._dim == 2): return self.gridEy

        cdef np.float64_t[:, :] gridFx
        cdef Face *face
        cdef np.int64_t ii, ind, dim
        if self._gridFx is None:
            dim = self._dim
            self._gridFx = np.empty((self.nFx, dim), dtype=np.float64)
            gridFx = self._gridFx
            for it in self.tree.faces_x:
                face = it.second
                if not face.hanging:
                    ind = face.index
                    for ii in range(dim):
                        gridFx[ind, ii] = face.location[ii]
        return self._gridFx

    @property
    def gridFy(self):
        """
        Returns a numpy array of shape (nFy, dim) with the centers of all
        non-hanging faces along the second dimension in order.
        """
        if(self._dim == 2): return self.gridEx
        cdef np.float64_t[:, :] gridFy
        cdef Face *face
        cdef np.int64_t ii, ind, dim
        if self._gridFy is None:
            dim = self._dim
            self._gridFy = np.empty((self.nFy, dim), dtype=np.float64)
            gridFy = self._gridFy
            for it in self.tree.faces_y:
                face = it.second
                if not face.hanging:
                    ind = face.index
                    for ii in range(dim):
                        gridFy[ind, ii] = face.location[ii]
        return self._gridFy

    @property
    def gridFz(self):
        """
        Returns a numpy array of shape (nFz, dim) with the centers of all
        non-hanging faces along the third dimension in order.
        """
        if(self._dim == 2): return self.gridCC

        cdef np.float64_t[:, :] gridFz
        cdef Face *face
        cdef np.int64_t ii, ind, dim
        if self._gridFz is None:
            dim = self._dim
            self._gridFz = np.empty((self.nFz, dim), dtype=np.float64)
            gridFz = self._gridFz
            for it in self.tree.faces_z:
                face = it.second
                if not face.hanging:
                    ind = face.index
                    for ii in range(dim):
                        gridFz[ind, ii] = face.location[ii]
        return self._gridFz

    @property
    def gridhFx(self):
        """
        Returns a numpy array of shape (nhFx, dim) with the centers of all
        hanging faces along the first dimension in order.
        """
        if(self._dim == 2): return self.gridhEy

        cdef np.float64_t[:, :] gridFx
        cdef Face *face
        cdef np.int64_t ii, ind, dim
        if self._gridhFx is None:
            dim = self._dim
            self._gridhFx = np.empty((self.nhFx, dim), dtype=np.float64)
            gridhFx = self._gridhFx
            for face in self.tree.hanging_faces_x:
                ind = face.index-self.nFx
                for ii in range(dim):
                    gridhFx[ind, ii] = face.location[ii]
        return self._gridhFx

    @property
    def gridhFy(self):
        """
        Returns a numpy array of shape (nhFy, dim) with the centers of all
        hanging faces along the second dimension in order.
        """
        if(self._dim == 2): return self.gridhEx

        cdef np.float64_t[:, :] gridhFy
        cdef Face *face
        cdef np.int64_t ii, ind, dim
        if self._gridhFy is None:
            dim = self._dim
            self._gridhFy = np.empty((self.nhFy, dim), dtype=np.float64)
            gridhFy = self._gridhFy
            for face in self.tree.hanging_faces_y:
                ind = face.index-self.nFy
                for ii in range(dim):
                    gridhFy[ind, ii] = face.location[ii]
        return self._gridhFy

    @property
    def gridhFz(self):
        """
        Returns a numpy array of shape (nhFz, dim) with the centers of all
        hanging faces along the third dimension in order.
        """
        if(self._dim == 2): return np.array([])

        cdef np.float64_t[:, :] gridhFz
        cdef Face *face
        cdef np.int64_t ii, ind, dim
        if self._gridhFz is None:
            dim = self._dim
            self._gridhFz = np.empty((self.nhFz, dim), dtype=np.float64)
            gridhFz = self._gridhFz
            for face in self.tree.hanging_faces_z:
                ind = face.index-self.nFz
                for ii in range(dim):
                    gridhFz[ind, ii] = face.location[ii]
        return self._gridhFz

    @property
    def vol(self):
        """
        Returns a numpy array of length nC with the volumes (areas in 2D) of all
        cells in order.
        """
        cdef np.float64_t[:] vol
        if self._vol is None:
            self._vol = np.empty(self.nC, dtype=np.float64)
            vol = self._vol
            for cell in self.tree.cells:
                vol[cell.index] = cell.volume
        return self._vol

    @property
    def area(self):
        """
        Returns a numpy array of length nF with the area (length in 2D) of all
        faces ordered by x, then y, then z.
        """
        if self._dim == 2 and self._area is None:
            self._area = np.r_[self.edge[self.nEx:], self.edge[:self.nEx]]
        cdef np.float64_t[:] area
        cdef int_t ind, offset = 0
        cdef Face *face
        if self._area is None:
            self._area = np.empty(self.nF, dtype=np.float64)
            area = self._area

            for it in self.tree.faces_x:
                face = it.second
                if face.hanging: continue
                area[face.index] = face.area

            offset = self.nFx
            for it in self.tree.faces_y:
                face = it.second
                if face.hanging: continue
                area[face.index + offset] = face.area

            offset = self.nFx + self.nFy
            for it in self.tree.faces_z:
                face = it.second
                if face.hanging: continue
                area[face.index + offset] = face.area
        return self._area

    @property
    def edge(self):
        """
        Returns a numpy array of length nE with the length of all edges ordered
        by x, then y, then z.
        """
        cdef np.float64_t[:] edge_l
        cdef Edge *edge
        cdef int_t ind, offset
        if self._edge is None:
            self._edge = np.empty(self.nE, dtype=np.float64)
            edge_l = self._edge

            for it in self.tree.edges_x:
                edge = it.second
                if edge.hanging: continue
                edge_l[edge.index] = edge.length

            offset = self.nEx
            for it in self.tree.edges_y:
                edge = it.second
                if edge.hanging: continue
                edge_l[edge.index + offset] = edge.length

            if self._dim > 2:
                offset = self.nEx + self.nEy
                for it in self.tree.edges_z:
                    edge = it.second
                    if edge.hanging: continue
                    edge_l[edge.index + offset] = edge.length
        return self._edge

    @property
    def cellBoundaryInd(self):
        """Returns a tuple of arrays of indexes for boundary cells in each direction
        xdown, xup, ydown, yup, zdown, zup
        """
        cdef np.int64_t[:] indxu, indxd, indyu, indyd, indzu, indzd
        indxu = np.empty(self.nC, dtype=np.int64)
        indxd = np.empty(self.nC, dtype=np.int64)
        indyu = np.empty(self.nC, dtype=np.int64)
        indyd = np.empty(self.nC, dtype=np.int64)
        if self._dim == 3:
            indzu = np.empty(self.nC, dtype=np.int64)
            indzd = np.empty(self.nC, dtype=np.int64)
        cdef int_t nxu, nxd, nyu, nyd, nzu, nzd
        nxu = 0
        nxd = 0
        nyu = 0
        nyd = 0
        nzu = 0
        nzd = 0
        for cell in self.tree.cells:
            if cell.neighbors[0] == NULL:
                indxd[nxd] = cell.index
                nxd += 1
            if cell.neighbors[1] == NULL:
                indxu[nxu] = cell.index
                nxu += 1
            if cell.neighbors[2] == NULL:
                indyd[nyd] = cell.index
                nyd += 1
            if cell.neighbors[3] == NULL:
                indyu[nyu] = cell.index
                nyu += 1
            if self._dim == 3:
                if cell.neighbors[4] == NULL:
                    indzd[nzd] = cell.index
                    nzd += 1
                if cell.neighbors[5] == NULL:
                    indzu[nzu] = cell.index
                    nzu += 1
        ixd = np.array(indxd)[:nxd]
        ixu = np.array(indxu)[:nxu]
        iyd = np.array(indyd)[:nyd]
        iyu = np.array(indyu)[:nyu]
        if self._dim == 3:
            izd = np.array(indzd)[:nzd]
            izu = np.array(indzu)[:nzu]
            return ixd, ixu, iyd, iyu, izd, izu
        else:
            return ixd, ixu, iyd, iyu

    @property
    def faceBoundaryInd(self):
        """Returns a tuple of arrays of indexes for boundary faces in each direction
        xdown, xup, ydown, yup, zdown, zup
        """
        cell_boundary_inds = self.cellBoundaryInd
        cdef np.int64_t[:] c_indxu, c_indxd, c_indyu, c_indyd, c_indzu, c_indzd
        cdef np.int64_t[:] f_indxu, f_indxd, f_indyu, f_indyd, f_indzu, f_indzd
        if self._dim == 2:
            c_indxd, c_indxu, c_indyd, c_indyu = cell_boundary_inds
        else:
            c_indxd, c_indxu, c_indyd, c_indyu, c_indzd, c_indzu = cell_boundary_inds

        f_indxd = np.empty(c_indxd.shape[0], dtype=np.int64)
        f_indxu = np.empty(c_indxu.shape[0], dtype=np.int64)
        f_indyd = np.empty(c_indyd.shape[0], dtype=np.int64)
        f_indyu = np.empty(c_indyu.shape[0], dtype=np.int64)
        if self._dim == 2:
            for i in range(f_indxd.shape[0]):
                f_indxd[i] = self.tree.cells[c_indxd[i]].edges[2].index
            for i in range(f_indxu.shape[0]):
                f_indxu[i] = self.tree.cells[c_indxu[i]].edges[3].index
            for i in range(f_indyd.shape[0]):
                f_indyd[i] = self.tree.cells[c_indyd[i]].edges[0].index
            for i in range(f_indyu.shape[0]):
                f_indyu[i] = self.tree.cells[c_indyu[i]].edges[1].index
        if self._dim == 3:
            f_indzd = np.empty(c_indzd.shape[0], dtype=np.int64)
            f_indzu = np.empty(c_indzu.shape[0], dtype=np.int64)

            for i in range(f_indxd.shape[0]):
                f_indxd[i] = self.tree.cells[c_indxd[i]].faces[0].index
            for i in range(f_indxu.shape[0]):
                f_indxu[i] = self.tree.cells[c_indxu[i]].faces[1].index
            for i in range(f_indyd.shape[0]):
                f_indyd[i] = self.tree.cells[c_indyd[i]].faces[2].index
            for i in range(f_indyu.shape[0]):
                f_indyu[i] = self.tree.cells[c_indyu[i]].faces[3].index
            for i in range(f_indzd.shape[0]):
                f_indzd[i] = self.tree.cells[c_indzd[i]].faces[4].index
            for i in range(f_indzu.shape[0]):
                f_indzu[i] = self.tree.cells[c_indzu[i]].faces[5].index
        ixd = np.array(f_indxd)
        ixu = np.array(f_indxu)
        iyd = np.array(f_indyd)
        iyu = np.array(f_indyu)
        if self._dim == 3:
            izd = np.array(f_indzd)
            izu = np.array(f_indzu)
            return ixd, ixu, iyd, iyu, izd, izu
        else:
            return ixd, ixu, iyd, iyu

    def get_boundary_cells(self, active_ind=None, direction='zu'):
        """Returns the indices of boundary cells in a given direction given an active index array.

        Parameters
        ----------
        active_ind : array_like of bool, optional
            If not None, then this must show which cells are active
        direction: str, optional
            must be one of ('zu', 'zd', 'xu', 'xd', 'yu', 'yd')

        Returns
        -------
        numpy.array
            Array of indices for the boundary cells in the requested direction
        """

        direction = direction.lower()
        if direction[0] == 'z' and self._dim == 2:
            dir_str = 'y'+direction[1]
        else:
            dir_str = direction
        cdef int_t dir_ind = {'xd':0, 'xu':1, 'yd':2, 'yu':3, 'zd':4, 'zu':5}[dir_str]
        if active_ind is None:
            return self.cellBoundaryInd[dir_ind]

        active_ind = np.require(active_ind, dtype=np.int8, requirements='C')
        cdef np.int8_t[:] act = active_ind
        cdef np.int8_t[:] is_on_boundary = np.zeros(self.nC, dtype=np.int8)

        cdef c_Cell *cell
        cdef c_Cell *neighbor

        for cell in self.tree.cells:
            if not act[cell.index]:
                continue
            is_bound = 0
            neighbor = cell.neighbors[dir_ind]
            if neighbor is NULL:
                is_bound = 1
            elif neighbor.is_leaf():
                is_bound = not act[neighbor.index]
            else:
                if dir_ind == 1 or dir_ind == 3 or dir_ind == 5:
                    is_bound = is_bound or (not act[neighbor.children[0].index])
                if dir_ind == 0 or dir_ind == 3 or dir_ind == 5:
                    is_bound = is_bound or (not act[neighbor.children[1].index])
                if dir_ind == 1 or dir_ind == 2 or dir_ind == 5:
                    is_bound = is_bound or (not act[neighbor.children[2].index])
                if dir_ind == 0 or dir_ind == 2 or dir_ind == 5:
                    is_bound = is_bound or (not act[neighbor.children[3].index])

                if self._dim == 3:
                    if dir_ind == 1 or dir_ind == 3 or dir_ind == 4:
                        is_bound = is_bound or (not act[neighbor.children[4].index])
                    if dir_ind == 0 or dir_ind == 3 or dir_ind == 4:
                        is_bound = is_bound or (not act[neighbor.children[5].index])
                    if dir_ind == 1 or dir_ind == 2 or dir_ind == 4:
                        is_bound = is_bound or (not act[neighbor.children[6].index])
                    if dir_ind == 0 or dir_ind == 2 or dir_ind == 4:
                        is_bound = is_bound or (not act[neighbor.children[7].index])

            is_on_boundary[cell.index] = is_bound

        return np.where(is_on_boundary)

    @cython.cdivision(True)
    def get_cells_along_line(self, x0, x1):
        """Finds the cells along a line segment defined by two points

        Parameters
        ----------
        x0,x1 : array_like of length (dim)
            Begining and ending point of the line segment.

        Returns
        -------
        list of ints
            Indexes for cells that contain the a line defined by the two input
            points, ordered in the direction of the line.
        """
        cdef np.float64_t ax, ay, az, bx, by, bz

        cdef int dim = self.dim
        ax = x0[0]
        ay = x0[1]
        az = x0[2] if dim==3 else 0

        bx = x1[0]
        by = x1[1]
        bz = x1[2] if dim==3 else 0

        cdef vector[long long int] cell_indexes;

        #find initial cell
        cdef c_Cell *cur_cell = self.tree.containing_cell(ax, ay, az)
        cell_indexes.push_back(cur_cell.index)
        #find last cell
        cdef c_Cell *last_cell = self.tree.containing_cell(bx, by, bz)
        cdef c_Cell *next_cell
        cdef int ix, iy, iz
        cdef double tx, ty, tz, ipx, ipy, ipz

        if dim==3:
            last_point = 7
        else:
            last_point = 3

        cdef int iter = 0

        while cur_cell.index != last_cell.index:
            #find which direction to look:
            p0 = cur_cell.points[0].location
            pF = cur_cell.points[last_point].location

            if ax>bx:
                tx = (p0[0]-ax)/(bx-ax)
            elif ax<bx:
                tx = (pF[0]-ax)/(bx-ax)
            else:
                tx = INFINITY

            if ay>by:
                ty = (p0[1]-ay)/(by-ay)
            elif ay<by:
                ty = (pF[1]-ay)/(by-ay)
            else:
                ty = INFINITY

            if az>bz:
                tz = (p0[2]-az)/(bz-az)
            elif az<bz:
                tz = (pF[2]-az)/(bz-az)
            else:
                tz = INFINITY

            t = min(tx,ty,tz)

            #intersection point
            ipx = (bx-ax)*t+ax
            ipy = (by-ay)*t+ay
            ipz = (bz-az)*t+az

            next_cell = cur_cell
            if tx<=ty and tx<=tz:
                # step in x direction
                if ax>bx: # go -x
                    next_cell = next_cell.neighbors[0]
                else: # go +x
                    next_cell = next_cell.neighbors[1]
            if ty<=tx and ty<=tz:
                # step in y direction
                if ay>by: # go -y
                    next_cell = next_cell.neighbors[2]
                else: # go +y
                    next_cell = next_cell.neighbors[3]
            if dim==3 and tz<=tx and tz<=ty:
                # step in z direction
                if az>bz: # go -z
                    next_cell = next_cell.neighbors[4]
                else: # go +z
                    next_cell = next_cell.neighbors[5]

            # check if next_cell is not a leaf
            # (if so need to traverse down the children and find the closest leaf cell)
            while not next_cell.is_leaf():
                # should be able to use cp to check which cell to go to
                cp = next_cell.children[0].points[last_point].location
                # this basically finds the child cell closest to the intersection point
                ix = ipx>cp[0] or (ipx==cp[0] and ax<bx)
                iy = ipy>cp[1] or (ipy==cp[1] and ay<by)
                iz = dim==3 and (ipz>cp[2] or  (ipz==cp[2] and az<bz))
                next_cell = next_cell.children[ix + 2*iy + 4*iz]

            #this now should have stepped appropriately across diagonals and such

            cur_cell = next_cell
            cell_indexes.push_back(cur_cell.index)
            if cur_cell.index == -1:
                raise Exception('Path not found')
        return cell_indexes


    @property
    def faceDiv(self):
        """
        Construct divergence operator (face-stg to cell-centres).
        """
        if self._faceDiv is not None:
            return self._faceDiv
        if self._dim == 2:
            D = self._faceDiv2D() # Because it uses edges instead of faces
        else:
            D = self._faceDiv3D()
        R = self._deflate_faces()
        self._faceDiv = D*R
        return self._faceDiv

    @cython.cdivision(True)
    @cython.boundscheck(False)
    def _faceDiv2D(self):
        cdef np.int64_t[:] I = np.empty(self.nC*4, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(self.nC*4, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(self.nC*4, dtype=np.float64)

        cdef np.int64_t i = 0
        cdef Edge *edges[4]
        cdef np.int64_t offset = self.tree.edges_y.size()
        cdef double volume

        for cell in self.tree.cells:
            edges = cell.edges
            i = cell.index
            I[i*4 : i*4 + 4] = i
            J[i*4    ] = edges[0].index + offset #x edge, y face (add offset)
            J[i*4 + 1] = edges[1].index + offset #x edge, y face (add offset)
            J[i*4 + 2] = edges[2].index #y edge, x face
            J[i*4 + 3] = edges[3].index #y edge, x face

            volume = cell.volume
            V[i*4    ] = -edges[0].length/volume
            V[i*4 + 1] =  edges[1].length/volume
            V[i*4 + 2] = -edges[2].length/volume
            V[i*4 + 3] =  edges[3].length/volume
        return sp.csr_matrix((V, (I, J)))

    @cython.cdivision(True)
    @cython.boundscheck(False)
    def _faceDiv3D(self):
        cdef:
            np.int64_t[:] I = np.empty(self.nC*6, dtype=np.int64)
            np.int64_t[:] J = np.empty(self.nC*6, dtype=np.int64)
            np.float64_t[:] V = np.empty(self.nC*6, dtype=np.float64)

            np.int64_t i = 0
            Face *faces[6]
            np.int64_t offset1 = self.tree.faces_x.size()
            np.int64_t offset2 = offset1 + self.tree.faces_y.size()
            double volume, fx_area, fy_area, fz_area

        for cell in self.tree.cells:
            faces = cell.faces
            i = cell.index
            I[i*6 : i*6 + 6] = i
            J[i*6    ] = faces[0].index #x1 face
            J[i*6 + 1] = faces[1].index #x2 face
            J[i*6 + 2] = faces[2].index + offset1 #y face (add offset1)
            J[i*6 + 3] = faces[3].index + offset1 #y face (add offset1)
            J[i*6 + 4] = faces[4].index + offset2 #z face (add offset2)
            J[i*6 + 5] = faces[5].index + offset2 #z face (add offset2)

            volume = cell.volume
            fx_area = faces[0].area
            fy_area = faces[2].area
            fz_area = faces[4].area
            V[i*6    ] = -fx_area/volume
            V[i*6 + 1] =  fx_area/volume
            V[i*6 + 2] = -fy_area/volume
            V[i*6 + 3] =  fy_area/volume
            V[i*6 + 4] = -fz_area/volume
            V[i*6 + 5] =  fz_area/volume
        return sp.csr_matrix((V, (I, J)))

    @property
    @cython.cdivision(True)
    @cython.boundscheck(False)
    def edgeCurl(self):
        """
        Construct the 3D curl operator.
        """
        if self._edgeCurl is not None:
            return self._edgeCurl
        cdef:
            int_t dim = self._dim
            np.int64_t[:] I = np.empty(4*self.nF, dtype=np.int64)
            np.int64_t[:] J = np.empty(4*self.nF, dtype=np.int64)
            np.float64_t[:] V = np.empty(4*self.nF, dtype=np.float64)
            Face *face
            int_t ii
            int_t face_offset_y = self.nFx
            int_t face_offset_z = self.nFx + self.nFy
            int_t edge_offset_y = self.ntEx
            int_t edge_offset_z = self.ntEx + self.ntEy
            double area

        for it in self.tree.faces_x:
            face = it.second
            if face.hanging:
                continue
            ii = face.index
            I[4*ii : 4*ii + 4] = ii
            J[4*ii    ] = face.edges[0].index + edge_offset_z
            J[4*ii + 1] = face.edges[1].index + edge_offset_y
            J[4*ii + 2] = face.edges[2].index + edge_offset_z
            J[4*ii + 3] = face.edges[3].index + edge_offset_y

            area = face.area
            V[4*ii    ] = -face.edges[0].length/area
            V[4*ii + 1] = -face.edges[1].length/area
            V[4*ii + 2] =  face.edges[2].length/area
            V[4*ii + 3] =  face.edges[3].length/area

        for it in self.tree.faces_y:
            face = it.second
            if face.hanging:
                continue
            ii = face.index + face_offset_y
            I[4*ii : 4*ii + 4] = ii
            J[4*ii    ] = face.edges[0].index + edge_offset_z
            J[4*ii + 1] = face.edges[1].index
            J[4*ii + 2] = face.edges[2].index + edge_offset_z
            J[4*ii + 3] = face.edges[3].index

            area = face.area
            V[4*ii    ] =  face.edges[0].length/area
            V[4*ii + 1] =  face.edges[1].length/area
            V[4*ii + 2] = -face.edges[2].length/area
            V[4*ii + 3] = -face.edges[3].length/area

        for it in self.tree.faces_z:
            face = it.second
            if face.hanging:
                continue
            ii = face.index + face_offset_z
            I[4*ii : 4*ii + 4] = ii
            J[4*ii    ] = face.edges[0].index + edge_offset_y
            J[4*ii + 1] = face.edges[1].index
            J[4*ii + 2] = face.edges[2].index + edge_offset_y
            J[4*ii + 3] = face.edges[3].index

            area = face.area
            V[4*ii    ] = -face.edges[0].length/area
            V[4*ii + 1] = -face.edges[1].length/area
            V[4*ii + 2] =  face.edges[2].length/area
            V[4*ii + 3] =  face.edges[3].length/area

        C = sp.csr_matrix((V, (I, J)),shape=(self.nF, self.ntE))
        R = self._deflate_edges()
        self._edgeCurl = C*R
        return self._edgeCurl

    @property
    @cython.cdivision(True)
    @cython.boundscheck(False)
    def nodalGrad(self):
        """
        Construct gradient operator (nodes to edges).
        """
        if self._nodalGrad is not None:
            return self._nodalGrad
        cdef:
            int_t dim = self._dim
            np.int64_t[:] I = np.empty(2*self.nE, dtype=np.int64)
            np.int64_t[:] J = np.empty(2*self.nE, dtype=np.int64)
            np.float64_t[:] V = np.empty(2*self.nE, dtype=np.float64)
            Edge *edge
            double length
            int_t ii
            np.int64_t offset1 = self.nEx
            np.int64_t offset2 = offset1 + self.nEy

        for it in self.tree.edges_x:
            edge = it.second
            if edge.hanging: continue
            ii = edge.index
            I[ii*2 : ii*2 + 2] = ii
            J[ii*2    ] = edge.points[0].index
            J[ii*2 + 1] = edge.points[1].index

            length = edge.length
            V[ii*2    ] = -1.0/length
            V[ii*2 + 1] =  1.0/length

        for it in self.tree.edges_y:
            edge = it.second
            if edge.hanging: continue
            ii = edge.index + offset1
            I[ii*2 : ii*2 + 2] = ii
            J[ii*2    ] = edge.points[0].index
            J[ii*2 + 1] = edge.points[1].index

            length = edge.length
            V[ii*2    ] = -1.0/length
            V[ii*2 + 1] =  1.0/length

        if(dim>2):
            for it in self.tree.edges_z:
                edge = it.second
                if edge.hanging: continue
                ii = edge.index + offset2
                I[ii*2 : ii*2 + 2] = ii
                J[ii*2    ] = edge.points[0].index
                J[ii*2 + 1] = edge.points[1].index

                length = edge.length
                V[ii*2    ] = -1.0/length
                V[ii*2 + 1] =  1.0/length


        Rn = self._deflate_nodes()
        G = sp.csr_matrix((V, (I, J)), shape=(self.nE, self.ntN))
        self._nodalGrad = G*Rn
        return self._nodalGrad

    @property
    def nodalLaplacian(self):
        raise NotImplementedError('Nodal Laplacian has not been implemented for TreeMesh')

    @cython.boundscheck(False)
    def _aveCC2FxStencil(self):
        cdef np.int64_t[:] I = np.zeros(2*self.ntFx, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFx, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFx, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind

        for cell in self.tree.cells :
            next_cell = cell.neighbors[1]
            if next_cell == NULL:
                continue
            if dim == 2:
                if next_cell.is_leaf():
                    ind = cell.edges[3].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = 0.5
                    V[2*ind + 1] = 0.5
                else:
                    for i in range(2): # two neighbors in +x direction
                        ind = next_cell.children[2*i].edges[2].index
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[2*i].index
                        V[2*ind    ] = 0.5
                        V[2*ind + 1] = 0.5
            else:
                if cell.neighbors[1].is_leaf():
                    ind = cell.faces[1].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = 0.5
                    V[2*ind + 1] = 0.5
                else:
                    for i in range(4): # four neighbors in +x direction
                        ind = next_cell.children[2*i].faces[0].index
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[2*i].index
                        V[2*ind    ] = 0.5
                        V[2*ind + 1] = 0.5

        return sp.csr_matrix((V, (I,J)), shape=(self.ntFx, self.nC))

    @cython.boundscheck(False)
    def _aveCC2FyStencil(self):
        cdef np.int64_t[:] I = np.zeros(2*self.ntFy, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFy, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFy, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind

        for cell in self.tree.cells :
            next_cell = cell.neighbors[3]
            if next_cell==NULL:
                continue
            if dim==2:
                if next_cell.is_leaf():
                    ind = cell.edges[1].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = 0.5
                    V[2*ind + 1] = 0.5
                else:
                    for i in range(2): # two neighbors in +y direction
                        ind = next_cell.children[i].edges[0].index
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[i].index
                        V[2*ind    ] = 0.5
                        V[2*ind + 1] = 0.5
            else:
                if next_cell.is_leaf():
                    ind = cell.faces[3].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = 0.5
                    V[2*ind + 1] = 0.5
                else:
                    for i in range(4): # four neighbors in +y direction
                        ind = next_cell.children[(i>>1)*4 + i%2].faces[2].index
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[(i>>1)*4 + i%2].index
                        V[2*ind    ] = 0.5
                        V[2*ind + 1] = 0.5
        return sp.csr_matrix((V, (I,J)), shape=(self.ntFy, self.nC))

    @cython.boundscheck(False)
    def _aveCC2FzStencil(self):
        cdef np.int64_t[:] I = np.zeros(2*self.ntFz, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFz, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFz, dtype=np.float64)
        cdef int_t ind

        for cell in self.tree.cells :
            next_cell = cell.neighbors[5]
            if next_cell==NULL:
                continue
            if next_cell.is_leaf():
                ind = cell.faces[5].index
                I[2*ind    ] = ind
                I[2*ind + 1] = ind
                J[2*ind    ] = cell.index
                J[2*ind + 1] = next_cell.index
                V[2*ind    ] = 0.5
                V[2*ind + 1] = 0.5
            else:
                for i in range(4): # four neighbors in +z direction
                    ind = next_cell.children[i].faces[4].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.children[i].index
                    V[2*ind    ] = 0.5
                    V[2*ind + 1] = 0.5

        return sp.csr_matrix((V, (I,J)), shape=(self.ntFz, self.nC))

    @property
    @cython.boundscheck(False)
    def _cellGradxStencil(self):
        if getattr(self, '_cellGradxStencilMat', None) is not None:
            return self._cellGradxStencilMat
        cdef np.int64_t[:] I = np.zeros(2*self.ntFx, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFx, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFx, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind

        for cell in self.tree.cells :
            next_cell = cell.neighbors[1]
            if next_cell == NULL:
                continue
            if dim == 2:
                if next_cell.is_leaf():
                    ind = cell.edges[3].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = -1.0
                    V[2*ind + 1] =  1.0
                else:
                    for i in range(2): # two neighbors in +x direction
                        ind = next_cell.children[2*i].edges[2].index
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[2*i].index
                        V[2*ind    ] = -1.0
                        V[2*ind + 1] =  1.0
            else:
                if cell.neighbors[1].is_leaf():
                    ind = cell.faces[1].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = -1.0
                    V[2*ind + 1] =  1.0
                else:
                    for i in range(4): # four neighbors in +x direction
                        ind = next_cell.children[2*i].faces[0].index #0 2 4 6
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[2*i].index
                        V[2*ind    ] = -1.0
                        V[2*ind + 1] =  1.0

        self._cellGradxStencilMat = (
            sp.csr_matrix((V, (I,J)), shape=(self.ntFx, self.nC))
        )
        return self._cellGradxStencilMat

    @property
    @cython.boundscheck(False)
    def _cellGradyStencil(self):
        if getattr(self, '_cellGradyStencilMat', None) is not None:
            return self._cellGradyStencilMat

        cdef np.int64_t[:] I = np.zeros(2*self.ntFy, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFy, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFy, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind

        for cell in self.tree.cells :
            next_cell = cell.neighbors[3]
            if next_cell == NULL:
                continue
            if dim==2:
                if next_cell.is_leaf():
                    ind = cell.edges[1].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = -1.0
                    V[2*ind + 1] =  1.0
                else:
                    for i in range(2): # two neighbors in +y direction
                        ind = next_cell.children[i].edges[0].index
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[i].index
                        V[2*ind    ] = -1.0
                        V[2*ind + 1] =  1.0
            else:
                if next_cell.is_leaf():
                    ind = cell.faces[3].index
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.index
                    V[2*ind    ] = -1.0
                    V[2*ind + 1] =  1.0
                else:
                    for i in range(4): # four neighbors in +y direction
                        ind = next_cell.children[(i>>1)*4 + i%2].faces[2].index #0, 1, 4, 5
                        I[2*ind    ] = ind
                        I[2*ind + 1] = ind
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = next_cell.children[(i>>1)*4 + i%2].index
                        V[2*ind    ] = -1.0
                        V[2*ind + 1] = 1.0

        self._cellGradyStencilMat = (
            sp.csr_matrix((V, (I,J)), shape=(self.ntFy, self.nC))
        )
        return self._cellGradyStencilMat

    @property
    @cython.boundscheck(False)
    def _cellGradzStencil(self):
        if getattr(self, '_cellGradzStencilMat', None) is not None:
            return self._cellGradzStencilMat

        cdef np.int64_t[:] I = np.zeros(2*self.ntFz, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFz, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFz, dtype=np.float64)
        cdef int_t ind

        for cell in self.tree.cells :
            next_cell = cell.neighbors[5]
            if next_cell==NULL:
                continue
            if next_cell.is_leaf():
                ind = cell.faces[5].index
                I[2*ind    ] = ind
                I[2*ind + 1] = ind
                J[2*ind    ] = cell.index
                J[2*ind + 1] = next_cell.index
                V[2*ind    ] = -1.0
                V[2*ind + 1] =  1.0
            else:
                for i in range(4): # four neighbors in +z direction
                    ind = next_cell.children[i].faces[4].index #0, 1, 2, 3
                    I[2*ind    ] = ind
                    I[2*ind + 1] = ind
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = next_cell.children[i].index
                    V[2*ind    ] = -1.0
                    V[2*ind + 1] =  1.0

        self._cellGradzStencilMat = (
            sp.csr_matrix((V, (I,J)), shape=(self.ntFz, self.nC))
        )
        return self._cellGradzStencilMat

    @cython.boundscheck(False)
    def _deflate_edges_x(self):
        #I is output index (with hanging)
        #J is input index (without hanging)
        cdef np.int64_t[:] I = np.empty(2*self.ntEx, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(2*self.ntEx, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(2*self.ntEx, dtype=np.float64)
        cdef Edge *edge
        cdef np.int64_t ii
        #x edges:
        for it in self.tree.edges_x:
            edge = it.second
            ii = edge.index
            I[2*ii    ] = ii
            I[2*ii + 1] = ii
            if edge.hanging:
                J[2*ii    ] = edge.parents[0].index
                J[2*ii + 1] = edge.parents[1].index
            else:
                J[2*ii    ] = ii
                J[2*ii + 1] = ii
            V[2*ii    ] = 0.5
            V[2*ii + 1] = 0.5
        Rh = sp.csr_matrix((V, (I, J)), shape=(self.ntEx, self.ntEx))
        # Test if it needs to be deflated again, (if any parents were also hanging)
        last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nEx)
        while(last_ind > self.nEx):
            Rh = Rh*Rh
            last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nEx)
        Rh = Rh[:, : last_ind]
        return Rh

    @cython.boundscheck(False)
    def _deflate_edges_y(self):
        #I is output index (with hanging)
        #J is input index (without hanging)
        cdef int_t dim = self._dim
        cdef np.int64_t[:] I = np.empty(2*self.ntEy, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(2*self.ntEy, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(2*self.ntEy, dtype=np.float64)
        cdef Edge *edge
        cdef np.int64_t ii
        #x edges:
        for it in self.tree.edges_y:
            edge = it.second
            ii = edge.index
            I[2*ii    ] = ii
            I[2*ii + 1] = ii
            if edge.hanging:
                J[2*ii    ] = edge.parents[0].index
                J[2*ii + 1] = edge.parents[1].index
            else:
                J[2*ii    ] = ii
                J[2*ii + 1] = ii
            V[2*ii    ] = 0.5
            V[2*ii + 1] = 0.5
        Rh = sp.csr_matrix((V, (I, J)), shape=(self.ntEy, self.ntEy))
        # Test if it needs to be deflated again, (if any parents were also hanging)
        last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nEy)
        while(last_ind > self.nEy):
            Rh = Rh*Rh
            last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nEy)
        Rh = Rh[:, : last_ind]
        return Rh

    @cython.boundscheck(False)
    def _deflate_edges_z(self):
        #I is output index (with hanging)
        #J is input index (without hanging)
        cdef int_t dim = self._dim
        cdef np.int64_t[:] I = np.empty(2*self.ntEz, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(2*self.ntEz, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(2*self.ntEz, dtype=np.float64)
        cdef Edge *edge
        cdef np.int64_t ii
        #x edges:
        for it in self.tree.edges_z:
            edge = it.second
            ii = edge.index
            I[2*ii    ] = ii
            I[2*ii + 1] = ii
            if edge.hanging:
                J[2*ii    ] = edge.parents[0].index
                J[2*ii + 1] = edge.parents[1].index
            else:
                J[2*ii    ] = ii
                J[2*ii + 1] = ii
            V[2*ii    ] = 0.5
            V[2*ii + 1] = 0.5
        Rh = sp.csr_matrix((V, (I, J)), shape=(self.ntEz, self.ntEz))
        # Test if it needs to be deflated again, (if any parents were also hanging)
        last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nEz)
        while(last_ind > self.nEz):
            Rh = Rh*Rh
            last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nEz)
        Rh = Rh[:, : last_ind]
        return Rh

    def _deflate_edges(self):
        """Returns a matrix to remove hanging edges.
        A hanging edge can either have 1 or 2 parents.
        If a hanging edge has a single parent, it's value is the same as the parent
        If a hanging edge has 2 parents, it's an average of the two parents
        """
        if self._dim == 2:
            Rx = self._deflate_edges_x()
            Ry = self._deflate_edges_y()
            return sp.block_diag((Rx, Ry))
        else:
            Rx = self._deflate_edges_x()
            Ry = self._deflate_edges_y()
            Rz = self._deflate_edges_z()
            return sp.block_diag((Rx, Ry, Rz))

    def _deflate_faces(self):
        """ Returns a matrix that removes hanging faces
        The operation assigns the hanging face the value of its parent.
        A hanging face will only ever have 1 parent.
        """
        if(self._dim == 2):
            Rx = self._deflate_edges_x()
            Ry = self._deflate_edges_y()
            return sp.block_diag((Ry, Rx))
        else:
            Rx = self._deflate_faces_x()
            Ry = self._deflate_faces_y()
            Rz = self._deflate_faces_z()
            return sp.block_diag((Rx, Ry, Rz))

    @cython.boundscheck(False)
    def _deflate_faces_x(self):
        #I is output index (with hanging)
        #J is input index (without hanging)
        cdef np.int64_t[:] I = np.empty(self.ntFx, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(self.ntFx, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(self.ntFx, dtype=np.float64)
        cdef Face *face
        cdef np.int64_t ii;

        for it in self.tree.faces_x:
            face = it.second
            ii = face.index
            I[ii] = ii
            if face.hanging:
                J[ii] = face.parent.index
            else:
                J[ii] = ii
            V[ii] = 1.0
        return sp.csr_matrix((V, (I, J)))

    @cython.boundscheck(False)
    def _deflate_faces_y(self):
        #I is output index (with hanging)
        #J is input index (without hanging)
        cdef np.int64_t[:] I = np.empty(self.ntFy, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(self.ntFy, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(self.ntFy, dtype=np.float64)
        cdef Face *face
        cdef np.int64_t ii;

        for it in self.tree.faces_y:
            face = it.second
            ii = face.index
            I[ii] = ii
            if face.hanging:
                J[ii] = face.parent.index
            else:
                J[ii] = ii
            V[ii] = 1.0
        return sp.csr_matrix((V, (I, J)))

    @cython.boundscheck(False)
    def _deflate_faces_z(self):
        #I is output index (with hanging)
        #J is input index (without hanging)
        cdef np.int64_t[:] I = np.empty(self.ntFz, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(self.ntFz, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(self.ntFz, dtype=np.float64)
        cdef Face *face
        cdef np.int64_t ii;

        for it in self.tree.faces_z:
            face = it.second
            ii = face.index
            I[ii] = ii
            if face.hanging:
                J[ii] = face.parent.index
            else:
                J[ii] = ii
            V[ii] = 1.0
        return sp.csr_matrix((V, (I, J)))

    @cython.boundscheck(False)
    def _deflate_nodes(self):
        """ Returns a matrix that removes hanging faces
        A hanging node will have 2 parents in 2D or 2 or 4 parents in 3D.
        This matrix assigns the hanging node the average value of its parents.
        """
        cdef np.int64_t[:] I = np.empty(4*self.ntN, dtype=np.int64)
        cdef np.int64_t[:] J = np.empty(4*self.ntN, dtype=np.int64)
        cdef np.float64_t[:] V = np.empty(4*self.ntN, dtype=np.float64)

        # I is output index
        # J is input index
        cdef Node *node
        cdef np.int64_t ii, i, offset
        offset = self.nN
        cdef double[4] weights

        for it in self.tree.nodes:
            node = it.second
            ii = node.index
            I[4*ii:4*ii + 4] = ii
            if node.hanging:
                J[4*ii    ] = node.parents[0].index
                J[4*ii + 1] = node.parents[1].index
                J[4*ii + 2] = node.parents[2].index
                J[4*ii + 3] = node.parents[3].index
            else:
                J[4*ii : 4*ii + 4] = ii
            V[4*ii : 4*ii + 4] = 0.25;

        Rh = sp.csr_matrix((V, (I, J)), shape=(self.ntN, self.ntN))
        # Test if it needs to be deflated again, (if any parents were also hanging)
        last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nN)
        while(last_ind > self.nN):
            Rh = Rh*Rh
            last_ind = max(np.nonzero(Rh.getnnz(0)>0)[0][-1], self.nN)
        Rh = Rh[:, : last_ind]
        return Rh

    @property
    @cython.boundscheck(False)
    def aveEx2CC(self):
        """
        Construct the averaging operator on cell edges in the x direction to
        cell centers.
        """
        if self._aveEx2CC is not None:
            return self._aveEx2CC
        cdef np.int64_t[:] I,J
        cdef np.float64_t[:] V
        cdef np.int64_t ind, ii, n_epc
        cdef double scale

        n_epc = 2*(self._dim-1)
        I = np.empty(self.nC*n_epc, dtype=np.int64)
        J = np.empty(self.nC*n_epc, dtype=np.int64)
        V = np.empty(self.nC*n_epc, dtype=np.float64)
        scale = 1.0/n_epc
        for cell in self.tree.cells:
            ind = cell.index
            for ii in range(n_epc):
                I[ind*n_epc + ii] = ind
                J[ind*n_epc + ii] = cell.edges[ii].index
                V[ind*n_epc + ii] = scale

        Rex = self._deflate_edges_x()
        self._aveEx2CC = sp.csr_matrix((V, (I, J)))*Rex
        return self._aveEx2CC

    @property
    @cython.boundscheck(False)
    def aveEy2CC(self):
        """
        Construct the averaging operator on cell edges in the y direction to
        cell centers.
        """
        if self._aveEy2CC is not None:
            return self._aveEy2CC
        cdef np.int64_t[:] I,J
        cdef np.float64_t[:] V
        cdef np.int64_t ind, ii, n_epc
        cdef double scale

        n_epc = 2*(self._dim-1)
        I = np.empty(self.nC*n_epc, dtype=np.int64)
        J = np.empty(self.nC*n_epc, dtype=np.int64)
        V = np.empty(self.nC*n_epc, dtype=np.float64)
        scale = 1.0/n_epc
        for cell in self.tree.cells:
            ind = cell.index
            for ii in range(n_epc):
                I[ind*n_epc + ii] = ind
                J[ind*n_epc + ii] = cell.edges[n_epc + ii].index #y edges
                V[ind*n_epc + ii] = scale

        Rey = self._deflate_edges_y()
        self._aveEy2CC = sp.csr_matrix((V, (I, J)))*Rey
        return self._aveEy2CC

    @property
    @cython.boundscheck(False)
    def aveEz2CC(self):
        """
        Construct the averaging operator on cell edges in the z direction to
        cell centers.
        """
        if self._aveEz2CC is not None:
            return self._aveEz2CC
        if self._dim == 2:
            raise Exception('There are no z-edges in 2D')
        cdef np.int64_t[:] I,J
        cdef np.float64_t[:] V
        cdef np.int64_t ind, ii, n_epc
        cdef double scale

        n_epc = 2*(self._dim-1)
        I = np.empty(self.nC*n_epc, dtype=np.int64)
        J = np.empty(self.nC*n_epc, dtype=np.int64)
        V = np.empty(self.nC*n_epc, dtype=np.float64)
        scale = 1.0/n_epc
        for cell in self.tree.cells:
            ind = cell.index
            for ii in range(n_epc):
                I[ind*n_epc + ii] = ind
                J[ind*n_epc + ii] = cell.edges[ii + 2*n_epc].index
                V[ind*n_epc + ii] = scale

        Rez = self._deflate_edges_z()
        self._aveEz2CC = sp.csr_matrix((V, (I, J)))*Rez
        return self._aveEz2CC

    @property
    def aveE2CC(self):
        "Construct the averaging operator on cell edges to cell centers."
        if self._aveE2CC is None:
            stacks = [self.aveEx2CC, self.aveEy2CC]
            if self._dim == 3:
                stacks += [self.aveEz2CC]
            self._aveE2CC = 1.0/self._dim * sp.hstack(stacks).tocsr()
        return self._aveE2CC

    @property
    def aveE2CCV(self):
        "Construct the averaging operator on cell edges to cell centers."
        if self._aveE2CCV is None:
            stacks = [self.aveEx2CC, self.aveEy2CC]
            if self._dim == 3:
                stacks += [self.aveEz2CC]
            self._aveE2CCV = sp.block_diag(stacks).tocsr()
        return self._aveE2CCV

    @property
    @cython.boundscheck(False)
    def aveFx2CC(self):
        """
        Construct the averaging operator on cell faces in the x direction to
        cell centers.
        """
        if self._aveFx2CC is not None:
            return self._aveFx2CC
        if self._dim == 2:
            return self.aveEy2CC

        cdef np.int64_t[:] I,J
        cdef np.float64_t[:] V
        cdef Face *face1
        cdef Face *face2
        cdef np.int64_t ii
        I = np.empty(self.nC*2, dtype=np.int64)
        J = np.empty(self.nC*2, dtype=np.int64)
        V = np.empty(self.nC*2, dtype=np.float64)

        for cell in self.tree.cells:
            face1 = cell.faces[0] # x face
            face2 = cell.faces[1] # x face
            ii = cell.index
            I[ii*2 : ii*2 + 2] = ii
            J[ii*2    ] = face1.index
            J[ii*2 + 1] = face2.index
            V[ii*2 : ii*2 + 2] = 0.5

        Rfx = self._deflate_faces_x()
        self._aveFx2CC = sp.csr_matrix((V, (I, J)))*Rfx
        return self._aveFx2CC

    @property
    @cython.boundscheck(False)
    def aveFy2CC(self):
        """
        Construct the averaging operator on cell faces in the y direction to
        cell centers.
        """
        if self._aveFy2CC is not None:
            return self._aveFy2CC
        if self._dim == 2:
            return self.aveEx2CC

        cdef np.int64_t[:] I,J
        cdef np.float64_t[:] V
        cdef Face *face1
        cdef Face *face2
        cdef np.int64_t ii
        I = np.empty(self.nC*2, dtype=np.int64)
        J = np.empty(self.nC*2, dtype=np.int64)
        V = np.empty(self.nC*2, dtype=np.float64)

        for cell in self.tree.cells:
            face1 = cell.faces[2] # y face
            face2 = cell.faces[3] # y face
            ii = cell.index
            I[ii*2 : ii*2 + 2] = ii
            J[ii*2    ] = face1.index
            J[ii*2 + 1] = face2.index
            V[ii*2 : ii*2 + 2] = 0.5

        Rfy = self._deflate_faces_y()
        self._aveFy2CC = sp.csr_matrix((V, (I, J)))*Rfy
        return self._aveFy2CC

    @property
    @cython.boundscheck(False)
    def aveFz2CC(self):
        """
        Construct the averaging operator on cell faces in the z direction to
        cell centers.
        """
        if self._aveFz2CC is not None:
            return self._aveFz2CC
        if self._dim == 2:
            raise Exception('There are no z-faces in 2D')
        cdef np.int64_t[:] I,J
        cdef np.float64_t[:] V
        cdef Face *face1
        cdef Face *face2
        cdef np.int64_t ii
        I = np.empty(self.nC*2, dtype=np.int64)
        J = np.empty(self.nC*2, dtype=np.int64)
        V = np.empty(self.nC*2, dtype=np.float64)

        for cell in self.tree.cells:
            face1 = cell.faces[4]
            face2 = cell.faces[5]
            ii = cell.index
            I[ii*2 : ii*2 + 2] = ii
            J[ii*2    ] = face1.index
            J[ii*2 + 1] = face2.index
            V[ii*2 : ii*2 + 2] = 0.5

        Rfy = self._deflate_faces_z()
        self._aveFz2CC = sp.csr_matrix((V, (I, J)))*Rfy
        return self._aveFz2CC

    @property
    def aveF2CC(self):
        "Construct the averaging operator on cell faces to cell centers."
        if self._aveF2CC is None:
            stacks = [self.aveFx2CC, self.aveFy2CC]
            if self._dim == 3:
                stacks += [self.aveFz2CC]
            self._aveF2CC = 1./self._dim*sp.hstack(stacks).tocsr()
        return self._aveF2CC

    @property
    def aveF2CCV(self):
        "Construct the averaging operator on cell faces to cell centers."
        if self._aveF2CCV is None:
            stacks = [self.aveFx2CC, self.aveFy2CC]
            if self._dim == 3:
                stacks += [self.aveFz2CC]
            self._aveF2CCV = sp.block_diag(stacks).tocsr()
        return self._aveF2CCV

    @property
    @cython.boundscheck(False)
    def aveN2CC(self):
        "Construct the averaging operator on cell nodes to cell centers."
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id, n_ppc
        cdef double scale
        if self._aveN2CC is None:
            n_ppc = 1<<self._dim
            scale = 1.0/n_ppc
            I = np.empty(self.nC*n_ppc, dtype=np.int64)
            J = np.empty(self.nC*n_ppc, dtype=np.int64)
            V = np.empty(self.nC*n_ppc, dtype=np.float64)

            for cell in self.tree.cells:
                ii = cell.index
                for id in range(n_ppc):
                    I[ii*n_ppc + id] = ii
                    J[ii*n_ppc + id] = cell.points[id].index
                    V[ii*n_ppc + id] = scale

            Rn = self._deflate_nodes()
            self._aveN2CC = sp.csr_matrix((V, (I, J)), shape=(self.nC, self.ntN))*Rn
        return self._aveN2CC

    @property
    def aveN2Ex(self):
        """
        Averaging operator on cell nodes to x-edges
        """
        if self._aveN2Ex is not None:
            return self._aveN2Ex
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id
        I = np.empty(self.nEx*2, dtype=np.int64)
        J = np.empty(self.nEx*2, dtype=np.int64)
        V = np.empty(self.nEx*2, dtype=np.float64)

        for it in self.tree.edges_x:
            edge = it.second
            if edge.hanging:
                continue
            ii = edge.index
            for id in range(2):
                I[ii*2 + id] = ii
                J[ii*2 + id] = edge.points[id].index
                V[ii*2 + id] = 0.5

        Rn = self._deflate_nodes()
        self._aveN2Ex = sp.csr_matrix((V, (I, J)), shape=(self.nEx, self.ntN))*Rn
        return self._aveN2Ex

    @property
    def aveN2Ey(self):
        """
        Averaging operator on cell nodes to y-edges
        """
        if self._aveN2Ey is not None:
            return self._aveN2Ey
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id
        I = np.empty(self.nEy*2, dtype=np.int64)
        J = np.empty(self.nEy*2, dtype=np.int64)
        V = np.empty(self.nEy*2, dtype=np.float64)

        for it in self.tree.edges_y:
            edge = it.second
            if edge.hanging:
                continue
            ii = edge.index
            for id in range(2):
                I[ii*2 + id] = ii
                J[ii*2 + id] = edge.points[id].index
                V[ii*2 + id] = 0.5

        Rn = self._deflate_nodes()
        self._aveN2Ey = sp.csr_matrix((V, (I, J)), shape=(self.nEy, self.ntN))*Rn
        return self._aveN2Ey

    @property
    def aveN2Ez(self):
        """
        Averaging operator on cell nodes to z-edges
        """
        if self._dim == 2:
            raise Exception('TreeMesh has no z-edges in 2D')
        if self._aveN2Ez is not None:
            return self._aveN2Ez
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id
        I = np.empty(self.nEz*2, dtype=np.int64)
        J = np.empty(self.nEz*2, dtype=np.int64)
        V = np.empty(self.nEz*2, dtype=np.float64)

        for it in self.tree.edges_z:
            edge = it.second
            if edge.hanging:
                continue
            ii = edge.index
            for id in range(2):
                I[ii*2 + id] = ii
                J[ii*2 + id] = edge.points[id].index
                V[ii*2 + id] = 0.5

        Rn = self._deflate_nodes()
        self._aveN2Ez = sp.csr_matrix((V, (I, J)), shape=(self.nEz, self.ntN))*Rn
        return self._aveN2Ez

    @property
    def aveN2E(self):
        """
        Construct the averaging operator on cell nodes to cell edges, keeping
        each dimension separate.
        """
        if self._aveN2E is not None:
            return self._aveN2E

        stacks = [self.aveN2Ex, self.aveN2Ey]
        if self._dim == 3:
            stacks += [self.aveN2Ez]
        self._aveN2E = sp.vstack(stacks).tocsr()
        return self._aveN2E

    @property
    def aveN2Fx(self):
        """
        Averaging operator on cell nodes to x-faces
        """
        if self._dim == 2:
            return self.aveN2Ey
        if self._aveN2Fx is not None:
            return self._aveN2Fx
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id
        I = np.empty(self.nFx*4, dtype=np.int64)
        J = np.empty(self.nFx*4, dtype=np.int64)
        V = np.empty(self.nFx*4, dtype=np.float64)

        for it in self.tree.faces_x:
            face = it.second
            if face.hanging:
                continue
            ii = face.index
            for id in range(4):
                I[ii*4 + id] = ii
                J[ii*4 + id] = face.points[id].index
                V[ii*4 + id] = 0.25

        Rn = self._deflate_nodes()
        self._aveN2Fx = sp.csr_matrix((V, (I, J)), shape=(self.nFx, self.ntN))*Rn
        return self._aveN2Fx

    @property
    def aveN2Fy(self):
        """
        Averaging operator on cell nodes to y-faces
        """
        if self._dim == 2:
            return self.aveN2Ex
        if self._aveN2Fy is not None:
            return self._aveN2Fy
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id

        I = np.empty(self.nFy*4, dtype=np.int64)
        J = np.empty(self.nFy*4, dtype=np.int64)
        V = np.empty(self.nFy*4, dtype=np.float64)

        for it in self.tree.faces_y:
            face = it.second
            if face.hanging:
                continue
            ii = face.index
            for id in range(4):
                I[ii*4 + id] = ii
                J[ii*4 + id] = face.points[id].index
                V[ii*4 + id] = 0.25

        Rn = self._deflate_nodes()
        self._aveN2Fy = sp.csr_matrix((V, (I, J)), shape=(self.nFy, self.ntN))*Rn
        return self._aveN2Fy

    @property
    def aveN2Fz(self):
        """
        Averaging operator on cell nodes to z-faces
        """
        if self._dim == 2:
            raise Exception('TreeMesh has no z faces in 2D')
        cdef np.int64_t[:] I, J
        cdef np.float64_t[:] V
        cdef np.int64_t ii, id,
        if self._aveN2Fz is not None:
            return self._aveN2Fz

        I = np.empty(self.nFz*4, dtype=np.int64)
        J = np.empty(self.nFz*4, dtype=np.int64)
        V = np.empty(self.nFz*4, dtype=np.float64)

        for it in self.tree.faces_z:
            face = it.second
            if face.hanging:
                continue
            ii = face.index
            for id in range(4):
                I[ii*4 + id] = ii
                J[ii*4 + id] = face.points[id].index
                V[ii*4 + id] = 0.25

        Rn = self._deflate_nodes()
        self._aveN2Fz = sp.csr_matrix((V, (I, J)), shape=(self.nFz, self.ntN))*Rn
        return self._aveN2Fz

    @property
    def aveN2F(self):
        """
        Construct the averaging operator on cell nodes to cell edges, keeping
        each dimension separate.
        """
        if self._aveN2F is not None:
            return self._aveN2F

        stacks = [self.aveN2Fx, self.aveN2Fy]
        if self._dim == 3:
            stacks += [self.aveN2Fz]
        self._aveN2F = sp.vstack(stacks).tocsr()
        return self._aveN2F

    @property
    def aveCC2F(self):
        "Construct the averaging operator on cell centers to cell faces."
        if self._aveCC2F is not None:
            return self._aveCC2F
        stacks = [self.aveCC2Fx, self.aveCC2Fy]
        if self._dim == 3:
            stacks.append(self.aveCC2Fz)

        self._aveCC2F = sp.vstack(stacks).tocsr()
        return self._aveCC2F

    @property
    def aveCCV2F(self):
        "Construct the averaging operator on cell centers to cell faces."
        if self._aveCCV2F is not None:
            return self._aveCCV2F
        stacks = [self.aveCC2Fx, self.aveCC2Fy]
        if self._dim == 3:
            stacks.append(self.aveCC2Fz)

        self._aveCCV2F = sp.block_diag(stacks).tocsr()
        return self._aveCCV2F

    @property
    def aveCC2Fx(self):
        "Construct the averaging operator on cell centers to cell x-faces."
        if self._aveCC2Fx is not None:
            return self._aveCC2Fx
        cdef np.int64_t[:] I = np.zeros(2*self.ntFx, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFx, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFx, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind, ind_parent
        cdef int_t children_per_parent = (dim-1)*2
        cdef c_Cell* child
        cdef c_Cell* next_cell
        cdef c_Cell* prev_cell
        cdef double w

        for cell in self.tree.cells :
            next_cell = cell.neighbors[1]
            prev_cell = cell.neighbors[0]
            # handle extrapolation to boundary faces
            if next_cell == NULL:
                if dim == 2:
                    ind = cell.edges[3].index # +x face
                else:
                    ind = cell.faces[1].index # +x face
                I[2*ind  ] = ind
                J[2*ind  ] = cell.index
                V[2*ind  ] = 1.0
                continue
            if prev_cell == NULL:
                if dim == 2:
                    ind = cell.edges[2].index # -x face
                else:
                    ind = cell.faces[0].index # -x face
                I[2*ind  ] = ind
                J[2*ind  ] = cell.index
                V[2*ind  ] = 1.0

            if next_cell.is_leaf():
                if next_cell.level == cell.level:
                    #I am on the same level and easy to interpolate
                    if dim == 2:
                        ind = cell.edges[3].index
                        w = (next_cell.location[0] - cell.edges[3].location[0])/(
                             next_cell.location[0] - cell.location[0])
                    else:
                        ind = cell.faces[1].index
                        w = (next_cell.location[0] - cell.faces[1].location[0])/(
                             next_cell.location[0] - cell.location[0])
                    I[2*ind  ] = ind
                    I[2*ind+1] = ind
                    J[2*ind  ] = cell.index
                    J[2*ind+1] = next_cell.index
                    V[2*ind  ] = w
                    V[2*ind+1] = (1.0-w)
                else:
                    # if next cell is a level larger than i am, then i need to accumulate into w
                    if dim == 2:
                        ind = cell.edges[3].index
                        ind_parent = cell.edges[3].parents[0].index
                        w = (next_cell.location[0] - cell.edges[3].location[0])/(
                             next_cell.location[0] - cell.location[0])
                    else:
                        ind = cell.faces[1].index
                        ind_parent = cell.faces[1].parent.index
                        w = (next_cell.location[0] - cell.faces[1].location[0])/(
                             next_cell.location[0] - cell.location[0])
                    I[2*ind  ] = ind_parent
                    I[2*ind+1] = ind_parent
                    J[2*ind  ] = cell.index
                    J[2*ind+1] = next_cell.index
                    V[2*ind  ] = w/children_per_parent
                    V[2*ind+1] = (1.0-w)/children_per_parent
            else:
                #should mean next cell is not a leaf so need to loop over children
                if dim == 2:
                    ind_parent = cell.edges[3].index
                    w = (next_cell.children[0].location[0] - cell.edges[3].location[0])/(
                         next_cell.children[0].location[0] - cell.location[0])
                    for i in range(2):
                        child = next_cell.children[2*i]
                        ind = child.edges[2].index
                        I[2*ind    ] = ind_parent
                        I[2*ind + 1] = ind_parent
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = child.index
                        V[2*ind    ] = w/children_per_parent
                        V[2*ind + 1] = (1.0-w)/children_per_parent
                else:
                    ind_parent = cell.faces[1].index
                    w = (next_cell.children[0].location[0] - cell.faces[1].location[0])/(
                         next_cell.children[0].location[0] - cell.location[0])
                    for i in range(4): # four neighbors in +x direction
                        child = next_cell.children[2*i] #0 2 4 6
                        ind = child.faces[0].index
                        I[2*ind    ] = ind_parent
                        I[2*ind + 1] = ind_parent
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = child.index
                        V[2*ind    ] = w/children_per_parent
                        V[2*ind + 1] = (1.0-w)/children_per_parent

        self._aveCC2Fx = sp.csr_matrix((V, (I, J)), shape=(self.nFx, self.nC))
        return self._aveCC2Fx

    @property
    def aveCC2Fy(self):
        "Construct the averaging operator on cell centers to cell y-faces."
        if self._aveCC2Fy is not None:
            return self._aveCC2Fy
        cdef np.int64_t[:] I = np.zeros(2*self.ntFy, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFy, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFy, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind, ind_parent
        cdef int_t children_per_parent = (dim-1)*2
        cdef c_Cell* child
        cdef c_Cell* next_cell
        cdef c_Cell* prev_cell
        cdef double w

        for cell in self.tree.cells :
            next_cell = cell.neighbors[3]
            prev_cell = cell.neighbors[2]
            # handle extrapolation to boundary faces
            if next_cell == NULL:
                if dim == 2:
                    ind = cell.edges[1].index
                else:
                    ind = cell.faces[3].index
                I[2*ind  ] = ind
                J[2*ind  ] = cell.index
                V[2*ind  ] = 1.0
                continue
            if prev_cell == NULL:
                if dim == 2:
                    ind = cell.edges[0].index
                else:
                    ind = cell.faces[2].index
                I[2*ind  ] = ind
                J[2*ind  ] = cell.index
                V[2*ind  ] = 1.0

            if next_cell.is_leaf():
                if next_cell.level == cell.level:
                    #I am on the same level and easy to interpolate
                    if dim == 2:
                        ind = cell.edges[1].index
                        w = (next_cell.location[1] - cell.edges[1].location[1])/(
                             next_cell.location[1] - cell.location[1])
                    else:
                        ind = cell.faces[3].index
                        w = (next_cell.location[1] - cell.faces[3].location[1])/(
                             next_cell.location[1] - cell.location[1])
                    I[2*ind  ] = ind
                    I[2*ind+1] = ind
                    J[2*ind  ] = cell.index
                    J[2*ind+1] = next_cell.index
                    V[2*ind  ] = w
                    V[2*ind+1] = (1.0-w)
                else:
                    # if next cell is a level larger than i am
                    if dim == 2:
                        ind = cell.edges[1].index
                        ind_parent = cell.edges[1].parents[0].index
                        w = (next_cell.location[1] - cell.edges[1].location[1])/(
                             next_cell.location[1] - cell.location[1])
                    else:
                        ind = cell.faces[3].index
                        ind_parent = cell.faces[3].parent.index
                        w = (next_cell.location[1] - cell.faces[3].location[1])/(
                             next_cell.location[1] - cell.location[1])
                    I[2*ind  ] = ind_parent
                    I[2*ind+1] = ind_parent
                    J[2*ind  ] = cell.index
                    J[2*ind+1] = next_cell.index
                    V[2*ind  ] = w/children_per_parent
                    V[2*ind+1] = (1.0-w)/children_per_parent
            else:
                #should mean next cell is not a leaf so need to loop over children
                if dim == 2:
                    ind_parent = cell.edges[1].index
                    w = (next_cell.children[0].location[1] - cell.edges[1].location[1])/(
                         next_cell.children[0].location[1] - cell.location[1])
                    for i in range(2):
                        child = next_cell.children[i]
                        ind = child.edges[0].index
                        I[2*ind    ] = ind_parent
                        I[2*ind + 1] = ind_parent
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = child.index
                        V[2*ind    ] = w/children_per_parent
                        V[2*ind + 1] = (1.0-w)/children_per_parent
                else:
                    ind_parent = cell.faces[3].index
                    w = (next_cell.children[0].location[1] - cell.faces[3].location[1])/(
                         next_cell.children[0].location[1] - cell.location[1])
                    for i in range(4): # four neighbors in +y direction
                        child = next_cell.children[(i>>1)*4 + i%2] #0 1 4 5
                        ind = child.faces[2].index
                        I[2*ind    ] = ind_parent
                        I[2*ind + 1] = ind_parent
                        J[2*ind    ] = cell.index
                        J[2*ind + 1] = child.index
                        V[2*ind    ] = w/children_per_parent
                        V[2*ind + 1] = (1.0-w)/children_per_parent

        self._aveCC2Fy = sp.csr_matrix((V, (I,J)), shape=(self.nFy, self.nC))
        return self._aveCC2Fy

    @property
    def aveCC2Fz(self):
        "Construct the averaging operator on cell centers to cell z-faces."
        if self.dim == 2:
            raise Exception('TreeMesh has no z-faces in 2D')
        if self._aveCC2Fz is not None:
            return self._aveCC2Fz
        cdef np.int64_t[:] I = np.zeros(2*self.ntFz, dtype=np.int64)
        cdef np.int64_t[:] J = np.zeros(2*self.ntFz, dtype=np.int64)
        cdef np.float64_t[:] V = np.zeros(2*self.ntFz, dtype=np.float64)
        cdef int dim = self._dim
        cdef int_t ind, ind_parent
        cdef int_t children_per_parent = (dim-1)*2
        cdef c_Cell* child
        cdef c_Cell* next_cell
        cdef c_Cell* prev_cell
        cdef double w

        for cell in self.tree.cells :
            next_cell = cell.neighbors[5]
            prev_cell = cell.neighbors[4]
            # handle extrapolation to boundary faces
            if next_cell == NULL:
                ind = cell.faces[5].index # +z face
                I[2*ind  ] = ind
                J[2*ind  ] = cell.index
                V[2*ind  ] = 1.0
                continue
            if prev_cell == NULL:
                ind = cell.faces[4].index # -z face
                I[2*ind  ] = ind
                J[2*ind  ] = cell.index
                V[2*ind  ] = 1.0

            if next_cell.is_leaf():
                if next_cell.level == cell.level:
                    #I am on the same level and easy to interpolate
                    ind = cell.faces[5].index
                    w = (next_cell.location[2] - cell.faces[5].location[2])/(
                         next_cell.location[2] - cell.location[2])
                    I[2*ind  ] = ind
                    I[2*ind+1] = ind
                    J[2*ind  ] = cell.index
                    J[2*ind+1] = next_cell.index
                    V[2*ind  ] = w
                    V[2*ind+1] = (1.0-w)
                else:
                    # if next cell is a level larger than i am
                    ind = cell.faces[5].index
                    ind_parent = cell.faces[5].parent.index
                    w = (next_cell.location[2] - cell.faces[5].location[2])/(
                         next_cell.location[2] - cell.location[2])
                    I[2*ind  ] = ind_parent
                    I[2*ind+1] = ind_parent
                    J[2*ind  ] = cell.index
                    J[2*ind+1] = next_cell.index
                    V[2*ind  ] = w/children_per_parent
                    V[2*ind+1] = (1.0-w)/children_per_parent
            else:
                #should mean next cell is not a leaf so need to loop over children
                ind_parent = cell.faces[5].index
                w = (next_cell.children[0].location[2] - cell.faces[5].location[2])/(
                     next_cell.children[0].location[2] - cell.location[2])
                for i in range(4): # four neighbors in +x direction
                    child = next_cell.children[i]
                    ind = child.faces[4].index #0 1 2 3
                    I[2*ind    ] = ind_parent
                    I[2*ind + 1] = ind_parent
                    J[2*ind    ] = cell.index
                    J[2*ind + 1] = child.index
                    V[2*ind    ] = w/children_per_parent
                    V[2*ind + 1] = (1.0-w)/children_per_parent

        self._aveCC2Fz = sp.csr_matrix((V, (I,J)), shape=(self.nFz, self.nC))
        return self._aveCC2Fz

    def _get_containing_cell_index(self, loc):
        cdef double x, y, z
        x = loc[0]
        y = loc[1]
        if self._dim == 3:
            z = loc[2]
        else:
            z = 0
        return self.tree.containing_cell(x, y, z).index

    def _get_containing_cell_indexes(self, locs):
        locs = np.require(np.atleast_2d(locs), dtype=np.float64, requirements='C')
        cdef double[:,:] d_locs = locs
        cdef int_t n_locs = d_locs.shape[0]
        cdef np.int64_t[:] indexes = np.empty(n_locs, dtype=np.int64)
        cdef double x, y, z
        for i in range(n_locs):
            x = d_locs[i, 0]
            y = d_locs[i, 1]
            if self._dim == 3:
                z = d_locs[i, 2]
            else:
                z = 0
            indexes[i] = self.tree.containing_cell(x, y, z).index
        if n_locs==1:
            return indexes[0]
        return np.array(indexes)

    def _count_cells_per_index(self):
        cdef np.int64_t[:] counts = np.zeros(self.max_level+1, dtype=np.int64)
        for cell in self.tree.cells:
            counts[cell.level] += 1
        return np.array(counts)

    def _cell_levels_by_indexes(self, index):
        index = np.require(np.atleast_1d(index), dtype=np.int64, requirements='C')
        cdef np.int64_t[:] inds = index
        cdef int_t n_cells = inds.shape[0]
        cdef np.int64_t[:] levels = np.empty(n_cells, dtype=np.int64)
        for i in range(n_cells):
            levels[i] = self.tree.cells[inds[i]].level
        if n_cells == 1:
            return levels[0]
        else:
            return np.array(levels)

    def _getFaceP(self, xFace, yFace, zFace):
        cdef int dim = self._dim
        cdef int_t ind, id

        cdef np.int64_t[:] I, J, J1, J2, J3
        cdef np.float64_t[:] V

        J1 = np.empty(self.nC, dtype=np.int64)
        J2 = np.empty(self.nC, dtype=np.int64)
        if dim==3:
            J3 = np.empty(self.nC, dtype=np.int64)

        cdef int[3] faces
        cdef np.int64_t[:] offsets = np.empty(self._dim, dtype=np.int64)
        faces[0] = (xFace == 'fXp')
        faces[1] = (yFace == 'fYp')
        if dim == 3:
            faces[2] = (zFace == 'fZp')

        if dim == 2:
            offsets[0] = 0
            offsets[1] = self.ntFx
        else:
            offsets[0] = 0
            offsets[1] = self.ntFx
            offsets[2] = self.ntFx + self.ntFy

        for cell in self.tree.cells:
            ind = cell.index
            if dim==2:
                J1[ind] = cell.edges[2 + faces[0]].index
                J2[ind] = cell.edges[    faces[1]].index + offsets[1]
            else:
                J1[ind] = cell.faces[    faces[0]].index
                J2[ind] = cell.faces[2 + faces[1]].index + offsets[1]
                J3[ind] = cell.faces[4 + faces[2]].index + offsets[2]

        I = np.arange(dim*self.nC, dtype=np.int64)
        if dim==2:
            J = np.r_[J1, J2]
        else:
            J = np.r_[J1, J2, J3]
        V = np.ones(self.nC*dim, dtype=np.float64)

        P = sp.csr_matrix((V, (I, J)), shape=(self._dim*self.nC, self.ntF))
        Rf = self._deflate_faces()
        return P*Rf

    def _getFacePxx(self):
        def Pxx(xFace, yFace):
            return self._getFaceP(xFace, yFace, None)
        return Pxx

    def _getFacePxxx(self):
        def Pxxx(xFace, yFace, zFace):
            return self._getFaceP(xFace, yFace, zFace)
        return Pxxx

    def _getEdgeP(self, xEdge, yEdge, zEdge):
        cdef int dim = self._dim
        cdef int_t ind, id
        cdef int epc = 1<<(dim-1) #edges per cell 2/4

        cdef np.int64_t[:] I, J, J1, J2, J3
        cdef np.float64_t[:] V

        J1 = np.empty(self.nC, dtype=np.int64)
        J2 = np.empty(self.nC, dtype=np.int64)
        if dim == 3:
            J3 = np.empty(self.nC, dtype=np.int64)

        cdef int[3] edges
        cdef np.int64_t[:] offsets = np.empty(self._dim, dtype=np.int64)
        try:
            edges[0] = int(xEdge[-1]) #0, 1, 2, 3
            edges[1] = int(yEdge[-1]) #0, 1, 2, 3
            if dim == 3:
                edges[2] = int(zEdge[-1]) #0, 1, 2, 3
        except ValueError:
            raise Exception('Last character of edge string must be 0, 1, 2, or 3')

        offsets[0] = 0
        offsets[1] = self.ntEx
        if dim==3:
            offsets[2] = self.ntEx + self.ntEy

        for cell in self.tree.cells:
            ind = cell.index
            J1[ind] = cell.edges[0*epc + edges[0]].index + offsets[0]
            J2[ind] = cell.edges[1*epc + edges[1]].index + offsets[1]
            if dim==3:
                J3[ind] = cell.edges[2*epc + edges[2]].index + offsets[2]

        I = np.arange(dim*self.nC, dtype=np.int64)
        if dim==2:
            J = np.r_[J1, J2]
        else:
            J = np.r_[J1, J2, J3]
        V = np.ones(self.nC*dim, dtype=np.float64)

        P = sp.csr_matrix((V, (I, J)), shape=(self._dim*self.nC, self.ntE))
        Rf = self._deflate_edges()
        return P*Rf

    def _getEdgePxx(self):
        def Pxx(xEdge, yEdge):
            return self._getEdgeP(xEdge, yEdge, None)
        return Pxx

    def _getEdgePxxx(self):
        def Pxxx(xEdge, yEdge, zEdge):
            return self._getEdgeP(xEdge, yEdge, zEdge)
        return Pxxx

    def _getEdgeIntMat(self, locs, zerosOutside, direction):
        cdef:
            double[:, :] locations = locs
            int_t dir, dir1, dir2
            int_t dim = self._dim
            int_t n_loc = locs.shape[0]
            int_t n_edges = 2 if self._dim == 2 else 4
            np.int64_t[:] I = np.empty(n_loc*n_edges, dtype=np.int64)
            np.int64_t[:] J = np.empty(n_loc*n_edges, dtype=np.int64)
            np.float64_t[:] V = np.empty(n_loc*n_edges, dtype=np.float64)

            int_t ii, i, j, offset
            c_Cell *cell
            double x, y, z
            double w1, w2
            double eps = 100*np.finfo(float).eps
            int zeros_out = zerosOutside

        if direction == 'x':
            dir, dir1, dir2 = 0, 1, 2
            offset = 0
        elif direction == 'y':
            dir, dir1, dir2 = 1, 0, 2
            offset = self.ntEx
        elif direction == 'z':
            dir, dir1, dir2 = 2, 0, 1
            offset = self.ntEx + self.ntEy
        else:
            raise ValueError('Invalid direction, must be x, y, or z')

        for i in range(n_loc):
            x = locations[i, 0]
            y = locations[i, 1]
            z = locations[i, 2] if dim==3 else 0.0
            #get containing (or closest) cell
            cell = self.tree.containing_cell(x, y, z)
            for j in range(n_edges):
                I[n_edges*i+j] = i
                J[n_edges*i+j] = cell.edges[n_edges*dir+j].index + offset

            w1 = ((cell.edges[n_edges*dir+1].location[dir1] - locations[i, dir1])/
                  (cell.edges[n_edges*dir+1].location[dir1] - cell.edges[n_edges*dir].location[dir1]))
            if dim == 3:
                w2 = ((cell.edges[n_edges*dir+3].location[dir2] - locations[i, dir2])/
                      (cell.edges[n_edges*dir+3].location[dir2] - cell.edges[n_edges*dir].location[dir2]))
            else:
                w2 = 1.0
            if zeros_out:
                if (w1 < -eps or w1 > 1 + eps or w2 < -eps or w2 > eps):
                    for j in range(n_edges):
                        V[n_edges*i + j] = 0.0
                    continue
            w1 = _clip01(w1)
            w2 = _clip01(w2)

            V[n_edges*i  ] = w1*w2
            V[n_edges*i+1] = (1.0-w1)*w2
            if dim == 3:
                V[n_edges*i+2] = w1*(1.0-w2)
                V[n_edges*i+3] = (1.0-w1)*(1.0-w2)

        Re = self._deflate_edges()
        A = sp.csr_matrix((V, (I, J)), shape=(locs.shape[0], self.ntE))
        return A*Re

    def _getFaceIntMat(self, locs, zerosOutside, direction):
        cdef:
            double[:, :] locations = locs
            int_t dir, dir2d
            int_t dim = self._dim
            int_t n_loc = locs.shape[0]
            int_t n_faces = 2
            np.int64_t[:] I = np.empty(n_loc*n_faces, dtype=np.int64)
            np.int64_t[:] J = np.empty(n_loc*n_faces, dtype=np.int64)
            np.float64_t[:] V = np.empty(n_loc*n_faces, dtype=np.float64)

            int_t ii, i, offset
            c_Cell *cell
            double x, y, z
            double w
            double eps = 100*np.finfo(float).eps
            int zeros_out = zerosOutside

        if direction == 'x':
            dir = 0
            dir2d = 1
            offset = 0
        elif direction == 'y':
            dir = 1
            dir2d = 0
            offset = self.ntFx
        elif direction == 'z':
            dir = 2
            offset = self.ntFx + self.ntFy
        else:
            raise ValueError('Invalid direction, must be x, y, or z')

        for i in range(n_loc):
            x = locations[i, 0]
            y = locations[i, 1]
            z = locations[i, 2] if dim==3 else 0.0
            #get containing (or closest) cell
            cell = self.tree.containing_cell(x, y, z)
            I[n_faces*i  ] = i
            I[n_faces*i+1] = i
            if self._dim == 3:
                J[n_faces*i  ] = cell.faces[dir*2  ].index + offset
                J[n_faces*i+1] = cell.faces[dir*2+1].index + offset
                w = ((cell.faces[dir*2+1].location[dir] - locations[i, dir])/
                      (cell.faces[dir*2+1].location[dir] - cell.faces[dir*2].location[dir]))
            else:
                J[n_faces*i  ] = cell.edges[dir2d*2  ].index + offset
                J[n_faces*i+1] = cell.edges[dir2d*2+1].index + offset
                w = ((cell.edges[dir2d*2+1].location[dir] - locations[i, dir])/
                      (cell.edges[dir2d*2+1].location[dir] - cell.edges[dir2d*2].location[dir]))
            if zeros_out:
                if (w < -eps or w > 1 + eps):
                    V[n_faces*i  ] = 0.0
                    V[n_faces*i+1] = 0.0
                    continue
            w = _clip01(w)
            V[n_faces*i  ] = w
            V[n_faces*i+1] = 1.0-w

        Rf = self._deflate_faces()
        return sp.csr_matrix((V, (I, J)), shape=(locs.shape[0], self.ntF))*Rf

    def _getNodeIntMat(self, locs, zerosOutside):
        cdef:
            double[:, :] locations = locs
            int_t dim = self._dim
            int_t n_loc = locs.shape[0]
            int_t n_nodes = 1<<dim
            np.int64_t[:] I = np.empty(n_loc*n_nodes, dtype=np.int64)
            np.int64_t[:] J = np.empty(n_loc*n_nodes, dtype=np.int64)
            np.float64_t[:] V = np.empty(n_loc*n_nodes, dtype=np.float64)

            int_t ii, i
            c_Cell *cell
            double x, y, z
            double wx, wy, wz
            double eps = 100*np.finfo(float).eps
            int zeros_out = zerosOutside

        for i in range(n_loc):
            x = locations[i, 0]
            y = locations[i, 1]
            z = locations[i, 2] if dim==3 else 0.0
            #get containing (or closest) cell
            cell = self.tree.containing_cell(x, y, z)
            #calculate weights
            wx = ((cell.points[3].location[0] - x)/
                  (cell.points[3].location[0] - cell.points[0].location[0]))
            wy = ((cell.points[3].location[1] - y)/
                  (cell.points[3].location[1] - cell.points[0].location[1]))
            if dim == 3:
                wz = ((cell.points[7].location[2] - z)/
                      (cell.points[7].location[2] - cell.points[0].location[2]))
            else:
                wz = 1.0


            I[n_nodes*i:n_nodes*i + n_nodes] = i


            if zeros_out:
                if (wx < -eps or wy < -eps or wz < -eps or
                    wx>1 + eps or wy > 1 + eps or wz > 1 + eps):
                    for ii in range(n_nodes):
                        J[n_nodes*i + ii] = 0
                        V[n_nodes*i + ii] = 0.0
                    continue

            wx = _clip01(wx)
            wy = _clip01(wy)
            wz = _clip01(wz)
            for ii in range(n_nodes):
                J[n_nodes*i + ii] = cell.points[ii].index

            V[n_nodes*i    ] = wx*wy*wz
            V[n_nodes*i + 1] = (1 - wx)*wy*wz
            V[n_nodes*i + 2] = wx*(1 - wy)*wz
            V[n_nodes*i + 3] = (1 - wx)*(1 - wy)*wz
            if dim==3:
                V[n_nodes*i + 4] = wx*wy*(1 - wz)
                V[n_nodes*i + 5] = (1 - wx)*wy*(1 - wz)
                V[n_nodes*i + 6] = wx*(1 - wy)*(1 - wz)
                V[n_nodes*i + 7] = (1 - wx)*(1 - wy)*(1 - wz)

        Rn = self._deflate_nodes()
        return sp.csr_matrix((V, (I, J)), shape=(locs.shape[0],self.ntN))*Rn

    def _getCellIntMat(self, locs, zerosOutside):
        cdef:
            double[:, :] locations = locs
            int_t dim = self._dim
            int_t n_loc = locations.shape[0]
            np.int64_t[:] I = np.arange(n_loc, dtype=np.int64)
            np.int64_t[:] J = np.empty(n_loc, dtype=np.int64)
            np.float64_t[:] V = np.ones(n_loc, dtype=np.float64)

            int_t ii, i
            c_Cell *cell
            double x, y, z
            double eps = 100*np.finfo(float).eps
            int zeros_out = zerosOutside

        for i in range(n_loc):
            x = locations[i, 0]
            y = locations[i, 1]
            z = locations[i, 2] if dim==3 else 0.0
            # get containing (or closest) cell
            cell = self.tree.containing_cell(x, y, z)
            J[i] = cell.index
            if zeros_out:
                if x < cell.points[0].location[0]-eps:
                    V[i] = 0.0
                elif x > cell.points[3].location[0]+eps:
                    V[i] = 0.0
                elif y < cell.points[0].location[1]-eps:
                    V[i] = 0.0
                elif y > cell.points[3].location[1]+eps:
                    V[i] = 0.0
                elif dim == 3 and z < cell.points[0].location[2]-eps:
                    V[i] = 0.0
                elif dim == 3 and z > cell.points[7].location[2]+eps:
                    V[i] = 0.0

        return sp.csr_matrix((V, (I, J)), shape=(locs.shape[0],self.nC))

    @requires({'matplotlib': matplotlib})
    def plotGrid(self,
        ax=None, nodes=False, faces=False, centers=False, edges=False,
        lines=True, cell_line=False,
        faces_x=False, faces_y=False, faces_z=False,
        edges_x=False, edges_y=False, edges_z=False,
        show_it=False, **kwargs):
        """ Plot the nodel, cell-centered, and staggered grids for 2 and 3 dimensions
        Plots the mesh grid in either 2D or 3D of the TreeMesh

        Parameters
        ----------
        ax : matplotlib.axes.Axes or None, optional
            The axes handle to plot on
        nodes : bool, optional
            Plot the nodal points
        faces : bool, optional
            Plot the center points of the faces
        centers : bool, optional
            Plot the center points of the cells
        edges : bool, optional
            Plot the center points of the edges
        lines : bool, optional
            Plot the lines connecting the nodes
        cell_line : bool, optional
            Plot the line through the cell centers in order
        faces_x, faces_y, faces_z : bool, optional
            Plot the center points of the x, y, or z faces
        edges_x, edges_y, edges_z : bool, optional
            Plot the center points of the x, y, or z edges
        show_it : bool, optional
            whether to call plt.show() within the codes
        color : Color or str, optional
            if lines=True, the color of the lines, defaults to first color.
        linewidth : float, optional
            if lines=True, the linewidth for the lines.

        Returns
        -------
        matplotlib.axes.Axes
            Axes handle for the plot

        """
        if "showIt" in kwargs:
            show_it = kwargs["showIt"]
            warnings.warn("showIt has been deprecated, please use show_it", DeprecationWarning)

        if ax is None:
            if(self._dim == 2):
                ax = plt.subplot(111)
            else:
                ax = plt.subplot(111, projection='3d')
        else:
            if not isinstance(ax, matplotlib.axes.Axes):
                raise TypeError("ax must be a matplotlib.axes.Axes")
            fig = ax.figure

        if faces:
            faces_x = faces_y = True
            if self._dim==3:
                faces_z = True
        if edges:
            edges_x = edges_y = True
            if self._dim==3:
                edges_z = True

        cdef:
            int_t i, offset
            Node *p1
            Node *p2
            Edge *edge

        if nodes:
            ax.plot(
                *np.r_[self.gridN, self.gridhN].T, color="C0", marker='s',
                linestyle="")
            # Hanging Nodes
            ax.plot(*self.gridhN.T, color="C0", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C0')
        if centers:
            ax.plot(*self.gridCC.T, color="C1", marker="o", linestyle="")
        if cell_line:
            ax.plot(*self.gridCC.T, color="C1", linestyle=":")
            ax.plot(
                self.gridCC[[0,-1],0], self.gridCC[[0,-1],1],
                color="C1", marker='o', linestyle="")

        y_mark = "<" if self._dim==3 else "^"

        if faces_x:
            ax.plot(*np.r_[self.gridFx, self.gridhFx].T,
                    color="C2", marker=">", linestyle="")
            # Hanging Faces x
            ax.plot(*self.gridhFx.T, color="C2", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C2')
        if faces_y:
            ax.plot(*np.r_[self.gridFy, self.gridhFy].T,
                    color="C2", marker=y_mark, linestyle="")
            # Hanging Faces y
            ax.plot(*self.gridhFy.T, color="C2", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C2')
        if faces_z:
            ax.plot(*np.r_[self.gridFz, self.gridhFz].T,
                    color="C2", marker="^", linestyle="")
            # Hangin Faces z
            ax.plot(*self.gridhFz.T, color="C2", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C2')
        if edges_x:
            ax.plot(*np.r_[self.gridEx, self.gridhEx].T,
                    color="C3", marker=">", linestyle="")
            # Hanging Edges x
            ax.plot(*self.gridhEx.T, color="C3", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C3')
        if edges_y:
            ax.plot(*np.r_[self.gridEy, self.gridhEy].T,
                    color="C3", marker=y_mark, linestyle="")
            # Hanging Edges y
            ax.plot(*self.gridhEy.T, color="C3", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C3')
        if edges_z:
            ax.plot(*np.r_[self.gridEz, self.gridhEz].T,
                    color="C3", marker="^", linestyle="")
            # Hanging Edges z
            ax.plot(*self.gridhEz.T, color="C3", marker='s', linestyle="",
                    markersize=10, markerfacecolor='none', markeredgecolor='C3')

        if lines:
            color = kwargs.get('color', 'C0')
            linewidth = kwargs.get('linewidth', 1.)
            if(self._dim) == 2:
                X = np.empty((self.nE*3))
                Y = np.empty((self.nE*3))
                for it in self.tree.edges_x:
                    edge = it.second
                    if(edge.hanging): continue
                    i = edge.index*3
                    p1 = edge.points[0]
                    p2 = edge.points[1]
                    X[i:i + 3] = [p1.location[0], p2.location[0], np.nan]
                    Y[i:i + 3] = [p1.location[1], p2.location[1], np.nan]

                offset = self.nEx
                for it in self.tree.edges_y:
                    edge = it.second
                    if(edge.hanging): continue
                    i = (edge.index + offset)*3
                    p1 = edge.points[0]
                    p2 = edge.points[1]
                    X[i : i+3] = [p1.location[0], p2.location[0], np.nan]
                    Y[i : i+3] = [p1.location[1], p2.location[1], np.nan]

                ax.plot(X, Y, color=color, linestyle="-", lw=linewidth)
            else:
                X = np.empty((self.nE*3))
                Y = np.empty((self.nE*3))
                Z = np.empty((self.nE*3))
                for it in self.tree.edges_x:
                    edge = it.second
                    if(edge.hanging): continue
                    i = edge.index*3
                    p1 = edge.points[0]
                    p2 = edge.points[1]
                    X[i : i+3] = [p1.location[0], p2.location[0], np.nan]
                    Y[i : i+3] = [p1.location[1], p2.location[1], np.nan]
                    Z[i : i+3] = [p1.location[2], p2.location[2], np.nan]

                offset = self.nEx
                for it in self.tree.edges_y:
                    edge = it.second
                    if(edge.hanging): continue
                    i = (edge.index+offset)*3
                    p1 = edge.points[0]
                    p2 = edge.points[1]
                    X[i : i+3] = [p1.location[0], p2.location[0], np.nan]
                    Y[i : i+3] = [p1.location[1], p2.location[1], np.nan]
                    Z[i : i+3] = [p1.location[2], p2.location[2], np.nan]

                offset += self.nEy
                for it in self.tree.edges_z:
                    edge = it.second
                    if(edge.hanging): continue
                    i = (edge.index + offset)*3
                    p1 = edge.points[0]
                    p2 = edge.points[1]
                    X[i : i+3] = [p1.location[0], p2.location[0], np.nan]
                    Y[i : i+3] = [p1.location[1], p2.location[1], np.nan]
                    Z[i : i+3] = [p1.location[2], p2.location[2], np.nan]

                ax.plot(X, Y, Z, color=color, linestyle="-", lw=linewidth)

        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        if self._dim == 3:
            ax.set_zlabel('x3')

        ax.grid(True)
        if show_it:
            plt.show()

        return ax

    @requires({'matplotlib': matplotlib})
    def plotImage(self, v, v_type='CC', grid=False, view='real',
                  ax=None, clim=None, show_it=False,
                  pcolor_opts=None,
                  grid_opts=None,
                  range_x=None, range_y=None,
                  **kwargs,
                  ):
        """ Plots an image of values defined on the TreeMesh
        If 3D, this function plots a default slice of the TreeMesh

        Parameters
        ----------
        v : array_like
            Array containing the values to plot
        v_type : str, optional
            type of value in `v` one of 'CC', 'N', 'Fx', 'Fy', 'Fz', 'Ex', 'Ey', or 'Ez'
        grid : bool, optional
            plot the grid lines
        view : ['real', 'imag', 'abs'], optional
            The values to plot from v
        ax : matplotlib.axes.Axes or None, optional
            The axes handle
        clim : array_like of length 2, or None, optional
            A pair of [min, max] for the Colorbar
        pcolor_opts : dict, or None
            options to be passed on to pcolormesh
        gridOpt : dict, or None
            options for the plotting the grid
        range_x, range_y: array_like, optional
            pairs of [min, max] values for the x and y ranges
        """
        if self._dim == 3:
            self.plotSlice(v, v_type=v_type, grid=grid, view=view,
                           ax=ax, clim=clim, show_it=show_it,
                           pcolor_opts=pcolor_opts,
                           range_x=range_x, range_y=range_y,
                           **kwargs)

        if view == 'vec':
            raise NotImplementedError('Vector ploting is not supported on TreeMesh (yet)')

        if view in ['real', 'imag', 'abs']:
            v = getattr(np, view)(v) # e.g. np.real(v)
        if v_type == 'CC':
            I = v
        elif v_type == 'N':
            I = self.aveN2CC*v
        elif v_type in ['Fx', 'Fy', 'Ex', 'Ey']:
            aveOp = 'ave' + v_type[0] + '2CCV'
            ind_xy = {'x': 0, 'y': 1}[v_type[1]]
            I = (getattr(self, aveOp)*v).reshape(2, self.nC)[ind_xy] # average to cell centers

        if "pcolorOpts" in kwargs:
            pcolor_opts = kwargs["pcolorOpts"]
            warnings.warn("pcolorOpts has been deprecated, please use pcolor_opts", DeprecationWarning)
        if "gridOpts" in kwargs:
            grid_opts = kwargs["gridOpts"]
            warnings.warn("gridOpts has been deprecated, please use grid_opts", DeprecationWarning)
        if "showIt" in kwargs:
            show_it = kwargs["showIt"]
            warnings.warn("showIt has been deprecated, please use show_it", DeprecationWarning)
        if "vType" in kwargs:
            v_type = kwargs["vType"]
            warnings.warn("vType has been deprecated, please use v_type", DeprecationWarning)

        if ax is None:
            ax = plt.subplot(111)
        if pcolor_opts is None:
            pcolor_opts = {}
        if 'cmap' in pcolor_opts:
            cm = pcolor_opts['cmap']
        else:
            cm = plt.get_cmap()
        if 'vmin' in pcolor_opts:
            vmin = pcolor_opts['vmin']
        else:
            vmin = np.nanmin(I) if clim is None else clim[0]
        if 'vmax' in pcolor_opts:
            vmax = pcolor_opts['vmax']
        else:
            vmax = np.nanmax(I) if clim is None else clim[1]
        if 'alpha' in pcolor_opts:
            alpha = pcolor_opts['alpha']
        else:
            alpha = 1.0

        if grid_opts is None:
            grid_opts = {'color':'k'}
        if 'color' not in grid_opts:
            grid_opts['color'] = 'k'

        if 'norm' in pcolor_opts:
           cNorm = pcolor_opts['norm']
        else:
           cNorm = colors.Normalize(vmin=vmin, vmax=vmax)

        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

        if 'edge_color' in pcolor_opts:
            edge_color = pcolor_opts['edge_color']
        else:
            edge_color = grid_opts['color'] if grid else 'none'
        if 'alpha' in grid_opts:
            edge_alpha = grid_opts['alpha']
        else:
            edge_alpha = 1.0
        if edge_color.lower() != 'none':
            if isinstance(edge_color, str):
                edge_color = colors.to_rgba(edge_color, edge_alpha)
            else:
                edge_color = colors.to_rgba_array(edge_color, edge_alpha)

        rectangles = []
        facecolors = scalarMap.to_rgba(I[~np.isnan(I)])
        facecolors[:,-1] = alpha
        for cell in self.tree.cells:
            ii = cell.index
            if np.isnan(I[ii]):
                continue
            x0 = np.array([cell.points[0].location[0], cell.points[0].location[1]])
            sz = np.array([cell.edges[0].length, cell.edges[2].length])
            rectangles.append(plt.Rectangle((x0[0], x0[1]), sz[0], sz[1]))

        pc = PatchCollection(rectangles, facecolor=facecolors, edgecolor=edge_color)
        # Add collection to axes
        ax.add_collection(pc)
        # http://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots
        scalarMap._A = []
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        if range_x is not None:
            ax.set_xlim(*range_x)
        else:
            ax.set_xlim(*self.vectorNx[[0, -1]])

        if range_y is not None:
            ax.set_ylim(*range_y)
        else:
            ax.set_ylim(*self.vectorNy[[0, -1]])

        if show_it:
            plt.show()
        return [scalarMap]

    def __getstate__(self):
        cdef int id, dim = self._dim
        indArr = np.empty((self.nC, dim), dtype=np.int)
        levels = np.empty((self.nC), dtype=np.int)
        cdef np.int_t[:, :] _indArr = indArr
        cdef np.int_t[:] _levels = levels
        for cell in self.tree.cells:
            for id in range(dim):
                _indArr[cell.index, id] = cell.location_ind[id]
            _levels[cell.index] = cell.level
        return indArr, levels

    def __setstate__(self, state):
        indArr, levels = state
        indArr = np.asarray(indArr)
        levels = np.asarray(levels)
        xs = np.array(self._xs)
        ys = np.array(self._ys)
        if self._dim == 3:
            zs = np.array(self._zs)
            points = np.column_stack((xs[indArr[:, 0]],
                                      ys[indArr[:, 1]],
                                      zs[indArr[:, 2]]))
        else:
            points = np.column_stack((xs[indArr[:, 0]], ys[indArr[:, 1]]))
        self.insert_cells(points, levels)

    def __len__(self):
        return self.nC

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Get the start, stop, and step from the slice
            return [self[ii] for ii in range(*key.indices(len(self)))]
        elif isinstance(key, (*integer_types, np.integer)):
            if key < 0:  # Handle negative indices
                key += len(self)
            if key >= len(self):
                raise IndexError(
                    "The index ({0:d}) is out of range.".format(key)
                )
            pycell = TreeCell()
            pycell._set(self.tree.cells[key])
            return pycell
        else:
            raise TypeError("Invalid argument type.")

    @property
    def _ubc_indArr(self):
        if self.__ubc_indArr is not None:
            return self.__ubc_indArr
        indArr, levels = self.__getstate__()

        max_level = self.tree.max_level

        levels = 1<<(max_level - levels)

        if self.dim == 2:
            indArr[:, -1] = (self._ys.shape[0]-1) - indArr[:, -1]
        else:
            indArr[:, -1] = (self._zs.shape[0]-1) - indArr[:, -1]

        indArr = (indArr - levels[:, None])//2
        indArr += 1

        self.__ubc_indArr = (indArr, levels)
        return self.__ubc_indArr

    @property
    def _ubc_order(self):
        if self.__ubc_order is not None:
            return self.__ubc_order
        indArr, _ = self._ubc_indArr
        if self.dim == 2:
            self.__ubc_order = np.lexsort((indArr[:, 0], indArr[:, 1]))
        else:
            self.__ubc_order = np.lexsort((indArr[:, 0], indArr[:, 1], indArr[:, 2]))
        return self.__ubc_order

    def __dealloc__(self):
        del self.tree
        del self.wrapper

    @cython.boundscheck(False)
    @cython.cdivision(True)
    def _vol_avg_from_tree(self, _TreeMesh meshin, values=None, output=None):
        # first check if they have the same tensor base, as it makes it a lot easier...
        cdef int_t same_base
        try:
            same_base = (
                np.allclose(self.vectorNx, meshin.vectorNx)
                and np.allclose(self.vectorNy, meshin.vectorNy)
                and (self.dim == 2 or np.allclose(self.vectorNz, meshin.vectorNz))
            )
        except ValueError:
            same_base = False
        cdef c_Cell * out_cell
        cdef c_Cell * in_cell

        cdef np.float64_t[:] vals = np.array([])
        cdef np.float64_t[:] outs = np.array([])
        cdef int_t build_mat = 1

        if values is not None:
            vals = values
            if output is None:
                output = np.empty(self.nC)
            output[:] = 0
            outs = output

            build_mat = 0

        cdef vector[int_t] row_inds, col_inds
        cdef vector[int_t] indptr
        cdef vector[double] all_weights

        cdef vector[int_t] *overlapping_cells
        cdef double *weights
        cdef double over_lap_vol
        cdef double x1m, x1p, y1m, y1p, z1m, z1p
        cdef double x2m, x2p, y2m, y2p, z2m, z2p
        cdef double[:] x0 = meshin._x0
        cdef double[:] xF
        if self.dim == 2:
            xF = np.array([meshin._xs[-1], meshin._ys[-1]])
        else:
            xF = np.array([meshin._xs[-1], meshin._ys[-1], meshin._zs[-1]])

        cdef int_t nnz_counter = 0
        cdef int_t nnz_row = 0
        if build_mat:
            indptr.push_back(0)
        cdef int_t i, in_cell_ind
        cdef int_t n_overlap
        cdef double weight_sum
        cdef double weight
        cdef vector[int_t] out_visited
        cdef int_t n_unvisited

        # easier path if they share the same base:
        if same_base:
            if build_mat:
                all_weights.resize(meshin.nC, 0.0)
                row_inds.resize(meshin.nC, 0)
            out_visited.resize(self.nC, 0)
            for in_cell in meshin.tree.cells:
                # for each input cell find containing output cell
                out_cell = self.tree.containing_cell(
                    in_cell.location[0],
                    in_cell.location[1],
                    in_cell.location[2]
                )
                # if containing output cell is lower level (larger) than input cell:
                # contribution is related to difference of levels (aka ratio of volumes)
                # else:
                # contribution is 1.0
                if out_cell.level < in_cell.level:
                    out_visited[out_cell.index] = 1
                    weight = in_cell.volume/out_cell.volume
                    if not build_mat:
                        outs[out_cell.index] += weight*vals[in_cell.index]
                    else:
                        all_weights[in_cell.index] = weight
                        row_inds[in_cell.index] = out_cell.index

            if build_mat:
                P = sp.csr_matrix((all_weights, (row_inds, np.arange(meshin.nC))),
                                  shape=(self.nC, meshin.nC))

                n_unvisited = self.nC - np.sum(out_visited)
                row_inds.resize(n_unvisited, 0)
                col_inds.resize(n_unvisited, 0)
            i = 0
            # assign weights of 1 to unvisited output cells and find their containing cell
            for out_cell in self.tree.cells:
                if not out_visited[out_cell.index]:
                    in_cell = meshin.tree.containing_cell(
                        out_cell.location[0],
                        out_cell.location[1],
                        out_cell.location[2]
                    )

                    if not build_mat:
                        outs[out_cell.index] = vals[in_cell.index]
                    else:
                        row_inds[i] = out_cell.index
                        col_inds[i] = in_cell.index
                        i += 1
            if build_mat and n_unvisited > 0:
                P += sp.csr_matrix(
                    (np.ones(n_unvisited), (row_inds, col_inds)),
                    shape=(self.nC, meshin.nC)
                )
            if not build_mat:
                return output
            return P

        for cell in self.tree.cells:
            x1m = min(cell.points[0].location[0], xF[0])
            y1m = min(cell.points[0].location[1], xF[1])

            x1p = max(cell.points[3].location[0], x0[0])
            y1p = max(cell.points[3].location[1], x0[1])
            if self._dim==3:
                z1m = min(cell.points[0].location[2], xF[2])
                z1p = max(cell.points[7].location[2], x0[2])
            overlapping_cell_inds = meshin.tree.find_overlapping_cells(x1m, x1p, y1m, y1p, z1m, z1p)
            n_overlap = overlapping_cell_inds.size()
            weights = <double *> malloc(n_overlap*sizeof(double))
            i = 0
            weight_sum = 0.0
            nnz_row = 0
            for in_cell_ind in overlapping_cell_inds:
                in_cell = meshin.tree.cells[in_cell_ind]
                x2m = in_cell.points[0].location[0]
                y2m = in_cell.points[0].location[1]
                z2m = in_cell.points[0].location[2]
                x2p = in_cell.points[3].location[0]
                y2p = in_cell.points[3].location[1]
                z2p = in_cell.points[7].location[2] if self._dim==3 else 0.0

                if x1m == xF[0] or x1p == x0[0]:
                    over_lap_vol = 1.0
                else:
                    over_lap_vol = min(x1p, x2p) - max(x1m, x2m)
                if y1m == xF[1] or y1p == x0[1]:
                    over_lap_vol *= 1.0
                else:
                    over_lap_vol *= min(y1p, y2p) - max(y1m, y2m)
                if self._dim==3:
                    if z1m == xF[2] or z1p == x0[2]:
                        over_lap_vol *= 1.0
                    else:
                        over_lap_vol *= min(z1p, z2p) - max(z1m, z2m)

                weights[i] = over_lap_vol
                if build_mat and weights[i] != 0.0:
                    nnz_row += 1
                    row_inds.push_back(in_cell_ind)

                weight_sum += weights[i]
                i += 1
            for i in range(n_overlap):
                weights[i] /= weight_sum
                if build_mat and weights[i] != 0.0:
                    all_weights.push_back(weights[i])

            if not build_mat:
                for i in range(n_overlap):
                    outs[cell.index] += vals[overlapping_cell_inds[i]]*weights[i]
            else:
                nnz_counter += nnz_row
                indptr.push_back(nnz_counter)

            free(weights)
            overlapping_cell_inds.clear()

        if not build_mat:
            return output
        return sp.csr_matrix((all_weights, row_inds, indptr), shape=(self.nC, meshin.nC))

    @cython.boundscheck(False)
    @cython.cdivision(True)
    def _vol_avg_to_tens(self, out_tens_mesh, values=None, output=None):
        cdef vector[int_t] *overlapping_cells
        cdef double *weights
        cdef double over_lap_vol
        cdef double x1m, x1p, y1m, y1p, z1m, z1p
        cdef double x2m, x2p, y2m, y2p, z2m, z2p
        cdef double[:] x0
        cdef double[:] xF

        # first check if they have the same tensor base, as it makes it a lot easier...
        cdef int_t same_base
        try:
            same_base = (
                np.allclose(self.vectorNx, out_tens_mesh.vectorNx)
                and np.allclose(self.vectorNy, out_tens_mesh.vectorNy)
                and (self.dim == 2 or np.allclose(self.vectorNz, out_tens_mesh.vectorNz))
            )
        except ValueError:
            same_base = False

        if same_base:
            in_cell_inds = self._get_containing_cell_indexes(out_tens_mesh.gridCC)
            # Every cell input cell is gauranteed to be a lower level than the output tenser mesh
            # therefore all weights a 1.0
            if values is not None:
                if output is None:
                    output = np.empty(out_tens_mesh.nC)
                output[:] = values[in_cell_inds]
                return output
            return sp.csr_matrix(
                (np.ones(out_tens_mesh.nC), (np.arange(out_tens_mesh.nC), in_cell_inds)),
                shape=(out_tens_mesh.nC, self.nC)
            )

        if self.dim == 2:
            x0 = np.r_[self.x0, 0.0]
            xF = np.array([self._xs[-1], self._ys[-1], 0.0])
        else:
            x0 = self._x0
            xF = np.array([self._xs[-1], self._ys[-1], self._zs[-1]])
        cdef c_Cell * in_cell

        cdef np.float64_t[:] vals = np.array([])
        cdef np.float64_t[::1, :, :] outs = np.array([[[]]])

        cdef vector[int_t] row_inds
        cdef vector[int_t] indptr
        cdef vector[double] all_weights
        cdef int_t nnz_row = 0
        cdef int_t nnz_counter = 0

        cdef double[:] nodes_x = out_tens_mesh.vectorNx
        cdef double[:] nodes_y = out_tens_mesh.vectorNy
        cdef double[:] nodes_z = np.array([0.0, 0.0])
        if self._dim==3:
            nodes_z = out_tens_mesh.vectorNz
        cdef int_t nx = len(nodes_x)-1
        cdef int_t ny = len(nodes_y)-1
        cdef int_t nz = len(nodes_z)-1

        cdef int_t build_mat = 1
        if values is not None:
            vals = values
            if output is None:
                output = np.empty((nx, ny, nz), order='F')
            else:
                output = output.reshape((nx, ny, nz), order='F')
            output[:] = 0
            outs = output

            build_mat = 0
        if build_mat:
            indptr.push_back(0)

        cdef int_t ix, iy, iz, in_cell_ind, i
        cdef int_t n_overlap
        cdef double weight_sum

        #for cell in self.tree.cells:
        for iz in range(nz):
            z1m = min(nodes_z[iz], xF[2])
            z1p = max(nodes_z[iz+1], x0[2])
            for iy in range(ny):
                y1m = min(nodes_y[iy], xF[1])
                y1p = max(nodes_y[iy+1], x0[1])
                for ix in range(nx):
                    x1m = min(nodes_x[ix], xF[0])
                    x1p = max(nodes_x[ix+1], x0[0])
                    overlapping_cell_inds = self.tree.find_overlapping_cells(x1m, x1p, y1m, y1p, z1m, z1p)
                    n_overlap = overlapping_cell_inds.size()
                    weights = <double *> malloc(n_overlap*sizeof(double))
                    i = 0
                    weight_sum = 0.0
                    nnz_row = 0
                    for in_cell_ind in overlapping_cell_inds:
                        in_cell = self.tree.cells[in_cell_ind]
                        x2m = in_cell.points[0].location[0]
                        y2m = in_cell.points[0].location[1]
                        z2m = in_cell.points[0].location[2]
                        x2p = in_cell.points[3].location[0]
                        y2p = in_cell.points[3].location[1]
                        z2p = in_cell.points[7].location[2] if self._dim==3 else 0.0

                        if x1m == xF[0] or x1p == x0[0]:
                            over_lap_vol = 1.0
                        else:
                            over_lap_vol = min(x1p, x2p) - max(x1m, x2m)
                        if y1m == xF[1] or y1p == x0[1]:
                            over_lap_vol *= 1.0
                        else:
                            over_lap_vol *= min(y1p, y2p) - max(y1m, y2m)
                        if self._dim==3:
                            if z1m == xF[2] or z1p == x0[2]:
                                over_lap_vol *= 1.0
                            else:
                                over_lap_vol *= min(z1p, z2p) - max(z1m, z2m)

                        weights[i] = over_lap_vol
                        if build_mat and weights[i] != 0.0:
                            nnz_row += 1
                            row_inds.push_back(in_cell_ind)
                        weight_sum += weights[i]
                        i += 1
                    for i in range(n_overlap):
                        weights[i] /= weight_sum
                        if build_mat and weights[i] != 0.0:
                            all_weights.push_back(weights[i])

                    if not build_mat:
                        for i in range(n_overlap):
                            outs[ix, iy, iz] += vals[overlapping_cell_inds[i]]*weights[i]
                    else:
                        nnz_counter += nnz_row
                        indptr.push_back(nnz_counter)

                    free(weights)
                    overlapping_cell_inds.clear()

        if not build_mat:
            return output.reshape(-1, order='F')
        return sp.csr_matrix((all_weights, row_inds, indptr), shape=(out_tens_mesh.nC, self.nC))

    @cython.boundscheck(False)
    @cython.cdivision(True)
    def _vol_avg_from_tens(self, in_tens_mesh, values=None, output=None):
        cdef double *weights
        cdef double over_lap_vol
        cdef double x1m, x1p, y1m, y1p, z1m, z1p
        cdef double x2m, x2p, y2m, y2p, z2m, z2p
        cdef int_t ix, ix1, ix2, iy, iy1, iy2, iz, iz1, iz2
        cdef double[:] x0 = in_tens_mesh.x0
        cdef double[:] xF

        # first check if they have the same tensor base, as it makes it a lot easier...
        cdef int_t same_base
        try:
            same_base = (
                np.allclose(self.vectorNx, in_tens_mesh.vectorNx)
                and np.allclose(self.vectorNy, in_tens_mesh.vectorNy)
                and (self.dim == 2 or np.allclose(self.vectorNz, in_tens_mesh.vectorNz))
            )
        except ValueError:
            same_base = False


        if same_base:
            out_cell_inds = self._get_containing_cell_indexes(in_tens_mesh.gridCC)
            ws = in_tens_mesh.vol/self.vol[out_cell_inds]
            if values is not None:
                if output is None:
                    output = np.empty(self.nC)
                output[:] = np.bincount(out_cell_inds, ws*values)
                return output
            return sp.csr_matrix(
                (ws, (out_cell_inds, np.arange(in_tens_mesh.nC))),
                shape=(self.nC, in_tens_mesh.nC)
            )


        cdef np.float64_t[:] nodes_x = in_tens_mesh.vectorNx
        cdef np.float64_t[:] nodes_y = in_tens_mesh.vectorNy
        cdef np.float64_t[:] nodes_z = np.array([0.0, 0.0])
        if self._dim == 3:
            nodes_z = in_tens_mesh.vectorNz
        cdef int_t nx = len(nodes_x)-1
        cdef int_t ny = len(nodes_y)-1
        cdef int_t nz = len(nodes_z)-1

        cdef double * dx
        cdef double * dy
        cdef double * dz

        if self.dim == 2:
            xF = np.array([nodes_x[-1], nodes_y[-1]])
        else:
            xF = np.array([nodes_x[-1], nodes_y[-1], nodes_z[-1]])

        cdef np.float64_t[::1, :, :] vals = np.array([[[]]])
        cdef np.float64_t[:] outs = np.array([])

        cdef int_t build_mat = 1
        if values is not None:
            vals = values.reshape((nx, ny, nz), order='F')
            if output is None:
                output = np.empty(self.nC)
            output[:] = 0
            outs = output

            build_mat = 0

        cdef vector[int_t] row_inds
        cdef vector[double] all_weights
        cdef np.int64_t[:] indptr = np.zeros(self.nC+1, dtype=np.int64)
        cdef int_t nnz_counter = 0
        cdef int_t nnz_row = 0

        cdef int_t nx_overlap, ny_overlap, nz_overlap, n_overlap
        cdef int_t i
        cdef double weight_sum

        for cell in self.tree.cells:
            x1m = min(cell.points[0].location[0], xF[0])
            y1m = min(cell.points[0].location[1], xF[1])

            x1p = max(cell.points[3].location[0], x0[0])
            y1p = max(cell.points[3].location[1], x0[1])
            if self._dim==3:
                z1m = min(cell.points[0].location[2], xF[2])
                z1p = max(cell.points[7].location[2], x0[2])
            # then need to find overlapping cells of TensorMesh...
            ix1 = max(_bisect_left(nodes_x, x1m) - 1, 0)
            ix2 = min(_bisect_right(nodes_x, x1p), nx)
            iy1 = max(_bisect_left(nodes_y, y1m) - 1, 0)
            iy2 = min(_bisect_right(nodes_y, y1p), ny)
            if self._dim==3:
                iz1 = max(_bisect_left(nodes_z, z1m) - 1, 0)
                iz2 = min(_bisect_right(nodes_z, z1p), nz)
            else:
                iz1 = 0
                iz2 = 1
            nx_overlap = ix2-ix1
            ny_overlap = iy2-iy1
            nz_overlap = iz2-iz1
            n_overlap = nx_overlap*ny_overlap*nz_overlap
            weights = <double *> malloc(n_overlap*sizeof(double))

            dx = <double *> malloc(nx_overlap*sizeof(double))
            for ix in range(ix1, ix2):
                x2m = nodes_x[ix]
                x2p = nodes_x[ix+1]
                if x1m == xF[0] or x1p == x0[0]:
                    dx[ix-ix1] = 1.0
                else:
                    dx[ix-ix1] = min(x1p, x2p) - max(x1m, x2m)

            dy = <double *> malloc(ny_overlap*sizeof(double))
            for iy in range(iy1, iy2):
                y2m = nodes_y[iy]
                y2p = nodes_y[iy+1]
                if y1m == xF[1] or y1p == x0[1]:
                    dy[iy-iy1] = 1.0
                else:
                    dy[iy-iy1] = min(y1p, y2p) - max(y1m, y2m)

            dz = <double *> malloc(nz_overlap*sizeof(double))
            for iz in range(iz1, iz2):
                z2m = nodes_z[iz]
                z2p = nodes_z[iz+1]
                if self._dim==3:
                    if z1m == xF[2] or z1p == x0[2]:
                        dz[iz-iz1] = 1.0
                    else:
                        dz[iz-iz1] = min(z1p, z2p) - max(z1m, z2m)
                else:
                    dz[iz-iz1] = 1.0

            i = 0
            weight_sum = 0.0
            nnz_row = 0
            for iz in range(iz1, iz2):
                for iy in range(iy1, iy2):
                    for ix in range(ix1, ix2):
                        in_cell_ind = ix + (iy + iz*ny)*nx
                        weights[i] = dx[ix-ix1]*dy[iy-iy1]*dz[iz-iz1]
                        if build_mat and weights[i] != 0.0:
                            nnz_row += 1
                            row_inds.push_back(in_cell_ind)

                        weight_sum += weights[i]
                        i += 1

            for i in range(n_overlap):
                weights[i] /= weight_sum
                if build_mat and weights[i] != 0.0:
                    all_weights.push_back(weights[i])

            if not build_mat:
                i = 0
                for iz in range(iz1, iz2):
                    for iy in range(iy1, iy2):
                        for ix in range(ix1, ix2):
                            outs[cell.index] += vals[ix, iy, iz]*weights[i]
                            i += 1
            else:
                nnz_counter += nnz_row
                indptr[cell.index+1] = nnz_counter

            free(weights)
            free(dx)
            free(dy)
            free(dz)

        if not build_mat:
            return output
        return sp.csr_matrix((all_weights, row_inds, indptr), shape=(self.nC, in_tens_mesh.nC))

    def get_overlapping_cells(self, rectangle):
        cdef double xm, ym, zm, xp, yp, zp
        cdef double[:] x0 = self._x0
        cdef double[:] xF
        if self.dim == 2:
            xF = np.array([self._xs[-1], self._ys[-1]])
        else:
            xF = np.array([self._xs[-1], self._ys[-1], self._zs[-1]])
        xm = min(rectangle[0], xF[0])
        xp = max(rectangle[1], x0[0])
        ym = min(rectangle[2], xF[1])
        yp = max(rectangle[3], x0[1])
        if self.dim==3:
            zm = min(rectangle[4], xF[2])
            zp = max(rectangle[5], x0[2])
        else:
            zm = 0.0
            zp = 0.0
        return self.tree.find_overlapping_cells(xm, xp, ym, yp, zm, zp)


cdef inline double _clip01(double x) nogil:
    return min(1, max(x, 0))
