import numpy as np

# ================================
# 1. 密码子 (codon) 与索引的双向映射
# ================================

def generate_codon_list():
    """
    生成所有 64 个密码子，顺序为：
    AAA, AAC, AAG, AAU, ACA, ACC, ..., UUU
    只是一个遍历顺序，数学上是完整覆盖 4^3 种组合即可。
    """
    bases = ['A', 'C', 'G', 'U']  # 你也可以用 T 替换 U
    codons = []
    for b1 in bases:
        for b2 in bases:
            for b3 in bases:
                codons.append(b1 + b2 + b3)
    return codons

def base_to_bits(base):
    """
    将碱基编码为 2-bit（二进制字符串）：
    A -> 00, C -> 01, G -> 10, U -> 11
    这是我们与“6 位二进制 = 0..63”统一的关键。
    """
    mapping = {'A': '00', 'C': '01', 'G': '10', 'U': '11'}
    return mapping[base]

def codon_to_index(codon):
    """
    把一个 3 碱基密码子映射为 0..63 的整数索引。
    过程：每个碱基 -> 2 bit，共 6 bit -> 整数。
    """
    if len(codon) != 3:
        raise ValueError("codon must be length 3, e.g. 'AUG'")
    bits = ''.join(base_to_bits(b) for b in codon)
    return int(bits, 2)

def index_to_codon(index):
    """
    由 0..63 的索引恢复密码子。
    过程：index -> 6 bit -> 每 2 bit -> 一个碱基。
    """
    if not (0 <= index < 64):
        raise ValueError("index must be between 0 and 63")
    bits = format(index, '06b')  # 6 位二进制
    bits_pairs = [bits[i:i+2] for i in range(0, 6, 2)]
    mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'U'}
    return ''.join(mapping[pair] for pair in bits_pairs)

# ================================
# 2. 卦象 (六十四卦) 与索引的双向映射
# ================================

def hexagram_to_index(binary_six_bits):
    """
    将一个 6 位的卦（二进制字符串，如 '000000'、'111111'）映射为 0..63 索引。
    这里简单用二进制解释为整数。
    你可以约定 0=阴,1=阳（或反过来），关键是一致即可。
    """
    if len(binary_six_bits) != 6 or any(b not in '01' for b in binary_six_bits):
        raise ValueError("hexagram must be a 6-character string of '0' and '1'")
    return int(binary_six_bits, 2)

def index_to_hexagram(index):
    """
    将 0..63 索引映射回 6 位二进制卦象。
    """
    if not (0 <= index < 64):
        raise ValueError("index must be between 0 and 63")
    return format(index, '06b')  # e.g. 0 -> '000000', 63 -> '111111'

# ================================
# 3. 构造 64×64 映射矩阵
# ================================

def build_mapping_matrix():
    """
    构造一个 64×64 的映射矩阵 M：
    - 列索引：六十四卦（index 0..63）
    - 行索引：64 密码子（index 0..63）

    这里我们采用最简单 & 最自然的同构：
    index(卦) == index(密码子)
    因此 M 实际上是一个单位矩阵（permutation matrix 的特例）。

    若未来你想加入“生物学语义 + 卦象结构”的特定对应，
    只需把 i 映射到某个 f(i) 即可，M[f(i), i] = 1。
    """
    M = np.zeros((64, 64), dtype=int)
    for i in range(64):
        # 在最简单模型中，卦的索引 i 对应密码子的索引 i
        M[i, i] = 1
    return M

# ================================
# 4. 示例：在 Hilbert 空间里做一次“卦 → 密码子”基变换
# ================================

def example_demo():
    codons = generate_codon_list()
    M = build_mapping_matrix()

    print("共有密码子数量:", len(codons))
    print("映射矩阵形状:", M.shape)

    # 检查是否是置换矩阵（每行每列恰好一个 1）
    print("前 5 列列和:", M.sum(axis=0)[:5])
    print("前 5 行行和:", M.sum(axis=1)[:5])

    # 假设我们在“卦空间”有一个向量 v_hex：
    # 例如：只在卦 index=3 上有振幅 1，其它为 0
    v_hex = np.zeros(64)
    v_hex[3] = 1.0

    # 使用 M 做基变换，得到对应的“密码子空间”向量 v_codon
    # 约定：v_codon = M @ v_hex
    v_codon = M @ v_hex

    # 找到在 codon 空间中哪个索引为 1
    codon_index = np.argmax(v_codon)
    codon = index_to_codon(codon_index)

    print("\n示例：")
    print("卦索引 = 3  -> 卦二进制 = ", index_to_hexagram(3))
    print("通过映射矩阵，对应的密码子索引 = ", codon_index)
    print("对应密码子 = ", codon)

if __name__ == "__main__":
    example_demo()