import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# ---------- 1. 定义指针网络模型 ----------
class PointerNetwork(nn.Module):
    def __init__(self, hidden_dim=64):
        super().__init__()
        self.hidden_dim = hidden_dim
        
        # 编码器：将数字标量映射到向量，再输入LSTM
        self.encoder_fc = nn.Linear(1, hidden_dim)
        self.encoder_lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        
        # 解码器LSTM
        self.decoder_lstm = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        
        # 指针机制的 Query 和 Key 投影（用于计算注意力分数）
        self.W_q = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.W_k = nn.Linear(hidden_dim, hidden_dim, bias=False)
        
        # 可学习的起始标志向量（对应解码器第一步的输入）
        self.start_token = nn.Parameter(torch.randn(1, 1, hidden_dim))
        
    def forward(self, x, targets=None):
        """
        x: 输入序列，shape = (batch_size, seq_len)，例如 [[20, 5, 15, 8]]
        targets: 训练时的真实指针序列（Teacher Forcing），例如 [[2, 4, 3, 1]]
                 表示依次指向原序列的第2、4、3、1个位置（索引从1开始）。
                 若为 None，则处于推理模式（自回归）。
        """
        batch_size, seq_len = x.shape
        device = x.device
        
        # ---------- 编码阶段 ----------
        # 将数字转为 (batch, seq, 1) 并映射到隐藏维度
        x = x.unsqueeze(-1).float()  # shape: (batch, seq, 1)
        enc_emb = torch.tanh(self.encoder_fc(x))  # (batch, seq, hidden)
        enc_outputs, (h_n, c_n) = self.encoder_lstm(enc_emb)
        
        # 预先计算所有编码位置的 Key 向量（用于和 Query 做点积）
        keys = self.W_k(enc_outputs)  # (batch, seq, hidden)
        
        # ---------- 解码阶段 ----------
        # 初始化解码器的隐藏状态为编码器的最终状态
        decoder_h = h_n
        decoder_c = c_n
        
        # 第一步解码器的输入是起始标志
        decoder_input = self.start_token.expand(batch_size, -1, -1)  # (batch, 1, hidden)
        
        # 掩码矩阵，记录哪些输入位置已经被选中（避免重复指向）
        mask = torch.zeros(batch_size, seq_len, dtype=torch.bool, device=device)
        
        # 存储每一步的输出 logits（Softmax 之前的分数）
        logits_list = []
        
        # 循环解码 seq_len 步（输出长度等于输入长度）
        for t in range(seq_len):
            # 解码器 LSTM 前向
            decoder_out, (decoder_h, decoder_c) = self.decoder_lstm(decoder_input, (decoder_h, decoder_c))
            
            # ------- 指针机制核心 -------
            # 计算 Query（当前解码状态）
            query = self.W_q(decoder_out)  # (batch, 1, hidden)
            
            # 点积注意力得到分数 (batch, 1, seq)
            scores = torch.bmm(query, keys.transpose(1, 2)) / (self.hidden_dim ** 0.5)
            scores = scores.squeeze(1)  # (batch, seq)
            
            # 屏蔽已选位置（将其分数设为 -inf，Softmax 后概率为0）
            scores = scores.masked_fill(mask, float('-inf'))
            logits_list.append(scores)  # 保存用于计算损失
            
            # ------- 决定下一步的输入 -------
            if targets is not None:
                # 训练模式：使用 Teacher Forcing，直接取真实的目标索引
                idx = targets[:, t]  # (batch,)
            else:
                # 推理模式：贪心选择当前概率最大的位置
                probs = F.softmax(scores, dim=-1)
                idx = torch.argmax(probs, dim=-1)  # (batch,)
            
            # 更新掩码：标记本轮选中的位置，后续不能再选
            for i in range(batch_size):
                mask = mask.clone()
                mask.scatter_(1, idx.unsqueeze(1), True)
            
            # 准备下一步解码器的输入：取出刚刚选中位置的编码嵌入
            # 这体现了"指针"的含义——将指向位置的内容作为下一时刻输入
            next_input = enc_emb[torch.arange(batch_size), idx]  # (batch, hidden)
            decoder_input = next_input.unsqueeze(1)  # (batch, 1, hidden)
        
        # 将所有时间步的 logits 堆叠起来
        logits = torch.stack(logits_list, dim=1)  # (batch, seq_len, seq_len)
        return logits


# ---------- 2. 生成训练数据 ----------
def generate_data(batch_size, seq_len):
    """生成随机数字序列及其升序排序的索引（目标指针）"""
    # 随机生成 0~99 之间的整数
    data = np.random.randint(0, 100, size=(batch_size, seq_len))
    # argsort 返回升序排列的原始索引，即我们期望的指针序列
    targets = np.argsort(data, axis=1)  # shape: (batch, seq)
    return torch.tensor(data, dtype=torch.float32), torch.tensor(targets, dtype=torch.long)


# ---------- 3. 训练循环 ----------
if __name__ == "__main__":
    # 超参数
    HIDDEN_DIM = 64
    BATCH_SIZE = 32
    SEQ_LEN = 6   # 输入序列长度（也是输出指针长度）
    EPOCHS = 500
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PointerNetwork(hidden_dim=HIDDEN_DIM).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    
    print("开始训练指针网络（数字排序任务）...")
    for epoch in range(EPOCHS):
        # 生成一批数据
        x, targets = generate_data(BATCH_SIZE, SEQ_LEN)
        x, targets = x.to(device), targets.to(device)
        
        # 前向传播（传入 targets 启用 Teacher Forcing）
        logits = model(x, targets=targets)
        
        # 计算交叉熵损失
        # logits: (batch, seq_len, seq_len) -> 展平为 (batch*seq_len, seq_len)
        # targets: (batch, seq_len) -> 展平为 (batch*seq_len)
        loss = F.cross_entropy(logits.reshape(-1, SEQ_LEN), targets.reshape(-1))
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if epoch % 100 == 0:
            print(f"Epoch {epoch:3d}, Loss: {loss.item():.4f}")
    
    # ---------- 4. 推理测试 ----------
    print("\n--- 推理测试 ---")
    test_x, test_targets = generate_data(1, SEQ_LEN)  # 单个样本
    test_x = test_x.to(device)
    
    model.eval()
    with torch.no_grad():
        # targets=None 表示自回归推理
        logits = model(test_x, targets=None)
        pred_indices = torch.argmax(logits, dim=-1)  # (1, seq_len)
    
    print(f"输入序列: {test_x.squeeze(0).cpu().tolist()}")
    print(f"预测的指针序列 (升序索引): {pred_indices.squeeze(0).cpu().tolist()}")
    print(f"真实指针序列: {test_targets.squeeze(0).tolist()}")
    
    # 验证结果：根据预测索引取出原序列元素，验证是否升序
    sorted_values = test_x.squeeze(0)[pred_indices.squeeze(0)].cpu().tolist()
    print(f"按预测指针取出的数值: {sorted_values}")