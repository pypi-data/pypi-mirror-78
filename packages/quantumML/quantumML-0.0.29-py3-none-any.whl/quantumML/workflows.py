from pymatgen.io.vasp.sets import DictSet, _load_yaml_config
from pymatgen.core.structure import Structure
from atomate.vasp.workflows.base.core import get_wf
from atomate.vasp.fireworks.core import StaticFW, NonSCFFW
from atomate.vasp.powerups import add_small_gap_multiply, add_stability_check, add_modify_incar, \
    add_wf_metadata, add_common_powerups
from quantumML.fireworks import OptimizeFW2D

from atomate.vasp.config import SMALLGAP_KPOINT_MULTIPLY, STABILITY_CHECK, VASP_CMD, DB_FILE, \
    ADD_WF_METADATA, VDW_KERNEL_DIR
import numpy as np
import os
from fireworks import  Workflow
from monty.serialization import loadfn
from pathlib import Path

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def _read_user_incar(fname):
    fpath = os.path.join(module_dir,fname)
    fil = open(fpath, 'r')
    lines = fil.readlines()
    incar = {}
    for line in lines:
        key = (line.split('=')[0].strip())
        val = line.split('=')[-1].strip()
        incar[key] = val
    return incar



class MPRelaxSet2D(DictSet):
    """
    Implementation of VaspInputSet utilizing parameters in the public
    Materials Project. Typically, the pseudopotentials chosen contain more
    electrons than the MIT parameters, and the k-point grid is ~50% more dense.
    The LDAUU parameters are also different due to the different psps used,
    which result in different fitted values.
    """

    CONFIG = _load_yaml_config("MPRelaxSet")

    def __init__(self, structure, **kwargs):
        """
        :param structure: Structure
        :param kwargs: Same as those supported by DictSet.
        """
        incar = _read_user_incar('Relax2D.txt')
        super().__init__(structure, MPRelaxSet2D.CONFIG, user_incar_settings=incar, **kwargs)
        self.kwargs = kwargs



def wf_bandstructure2D(structure, c=None):

    c = c or {}
    vasp_cmd = c.get("VASP_CMD", VASP_CMD)
    db_file = c.get("DB_FILE", DB_FILE)
    vdw_kernel = c.get("VDW_KERNEL_DIR", VDW_KERNEL_DIR)

    mpr2d = MPRelaxSet2D(structure, force_gamma=True)
    fws = [OptimizeFW2D(structure=structure, vasp_input_set=mpr2d, vasp_cmd=vasp_cmd, db_file=db_file, vdw_kernel_dir=vdw_kernel)]
    fws.append(StaticFW(parents=fws[0]))
    fws.append(NonSCFFW(parents=fws[1], mode='uniform'))
    fws.append(NonSCFFW(parents=fws[1], mode='line'))
    wf = Workflow(fws)
    '''check bandstructure.yaml'''
    '''
    wf = get_wf(structure, "bandstructure.yaml", vis=MPScanRelaxSet2D(structure, force_gamma=True,), \
                params=[{'vasp_input_set': mpr2d},{},{},{}], common_params={"vasp_cmd": vasp_cmd, "db_file": db_file,}) #"vdw_kernel_dir": vdw_kernel})

    wf = add_common_powerups(wf, c)
    '''
    if c.get("SMALLGAP_KPOINT_MULTIPLY", SMALLGAP_KPOINT_MULTIPLY):
        wf = add_small_gap_multiply(wf, 0.5, 5, "static")
        wf = add_small_gap_multiply(wf, 0.5, 5, "nscf")

    if c.get("STABILITY_CHECK", STABILITY_CHECK):
        wf = add_stability_check(wf, fw_name_constraint="structure optimization")

    if c.get("ADD_WF_METADATA", ADD_WF_METADATA):
        wf = add_wf_metadata(wf, structure)

    print(wf)
    '''
    fws = wf.fws
    fws[0] = new_firework
    print(fws)
    '''
    return wf