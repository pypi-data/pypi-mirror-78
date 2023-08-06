"""配置文件"""
model_name = "pytorch"
framework = "pytorch"

"""模型保存加载路径"""
pre_trained = "pytorch.pth"
onnx_path = "pytorch.onnx"

"""hyperparameter"""
inputs_size = [[1, 28, 28]]  # 网络输入 list of list, no batch
train_batch = 16  # 训练 batch size
num_workers = 0  # 训练加载数据的cpu数量
epoch_range = [0, 100, 1]  # [起始, 终止, 间隔]  epoch设置, 每个epoch间隔会执行模型保存，评估等
model_backup_upper = 3  # 训练阶段，自动保存模型数量上限
loss_avg_step = 1000  # 每个多少个batch， 统计一次loss



