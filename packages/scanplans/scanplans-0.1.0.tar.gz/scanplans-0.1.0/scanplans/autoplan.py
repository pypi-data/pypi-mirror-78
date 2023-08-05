"""A function to measure a series of samples automatically."""
from bluesky.plan_stubs import mv, sleep, checkpoint, wait
from bluesky.preprocessors import plan_mutator
from xpdacq.beamtime import xpd_configuration, Beamtime

import scanplans.mdgetters as mg
from scanplans.tools import inner_shutter_control

__all__ = [
    "autoplan"
]


def autoplan(bt: Beamtime, sample_index, plan_index, wait_time=30., auto_shutter=False):
    """
    Yield messages to count the predefined measurement plan on the a list of samples on a sample rack. It requires
    the following information to be added for each sample.
        position_x The x position of the sample in mm.
        position_y The y position of the sample in mm.
        wait_time The waiting time between the end of the former plan and the start of the latter plan in second.

    Parameters
    ----------
    bt: Beamtime
        The Beamtime instance that contains the sample information.
    sample_index : List[int]
        A list of the sample index in the BeamTime instance.
    plan_index: List[int]
        A list of the plan index in the BeamTime instance.
    wait_time : float
        Waiting time before conduct plan for each sample in second.
    auto_shutter : bool
        Whether to mutate the plan with inner_shutter_control.

    Yields
    ------
    Msg
        Messages of the plan.

    Examples
    --------
    Add position controller to the xpd_configuration.
        >>> xpd_configuration["posx_controller"] = Grid_X
        >>> xpd_configuration["posy_controller"] = Grid_Y
    Register the scan plan to the beamtime.
        >>> ScanPlan(bt, ct, 30)
    Add the information of 'position_x', 'position_y' and 'wait_time' to the excel and import.
    Automatically conduct the scan plan for sample No.0 and No.1
        >>> plan = autoplan(bt, [0, 1])
        >>> xrun({}, plan)
    """
    posx_controller = xpd_configuration["posx_controller"]
    posy_controller = xpd_configuration["posy_controller"]

    for sample_ind, plan_ind in zip(sample_index, plan_index):
        sample = translate_to_sample(bt, int(sample_ind))
        posx = mg.get_from_sample(sample, "position_x")
        posy = mg.get_from_sample(sample, "position_y")
        count_plan = mg.translate_to_plan(bt, int(plan_ind), sample)
        if auto_shutter:
            count_plan = plan_mutator(count_plan, inner_shutter_control)
        if posx and posy and count_plan:
            yield from checkpoint()
            print(f"INFO: Move to x: {posx}")
            yield from mv(posx_controller, float(posx))
            yield from checkpoint()
            print(f"INFO: Move to y: {posy}")
            yield from mv(posy_controller, float(posy))
            yield from checkpoint()
            yield from wait()
            print(f"INFO: Wait for {wait_time} s")
            yield from sleep(float(wait_time))
            yield from checkpoint()
            yield from count_plan
