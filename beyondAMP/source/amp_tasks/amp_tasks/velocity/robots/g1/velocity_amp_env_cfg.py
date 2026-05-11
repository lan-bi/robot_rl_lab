
from isaaclab.utils import configclass
from .velocity_env_cfg import RobotEnvCfg

from robotlib.robot_keys.g1_29d import g1_key_body_names

from beyondAMP.obs_groups import AMPObsBodyHardTrackCfg


@configclass
class G1VelocityAMPEnvCfg(RobotEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.observations.amp = AMPObsBodyHardTrackCfg().adjust_key_body_indexes(
            ["body_pos_w", "body_quat_w", "body_lin_vel_w", "body_ang_vel_w"],
            g1_key_body_names,
        )