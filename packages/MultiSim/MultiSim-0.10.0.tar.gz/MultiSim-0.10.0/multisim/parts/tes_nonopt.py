# -*- coding: utf-8 -*-
"""
@author: Johannes Elfner <johannes.elfner@googlemail.com>
Date: Oct 2017
"""

import numpy as np

from ..simenv import SimEnv
from .. import precomp_funs as _pf


class TesNonOpt(SimEnv):
    """
    type: Thermal Energy Storage

    Can be added to the simulation environment by using the following method:
        .add_part(Tes, name, volume=..., grid_points=..., outer_diameter=...,
        shell_thickness=...)
    Part creation parameters:
    -------------------------
    Tes : class name
        This parameter can\'t be changed and needs to be passed exactly like
        this.
    name : string
        Thermal energy storage identifier as string. Needs to be unique.
    volume : integer, float
        Thermal energy storage volume in [m^3].
    grid_points : integer
        Number of grid points to discretize the thermal energy storage with.
    outer_diameter : integer, float
        Outer diameter of the thermal energy storage in [m], not including
        insulation but including shell thickness.
    shell_thickness : float
        Shell thickness of the thermal energy storage casing in [m]. are most
        likely inappropriate.

    For part initialization the following additional parameters need to be
    passed:
        .init_tes(insulation_thickness=..., insulation_lambda=...)

    Part initialization parameters:
    -------------------------------
    insulation_thickness : float
        in [m]
    insulation_lambda : float
        in [W/(m*K)]
    new_ports : dict
        New ports to add to a thermal energy storage have to be passed in a
        dict with the port name as key and the port position and position type
        as a list as value. '
                       'The port position can either be given as integer '
                       'cell index or as as the volume between the inlet '
                       'port and the desired port location. The chosen kind '
                       'has to be specified in the position type either as '
                       '\'index\' or \'volume\'. The resulting '
                       'key:value-pair has to look like:\n'
                       '\'{\'p1\': [25, \'index\'],'
                       '\'p2\': [2.7, \'volume\']}\''

    """

    def __init__(self, name, master_cls, **kwargs):
        self._models = master_cls

        self.constr_type = 'TES'  # define construction type
        base_err = (  # define leading base error message
            'While adding {0} `{1}` to the simulation '
            'environment, the following error occurred:\n'
        ).format(self.constr_type, str(name))
        arg_err = (  # define leading error for missing/incorrect argument
            'Missing argument or incorrect type/value: {0}\n\n'
        )
        self._base_err = base_err  # save to self to access it in methods
        self._arg_err = arg_err  # save to self to access it in methods

        # save set of known kwargs to be able to show errors if unknown kwargs
        # or typos have been passed:
        known_kwargs = set(
            (
                'volume',
                'grid_points',
                'outer_diameter',
                'shell_thickness',
                'new_ports',
            )
        )
        # assert if kwargs dict exists:
        err_str = (
            'No additional arguments have been passed to `add_part()` '
            'for thermal energy storage ' + name + '! Pass at least '
            'the thermal energy storage volume in [m^3] with '
            '`volume=X` to get additional information which '
            'arguments are required!'
        )
        assert kwargs, err_str
        # assert that only known kwargs have been passed (set comparison must
        # be empty):
        err_str = (
            'The following arguments passed to `add_part()` for '
            'thermal energy storage ' + name + ' were not understood:'
            '\n' + ', '.join(set(kwargs.keys()) - known_kwargs) + '\n'
            'Please check the spelling!'
        )
        #        assert set(kwargs.keys()) - known_kwargs == set(), err_str
        # assert that all required arguments have been passed:
        err_str = (
            'The thermal enery storage volume has to be passed to its '
            '`add_part()` method in [m^3] with `volume=X`!'
        )
        assert 'volume' in kwargs, err_str
        self.V_tes = float(kwargs['volume'])
        err_str = (
            'The number of grid points for the thermal enery storage '
            'has to be passed to its `add_part()` method as integer '
            'with `grid_points=X`!'
        )
        assert 'grid_points' in kwargs, err_str
        assert type(kwargs['grid_points']) == int
        self.num_gp = kwargs['grid_points']
        err_str = (
            'The outer diameter of the thermal enery storage (without '
            ' insulation!) has to be passed to its `add_part()` method '
            'in [m] with `outer_diameter=X`!'
        )
        assert 'outer_diameter' in kwargs, err_str
        self._d_o = float(kwargs['outer_diameter'])
        self._r_o = self._d_o / 2
        err_str = (
            self._base_err
            + self._arg_err.format('shell_thickness')
            + 'The shell thickness of a thermal enery storage (only the metal '
            'shell without insulation) has to be given in [m] with '
            '`shell_thickness=X` as an integer or float value >0.'
        )
        assert (
            'shell_thickness' in kwargs
            and isinstance(kwargs['shell_thickness'], (int, float))
            and kwargs['shell_thickness'] > 0
        ), err_str
        self._d_shell = float(kwargs['shell_thickness'])
        assert self._d_shell < 1, (
            'A shell thickness of '
            + self._d_shell
            + ' is highly unlikely! Are you sure that '
            'you passed it in [m]?'
        )

        # check for port size:
        #        err_str = ('The nominal diameter and pipe type of the thermal energy '
        #                   'storage\'s connection ports has to be passed to its '
        #                   '`add_part()` method with \'port_specs=...\'!\n'
        #                   'If all ports have the same diameter (also including ports '
        #                   'added later), the `port_specs` must be a dict containing '
        #                   'the pipe type as \'pipe_type=...\' and the nominal '
        #                   'diameter as \'DN=...\', for example like:\n'
        #                   'port_specs={\'pipe_type\': \'EN10255-medium\',\n'
        #                   '            \'DN\': \'DN50\'}\n'
        #                   'If at least one port needs a different value, the '
        #                   'specifications for all ports need to be passed separately '
        #                   '(when adding a part only for the in and out port, the '
        #                   'other ports need to be specified when adding them). '
        #                   'The passed \'port_specs\'-dict must be a 2-level dict and '
        #                   'look like:\n'
        #                   'port_specs={\'in\': {\'pipe_type\': \'EN10255-medium\','
        #                   '\'DN\': \'DN50\'},\n'
        #                   '            \'out\': {\'pipe_type\': \'EN10255-heavy\','
        #                   '\'DN\': \'DN65\'}}\n'
        #                   'Here `in` and `out` are the respective port identifiers. '
        #                   'For other ports these need match the other port\'s '
        #                   'identifiers.')
        #        assert 'port_specs' in kwargs, err_str
        #        assert type(kwargs['port_specs']) == dict, err_str
        #        # get dict port specs (by checking if a specific port was given):
        #        if 'in' in kwargs['port_specs']:
        #            """
        #            TODO: if going to +1 on both sides for mem views: [-1] has to be
        #            changed to the correct value!
        #            """
        #            self._A_wll_own_p = np.zeros(self.num_gp, dtype=np.float64)
        #            self._A_fld_own_p = np.zeros_like(self._A_wll_own_p)
        #            # extract pipe_type and DN for both ports from kwargs:
        #            in_pipe_type = kwargs['port_specs']['in']['pipe_type']
        #            in_DN = kwargs['port_specs']['in']['DN']
        #            out_pipe_type = kwargs['port_specs']['out']['pipe_type']
        #            out_DN = kwargs['port_specs']['out']['DN']
        #            # get in/out diameter:
        #            self._get_specs_n_props(pipe_type=in_pipe_type, DN=in_DN,
        #                                    pipe_specs_only=True)
        #            self._get_specs_n_props(pipe_type=out_pipe_type, DN=out_DN,
        #                                    pipe_specs_only=True)
        # #            self._A_wll_own_p[0] = kwargs['port_inner_diameter'][0]
        # #            self._A_wll_own_p[-1] = kwargs['port_inner_diameter'][1]
        #        # get port specs for all ports:
        #        else:
        #            pipe_type = kwargs['port_specs']['pipe_type']
        #            DN = kwargs['port_specs']['DN']
        #            self._get_specs_n_props(pipe_type=pipe_type, DN=DN,
        #                                    pipe_specs_only=True)

        # ---> start part construction:
        #        super().__init__()
        self.name = name
        self.part_id = self._models.num_parts - 1
        # save smallest possible float number for avoiding 0-division:
        self._tiny = self._models._tiny

        # ---> geometry/grid definition
        self._d_i = self._d_o - self._d_shell
        self._r_i = self._d_i / 2
        # cross section area and volume of cell:
        self.A_cell = np.pi * self._d_i ** 2 / 4
        self.V_cell = self.V_tes / self.num_gp
        # get length (in this case: height. but sticking to naming convention)
        self.length = self.V_tes / (np.pi * self._d_i ** 2 / 4)
        # get gridspacing:
        self.grid_spacing = self.length / self.num_gp
        # set array for each cell's distance from the start of the tes. in the
        # case of a tes this is the total tes height multiplicated with a
        # factor to get the equation of the mean Nusselt number, since a tes
        # is comparably short and has a variable massflow in its cells.
        self._cell_dist = np.full(
            self.num_gp, self.length * (1.077 / 1.615) ** 3
        )
        # surface area of TES wall per cell (fluid-wall-contact-area):
        self._A_shell_i = np.pi * self._d_i * self.grid_spacing
        # outer surface area of TES wall:
        self._A_shell_o = np.pi * self._d_o * self.grid_spacing
        # cross section area of shell:
        self._A_shell_cs = np.pi / 4 * (self._d_o ** 2 - self._d_i ** 2)
        # shell volume (except top and bottom cover):
        self._V_shell_cs = self._A_shell_cs * self.length
        # shell volume of top and bottom cover (simply a cylinder plate):
        self._V_shell_tb = self._d_o ** 2 / 4 * np.pi * self._d_shell

        #        ### preallocate temperature and property grids:
        #        self.T = np.zeros(self.num_gp, dtype=np.float64)
        # ---> preallocate temperature and property grids:
        # use an extended temeprature array with +1 cell at each end to be able
        # to use memoryviews for all top/bot assigning. Thus DO NOT ALTER T_ext
        self._T_ext = np.zeros(self.num_gp + 2, dtype=np.float64)
        self.T = self._T_ext[1:-1]  # memview of T_ext
        # preallocate views to temperature grid for upper and lower cells
        self._T_top = self._T_ext[:-2]  # memview of T_ext
        self._T_bot = self._T_ext[2:]  # memview of T_ext

        #        # preallocate temperature grids for upper and lower cells
        #        self._T_top = np.zeros_like(self.T)
        #        self._T_bot = np.zeros_like(self.T)
        # preallocate temperature grid for ports:
        self._T_port = np.zeros_like(self.T)
        # preallocate temperature grid for outer surface temperature:
        self._T_s = np.zeros_like(self.T)
        # view to surface temperature for top and bottom lid:
        self._T_s_lid = self._T_s[:: self._T_s.shape[0] - 1]
        # orientation of lid, 1 is top lid, 0 is bottom lid
        self._lid_top = np.array([1, 0])
        # preallocate lambda grids and alpha grid for heat conduction with the
        # smallest possible value to avoid zero division:
        self._lam_T = np.zeros(self.num_gp)
        self._lam_mean = np.zeros(self.num_gp - 1)  # mean value between cells
        #        self._lam_top = np.zeros_like(self._lam_T)  # , self._tiny)
        #        self._lam_bot = np.zeros_like(self._lam_T)  # , self._tiny)
        #        self._lam_ports = np.zeros_like(self._lam_T)  # , self._tiny)
        self._alpha_i = np.full_like(self._lam_T, 3.122)
        self._alpha_inf = np.full_like(self._lam_T, 3.122)
        # preallocate heat capacity grids:
        self._cp_T = np.zeros(self.num_gp + 2)  # extended array
        self._cp_top = self._cp_T[:-2]  # view for top and bot grid
        self._cp_bot = self._cp_T[2:]
        #        self._cp_T = np.zeros(self.num_gp)
        #        self._cp_top = np.zeros_like(self._cp_T)
        #        self._cp_bot = np.zeros_like(self._cp_T)
        self._cp_port = np.zeros_like(self._cp_T)  # , self._tiny)
        # preallocate density grids:
        self._rho_T = np.zeros(self.num_gp)
        self._rhocp = np.zeros_like(self._rho_T)  # volume specific heat cap.
        # preallocate kinematic viscosity grid:
        self._ny_T = np.zeros(self.num_gp)
        # cell mass specific inner energy grid:
        self._ui = np.zeros_like(self.T)
        # heat capacity of fluid AND wall:
        self._mcp = np.zeros_like(self.T)
        # preallocate U*A grids:
        self._UA_tb = np.zeros(self.T.shape[0] + 1)
        #        self._UA_top = np.zeros_like(self.T)
        #        self._UA_bot = np.zeros_like(self.T)
        self._UA_port = np.zeros_like(self.T)
        self._UA_amb_shell = np.zeros_like(self.T)
        self._UA_amb_lid = np.zeros_like(self._T_s_lid)
        # preallocate mass flow grids:
        self.dm = np.zeros_like(self.T)
        #        self.dm_cell = np.zeros_like(self.T)
        self._dm_top = np.zeros_like(self.T)
        self._dm_bot = np.zeros_like(self.T)
        self._dm_port = np.zeros_like(self.T)
        self._dm_io = np.zeros_like(self._T_port)  # array for I/O flow
        # this I/O flow array MUST NOT BE CHANGED by anything else than
        # _update_FlowNet() method!
        #        self._dm_port = np.zeros((1, self.dm.shape[0]))
        # preallocate result grid with one row. An estimate of total rows will
        # be preallocated before simulation start in initialize_sim. massflow
        # grid is preallocated in set_initial_cond:
        self.res = np.zeros((1, self.num_gp))
        self.res_dm = np.zeros((2, 1))
        # separate result grids for conduction and advection to make the code
        # less complicated:
        self.dT_cond = np.zeros_like(self.T)
        self.dT_adv = np.zeros_like(self.T)
        self.dT_total = np.zeros_like(self.T)

        # port definition (first and last array element):
        self.port_num = 2
        # Index to own value array to get values of own ports, meaning if I
        # index a FLATTENED self.T.flat with self._port_own_idx, I need to
        # get values accoring to the order given in self.port_names.
        # That is, this must yield the value of the cell in self.T, which is
        # belonging to the port 'in':
        # self.T.flat[self._port_own_idx[self.port_names.index('in')]]
        self._port_own_idx = np.array((0, self.T.shape[0] - 1), dtype=np.int32)
        """port_array"""
        self.port_ids = np.array((), dtype=np.int32)
        # set to read-only to avoid manipulation, same for port_name by using
        # tuple:
        #        self._port_own_idx.flags.writeable = False
        self.port_names = tuple(('in', 'out'))
        # set massflow characteristics for ports: in means that an inflowing
        # massflow has a positive sign, out means that an outflowing massflow
        # is pos. Since a TES may need a cumulative sum over all ports to get
        # the massflow of the last port, massflow is ALWAYS positive when
        # inflowing!
        self.dm_char = tuple(('in', 'in'))
        # add additional ports if given:
        self.__add_ports(**kwargs)
        # construct partname+portname to get fast access to own ports:
        dummy_var = list(self.port_names)
        for i in range(self.port_num):
            dummy_var[i] = self.name + ';' + dummy_var[i]
        self._own_ports = tuple(dummy_var)
        # preallocate port values to avoid allocating in loop:
        self._port_vals = np.zeros(self.port_num)
        # preallocate grids for port connection parameters
        # cross section area of wall of connected pipe, fluid cross section
        # area of, gridspacing and lambda of wall of connected pipe
        self._A_wll_conn_p = np.zeros_like(self._T_port)
        self._A_fld_conn_p = np.zeros_like(self._T_port)
        self._port_gsp = np.zeros_like(self._T_port)  # , self._tiny)
        self._lam_wll_conn_p = np.full_like(self._T_port, 1e-2)
        self._lam_port_fld = np.zeros_like(self._T_port)  # , self._tiny)
        self._lam_fld_own_p = np.full_like(self._T_port, 0.6)
        self._UA_port_fld = np.zeros_like(self._T_port)
        # preallocate list to mark ports which have already been solved in
        # topology (to enable creating subnets)
        self._solved_ports = list()
        # preallocate grids for von Neumann stability checking:
        self._vN_diff = np.zeros(3)
        self._vN_dm = np.zeros(1)
        self._trnc_err = 0
        # add truncation error cell weight to weight or disable the trunc. err.
        # calculation in adaptive steps for the part (weight has to be a single
        # float or integer) or for specific cells (weight has to be an array
        # of the shape of self.T):
        self._trnc_err_cell_weight = 1
        # counter for how many times THIS part has breached von Neumann stab.
        self._stability_breaches = np.zeros(1).astype(int)  # array for view
        # preallocate grids for precalculated stuff: REPLACED WITH LOCAL VARS!
        #        self.__rhocp = np.zeros_like(self.T)
        #        self.__cpT = np.zeros_like(self.T)

        # set if type has to be solved numerically:
        self.solve_numeric = True
        # if part can be solved explicitly (otherwise a time-costly implicit
        # solving will be used):
        self.solve_explicitly = True
        # if port arrays shall be collapsed to amount of ports to improve speed
        self.collapse_arrays = True
        self._collapsed = False  # bool checker if already collapsed
        # determine if part is treated as hydraulic compensator
        self.hydr_comp = True
        # if part can be a parent part of a primary flow net:
        self._flow_net_parent = False
        # add each flow channel of part to hydr_comps (will be removed once its
        # massflow solving method is completely integrated in flow_net.
        # remaining parts except real hydr comps will be used to generate an
        # error):
        self._models._hydr_comps.add(self.name)
        # if the topology construction method has to stop when it reaches the
        # part to solve more ports from other sides before completely solving
        # the massflow of it. This will always be True for hydr comps to
        # postpone solving the last port by making expensive cumulative sums.
        self.break_topology = True
        # count how many ports are still open to be solved by topology
        self._cnt_open_prts = self.port_num
        self._port_heatcond = True  # if heatcond. over ports is enabled
        # determine if part has the capability to affect massflow (dm) by
        # diverting flow through ports or adding flow through ports:
        self.affect_dm = True
        # if the massflow (dm) has the same value in all cells of the part
        # (respectively in each flow channel for parts with multiple flows):
        self.dm_invariant = False
        # if the part has multiple separated flow channels which do NOT mix
        # (like a heat exchanger for exampe):
        self.multiple_flows = False
        # bool checker if flows were updated in update_flownet to avoid
        # processing flows in get_diff each time (array for referencing):
        self._process_flows = np.array([True])
        # if buoyancy shall be calculated (caution: only possible if cell with
        # index 0 is on top!):
        self.calculate_buoyancy = True
        # if the part CAN BE controlled by the control algorithm:
        self.is_actuator = False
        # if the part HAS TO BE controlled by the control algorithm:
        self.control_req = False
        # if the part's get_diff method is solved with memory views entirely
        # and thus has arrays which are extended by +2 (+1 at each end):
        self.enlarged_memview = False
        # if the part has a special plot method which is defined within the
        # part's class:
        self.plot_special = False

        # save initialization status:
        self.initialized = False

        # save memory address of T
        self._memadd_T = self.T.__array_interface__['data'][0]

        # save all kind of info stuff to dicts:
        # topology info:
        self.info_topology = dict()

        # IMPORTANT: THIS VARIABLE **MUST NOT BE INHERITED BY SUB-CLASSES**!!
        # If sub-classes are inherited from this part, this bool checker AND
        # the following variables MUST BE OVERWRITTEN!
        # ist the diff function fully njitted AND are all input-variables
        # stored in a container?
        self._diff_fully_njit = False
        # self._diff_njit = pipe1D_diff  # handle to njitted diff function
        # input args are created in simenv _create_diff_inputs method

    def init_part(self, **kwargs):
        err_str = (
            self._base_err
            + self._arg_err.format('insulation_thickness OR s_ins')
            + 'The insulation thickness has to be given in [m] with '
            '`insulation_thickness=X` OR `s_ins=X`, where X is an integer or '
            'float value >=0.'
        )
        assert 'insulation_thickness' in kwargs or 's_ins' in kwargs, err_str
        self._s_ins = (
            kwargs['s_ins']
            if 's_ins' in kwargs
            else kwargs['insulation_thickness']
        )
        assert (
            isinstance(self._s_ins, (int, float)) and self._s_ins >= 0
        ), err_str
        self._s_ins = float(self._s_ins)  # make sure it is float!

        err_str = (
            self._base_err
            + self._arg_err.format('insulation_lambda OR lambda_ins')
            + 'The heat conductivity (lambda) value of the insulation has '
            'to be given in [W/(m*K)] with `insulation_lambda=X` OR '
            '`lambda_ins=X`, where X is an integer or float value >= 0.'
        )
        assert 'insulation_lambda' in kwargs or 'lambda_ins' in kwargs, err_str
        self._lam_ins = (
            kwargs['lambda_ins']
            if 'lambda_ins' in kwargs
            else kwargs['insulation_lambda']
        )
        assert (
            isinstance(self._lam_ins, (int, float)) and self._lam_ins >= 0
        ), err_str
        self._lam_ins = float(self._lam_ins)  # make sure it is float

        # assert and get initial temperature:
        err_str = (
            self._base_err
            + self._arg_err.format('T_init')
            + 'The initial temperature `T_init=X` in [°C] has to be given, '
            'where X is a single float or integer value or as an array with '
            'shape (' + str(self.num_gp) + ',).'
        )
        assert 'T_init' in kwargs, err_str
        self._T_init = kwargs['T_init']
        assert isinstance(self._T_init, (float, int, np.ndarray)), err_str
        # set init values to T array:
        if type(self._T_init) != np.ndarray:
            self.T[:] = float(self._T_init)
            self._T_init = float(self._T_init)
        else:
            # assert that correct shape is given and if yes, save to T
            assert self._T_init.shape == self.T.shape, err_str
            self.T[:] = self._T_init

        # get port specifications:
        self._get_specs_n_props(**kwargs)
        # calculate m*cp for the wall PER CELL with the material information:
        self._mcp_wll = (
            self._cp_wll * self._rho_wll * self._V_shell_cs / self.num_gp
        )
        # total RADIUS from center of the pipe/tes to the outer radius of the
        # insulation:
        self._r_total = self._d_o / 2 + self._s_ins
        # precalculated log parameters for heat conduction calculation:
        # factor for wall lambda value referred to r_i
        self._r_ln_wll = self._r_i * np.log(self._r_o / self._r_i)
        # factor for insulation lambda value referred to r_i
        self._r_ln_ins = self._r_i * np.log(self._r_total / self._r_o)
        # factor for outer alpha value referred to r_i
        self._r_rins = self._r_i / self._r_total
        # thickness of the wall:
        self._s_wll = self._r_o - self._r_i
        # outer surface area of TES including insulation:
        self._A_shell_ins = np.pi * self._r_total * 2 * self.grid_spacing

        # get remaining constant UA value for top-bottom wall heat conduciton:
        self._UA_tb_wll = self._A_shell_cs / self.grid_spacing * self._lam_wll

        # check if ambient temperature is given and save it:
        self._chk_amb_temp(**kwargs)

        # check if buoyancy shall be calculated:
        if self.calculate_buoyancy:
            # preallocate for previous and current step buoyancy flow speed:
            #            self._v_prev = np.zeros(self.T.shape[0] - 1)
            #            self._v_vert = np.zeros(self.T.shape[0] - 1)
            # calculate amount of cells over which rolling average to smooth
            # small pertubations in the density gradient:
            if self.num_gp > 19:
                # smooth over one fourth of cells:
                self.__n = int(self.num_gp / 4)
            elif 8 < self.num_gp < 20:
                # smooth over half of cells:
                self.__n = int(self.num_gp / 2)
            else:
                # smooth over 3 cells if this is not >num_gp:
                self.__n = 3 if self.num_gp > 2 else self.num_gp

        # save shape parameters for the calculation of heat losses.
        self._vertical = True
        self._vertical_lid = not self._vertical
        # get flow length for cylinder for Nusselt calculation depending on
        self._flow_length = _pf.calc_flow_length(  # vertical or horizontal
            part_shape='cylinder',
            vertical=self._vertical,
            height=self.grid_spacing,
            diameter=self._r_total * 2,
        )
        # get flow length of lid for a cylinder for Nusselt calculation:
        self._flow_length_lid = _pf.calc_flow_length(
            part_shape='plane',
            vertical=self._vertical_lid,
            height=self._r_total * 2,  # hor. cyl with vertical caps
            width=self._r_total * 2,
            depth=self._r_total * 2,
        )  # vert. cyl.

        # construct list of differential input argument names IN THE CORRECT
        # ORDER!!!
        self._input_arg_names_sorted = [
            '_T_ext',
            '_T_port',
            '_T_s',
            '_T_s_lid',
            '_T_amb',
            'ports_all',  # temperatures
            '_dm_io',
            'dm',
            '_dm_top',
            '_dm_bot',
            '_dm_port',
            'res_dm',  # flows
            '_cp_T',
            '_lam_T',
            '_rho_T',
            '_ny_T',
            '_lam_mean',
            '_cp_port',
            '_lam_port_fld',  # mat. props.
            '_mcp',
            '_rhocp',
            '_lam_wll',
            '_lam_ins',
            '_mcp_wll',
            '_ui',
            '_alpha_i',
            '_alpha_inf',
            '_UA_tb',
            '_UA_tb_wll',
            '_UA_amb_shell',
            '_UA_amb_lid',
            '_UA_port',
            '_UA_port_wll',  # UA values
            '_port_own_idx',
            '_port_own_idx_2D',
            '_port_link_idx',
            # indices
            'grid_spacing',
            '_port_gsp',
            '_port_subs_gsp',
            '_d_i',
            '_cell_dist',
            '_flow_length',
            '_flow_length_lid',
            '_r_total',
            '_r_ln_wll',
            '_r_ln_ins',
            '_r_rins',
            '_s_wll',
            '_s_ins',  # lengths
            'A_cell',
            'V_cell',
            '_A_shell_i',
            '_A_shell_ins',
            '_A_p_fld_mean',  # areas and vols
            '_process_flows',
            '_vertical',
            '_vertical_lid',
            '_lid_top',
            '_step_stable',  # bools
            'part_id',
            '_stability_breaches',
            '_vN_max_step',
            '_max_factor',  # misc.
            'stepnum',  # step information
            'dT_cond',
            'dT_adv',
            'dT_total',
        ]

        #        # arguments for using closures (HUGE compile time but fast exec., thus
        #        # currently not in use):
        #        # for calls in iteration
        #        self._input_arg_names_calls = [
        #            '_T_ext', '_T_port', '_T_s', '_T_s_lid', '_T_amb',
        #            'ports_all',  # temperatures
        #            '_dm_io', 'dm', '_dm_top', '_dm_bot', '_dm_port', 'res_dm',  # flows
        #            '_alpha_i', '_alpha_inf',
        #            '_UA_tb',
        #            '_UA_amb_shell', '_UA_amb_lid',
        #            '_UA_port', '_UA_port_wll',  # UA values
        #            '_process_flows', '_step_stable',  # bools
        #            '_stability_breaches',
        #            '_vN_max_step',
        #            '_max_factor',  # misc.
        #            'stepnum',  # step information
        #            'dT_cond', 'dT_adv', 'dT_total'
        #            ]
        #        # constant args to be enclosed:
        #        self._input_arg_names_closure = [
        #            '_lam_wll',
        #            '_lam_ins', '_mcp_wll',
        #            '_UA_tb_wll',
        #            '_port_own_idx', '_port_own_idx_2D', '_port_link_idx',  # indices
        #            'grid_spacing', '_port_gsp',
        #            '_port_subs_gsp', '_d_i',
        #            '_cell_dist', '_flow_length',
        #            '_flow_length_lid', '_r_total',
        #            '_r_ln_wll', '_r_ln_ins',
        #            '_r_rins', '_s_wll', '_s_ins',  # lengths
        #            'A_cell', 'V_cell', '_A_shell_i',
        #            '_A_shell_ins', '_A_p_fld_mean',  # areas and vols
        #            '_vertical', '_vertical_lid', '_lid_top', 'part_id',
        #            ]
        #
        #        # save closure function:
        #        self._diff_clsr = tes_diff_clsr

        # set initialization to true:
        self.initialized = True

    def _reset_to_init_cond(self):
        self._dm_io[:] = 0
        self.T[:] = self._T_init

    def __add_ports(self, **kwargs):
        """
        This method adds new ports if these have been passed to the parts
        `add_part()` method with \'new_ports\'.
        """

        # define method to expand array dims, append and add new port things
        def expand_port_arr(arr):
            # check if array dimensions have already been expandede with a
            # new row at least once before.
            # if not yet expanded, ndim is still 1
            if arr.ndim == 1:
                # expand all arrays to 2D-arrays:
                arr = np.expand_dims(arr, axis=0)
            # add a new column filled with smallest value to array:
            arr = np.append(arr, np.full((1, arr.shape[1]), 0), axis=0)

            return arr

        # assert that new ports was passed as kwarg to the tes __init__ method:
        err_str = (
            self._base_err
            + self._arg_err.format('new_ports')
            + 'The argument `new_ports=X` has to be given for a thermal energy '
            'storage. If adding new ports is not required, pass '
            '`new_ports=\'None\'`, else just pass anything for X to get '
            'additional information on how to add ports.'
        )
        assert 'new_ports' in kwargs, err_str
        # get additional ports:
        if kwargs['new_ports'] != 'none':
            err_str = (
                'New ports to add to thermal energy storage '
                + self.name
                + ' have to be passed to its `add_part()` method in a dict '
                'with the port name(s) as key(s) and the port position(s) '
                'and position type(s) in a list as value(s).\n'
                'The port position can either be given as an integer cell '
                'index or as a float/integer value giving the volume in '
                '[m^3] between the inlet port (at the top) and the '
                'desired port location. The chosen kind has to be '
                'specified in the position type either as \'index\' or '
                '\'volume\'. The resulting key:value-pair-dict has to '
                'look like:\n'
                '`new_ports={\'p1\': [25, \'index\'],\n'
                '            \'p2\': [2.7, \'volume\']}`'
            )
            assert type(kwargs['new_ports']) == dict, err_str
            # assert that sub-structure of new ports is composed of lists:
            for value in kwargs['new_ports'].values():
                assert type(value) == list, err_str
            # make a DEEP copy of the new ports dict to be able to alter it
            # without sending alterations to the calling functions (and thus
            # avoid errors due when the part-construction is called twice):
            nep_cpy = {key: val[:] for key, val in kwargs['new_ports'].items()}
            # construct dict of currently existing ports with the
            # port index as key and the number of occurences as value to
            # be able to calculate the number of extensions needed for new
            # ports:
            pidx, counter = np.unique(self._port_own_idx, return_counts=True)
            port_occurrence = dict(zip(pidx, counter))

            # loop over new ports. Value contains the new port's index at
            # element 0.
            for key, value in nep_cpy.items():
                # assert that correct position type is given:
                assert value[1] == 'index' or value[1] == 'volume', err_str
                # if port position is given as index:
                if value[1] == 'index':
                    # assert correct position:
                    assert type(value[0]) == int, err_str
                    # assert that index exists:
                    err_str2 = (
                        'While adding new port `'
                        + key
                        + '` to part `'
                        + self.name
                        + '` an error occurred:\n'
                        'Index ' + str(value[0]) + ' is out of range for '
                        'the defined grid with '
                        + str(self.num_gp)
                        + ' grid points!'
                    )
                    assert -1 <= value[0] <= (self.num_gp - 1), err_str2
                    # if -1 was given (last element index), get the direct idx:
                    if value[0] == -1:
                        value[0] = self.num_gp - 1
                # if port position is given as volume, calculate index:
                else:
                    # assert correct type:
                    assert (
                        type(value[0]) == float or type(value[0]) == int
                    ), err_str
                    err_str2 = (
                        'The given volume position at '
                        + str(value[0])
                        + 'm³ for port `'
                        + key
                        + '` must be within the '
                        'interval 0 <= volume_position <= '
                        + str(self.V_tes)
                        + 'm³!'
                    )
                    # assert correct position/that volume element exists:
                    assert 0 <= value[0] <= self.V_tes, err_str2
                    # get index of volume element where to place the port and
                    # save as integer index to value[0]
                    # ((self.V_cell / 2 - 1e-9) makes that the volume position
                    # is always rounded towards the position of the cell
                    # center!)
                    value[0] = round(
                        (value[0] - (self.V_cell / 2 - 1e-9)) / self.V_cell
                    )
                #                # backup value[0] to be able to access it in _A_wll_own_p
                #                # creation
                #                value0_bkp = value[0]

                # check if a port at that position already exists:
                if value[0] in self._port_own_idx:
                    # increase counter of port in port_occurrence dict:
                    port_occurrence[value[0]] += 1
                    # append new row to all arrays which have to cope with
                    # ports if ndim is still 1 (no double port so far) or the
                    # number of occurrences is equal to (or since shape is
                    # starting from 0 indexing -> greater than) the number of
                    # rows (and thus also equal to the max. amount of double
                    # ports):
                    if self._T_port.ndim == 1 or (
                        self._T_port.ndim == 2
                        and (self._T_port.shape[0] < port_occurrence[value[0]])
                    ):
                        self._T_port = expand_port_arr(self._T_port)
                        self._dm_port = expand_port_arr(self._dm_port)
                        self._dm_io = expand_port_arr(self._dm_io)
                        #                        self._lam_ports = expand_port_arr(self._lam_ports)
                        self._cp_port = expand_port_arr(self._cp_port)
                        self._UA_port = expand_port_arr(self._UA_port)
                        # calculate new flattened index from given port index,
                        # number of gridpoints and shape of arrays to later be
                        # able to transform the flattened index array into
                        # a 2D-index-array. this means if the new index to add
                        # in value[0] is for example 7, it has to be index 7
                        # of the newly appended row. thus the new flattened
                        # index is: 7 + (length_of_the_old_T_port-array
                        #                * times_T_port_was_extended)
                        value[0] += self._T_port.shape[1] * (
                            self._T_port.shape[0] - 1
                        )
                    # if double port occurrence but no extension needed:
                    else:
                        # if port already existed but arrays were not extended,
                        # the new flattened index value has to be calculated
                        # like above except that the number of occurrences is
                        # used instead of the array shape:
                        value[0] += self._T_port.shape[1] * (
                            port_occurrence[value[0]] - 1
                        )
                # if port not yet existing, only add it to port_occurence dict,
                # everything else will be done in general in the next line:
                else:
                    port_occurrence[value[0]] = 1

                # things which can be done in general:
                # now add/insert new port in _port_own_idx
                # find place where to insert:
                idx_to_insert = self._port_own_idx.searchsorted(value[0])
                # insert
                self._port_own_idx = np.insert(
                    self._port_own_idx, idx_to_insert, value[0]
                )
                # expand port massflow characteristics tuple:
                self.dm_char += ('in',)

                # if inner port diameter was specified for each port separately
                #                if type(self._A_wll_own_p) == np.ndarray:
                #                    err_str = ('Since for thermal energy storage ' + self.name
                #                               + ' the inner diameter of ports was chosen to '
                #                               'be not consistent, the inner port diameter in '
                #                               '[m] has to be appended to \'new_ports\' '
                #                               'value-list as third element! For example for '
                #                               'desired port diameters of 30mm the resulting '
                #                               'key:value-pair has to look like:\n'
                #                               '\'{\'p1\': [25, \'index\', 30e-3],'
                #                               '\'p2\': [2.7, \'volume\', 30e-3]}\'')
                #                    assert len(value) == 3, err_str
                #                    # add to _A_wll_own_p
                #                    # if the other arrays have been extended, shapes differ:
                #                    if self._A_wll_own_p.shape != self._T_port.shape:
                #                        # expand and append to match shapes again:
                #                        self._A_wll_own_p = expand_port_arr(self._A_wll_own_p)
                #                        # insert value at index position in last row:
                #                        self._A_wll_own_p[-1, value0_bkp] = value[2]
                #                    # if the other arrays have not been extended:
                #                    else:
                #                        # check for shape of _A_wll_own_p if not extended:
                #                        if self._A_wll_own_p.ndim == 1:
                #                            self._A_wll_own_p[value0_bkp] = value[2]
                #                        # if already extended use port occurrences to get
                #                        # correct position:
                #                        else:
                #                            self._A_wll_own_p[port_occurrence[value0_bkp] - 1,
                #                                              value0_bkp] = value[2]

                # insert port name at correct place in port names::
                self.port_names = (
                    self.port_names[:idx_to_insert]
                    + (key,)
                    + self.port_names[idx_to_insert:]
                )
                # update number of ports:
                self.port_num += 1
        # if arrays have been extended, _port_own_idx array consists of
        # flattened indices. these have to be unflattened to the shape
        # of _T_port with unravel, then transposed to the correct c-order
        # shape (transpose also transforms the tuple from unravel to a
        # numpy.ndarray) and then made c-contiguous:
        if self._T_port.ndim > 1:
            # REPLACED WITH FLATTENED INDICES BELOW:
            #            self._port_own_idx1 = (np.ascontiguousarray(
            #                    np.transpose(
            #                            np.unravel_index(self._port_own_idx,
            #                                             self._T_port.shape))))
            # now transform port index into a 1D-form by only using the
            # last column of it (_port_own_idx is used outside tes to
            # update ports, thus it needs to be 1D!) and copy a 2D-version
            # which will only be used inside TES' own get_diff method!
            """
            TODO: Remove once update ports is transformed to using
            memory views! Then _port_own_idx is only needed inside the own
            type like Tes and thus no 1D version will be required!
            """
            # construct tuple as 2D to be able to use it easy and fast in
            # numpy
            """
            TODO: once get_diff is migrated to numba, this tuple conversion
            needs to be replaced by:
                self._port_own_idx_2D = self._port_own_idx.copy()
            """
            """
            TODO: SINCE NUMBA 0.36 numba supports np.take with fancy 2d indices
                thus this port index 2d stuff can be made alot easier!!!!!!!
            """
            #            self._port_own_idx_21 = tuple(self._port_own_idx1.transpose())
            #            self._port_own_idx1 = self._port_own_idx1[:, 1].copy()
            # since 1D and 2D indexing is easy and fast with flattened arrays,
            # the 2D array is left as it is, while the 1D (needed for updating
            # stuff outside of tes) is the plain first dimension array index:
            self._port_own_idx_2D = self._port_own_idx.copy()
            self._port_own_idx = np.unravel_index(
                self._port_own_idx, self._T_port.shape
            )[1].astype(int)
        else:
            # if arrays have not been extended, _port_own_idx_2D will be
            # a view to _port_own_idx:
            self._port_own_idx_2D = self._port_own_idx[:]

    def _get_flow_routine(
        self, port, parent_port=None, subnet=False, **kwargs
    ):
        """
        Returns the massflow calculation routine for the port of the current
        part to the topology construction. The massflow calculation routine has
        to look like:

        routine = (memory_view_to_target_port,
                   operation_id,
                   memory_view_to_port1, memory_view_to_port2, ...)

        with target_port being the port which has to be calculated and port1
        and port2 being the other/source ports which **don't** have to be
        calculated with this routine! These source ports **must be given**
        when the routine is called.

        Parameters:
        -----------
        port : string
            Port name of the port which shall be calculated (target port).

        """

        # if more than one port is open to be solved, it will always be solved
        # by passing on the value from the connected parent part
        if self._cnt_open_prts != 1:
            # get topology connection conditions (target index, source
            # part/port identifiers, source index and algebraic sign for passed
            # massflow):
            (
                trgt_idx,
                src_part,
                src_port,
                src_idx,
                alg_sign,
            ) = self._get_topo_cond(port, parent_port)
            # for TES the operation id is always 0 or -1, depending on the
            # algebraic sign of the ports which are connected, when there is
            # more than one port remaining to be solved. This means the value
            # of connected port is either passed on (0) or the negative value
            # of it is used (-1):
            if alg_sign == 'positive':
                operation_id = 0
            else:
                operation_id = -1
            # add operation instructions to tuple (memory view to target
            # massflow array cell, operation id and memory view source port's
            # massflow array cells)
            op_routine = tuple()
            # construct memory view to target massflow array cell and append to
            # op routine tuple
            op_routine += (self._dm_io.reshape(-1)[trgt_idx],)
            # add operation id:
            op_routine += (operation_id,)
            # add memory view to source massflow array cell:
            op_routine += (
                self._models.parts[src_part]._dm_io.reshape(-1)[src_idx],
            )

        # Tes has only one port remaining to be solved:
        else:
            # There are two possibilities to get the last port of a TES:
            # 1. - Get it from a connected port -> parent_port must be given
            # 2. - Calculate it from the missing massflow through the other
            #      already solved own ports. - > no parent_port needed
            # Method 1 is highly preferred, since it only involves accessing
            # the connected port's massflow array cell, while method 2 requires
            # summing up all other ports.
            if parent_port is not None:
                # Method 1!
                # get topology connection conditions (target index, source
                # part/port identifiers, source index and algebraic sign for
                # passed massflow):
                (
                    trgt_idx,
                    src_part,
                    src_port,
                    src_idx,
                    alg_sign,
                ) = self._get_topo_cond(port, parent_port)
                # passing values to TES is always 0 or -1, depending on pos.
                # massflow directions of connected ports
                if alg_sign == 'positive':
                    # in/out connected
                    operation_id = 0
                else:
                    # in/in or out/out connected
                    operation_id = -1
                # add operation instructions to tuple (memory view to target
                # massflow array cell, operation id and memory view source
                # port's massflow array cells)
                op_routine = tuple()
                # construct memory view to target massflow array cell and
                # append to op routine tuple
                op_routine += (self._dm_io.reshape(-1)[trgt_idx],)
                # add operation id:
                op_routine += (operation_id,)
                # add memory view to source massflow array cell:
                op_routine += (
                    self._models.parts[src_part]._dm_io.reshape(-1)[src_idx],
                )
            else:
                # Method 2!
                # get port index slice of target port to create memory view:
                trgt_idx = self._get_topo_cond(port)
                # operation id for this case is always -1, since the positive
                # massflow direction of all ports is facing inwards
                operation_id = -1
                # add operation instructions to tuple (memory view to target
                # massflow array cell, operation id and memory view to ALL
                # source/other port's massflow array cells of the TES)
                op_routine = tuple()
                # construct memory view to target massflow array cell and
                # append to op routine tuple
                op_routine += (self._dm_io.reshape(-1)[trgt_idx],)
                # add operation id:
                op_routine += (operation_id,)
                # add memory view to source massflow array cell(s)
                # therefore loop over already solved ports
                for slvd_prt in self._solved_ports:
                    # get solved port index as slice to create memory view
                    # depending on number of dimensions of the massflow array
                    # grid:
                    if self._T_port.ndim == 1:
                        # if no double ports have been added to target part
                        slvd_prt_idx = self._port_own_idx[
                            self.port_names.index(slvd_prt)
                        ]
                        slvd_prt_idx = slice(slvd_prt_idx, slvd_prt_idx + 1)
                    elif self._T_port.ndim == 2:
                        # if double ports have been added and thus all grids
                        # have more than one dimension
                        #                        slvd_prt_idx_ax0 = (self.
                        #                                            _port_own_idx_2D[0][self.
                        #                                                             port_names.
                        #                                                             index(slvd_prt)])
                        # #                            wrong,s ince pidx 2d ist nicht mehr 2d sondern flat
                        #                        slvd_prt_idx_ax1 = (self.
                        #                                            _port_own_idx_2D[1][self.
                        #                                                             port_names.
                        #                                                             index(slvd_prt)])
                        #                        # make tuple with slice:
                        #                        slvd_prt_idx = (slvd_prt_idx_ax0,
                        #                                        slice(slvd_prt_idx_ax1,
                        #                                              slvd_prt_idx_ax1 + 1))
                        slvd_prt_idx = self._get_arr_idx(
                            part=self.name,
                            port=slvd_prt,
                            target='massflow',
                            as_slice=True,
                            flat_index=True,
                        )
                    # add memory view to this ports massflow
                    op_routine += (self._dm_io.reshape(-1)[slvd_prt_idx],)

        # update solved ports list and counter stop break:
        self._solved_ports.append(port)
        self._cnt_open_prts = self.port_num - len(self._solved_ports)
        # set break topology to False if enough ports have been solved:
        self.break_topology = True if self._cnt_open_prts > 0 else False
        # remove part from hydr_comps if completely solved:
        #        if self._cnt_open_prts == 0:
        #            self._models._hydr_comps.remove(self.name)

        # save topology parameters to dict for easy information lookup:
        net = 'Subnet' if subnet else 'Flownet'
        operation_routine = (
            'Negative of sum'
            if operation_id == -1
            else 'Pass on value'
            if operation_id == 0
            else 'Error'
        )
        src_part = src_part if self._cnt_open_prts > 1 else self.name
        source_ports = (
            parent_port
            if operation_id == 0
            else tuple(set(self.port_names) - set(port))
        )
        kwargs['pump_side'] = (
            'decoupled from pump by hydraulic compensator'
            if kwargs['pump_side'] == 'sub net - undefined'
            else kwargs['pump_side']
        )
        # add port dict for current port and fill it:
        if port not in self.info_topology:
            self.info_topology[port] = dict()
        self.info_topology[port].update(
            {
                'Net': net,
                'Massflow': self._dm_io.reshape(-1)[trgt_idx],
                'Calculation routine': operation_routine,
                'Source part': src_part,
                'Source port(s)': source_ports,
                'Connected part': (
                    self._models.port_links[self.name + ';' + port].split(';')[
                        0
                    ]
                ),
                'Connected port': (
                    self._models.port_links[self.name + ';' + port].split(';')[
                        1
                    ]
                ),
                'Parent pump/part': kwargs['parent_pump'],
                'Pump side': kwargs['pump_side'],
            }
        )

        return op_routine

    def get_diff(self, timestep):
        #        self._cnt_inside_step += 1
        # ---> get temperature arrays

        # get temperatures of connected ports:
        #        self._port_vals[:] = self._models.ports_all[self._port_link_idx]
        #        # print(self.name, 'Ports retrieved:', port_values)
        #        # save port values to ports array:
        #
        #        self._T_port.flat[self._port_own_idx_2D] = self._port_vals

        # get new values for top and bot grids:
        #        self._T_top[1:] = self.T[:-1]
        #        self._T_bot[:-1] = self.T[1:]

        # ---> get massflows
        # massflow through ports is aquired by update_FlowNet
        # get massflow through each cell (sum up in/out dm of ports and then
        # run cumulative sum over all cells)
        # copy I/O flows to NOT alter the I/O array during calculations:
        #        self._dm_port[:] = self._dm_io
        #        # if no double ports have been added only cumsum needed:
        #        if self._dm_port.ndim == 1:
        #            self.dm[:] = np.cumsum(self._dm_port)
        #        # if double ports have been added:
        #        else:
        #            self.dm[:] = np.cumsum(np.sum(self._dm_port, axis=0))
        #
        #        # get massflow though top cell-cell border:
        #        self._dm_top[1:] = self.dm[:-1]
        #        # get massflow though bottom cell-cell border (and *-1!):
        #        self._dm_bot[:-1] = - self.dm[:-1]
        #        # remove negative values:
        #        self._dm_top[self._dm_top < 0] = 0
        #        self._dm_bot[self._dm_bot < 0] = 0
        #        self._dm_port[self._dm_port < 0] = 0
        #        # set last value of dm to be the same as the value of the previous cell
        #        # to avoid having 0-massflow in it due to cumsum:
        #        self.dm[-1] = self.dm[-2]
        #
        #        self.res_dm[self._models.stepnum] = self.dm

        #        self._process_flows = _process_flow_var(
        #                process_flows=self._process_flows, dm_io=self._dm_io,
        #                dm=self.dm, dm_top=self._dm_top, dm_bot=self._dm_bot,
        #                dm_port=self._dm_port, stepnum=self._models.stepnum,
        #                res_dm=self.res_dm)

        # ---> get thermodynamic properties of water
        # for cell temp:

        #        get_cp_water(self.T, self._cp_T)
        #        get_lambda_water(self.T, self._lam_T)
        #        get_rho_water(self.T, self._rho_T)
        #        get_ny_water(self.T, self._ny_T)

        #        water_mat_props_ext(
        #                T_ext=self._T_ext, cp_T=self._cp_T, lam_T=self._lam_T,
        #                rho_T=self._rho_T, ny_T=self._ny_T)

        #        # get them for port temperatures:
        #        get_cp_water(self._T_port, self._cp_port)
        #        get_lambda_water(self._T_port, self._lam_port_fld)

        #        get_lambda(self.T, self._lam_fld_own_p)  # done by indexing
        # for bottom and top temps
        #        self._cp_top[1:] = self._cp_T[:-1]
        #        self._cp_bot[:-1] = self._cp_T[1:]
        #        self._lam_top[1:] = self._lam_T[:-1]
        #        self._lam_bot[:-1] = self._lam_T[1:]

        #        # for own ports in shape of _T_port:
        #        self._lam_fld_own_p.flat[self._port_own_idx_2D] = self._lam_T[self._port_own_idx]

        # get mean lambda of the path between two cell centers:

        #        _lambda_mean(lam_T=self._lam_T, out=self._lam_mean)
        #        self._lam_mean = (2 * self._lam_T[:-1] * self._lam_T[1:]
        #                          / (self._lam_T[:-1] + self._lam_T[1:]))

        # ---> calculate buoyancy
        #        self._buoyancy(timestep)
        #        self.buo_Nu()
        #        buoyancy_byNusselt(T=self.T, ny=self._ny_T, d_i=self._d_i,
        #                           lam_mean=self._lam_mean)

        # calculate U values
        # for conduction between current cell and cell on top (first cell 0):
        #        self._UA_top[1:] = (
        #                self.A_cell / (self.grid_spacing / (2 * self._lam_T[1:])
        #                               + self.grid_spacing / (2 * self._lam_top[1:])))
        #        # for conduction between current cell and cell at bottom (last cell 0):
        #        self._UA_bot[:-1] = (
        #                self.A_cell / (self.grid_spacing / (2 * self._lam_T[:-1])
        #                               + self.grid_spacing / (2 * self._lam_bot[:-1])))
        # for conduction between current cell and cell on top or bottom
        # (first and last cell is 0, to enable using a full view of this array
        # for heat flow calculation):

        #        self._UA_tb[1:-1] = (
        #                self.A_cell / self.grid_spacing * self._lam_mean
        #                + self._UA_tb_wll)  # add up wall heat conduction

        #        UA_plate_tb(
        #            A_cell=self.A_cell, grid_spacing=self.grid_spacing,
        #            lam_mean=self._lam_mean,
        #            UA_tb_wll=self._UA_tb_wll, out=self._UA_tb)

        #        # for conduction between current cell and cells at ports:
        #        self._UA_port_fld[:] = (self._A_p_fld_mean
        #                                / (+ (self._port_gsp
        #                                      / (2 * self._lam_port_fld))
        #                                   + (self.grid_spacing
        #                                      / (2 * self._lam_fld_own_p))
        #                                   )
        #                                )
        #        # parallel circuit of heat conduction through wall and fluid of ports:
        #        self._UA_port[:] = self._UA_port_fld + self._UA_port_wll

        # for conduction between current cell and ambient:
        # get outer TES (insulation) surface temperature using a linearized
        # approach assuming steady state (assuming surface temperature = const.
        # for t -> infinity) and for cylinder shell (lids are omitted)
        #        surface_temp_steady_state(
        #                T=self.T, T_inf=self._T_amb, A_s=self._A_shell_ins,
        #                alpha_inf=self._alpha_inf, UA=self._UA_amb_shell,
        #                T_s=self._T_s)
        # get inner alpha value between fluid and wall from nusselt equations:
        #        pipe_alpha_i(
        #                self.dm, self.T, self._rho_T, self._ny_T, self._lam_T,
        #                self.A_cell, self._d_i, self._cell_dist, self._alpha_i)
        # get outer alpha value between insulation and surrounding air:
        #        cylinder_alpha_inf(  # for a cylinder
        #            T_s=self._T_s, T_inf=self._T_amb, flow_length=self._flow_length,
        #            vertical=self._vertical, r_total=self._r_total,
        #            alpha_inf=self._alpha_inf)
        # get alpha_inf of top and bottom caps:
        #        self._alpha_inf_lid = plane_alpha_inf(  # for TES end cap, bottom side
        #                T_s=self._T_s_lid, T_inf=self._T_amb,
        #                flow_length=self._flow_length_lid,
        #                vertical=self._vertical_lid, top=self._lid_top)
        # get resulting UA to ambient relative to the inner casing area:
        #        UA_fld_wll_ins_amb_cyl(
        #                A_i=self._A_shell_i, r_ln_wll=self._r_ln_wll,
        #                r_ln_ins=self._r_ln_ins, r_rins=self._r_rins,
        #                alpha_i=self._alpha_i, alpha_inf=self._alpha_inf,
        #                lam_wll=self._lam_wll, lam_ins=self._lam_ins,
        #                out=self._UA_amb_shell)
        # add up UA to ambient of the caps:
        #        self._UA_amb_lid = UA_fld_wll_ins_amb_plate(
        #                A=self.A_cell, s_wll=self._s_wll, s_ins=self._s_ins,
        #                alpha_fld=self._alpha_i[0], alpha_inf=self._alpha_inf_lid,
        #                lam_wll=self._lam_wll, lam_ins=self._lam_ins)

        #        # precalculate values which are needed multiple times:
        #        # volume specific heat capacity:
        #        rhocp = self._rho_T * self._cp_T
        #        # heat capacity of fluid AND wall:
        #        self._mcp = self.V_cell * rhocp + self._mcp_wll
        #        # mass specific inner energy:
        #        ui = self._cp_T * self.T

        #        cell_temp_props_ext(
        #            T_ext=self._T_ext, V_cell=self.V_cell, cp_T=self._cp_T,
        #            rho_T=self._rho_T, mcp_wll=self._mcp_wll,
        #            rhocp=self._rhocp, mcp=self._mcp, ui=self._ui)
        #        rhocp = self._rhocp
        #        ui = self._ui

        #        _process_ports_collapsed(
        #            ports_all=self._models.ports_all, port_link_idx=self._port_link_idx,
        #            port_own_idx=self._port_own_idx, T=self.T, mcp=self._mcp,
        #            UA_port=self._UA_port, UA_port_wll=self._UA_port_wll,
        #            A_p_fld_mean=self._A_p_fld_mean, port_gsp=self._port_gsp,
        #            grid_spacing=self.grid_spacing, lam_T=self._lam_T,
        #            cp_port=self._cp_port, lam_port_fld=self._lam_port_fld,
        #            T_port=self._T_port)

        #        ### check for L2/von Neumann stability
        #        # for diffusion:
        #        # save von Neumann stability values for cells by multiplying the cells
        #        # relevant total x-gridspacing with the maximum UA-value (this gives a
        #        # substitue heat conduction to get a total diffusion coefficient) and
        #        # the inverse maximum rho*cp value (of all cells! this may result in a
        #        # worst-case-result with a security factor of up to about 4.2%) to get
        #        # the substitute diffusion coefficient and then mult. with step and
        #        # div. by gridspacing**2 (not **2 since this is cut out with mult. by
        #        # it to get substitute diffusion from UA) and save to array:
        #        self.__rhocpmax = rhocp.max()
        #        self._vN_diff[0] = ((self._UA_tb.max() / self.__rhocpmax)
        #                            * timestep / self.grid_spacing)
        #        # for the next two with non-constant gridspacing, find max of UA/gsp:
        #        self._vN_diff[1] = ((self._UA_port / self._port_subs_gsp).max()
        #                            / self.__rhocpmax * timestep)
        #        self._vN_diff[2] = (self._UA_amb_shell.max() / self._r_total
        #                            / self.__rhocpmax * timestep)
        #        # for massflow:
        #        # get maximum cfl number (this is the von Neumann stability condition
        #        # for massflow through cells), again with total max. of rho to get a
        #        # small security factor for worst case:
        #        self.__Vcellrhomax = (self.V_cell * self._rho_T).max()
        #        if self._T_port.ndim == 1:
        #            self._vN_dm = (
        #                    max(self._dm_top.max(), self._dm_bot.max(),
        #                        np.abs(self._dm_port).max())
        #                    * timestep / self.__Vcellrhomax)
        #        else:
        #            self._vN_dm = (
        #                    max(self._dm_top.max(), self._dm_bot.max(),
        #                        np.abs(self._dm_port.sum(axis=0)).max())
        #                    * timestep / self.__Vcellrhomax)
        #
        #        # get maximum von Neumann stability condition values:
        #        vN_diff_max = self._vN_diff.max()
        #        vN_dm_max = self._vN_dm.max()
        #        # get dividers for maximum stable timestep to increase or decrease
        #        # stepsize:
        #        vN_diff_mult = vN_diff_max / 0.5
        #        vN_dm_mult = vN_dm_max / 1
        #        # get biggest divider:
        #        vN_div_max = max(vN_diff_mult, vN_dm_mult)
        #        # check if any L2 stability conditions are violated:
        #        if vN_div_max > 1:
        #            # only do something if von Neumann checking is active, else just
        #            # print an error but go on with the calculation:
        #            if self._models._check_vN:
        #                # if not stable, set stable step bool to False
        #                self._models._step_stable = False
        #                # calculate required timestep to make this part stable with a
        #                # security factor of 0.95:
        #                vN_max_step = timestep / vN_div_max * 0.95
        #                # if this is the smallest step of all parts needed to make all
        #                # parts stable save it to maximum von Neumann step:
        #                if self._models._vN_max_step > vN_max_step:
        #                    self._models._vN_max_step = vN_max_step
        #            else:
        #                print('\nVon Neumann stability violated at step '
        #                      + str(self._models.stepnum) + ' and part '
        #                      + self.name + '!')
        #                raise ValueError
        #        elif self._models._max_speed:
        #            # else get new maximum timestep for this part if maximum speed
        #            # option is set:
        #            raise ValueError('Checking with other parts is missing! This '
        #                             'should only get the max. error of the weakest '
        #                             'part!')
        #            timestep /= vN_div_max

        #        (self._models._step_stable, self._models._vN_max_step,
        #         self._models._max_factor) = _vonNeumann_stability_var(
        #            part_id=self.part_id, UA_tb=self._UA_tb, UA_port=self._UA_port,
        #            UA_amb_shell=self._UA_amb_shell,
        #            dm_top=self._dm_top, dm_bot=self._dm_bot, dm_port=self._dm_port,
        #            rho_T=self._rho_T, rhocp=self._rhocp,
        #            grid_spacing=self.grid_spacing, port_subs_gsp=self._port_subs_gsp,
        #            r_total=self._r_total, V_cell=self.V_cell,
        #            step_stable=self._models._step_stable, vN_max_step=self._models._vN_max_step,
        #            max_factor=self._models._max_factor,
        #            stepnum=self._models.stepnum, timestep=timestep)

        # CALCULATE DIFFERENTIALS

        #        (self._process_flows, self._models._step_stable,
        #         self._models._vN_max_step, self._models._max_factor) = tes_diff(
        #                process_flows=self._process_flows, vertical=self._vertical,
        #                step_stable=self._models._step_stable,  # bools
        #                part_id=self.part_id, vN_max_step=self._models._vN_max_step,
        #                max_factor=self._models._max_factor,  # misc.
        #                # stepnum, timestep,  # step information
        #                # dT_cond, dT_adv  # differentials
        #                T=self.T, T_ext=self._T_ext, T_top=self._T_top,
        #                T_bot=self._T_bot,
        #                T_port=self._T_port, T_amb=self._T_amb,
        #                UA_tb=self._UA_tb, UA_port=self._UA_port,
        #                UA_amb_shell=self._UA_amb_shell, UA_amb_lid=self._UA_amb_lid,
        #                dm_top=self._dm_top, dm_bot=self._dm_bot,
        #                dm_port=self._dm_port,
        #                mcp=self._mcp, ui=self._ui, cp_T=self._cp_T,
        #                cp_top=self._cp_top,
        #                cp_bot=self._cp_bot, cp_port=self._cp_port,
        #                dT_cond=self.dT_cond, dT_adv=self.dT_adv,
        #                port_own_idx=self._port_own_idx,
        #                port_own_idx_2D=self._port_own_idx_2D,
        #                port_link_idx=self._port_link_idx)

        #        (self.dT_total, self._process_flows, self._models._step_stable,
        #         self._models._vN_max_step, self._models._max_factor,
        #         self.alpha_inf_lid) = tes_diff(
        #            T_ext=self._T_ext, T_port=self._T_port, T_s=self._T_s,
        #            T_s_lid=self._T_s_lid, T_amb=self._T_amb,
        #            ports_all=self._models.ports_all,  # temperatures
        #            dm_io=self._dm_io, dm=self.dm, dm_top=self._dm_top,
        #            dm_bot=self._dm_bot, dm_port=self._dm_port,
        #            res_dm=self.res_dm,  # flows
        #            cp_T=self._cp_T, lam_T=self._lam_T, rho_T=self._rho_T,
        #            ny_T=self._ny_T, lam_mean=self._lam_mean, cp_port=self._cp_port,
        #            lam_port_fld=self._lam_port_fld,  # mat. props.
        #            mcp=self._mcp, rhocp=self._rhocp, lam_wll=self._lam_wll,
        #            lam_ins=self._lam_ins, mcp_wll=self._mcp_wll, ui=self._ui,
        #            alpha_i=self._alpha_i, alpha_inf=self._alpha_inf,
        #            #alpha_inf_lid=self._alpha_inf_lid,  # alpha values
        #            UA_tb=self._UA_tb, UA_tb_wll=self._UA_tb_wll,
        #            UA_amb_shell=self._UA_amb_shell, UA_amb_lid=self._UA_amb_lid,
        #            UA_port=self._UA_port, UA_port_wll=self._UA_port_wll,  # UA values
        #            port_own_idx=self._port_own_idx, port_own_idx_2D=self._port_own_idx_2D,
        #            port_link_idx=self._port_link_idx,  # indices
        #            grid_spacing=self.grid_spacing, port_gsp=self._port_gsp,
        #            port_subs_gsp=self._port_subs_gsp, d_i=self._d_i,
        #            cell_dist=self._cell_dist, flow_length=self._flow_length,
        #            flow_length_lid=self._flow_length_lid, r_total=self._r_total,
        #            r_ln_wll=self._r_ln_wll, r_ln_ins=self._r_ln_ins,
        #            r_rins=self._r_rins, s_wll=self._s_wll, s_ins=self._s_ins,  # lengths
        #            A_cell=self.A_cell, V_cell=self.V_cell, A_shell_i=self._A_shell_i,
        #            A_shell_ins=self._A_shell_ins, A_p_fld_mean=self._A_p_fld_mean,  # areas and vols
        #            process_flows=self._process_flows, vertical=self._vertical,
        #            vertical_lid=self._vertical_lid, lid_top=self._lid_top,
        #            step_stable=self._models._step_stable,  # bools
        #            part_id=self.part_id, stability_breaches=self._stability_breaches,
        #            vN_max_step=self._models._vN_max_step,
        #            max_factor=self._models._max_factor,  # misc.
        #            stepnum=self._models.stepnum, timestep=timestep,  # step information
        #            dT_cond=self.dT_cond, dT_adv=self.dT_adv, dT_total=self.dT_total)  # differentials

        #        (self.dT_total, self._process_flows, self._models._step_stable,
        #         self._models._vN_max_step, self._models._max_factor,
        #         self.alpha_inf_lid) = tes_diff_overload(self._input_args, timestep)
        _pf.tes_diff(*self._input_args, timestep)
        #        self._tes_jcls.tes_diff_j(timestep)
        #        self.tes_diff_clsd(self._data_float1D, self._data_float2D,
        #                           self._data_bool, self._data_int, timestep)
        #        tes_diff_overload(self._input_args, timestep)

        #        self._diff_clsd(**self._input_args_call, timestep=timestep)

        #        if self.stepnum[0] == 100:
        #            raise ValueError

        #        if self._T_port.ndim == 1:
        #            # calculate heat transfer by conduction
        #            self.dT_cond[:] = (
        #                    (+ self._UA_tb[:-1] * (self._T_top - self.T)
        #                     + self._UA_tb[1:] * (self._T_bot - self.T)
        #                     + self._UA_port * (self._T_port - self.T)
        #                     + self._UA_amb_shell * (self._T_amb - self.T))
        #                    / self._mcp)
        #            # add losses through top and bottom lid:
        #            self.dT_cond[0] += (
        #                    self._UA_amb_lid[0] * (self._T_amb - self.T[0])
        #                    / self._mcp[0])
        #            self.dT_cond[-1] += (
        #                    self._UA_amb_lid[-1] * (self._T_amb - self.T[-1])
        #                    / self._mcp[-1])
        #            # calculate heat transfer by advection
        #            self.dT_adv[:] = (
        #                    (+ self._dm_top * (self._cp_top * self._T_top - ui)
        #                     + self._dm_bot * (self._cp_bot * self._T_bot - ui)
        #                     + self._dm_port * (self._cp_port * self._T_port - ui))
        #                    / self._mcp)
        #        else:
        #            # the same if multiple ports per cell exist. to correctly calculate
        #            # this, the sum of the arrays has to be taken:
        #            self.dT_cond[:] = (
        #                    (+ self._UA_tb[:-1] * (self._T_top - self.T)
        #                     + self._UA_tb[1:] * (self._T_bot - self.T)
        #                     + np.sum(self._UA_port * (self._T_port - self.T),
        #                              axis=0)
        #                     + self._UA_amb_shell * (self._T_amb - self.T))
        #                    / self._mcp)
        #            # add losses through top and bottom lid:
        #            self.dT_cond[0] += (
        #                    self._UA_amb_lid[0] * (self._T_amb - self.T[0])
        #                    / self._mcp[0])
        #            self.dT_cond[-1] += (
        #                    self._UA_amb_lid[-1] * (self._T_amb - self.T[-1])
        #                    / self._mcp[-1])
        #            # calculate heat transfer by advection
        #            self.dT_adv[:] = (
        #                    (+ self._dm_top * (self._cp_top * self._T_top - ui)
        #                     + self._dm_bot * (self._cp_bot * self._T_bot - ui)
        #                     + np.sum(self._dm_port
        #                              * (self._cp_port * self._T_port - ui), axis=0))
        #                    / self._mcp)

        #        return self.dT_cond + self.dT_adv
        return self.dT_total

    #        return ab

    def _buoyancy(self, timestep):
        """
        Calculates free convection due to buoyancy. This is only applicable for
        parts, where the cells are stacked vertically!

        The equations follow ???, ??: "Thermals in stratified Environment".

        General syntax information:
            [:-1] gets the cells on top of the current cell, if the current
            cells are being indexed starting with index 1: [1:]
            Thus all arrays using the cells for which the buoyancy has to be
            calculated are indexed with [1:] and the cells to calculate the
            anomalies in density etc. are using the index [:-1] since this
            method is always comparing each cell's properties to the properties
            of the cell above. This means each cell's fluid is assumed to
            displace the fluid of the cell above.
        """

        """
        TODO: temp array!
        """
        self.bf = np.zeros(self.T.shape[0] - 1)
        # get fluid density difference between current cell and cell above it
        # (rho_cell -  rho_cell_top). If this is positive, there is an
        # inverison between the two temperature layers:
        diff_rho = np.diff(self._rho_T)
        # check if any density inversions are existing (if cell at top
        # has index 0, a negative diff is an inversion, otherwise pos.):
        if np.any(diff_rho < 0):
            #            print('density difference: ', diff_rho)
            #            print('Temperature: ', self.T)
            # gravitational acceleration in [m/s^2]:
            g = 9.81
            """
            TODO: corr parameter needed?
            """
            # Korrekturparameter (zur Anpassung der Berechnung an die Realität):
            #            buo_corr = 0.5
            # get reduced gravitational acceleration by dividing the diff of
            # rho by the density of the cell above (density difference relative
            # to the cell above, thus relative to the density of the displaced
            # fluid):
            g_red = g * diff_rho / self._rho_T[:-1]
            # since comparison with the cell above is chosen, only negative
            # accelerations (negative acc. is pointing upwards) indicate a
            # density inversion:
            g_red[g_red > -1e-14] = 0
            #            g_red[g_red > 0] = 0
            # set values closer to zero than -1e-15 to zero to avoid floating
            # point error DO THAT IN THE LINE ABOVE!
            #            g_red[abs(g_red) < 1e-16] = 0
            # empirical differential equation integration constants for
            # buoyancy calculation (all precalculated and just displayed for
            # easy lookup):
            #            m = 2.54  # thermal shape constant
            #            a = 1.9
            # int_const = (a/(3*m))**3 / 4  # shape and integration constant
            #            int_const = 0.0038755727846830432  # precalculated integration const
            # shape and integration constant:
            # int_const_v = ((3*m/a)**3 * 4)**(0.25) / 4
            int_const_v = 1.0019730356831313  # precalculated integration const
            # save timestep to a shorter name variable:
            t = timestep
            # calculate stability frequency (Brunt-Väisälä-frequency) with the
            # reference density being each cells own density and the density
            # gradient by taking the central difference of the density in the
            # middle of the array and the forward/backward difference at the
            # ends. Since height convention for this simulation environment is
            # from top to bottom, the minus from Brunt-Väisälä is omitted. Omit
            # the first cell AFTER getting the gradient to retain central diff
            # while applying the calculation rule that each cell is only in
            # exchange with its top cell to avoid double intermixing of flow.
            # get moving average over N cells of gradient of rho to smooth out
            # local instabilites:
            """
            TODO: moving average replaced with general mean to make it more
            stable and avoid zero-dividing due to same temperature in two cells
            """
            mavggrad = _pf.moving_avg_fill_edges(
                np.gradient(self._rho_T, self.grid_spacing), 40
            )

            #            if np.any(mavggrad < 0):
            #                raise ValueError
            # absolute to disable instable stratification:
            N = np.sqrt(np.abs(g * mavggrad[1:] / self._rho_T[1:]))
            # set 0 values to a small number:
            N[N == 0] = 1e-300

            # get mean value of density gradient divided by reference density:
            #            rho_mean = (np.gradient(self._rho_T, self.grid_spacing)[1:]
            #                        / self._rho_T[1:]).mean()
            # get stability frequency (absolute to disable instable
            # stratification):
            #            N = np.sqrt(abs(g * rho_mean))

            #            print('BV frequency: ', N)

            # calculate the angular frequency of the Brunt-Väisälä-oscillation:
            omega = (2 / 3) ** 0.5 * N

            #            # only take last steps velocity if step was succesful (thus there
            #            # are no failed steps yet) to avoid accumulating vertical velocity:
            #            if self._models._failed_steps[self._models.stepnum] == 0:
            #                # moving all cell velocities one cell up since to move the
            #                # fluid volumes inertia with the fluid volume AND multiply with
            #                # the factor of exchanged cell volume to respect the mixing
            #                # with stationary fluid:
            #                self._v_prev[:-1] = self._v_vert[1:]
            # calculate the integration coefficients A and B with R_0 set to
            # the 1/2 of the inner radius R_0=0.5*d_i/2 and w_0 to w_old:
            R_0 = self._d_i / 16
            #            A = R_0**3 * self._v_prev * 0
            B = (2 / 3) ** 0.5 * R_0 ** 3 * g_red / N
            #            # calculate the vertical space that the fluid cells will cross in
            #            # one timestep due to buoyancy and get the mean velocity in [m/s]
            #            # during the timestep from this:
            #            v_vert = (
            #                    ((A * np.sin(omega * t) - B * np.cos(omega * t)) / omega
            #                     * int_const)**0.25  # this gets the vertical distance
            #                    / t).real  # this gets the mean velocity during t
            # NOW WITHOUT INERTIA:
            # get massflow directly
            #            is this really the velocity or the acceleration? / t makes this
            #            huge and impossible to calculate!
            # this equation gets the position and divides it by the time. thus
            # only in discrete form correct. since discrete is not an option
            # here, better get the derivative of it:
            #            bf = (((- B * np.cos(omega * t)) / (omega * int_const))**0.25
            #                  / t * self.A_cell * self._rho_T[1:])
            # equation for flow speed from derivative of above equation.
            # massflow extracted directly with A_cell, rho_T and 1/sqrt(2).
            # since the calculated flow speed/massflow is the peak-massflow at
            # the end of the timestep, 1/sqrt(2) = 1/1.414 is needed to get
            # the RMS of the peak massflow and the start massflow of 0:
            bf = (
                int_const_v
                * omega
                * np.tan(omega * t)
                * ((-B * np.cos(omega * t)) / omega) ** (0.25)  # get velocity
                * self.A_cell
                * self._rho_T[1:]
                / 1.41421356
            )  # get dm
            #            raise ValueError('ok, use Nusselt convection buoyancy, since this '
            #                             'is not critical with increasing timesteps! '
            #                             'Especially when t is big enough, the '
            #                             'calculaction here tends to be instable since '
            #                             'cosine becomes negative, resulting in nan!')
            # set nan values to 0:
            bf[np.isnan(bf)] = 0
            """
            TODO: remove temp saver"""
            self.bf = bf
            """
            TODO: remove negative bf equalizer"""
            bf = abs(bf)
            #            raise ValueError
            #            (a/3m)^3 z^3 dz/dt = A cos(omega t) + B sin(omega t)
            #            # get the buoyancy flow in [kg/s] from the flow velocity:
            #            bf = v_vert * self.A_cell * self._rho_T[1:]
            # apply inelastic collision for the rising fluid mixing with the
            # stationary fluid on top, based on proportion of exchanged mass.
            # v_vert*t/gridspacing is the exchange factor, mult. with v_vert to
            # get new combined v_vert:
            #            self._v_vert = v_vert**2 * t / self.grid_spacing

            #            if np.any(np.any(np.isnan(v_vert))):
            #                raise ValueError
            #            if np.any(self._v_vert > v_vert):
            #                print('v-factor: ', self._v_vert / v_vert)
            #                raise ValueError
            # add up the buoyancy flow to the top/bottom massflow grids. since
            # the density anomaly is calculated by comparison with the top
            # cell, the first entry of bf (index 0) corresponds to a
            # mass-exchange of the first and second cell. Thus the buoyancy
            # flow is added to the massflow inflowing into the first cell from
            # the bottom AND into the second cell from the top:
            self._dm_top[1:] += bf
            self._dm_bot[:-1] += bf

            bf_max = bf.max()
            if self.max_bf < bf_max:
                self.max_bf = bf_max

            #            if self._models.stepnum == 3 and self._cnt_inside_step == 4:
            #                raise ValueError('buo')

            if np.any(bf < 0):
                raise ValueError('negative bf!')

    #            if self._models.stepnum == 5000:
    #                raise ValueError

    #            if np.any(bf > 100):
    #                raise ValueError

    #            print('buoyancy flow: ', bf)
    #            raise ValueError

    def buo_Nu(self):
        # get temperature difference for all cells (temperature below last cell
        # is 0, thus don't use the last cell):
        #        T_diff = self._T_bot[:-1] - self.T[:-1]  # replaced by calc below:
        T_diff = self.T[1:] - self.T[:-1]
        # if there is no temperature inversion, skip this function:
        if np.all(T_diff <= 0):
            return
        # only use the positive difference (inverted cells):
        T_diff[T_diff < 0] = 0
        # buoyancy correction factor to get the buoyant flow from fluid-fluid
        # instead of a solid-fluid horizontal plate:
        corr_f = 20
        # preallocate arrays:
        shape = self.T.shape[0] - 1
        Nu = np.zeros(shape)

        # free convection over a horizontal plate, VDI F2 3.1:
        # get material properties for all bottom cells:
        Pr = _pf.Pr_water_return(self.T[1:])
        beta = _pf.beta_water_return(self.T[1:])
        # to deal with the minimum in water density at 4°C, just set negative
        # values to zero...
        #        beta_neg = beta < 0
        beta[beta < 0] *= -1
        # get characteristic length:
        L = self._d_i / 4
        # get Rayleigh number
        Ra = Pr * 9.81 * L ** 3 * beta * T_diff / self._ny_T[1:] ** 2
        # get Rayleigh number with Prandtl function, VDI F2 eq (9):
        Ra_f2 = Ra * (1 + (0.322 / Pr) ** (11 / 20)) ** (-20 / 11)
        # get bool index for laminar or turbulent convection:
        turb = Ra_f2 > 7e4
        # get Nusselt number, following VDI Wärmeatlas 2013 F2 eq (7) and (8):
        Nu[~turb] = 0.766 * (Ra_f2[~turb]) ** 0.2
        Nu[turb] = 0.15 * (Ra_f2[turb]) ** (1 / 3)
        # get the alpha number for free convection. each cell corresponds to
        # the alpha value for convection between the current cell and the cell
        # on top:
        #        alpha = Nu * self._lam_T[1:] / self.grid_spacing
        # get bool index for Nusselt number > 1 to ignore lower values
        Nu_idx = Nu >= 1
        # multiplicate lambda value between cells with the Nusselt number. The
        # calculation of the alpha value is implemented in the calculation of
        # the UA value.
        self._lam_mean[Nu_idx] *= Nu[Nu_idx] * corr_f

        # Rayleigh Bernard convection (too slow?)
        # get mean temperature for material properties:


#        T_mean = (self._T_bot + self.T) / 2
#        # get material properties:
#        get_ny_water(T_mean, ny_b)
#        get_Pr_water(T_mean, Pr_b)
#        get_beta_water(T_mean, beta_b)
#        # get Rayleigh-number as Ra=Gr*Pr:
#        L = self.grid_spacing
#        Ra_b = Pr_b * 9.81 * L**3 * beta_b * T_diff / ny_b**2
#        Nu_b[Ra_b < 2.2e4] = 0.208 * Ra_b[Ra_b < 2.2e4]**(0.25)
#        Nu_b[Ra_b >= 2.2e4] = 0.092 * Ra_b[Ra_b >= 2.2e4]**(0.33)
