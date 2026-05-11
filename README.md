# AMP 改造记录

## Step 1
- 已确认 walk 重定向数据已经转换为 `.npz`，并放入 `beyondAMP/data/datasets/LAFAN1_Retargeting_Dataset/g1/`。
- 后续将基于 G1 walk 任务逐步改造 AMP 训练链路、判别器和推理/仿真流程。

## Step 2
- 在 [beyondAMP/source/amp_tasks/amp_tasks/velocity/robots/g1/velocity_env_cfg.py](beyondAMP/source/amp_tasks/amp_tasks/velocity/robots/g1/velocity_env_cfg.py) 中新增了 `G1VelocityAMPEnvCfg`。
- 该环境变体接入了 `AMPObsBodyHardTrackCfg`，并将 G1 的 key body names 作为 AMP 观测对齐目标。
- 这一步只是在环境侧准备 AMP 观测接口，尚未修改 PPO 算法和判别器训练逻辑。

## Step 3
- 已将 [beyondAMP/source/amp_tasks/amp_tasks/velocity/robots/g1/rsl_rl_ppo_cfg.py](beyondAMP/source/amp_tasks/amp_tasks/velocity/robots/g1/rsl_rl_ppo_cfg.py) 切换为 AMP 训练配置。
- 训练数据改为 `data/datasets/LAFAN1_Retargeting_Dataset/g1/` 下的 12 个 walk `.npz`。
- 判别器观测切换为 `AMPObsHardTrackTerms`，与刚新增的 AMP 环境观测保持一致。
- 算法改为 `AMPPPOWeightedAlgorithmCfg`，并提高了 AMP reward 权重，让风格约束更强。

## Step 4
- 已修正 [beyondAMP/source/amp_tasks/amp_tasks/velocity/robots/g1/velocity_amp_env_cfg.py](beyondAMP/source/amp_tasks/amp_tasks/velocity/robots/g1/velocity_amp_env_cfg.py)，让注册表实际使用的 AMP 环境也接入 `AMPObsBodyHardTrackCfg`。
- 这样环境入口、判别器输入和 expert 数据三者现在是同一套 hard-track 观测对齐逻辑。

## Step 5
- 已把 [unitree_mujoco/simulate_python/config.py](unitree_mujoco/simulate_python/config.py) 的默认机器人切到 `g1`。
- unitree_mujoco 里已经有 G1 的 MJCF / scene 文件，可以直接作为 MuJoCo 侧的 sim-to-sim 验证后端。
- 后续会基于同一套 G1 结构继续补齐 AMP policy 的推理和对比验证流程。

## Step 6
- 新增了 [beyondAMP/source/third_party/sim2simlib/scripts/g1_amp_velocity.py](beyondAMP/source/third_party/sim2simlib/scripts/g1_amp_velocity.py) 作为 G1 walk AMP 的 MuJoCo sim-to-sim 运行入口。
- 这个脚本直接复用 G1 速度任务的关节映射、控制增益和动作缩放，并把观测项对齐到 AMP 训练时的 policy 输入。
- 训练完成后，只需要把导出的 TorchScript policy 路径传给这个脚本，就能在 MuJoCo 中做推理验证。

## Step 7
- 修正了 [beyondAMP/source/amp_tasks/amp_tasks/amp_task_demo_data_cfg.py](beyondAMP/source/amp_tasks/amp_tasks/amp_task_demo_data_cfg.py) 中 walk `.npz` 的路径。
- 之前用的是相对路径，从 [beyondAMP/scripts/factoryIsaac](beyondAMP/scripts/factoryIsaac) 启动训练时会找不到数据；现在改成基于仓库根目录的绝对路径。
- 这样 AMP 训练可以直接从当前工作流读取 expert motion。

## 待办
- 修改 G1 训练配置以接入 AMP。
- 配置判别器输入与 AMP 奖励。
- 完成训练、导出权重与推理脚本。
- 补齐 MuJoCo 与 IsaacSim 的 sim-to-sim 验证流程。
