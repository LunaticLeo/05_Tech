
import torch
import torch.nn as nn

# 1. 固定随机种子，让你运行结果和我一致
torch.manual_seed(43)

# 2. 设定词表：5个词，0=结束符(STOP)，1=我，2=爱，3=你，4=学习
vocab_size = 5

# 3. 定义一个超级简单的“伪大模型”（只有嵌入层+线性层）
class TinyLLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, 8)  # 把词变成向量
        self.fc = nn.Linear(8, vocab_size)            # 把向量映射回词表概率
    
    def forward(self, x):
        # x 形状: (batch, 序列长度)
        emb = self.embedding(x)   # (batch, 序列长度, 8)
        logits = self.fc(emb)     # (batch, 序列长度, 5)
        return logits

# 实例化模型
model = TinyLLM()

# ---------- 实战自回归推理（生成过程） ----------
print("👉 开始自回归生成：")
# 初始输入：提示词 "我"  (ID=1)
input_ids = torch.tensor([[1]])  # 形状 (1, 1)

# 我们让模型最多生成 5 个新词
for step in range(5):
    # 1. 前向传播：把当前整个序列输入模型
    output_logits = model(input_ids)  # 形状 (1, 当前长度, 5)
    
    # 2. 只取【最后一个位置】的预测结果（即下一个词的概率分布）
    next_token_logits = output_logits[:, -1, :]  # 形状 (1, 5)
    
    # 3. 贪心采样：挑出概率最大的词的ID（实战中常用 argmax）
    next_token_id = torch.argmax(next_token_logits, dim=-1, keepdim=True)  # 形状 (1, 1)
    
    # 4. 判断是否遇到结束符（ID=0）
    # if next_token_id.item() == 0:
    #     print("  ⏹️  遇到结束符，停止生成。")
    #     break
    
    # 5. ⭐⭐⭐ 这才是自回归的灵魂！把新生成的词拼接到尾巴上 ⭐⭐⭐
    input_ids = torch.cat([input_ids, next_token_id], dim=1)
    
    # 6. 打印当前进度，看看模型是怎么“一个字一个字往外蹦”的
    print(f"  第 {step+1} 步生成 ID: {next_token_id.item()}，当前序列: {input_ids.tolist()[0]}")

print(f"\n✅ 最终生成的完整序列: {input_ids.tolist()[0]}")