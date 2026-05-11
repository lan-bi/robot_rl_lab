
file_punch = "data/demo/punch/punch.npz"

file_soccer_shoot = "data/datasets/MocapG1Full/shoot.npz"

file_velocity_dog_move = "data/demo/dog_move/dog_move.npz"

file_velocity_knee_walk = "data/demo/knee_walk/knee_walk.npz"
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[3]
_G1_WALK_DIR = _REPO_ROOT / "data" / "datasets" / "LAFAN1_Retargeting_Dataset" / "g1"

velocity_task_files = [
	str(_G1_WALK_DIR / "walk1_subject1.npz"),
	str(_G1_WALK_DIR / "walk1_subject2.npz"),
	str(_G1_WALK_DIR / "walk1_subject5.npz"),
	str(_G1_WALK_DIR / "walk2_subject1.npz"),
	str(_G1_WALK_DIR / "walk2_subject3.npz"),
	str(_G1_WALK_DIR / "walk2_subject4.npz"),
	str(_G1_WALK_DIR / "walk3_subject1.npz"),
	str(_G1_WALK_DIR / "walk3_subject2.npz"),
	str(_G1_WALK_DIR / "walk3_subject3.npz"),
	str(_G1_WALK_DIR / "walk3_subject4.npz"),
	str(_G1_WALK_DIR / "walk3_subject5.npz"),
	str(_G1_WALK_DIR / "walk4_subject1.npz"),
]