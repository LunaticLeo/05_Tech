import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 设置随机种子，保证结果可复现
np.random.seed(42)

# ==========================================
# 1. 模拟CAD边界边的数据集
# ==========================================
# 假设你的B-Rep模型提取了10000条边
n_samples = 10000

# 模拟5个关键几何特征（与FeatureFox论文对应）
# 二面角 (0~180°)，内部边(同一个特征)通常接近180°(平滑)，边界边通常角度突变
dihedral_angle = np.random.uniform(0, 180, n_samples)

# 凹凸性 (0=凸, 1=凹, 2=平滑) - 用数值模拟
concavity = np.random.choice([0, 1, 2], n_samples)

# 面积比 (相邻面面积之比，范围0~1)
area_ratio = np.random.uniform(0, 1, n_samples)

# 周长比
perimeter_ratio = np.random.uniform(0, 1, n_samples)

# 归一化长度 (边长相对于模型总尺寸)
normalized_length = np.random.uniform(0, 0.5, n_samples)

# 将这5个特征组合成一个特征矩阵
X = np.column_stack([
    dihedral_angle, 
    concavity, 
    area_ratio, 
    perimeter_ratio, 
    normalized_length
])

# 模拟标签 y
# 在真实的CAD模型中，边界边（属于不同特征）通常占少数（约10%~20%）
# 这里我们用逻辑关系生成较为真实的标签：
# 当二面角 < 90° 或 > 150° 或 凹凸性为0/1时，更有可能是边界边(标签=1)
prob = np.zeros(n_samples)
for i in range(n_samples):
    # 核心规则：二面角偏离180°越多，越可能是边界
    angle_penalty = abs(dihedral_angle[i] - 150) / 100
    if dihedral_angle[i] < 90 or dihedral_angle[i] > 150:
        prob[i] = 0.8 + np.random.rand() * 0.2  # 高概率为边界
    else:
        prob[i] = 0.1 + np.random.rand() * 0.2  # 低概率为边界

# 根据概率生成0/1标签 (1=边界边)
y = (np.random.rand(n_samples) < prob).astype(int)
print(f"边界边占比: {y.mean():.2%}")  # 通常输出 20%~40%

# ==========================================
# 2. 划分训练集、验证集、测试集
# ==========================================
# 先分出30%作为临时集，剩下的70%作为训练集
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)
# 再从临时集分出验证集(15%)和测试集(15%)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)

print(f"训练集: {len(X_train)} 条边, 边界占比: {y_train.mean():.2%}")
print(f"验证集: {len(X_val)} 条边, 边界占比: {y_val.mean():.2%}")
print(f"测试集: {len(X_test)} 条边, 边界占比: {y_test.mean():.2%}")

# ==========================================
# 3. 训练 XGBoost 模型 (FeatureFox 参数)
# ==========================================
# 计算正负样本比例，用于处理不平衡数据
scale_pos_weight = (y_train == 0).sum() / (y_train == 1).sum()

model = xgb.XGBClassifier(
    n_estimators=200,           # 树的数量 (FeatureFox默认)
    max_depth=6,                # 最大深度 (FeatureFox默认)
    learning_rate=0.1,          # 学习率 (FeatureFox默认)
    objective='binary:logistic',# 二分类
    scale_pos_weight=scale_pos_weight,  # 自动平衡类别
    subsample=0.8,              # 行采样
    colsample_bytree=0.8,       # 列采样
    random_state=42,
    use_label_encoder=False,    # 避免警告
    eval_metric='logloss'
)

# 训练模型
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False  # 设为True可看训练过程
)
print("✅ XGBoost 训练完成")

# ==========================================
# 4. 概率校准 (Isotonic Calibration) 
# ==========================================
# XGBoost输出的原始概率往往有偏差，用验证集进行校准
raw_proba_val = model.predict_proba(X_val)[:, 1]

calibrator = IsotonicRegression(
    y_min=0.0, 
    y_max=1.0, 
    increasing=True,
    out_of_bounds='clip'
)
calibrator.fit(raw_proba_val, y_val)
print("✅ 概率校准器训练完成")

# ==========================================
# 5. 在测试集上评估
# ==========================================
# 获取测试集的原始概率，并校准
raw_proba_test = model.predict_proba(X_test)[:, 1]
calibrated_proba_test = calibrator.predict(raw_proba_test)

# 设定阈值 0.5 进行分类
threshold = 0.5
y_pred = (calibrated_proba_test >= threshold).astype(int)

# 输出详细评估报告
print("\n" + "="*60)
print("📊 测试集评估结果 (阈值 = 0.5)")
print("="*60)
print(classification_report(y_test, y_pred, target_names=['内部边(0)', '边界边(1)']))

# 混淆矩阵
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print(f"混淆矩阵:")
print(f"  TN(正确内部): {tn:5d}    FP(误报边界): {fp:5d}")
print(f"  FN(漏报边界): {fn:5d}    TP(正确边界): {tp:5d}")

# AUC分数
auc = roc_auc_score(y_test, calibrated_proba_test)
print(f"\nAUC (曲线下面积): {auc:.4f}")

# ==========================================
# 6. 特征重要性分析 (看看哪些几何特征最关键)
# ==========================================
feature_names = ['二面角', '凹凸性', '面积比', '周长比', '归一化长度']
importance = model.feature_importances_
sorted_idx = np.argsort(importance)[::-1]

print("\n📈 特征重要性排序:")
for i in sorted_idx:
    print(f"  {feature_names[i]:10s} : {importance[i]:.4f}")

# ==========================================
# 7. 保存模型 (方便后续直接推理)
# ==========================================
import joblib
joblib.dump(model, 'xgboost_cad_model.pkl')
joblib.dump(calibrator, 'calibrator.pkl')
print("\n💾 模型和校准器已保存为 xgboost_cad_model.pkl 和 calibrator.pkl")

# ==========================================
# 8. 推理演示: 判断一条新边是否为边界边
# ==========================================
def predict_edge(features, model, calibrator, threshold=0.5):
    """
    输入: features (5个数值: 二面角, 凹凸性, 面积比, 周长比, 归一化长度)
    输出: (概率, 分类结果)
    """
    if features.ndim == 1:
        features = features.reshape(1, -1)
    
    raw_prob = model.predict_proba(features)[:, 1]
    calib_prob = calibrator.predict(raw_prob)
    pred = (calib_prob >= threshold).astype(int)
    return calib_prob[0], pred[0]

# 测试一条新边 (例如: 二面角=170°(平滑), 凹凸性=2, 面积比=0.9, 周长比=0.8, 长度=0.05)
new_edge = np.array([170, 2, 0.9, 0.8, 0.05])
prob, pred = predict_edge(new_edge, model, calibrator)
print(f"\n🔍 新边预测: 边界概率 = {prob:.2%}, 预测结果 = {'边界边' if pred==1 else '内部边'}")