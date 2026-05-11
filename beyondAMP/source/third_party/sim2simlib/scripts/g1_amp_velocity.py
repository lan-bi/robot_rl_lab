"""G1 AMP velocity sim-to-sim runner for MuJoCo.

This script mirrors the G1 AMP velocity policy observation layout used by
BeyondAMP and loads a TorchScript policy exported from the training run.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from sim2simlib import MUJOCO_ASSETS
from sim2simlib.model.actuator_motor import PIDMotor
from sim2simlib.model.config import ActionsCfg, MotorCfg, ObservationsCfg, Sim2SimCfg
from sim2simlib.model.sim2sim_base import Sim2SimBaseModel


class G1AmpVelocityModel(Sim2SimBaseModel):
    """MuJoCo runner that matches the AMP-trained G1 velocity policy obs layout."""

    def _obs_projected_gravity(self) -> np.ndarray:
        return self._obs_gravity_orientation()

    def _obs_velocity_commands(self) -> np.ndarray:
        return self._obs_cmd()

    def _obs_joint_pos_rel(self) -> np.ndarray:
        return self._obs_joint_pos()

    def _obs_joint_vel_rel(self) -> np.ndarray:
        return self._obs_joint_vel()


def build_config(policy_path: str, xml_path: str, cmd: list[float]) -> Sim2SimCfg:
    policy_joint_names = [
        "left_hip_pitch_joint",
        "right_hip_pitch_joint",
        "waist_yaw_joint",
        "left_hip_roll_joint",
        "right_hip_roll_joint",
        "waist_roll_joint",
        "left_hip_yaw_joint",
        "right_hip_yaw_joint",
        "waist_pitch_joint",
        "left_knee_joint",
        "right_knee_joint",
        "left_shoulder_pitch_joint",
        "right_shoulder_pitch_joint",
        "left_ankle_pitch_joint",
        "right_ankle_pitch_joint",
        "left_shoulder_roll_joint",
        "right_shoulder_roll_joint",
        "left_ankle_roll_joint",
        "right_ankle_roll_joint",
        "left_shoulder_yaw_joint",
        "right_shoulder_yaw_joint",
        "left_elbow_joint",
        "right_elbow_joint",
        "left_wrist_roll_joint",
        "right_wrist_roll_joint",
        "left_wrist_pitch_joint",
        "right_wrist_pitch_joint",
        "left_wrist_yaw_joint",
        "right_wrist_yaw_joint",
    ]

    return Sim2SimCfg(
        robot_name="g1_amp_velocity",
        simulation_dt=0.002,
        slowdown_factor=1.0,
        control_decimation=10,
        xml_path=xml_path,
        policy_path=policy_path,
        policy_joint_names=policy_joint_names,
        default_pos=np.array([0.0, 0.0, 0.76], dtype=np.float32),
        default_angles={
            ".*_hip_pitch_joint": -0.312,
            ".*_knee_joint": 0.669,
            ".*_ankle_pitch_joint": -0.363,
            ".*_elbow_joint": 0.6,
            "left_shoulder_roll_joint": 0.2,
            "left_shoulder_pitch_joint": 0.2,
            "right_shoulder_roll_joint": -0.2,
            "right_shoulder_pitch_joint": 0.2,
        },
        observation_cfg=ObservationsCfg(
            base_observations_terms=[
                "base_lin_vel",
                "base_ang_vel",
                "projected_gravity",
                "velocity_commands",
                "joint_pos_rel",
                "joint_vel_rel",
                "last_action",
            ],
            using_base_obs_history=True,
            base_obs_flatten=False,
            base_obs_his_length=5,
            scale={
                "base_lin_vel": 1.0,
                "base_ang_vel": 0.2,
                "projected_gravity": 1.0,
                "velocity_commands": 1.0,
                "joint_pos_rel": 1.0,
                "joint_vel_rel": 0.05,
                "last_action": 1.0,
            },
        ),
        cmd=cmd,
        action_cfg=ActionsCfg(
            action_clip=(-100.0, 100.0),
            scale=0.25,
        ),
        motor_cfg=MotorCfg(
            motor_type=PIDMotor,
            effort_limit={
                ".*_hip_roll_joint": 300,
                ".*_hip_yaw_joint": 300,
                ".*_hip_pitch_joint": 300,
                ".*_knee_joint": 300,
                "waist_.*_joint": 300,
                ".*_shoulder_pitch_joint": 300,
                ".*_shoulder_roll_joint": 300,
                ".*_shoulder_yaw_joint": 300,
                ".*_elbow_joint": 300,
                ".*_wrist_roll_joint": 300,
                ".*_wrist_pitch_joint": 300,
                ".*_wrist_yaw_joint": 300,
                ".*_ankle_pitch_joint": 20,
                ".*_ankle_roll_joint": 20,
            },
            stiffness={
                ".*_hip_yaw_joint": 100.0,
                ".*_hip_roll_joint": 100.0,
                ".*_hip_pitch_joint": 100.0,
                ".*_knee_joint": 150.0,
                "waist_.*_joint": 200.0,
                ".*_shoulder_pitch_joint": 40.0,
                ".*_shoulder_roll_joint": 40.0,
                ".*_shoulder_yaw_joint": 40.0,
                ".*_elbow_joint": 40.0,
                ".*_wrist_roll_joint": 40.0,
                ".*_wrist_pitch_joint": 40.0,
                ".*_wrist_yaw_joint": 40.0,
                ".*_ankle_pitch_joint": 40.0,
                ".*_ankle_roll_joint": 40.0,
            },
            damping={
                ".*_hip_yaw_joint": 2.0,
                ".*_hip_roll_joint": 2.0,
                ".*_hip_pitch_joint": 2.0,
                ".*_knee_joint": 4.0,
                "waist_.*_joint": 5.0,
                ".*_shoulder_pitch_joint": 10.0,
                ".*_shoulder_roll_joint": 10.0,
                ".*_shoulder_yaw_joint": 10.0,
                ".*_elbow_joint": 10.0,
                ".*_wrist_roll_joint": 10.0,
                ".*_wrist_pitch_joint": 10.0,
                ".*_wrist_yaw_joint": 10.0,
                ".*_ankle_pitch_joint": 2.0,
                ".*_ankle_roll_joint": 2.0,
            },
        ),
        debug=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run G1 AMP velocity policy in MuJoCo")
    parser.add_argument(
        "--policy-path",
        type=str,
        default="./logs/rsl_rl/g1_amp_velocity/exported/policy.pt",
        help="Path to the exported TorchScript policy.",
    )
    parser.add_argument(
        "--xml-path",
        type=str,
        default=MUJOCO_ASSETS["unitree_g1_29dof"],
        help="Path to the MuJoCo XML model.",
    )
    parser.add_argument("--headless", action="store_true", help="Run without a viewer window.")
    parser.add_argument("--cmd", nargs=3, type=float, default=[1.0, 0.0, 0.0], help="Velocity command [vx vy wz].")
    args = parser.parse_args()

    policy_path = str(Path(args.policy_path).expanduser())
    xml_path = str(Path(args.xml_path).expanduser())

    config = build_config(policy_path=policy_path, xml_path=xml_path, cmd=list(args.cmd))
    model = G1AmpVelocityModel(config)

    if args.headless:
        model.headless_run()
    else:
        model.view_run()


if __name__ == "__main__":
    main()