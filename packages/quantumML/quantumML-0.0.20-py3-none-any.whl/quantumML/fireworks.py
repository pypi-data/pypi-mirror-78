from fireworks import Firework
from atomate.vasp.config import (
    HALF_KPOINTS_FIRST_RELAX,
    RELAX_MAX_FORCE,
    VASP_CMD,
    DB_FILE,
    VDW_KERNEL_DIR,
)
from pymatgen.io.vasp.sets import MPRelaxSet
import warnings
from atomate.vasp.firetasks.write_inputs import WriteVaspFromIOSet
from atomate.vasp.firetasks.run_calc import RunVaspCustodian
from atomate.common.firetasks.glue_tasks import PassCalcLocs, CopyFiles
from atomate.vasp.firetasks.parse_outputs import VaspToDb

class OptimizeFW2D(Firework):
    def __init__(
            self,
            structure,
            name="structure optimization",
            vasp_input_set=None,
            vasp_cmd=VASP_CMD,
            override_default_vasp_params=None,
            ediffg=None,
            db_file=DB_FILE,
            vdw_kernel_dir=VDW_KERNEL_DIR,
            force_gamma=True,
            job_type="double_relaxation_run",
            max_force_threshold=RELAX_MAX_FORCE,
            auto_npar=">>auto_npar<<",
            half_kpts_first_relax=HALF_KPOINTS_FIRST_RELAX,
            parents=None,
            **kwargs
    ):
        """
        Optimize the given structure.
        Args:
            structure (Structure): Input structure.
            name (str): Name for the Firework.
            vasp_input_set (VaspInputSet): input set to use. Defaults to MPRelaxSet() if None.
            override_default_vasp_params (dict): If this is not None, these params are passed to
                the default vasp_input_set, i.e., MPRelaxSet. This allows one to easily override
                some settings, e.g., user_incar_settings, etc.
            vasp_cmd (str): Command to run vasp.
            ediffg (float): Shortcut to set ediffg in certain jobs
            db_file (str): Path to file specifying db credentials to place output parsing.
            force_gamma (bool): Force gamma centered kpoint generation
            job_type (str): custodian job type (default "double_relaxation_run")
            max_force_threshold (float): max force on a site allowed at end; otherwise, reject job
            auto_npar (bool or str): whether to set auto_npar. defaults to env_chk: ">>auto_npar<<"
            half_kpts_first_relax (bool): whether to use half the kpoints for the first relaxation
            parents ([Firework]): Parents of this particular Firework.
            \*\*kwargs: Other kwargs that are passed to Firework.__init__.
        """
        override_default_vasp_params = override_default_vasp_params or {}
        vasp_input_set = vasp_input_set or MPRelaxSet(
            structure, force_gamma=force_gamma, **override_default_vasp_params
        )

        if vasp_input_set.incar["ISIF"] in (0, 1, 2, 7) and job_type == "double_relaxation":
            warnings.warn(
                "A double relaxation run might not be appropriate with ISIF {}".format(
                    vasp_input_set.incar["ISIF"]))

        t = []
        t.append(WriteVaspFromIOSet(structure=structure, vasp_input_set=vasp_input_set))
        t.append(CopyFiles(from_dir=vdw_kernel_dir))
        t.append(
            RunVaspCustodian(
                vasp_cmd=vasp_cmd,
                job_type=job_type,
                max_force_threshold=max_force_threshold,
                ediffg=ediffg,
                auto_npar=auto_npar,
                half_kpts_first_relax=half_kpts_first_relax,
            )
        )
        t.append(PassCalcLocs(name=name))
        t.append(VaspToDb(db_file=db_file, additional_fields={"task_label": name}))
        super(OptimizeFW, self).__init__(
            t,
            parents=parents,
            name="{}-{}".format(structure.composition.reduced_formula, name),
            **kwargs
        )

