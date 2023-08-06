"""配置文件"""
model_name = "RFBNet"
framework = "pytorch"

"""各类模型保存加载的路径"""
pre_trained = "rfbnet.pth"
onnx_path = "rfbnet.onnx"

"""hyperparameter 算法超参，包括训练参数,算法模型参数等"""
inputs_size = [[3, 300, 300]]  # tuple of list, no batch
num_classes = 2  # 类别数量
train_batch = 16  # 训练 batch size
num_workers = 4  # 训练加载数据的cpu数量
epoch_range = [50, 100, 5]  # [起始, 终止, 间隔]  epoch设置, 每个epoch间隔会执行模型保存，评估等
model_backup_upper = 3  # 训练阶段，自动保存模型数量上限
loss_avg_step = 10  # 每个多少个batch， 统计一次loss
train_data_path = "/home/liam/deepblue/projects/pandora/train_data" # 数据集路径
img_dim = 300  # 图像维度
p = 0.5  # 均值
rgb_means = (104, 117, 123)  # rgb均值
PriorBox_Config = {
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'min_dim': 300,
    'steps': [8, 16, 32, 64, 100, 300],
    'min_sizes': [30, 60, 111, 162, 213, 264],
    'max_sizes': [60, 111, 162, 213, 264, 315],
    'aspect_ratios': [[0.4, 1.0, 1.5],
                          [0.4, 1.0, 1.6],
                          [0.5, 1.1, 1.6],
                          [0.5, 1.1, 1.6],
                          [0.5, 1.1, 1.6],
                          [0.7, 1.4]],
    'max_ratios': [0.8, 0.8, 0.8, 0.9, 1, 1],
    'variance': [0.1, 0.2],
    'clip': True,
}  # 计算先验框的参数
lr_init = 0.001  # 初始学习率
overlap_thresh=0.4  # 重叠阈值
bkg_label = 0  # 背景标签
neg_mining=True # 多找一些negative加入负样本集，进行训练
neg_pos = 3  # 负样本和正样本的比值
neg_overlap = 0.3 # 负样本重叠阈值
prior_for_matching=True  # 先验匹配
encode_target=False  # 对target编码
momentum=0.9  # 动量
weight_decay=5e-4  # 权重衰减
confidence_thresh = 0.3  #NMS操作之前用到的置信度阈值
iou_thresh = 0.3 #NMS进行时用到的IoU阈值















