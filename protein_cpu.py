#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蛋白质CPU - Protein-Driven CPU
基于蛋白质结构和功能的生物计算架构

核心思想：
- 蛋白质折叠 = 计算
- 酶催化 = 逻辑门
- 蛋白质相互作用 = 信号传递
- 基因表达 = 程序执行
"""

import random
import math

class ProteinCPU:
    def __init__(self):
        self.instructions = self._define_instructions()
        self.proteins = self._define_proteins()
        # 蛋白质寄存器 (浓度 μM)
        self.protein_pool = {
            'Enzyme1': 0.0, 'Enzyme2': 0.0,
            'Receptor': 0.0, 'Kinase': 0.0,
            'Transcription_Factor': 0.0
        }
        self.atp = 1000.0  # μM (能量货币)
        self.temperature = 310.15  # K (37°C, 体温)
        
    def _define_proteins(self):
        """定义关键蛋白质"""
        return {
            # 酶类
            'DNA_Polymerase': {'function': 'DNA复制', 'speed': '1000 nt/s', 'error': '10⁻⁹'},
            'RNA_Polymerase': {'function': 'RNA转录', 'speed': '50 nt/s', 'processivity': '高'},
            'Ribosome': {'function': '蛋白质翻译', 'speed': '20 aa/s', 'complex': '大'},
            'Protease': {'function': '蛋白质降解', 'specificity': '序列特异', 'regulation': True},
            
            # 信号蛋白
            'Kinase': {'function': '磷酸化', 'substrate': '蛋白质', 'cascade': True},
            'Phosphatase': {'function': '去磷酸化', 'reverse': 'Kinase', 'regulation': True},
            'GTPase': {'function': 'GTP水解', 'switch': 'ON/OFF', 'timer': True},
            
            # 结构蛋白
            'Actin': {'function': '细胞骨架', 'polymerize': True, 'dynamic': True},
            'Tubulin': {'function': '微管', 'motor': True, 'transport': True},
            'Collagen': {'function': '结构支撑', 'strength': '高', 'extracellular': True},
            
            # 转运蛋白
            'Ion_Channel': {'function': '离子通道', 'gated': True, 'selective': True},
            'Transporter': {'function': '主动运输', 'ATP_dependent': True, 'directional': True},
            'Receptor': {'function': '信号接收', 'ligand_binding': True, 'amplification': True},
            
            # 调控蛋白
            'Transcription_Factor': {'function': '转录调控', 'DNA_binding': True, 'combinatorial': True},
            'Repressor': {'function': '基因抑制', 'negative_regulation': True, 'allosteric': True},
            'Activator': {'function': '基因激活', 'positive_regulation': True, 'cooperative': True}
        }
    
    def _define_instructions(self):
        """定义蛋白质指令集"""
        return {
            # 中心法则
            'REPLICATE': {'desc': 'DNA复制', 'enzyme': 'DNA聚合酶', 'fidelity': '极高'},
            'TRANSCRIBE': {'desc': '转录', 'enzyme': 'RNA聚合酶', 'product': 'mRNA'},
            'TRANSLATE': {'desc': '翻译', 'machine': '核糖体', 'product': '蛋白质'},
            'DEGRADE': {'desc': '降解', 'enzyme': '蛋白酶', 'regulation': '泛素化'},
            
            # 蛋白质折叠
            'FOLD': {'desc': '蛋白质折叠', 'helper': '分子伴侣', 'time': 'ms-s'},
            'MISFOLD': {'desc': '错误折叠', 'disease': '朊病毒', 'aggregation': True},
            'REFOLD': {'desc': '重折叠', 'chaperone': 'GroEL/GroES', 'ATP_cost': True},
            'UNFOLD': {'desc': '去折叠', 'denature': True, 'reversible': '有时'},
            
            # 酶催化
            'CATALYZE': {'desc': '酶催化', 'speedup': '10⁶-10¹⁷倍', 'specificity': '高'},
            'ALLOSTERIC': {'desc': '变构调节', 'mechanism': '构象变化', 'cooperative': True},
            'COMPETITIVE': {'desc': '竞争性抑制', 'inhibitor': '底物类似物', 'reversible': True},
            'FEEDBACK': {'desc': '反馈抑制', 'product': '抑制剂', 'homeostasis': True},
            
            # 信号转导
            'PHOSPHORYLATE': {'desc': '磷酸化', 'enzyme': '激酶', 'switch': 'ON'},
            'DEPHOSPHORYLATE': {'desc': '去磷酸化', 'enzyme': '磷酸酶', 'switch': 'OFF'},
            'CASCADE': {'desc': '信号级联', 'amplification': '指数级', 'MAPK': True},
            'CROSSTALK': {'desc': '信号交叉', 'integration': True, 'network': True},
            
            # 蛋白质相互作用
            'BIND': {'desc': '蛋白质结合', 'Kd': 'nM-μM', 'specificity': '高'},
            'COMPLEX': {'desc': '复合物形成', 'stoichiometry': '定义', 'cooperative': True},
            'SCAFFOLD': {'desc': '支架蛋白', 'organize': True, 'proximity': True},
            
            # 定位
            'LOCALIZE': {'desc': '亚细胞定位', 'signal': 'NLS/NES', 'compartment': True},
            'SECRETE': {'desc': '分泌', 'pathway': 'ER-Golgi', 'signal_peptide': True},
            'ANCHOR': {'desc': '膜锚定', 'lipid_modification': True, 'topology': True},
            
            # 修饰
            'GLYCOSYLATE': {'desc': '糖基化', 'location': 'ER/Golgi', 'function': '多样'},
            'ACETYLATE': {'desc': '乙酰化', 'target': '组蛋白/其他', 'regulation': True},
            'UBIQUITINATE': {'desc': '泛素化', 'mark': '降解', 'proteasome': True},
            'METHYLATE': {'desc': '甲基化', 'epigenetic': True, 'heritable': True},
            
            # 马达蛋白
            'WALK': {'desc': '分子马达', 'protein': 'Kinesin/Dynein', 'ATP_driven': True},
            'ROTATE': {'desc': '旋转马达', 'protein': 'ATP合酶', 'torque': True},
            'CONTRACT': {'desc': '肌肉收缩', 'protein': 'Myosin', 'sliding': True},
            
            # 逻辑门
            'AND_GATE': {'desc': '与门', 'mechanism': '双底物酶', 'both_required': True},
            'OR_GATE': {'desc': '或门', 'mechanism': '多途径激活', 'any_sufficient': True},
            'NOT_GATE': {'desc': '非门', 'mechanism': '抑制剂', 'invert': True},
            
            # 控制
            'HALT': {'desc': '停机', 'method': '细胞凋亡', 'caspase': True}
        }
    
    def protein_folding(self, sequence_length):
        """蛋白质折叠 - Levinthal悖论"""
        # 每个氨基酸3种构象，总构象数 = 3^n
        total_conformations = 3 ** sequence_length
        # 随机搜索需要的时间 (假设1ps/构象)
        random_search_time = total_conformations * 1e-12  # 秒
        # 实际折叠时间 (ms-s)
        actual_time = random.uniform(0.001, 1.0)
        
        speedup = random_search_time / actual_time
        return actual_time, speedup
    
    def enzyme_catalysis(self, substrate_conc, Km, Vmax):
        """米氏方程 v = Vmax[S]/(Km+[S])"""
        v = Vmax * substrate_conc / (Km + substrate_conc)
        return v
    
    def signal_cascade(self, initial_signal, amplification_per_step, steps):
        """信号级联放大"""
        signal = initial_signal
        for _ in range(steps):
            signal *= amplification_per_step
        return signal
    
    def protein_binding(self, protein_conc, ligand_conc, Kd):
        """蛋白质-配体结合 [PL] = [P][L]/Kd"""
        # 简化：假设总蛋白浓度 >> Kd
        fraction_bound = ligand_conc / (Kd + ligand_conc)
        complex_conc = protein_conc * fraction_bound
        return complex_conc, fraction_bound
    
    def transcription_rate(self, tf_conc, Kd, basal_rate, max_rate):
        """转录因子调控的基因表达"""
        # Hill方程简化版
        activation = tf_conc / (Kd + tf_conc)
        rate = basal_rate + (max_rate - basal_rate) * activation
        return rate
    
    def protein_lifetime(self, degradation_rate):
        """蛋白质半衰期 t1/2 = ln(2)/k"""
        half_life = math.log(2) / degradation_rate
        return half_life
    
    def display(self):
        """展示蛋白质CPU设计"""
        print("=" * 80)
        print("蛋白质CPU - Protein-Driven CPU")
        print("基于蛋白质结构和功能的生物计算架构")
        print("=" * 80)
        
        print(f"\n总指令数: {len(self.instructions)}")
        print(f"蛋白质库: {len(self.proteins)}种")
        print(f"ATP能量: {self.atp:.0f} μM")
        print(f"温度: {self.temperature}K ({self.temperature-273.15:.0f}°C)")
        
        print("\n关键蛋白质:")
        for name, props in list(self.proteins.items())[:6]:
            print(f"  {name:<20} - {props['function']}")
        
        print("\n指令分类:")
        categories = {
            '中心法则': ['REPLICATE', 'TRANSCRIBE', 'TRANSLATE', 'DEGRADE'],
            '蛋白质折叠': ['FOLD', 'MISFOLD', 'REFOLD', 'UNFOLD'],
            '酶催化': ['CATALYZE', 'ALLOSTERIC', 'COMPETITIVE', 'FEEDBACK'],
            '信号转导': ['PHOSPHORYLATE', 'DEPHOSPHORYLATE', 'CASCADE', 'CROSSTALK'],
            '蛋白质相互作用': ['BIND', 'COMPLEX', 'SCAFFOLD'],
            '翻译后修饰': ['GLYCOSYLATE', 'ACETYLATE', 'UBIQUITINATE', 'METHYLATE'],
            '分子马达': ['WALK', 'ROTATE', 'CONTRACT'],
            '逻辑门': ['AND_GATE', 'OR_GATE', 'NOT_GATE']
        }
        
        for cat, instrs in categories.items():
            print(f"\n{cat}:")
            for instr in instrs[:3]:
                if instr in self.instructions:
                    info = self.instructions[instr]
                    print(f"  {instr:<20} - {info['desc']}")

def demonstrate_protein_computing():
    """演示蛋白质计算"""
    cpu = ProteinCPU()
    
    print("\n" + "=" * 80)
    print("蛋白质计算演示")
    print("=" * 80)
    
    # 1. Levinthal悖论
    print("\n1. 蛋白质折叠 - Levinthal悖论:")
    sequence_lengths = [50, 100, 150, 200]
    for length in sequence_lengths:
        actual_time, speedup = cpu.protein_folding(length)
        print(f"  {length}个氨基酸: 实际{actual_time:.3f}s, "
              f"随机搜索需{speedup:.2e}年, 加速{speedup:.2e}倍")
    
    # 2. 酶催化
    print("\n2. 米氏方程 - 酶催化动力学:")
    Km = 10.0  # μM
    Vmax = 100.0  # μM/s
    substrate_concs = [1, 5, 10, 50, 100]
    print(f"  Km={Km}μM, Vmax={Vmax}μM/s")
    for S in substrate_concs:
        v = cpu.enzyme_catalysis(S, Km, Vmax)
        print(f"  [S]={S:3d}μM: v={v:5.1f}μM/s ({v/Vmax*100:4.1f}% Vmax)")
    
    # 3. 信号级联
    print("\n3. 信号级联放大 (MAPK通路):")
    initial = 1.0
    amplifications = [10, 100, 1000]
    steps = 3
    for amp in amplifications:
        final = cpu.signal_cascade(initial, amp, steps)
        print(f"  每步放大{amp}倍, {steps}步: {initial} → {final:.2e} (放大{final:.2e}倍)")
    
    # 4. 蛋白质结合
    print("\n4. 蛋白质-配体结合:")
    protein_conc = 100.0  # μM
    Kd = 10.0  # μM
    ligand_concs = [1, 5, 10, 50, 100]
    print(f"  [蛋白质]={protein_conc}μM, Kd={Kd}μM")
    for L in ligand_concs:
        complex, fraction = cpu.protein_binding(protein_conc, L, Kd)
        print(f"  [配体]={L:3d}μM: [复合物]={complex:5.1f}μM ({fraction*100:4.1f}%结合)")
    
    # 5. 基因表达调控
    print("\n5. 转录因子调控基因表达:")
    basal = 1.0  # 基础转录率
    max_rate = 100.0  # 最大转录率
    Kd = 10.0  # μM
    tf_concs = [0, 1, 5, 10, 50, 100]
    print(f"  基础={basal}, 最大={max_rate}, Kd={Kd}μM")
    for tf in tf_concs:
        rate = cpu.transcription_rate(tf, Kd, basal, max_rate)
        print(f"  [TF]={tf:3d}μM: 转录率={rate:5.1f} ({rate/max_rate*100:4.1f}%)")
    
    # 6. 蛋白质半衰期
    print("\n6. 蛋白质半衰期:")
    proteins = [
        ('短寿命蛋白', 0.1, '转录因子'),
        ('中等寿命', 0.01, '代谢酶'),
        ('长寿命蛋白', 0.001, '结构蛋白'),
        ('极长寿命', 0.0001, '晶状体蛋白')
    ]
    for name, k, example in proteins:
        t_half = cpu.protein_lifetime(k)
        print(f"  {name}: t1/2={t_half/3600:.1f}小时 (例:{example})")

def analyze_protein_cpu():
    """分析蛋白质CPU特性"""
    print("\n" + "=" * 80)
    print("蛋白质CPU特性分析")
    print("=" * 80)
    
    analysis = {
        '核心优势': [
            '• 自我复制: DNA→RNA→蛋白质',
            '• 自我修复: DNA修复酶、分子伴侣',
            '• 自我组装: 蛋白质自动折叠',
            '• 超高特异性: Kd可达pM级',
            '• 信号放大: 级联可达10⁶倍',
            '• 能量效率: ATP驱动，高效',
            '• 并行处理: 细胞内10⁹个蛋白质分子',
            '• 可进化: 突变+选择'
        ],
        '关键挑战': [
            '• 速度慢: ms-s级 (vs 电子ns级)',
            '• 噪声高: 随机性强',
            '• 环境敏感: 温度、pH、离子',
            '• 难以小型化: 需要细胞环境',
            '• 寿命有限: 蛋白质降解',
            '• 难以编程: 需要基因工程',
            '• 串扰: 信号通路交叉'
        ],
        '实际应用': [
            '• 合成生物学: 基因线路设计',
            '• 生物传感器: 蛋白质开关',
            '• 生物计算: 细胞逻辑门',
            '• 药物递送: 蛋白质纳米机器',
            '• 诊断: 酶联免疫',
            '• 生物制造: 代谢工程'
        ],
        '里程碑': [
            '• 2000: 首个合成基因振荡器 (Elowitz)',
            '• 2004: 首个合成生物开关 (Gardner)',
            '• 2010: 首个合成基因组 (Venter)',
            '• 2012: CRISPR基因编辑',
            '• 2020: AlphaFold蛋白质结构预测'
        ]
    }
    
    for category, points in analysis.items():
        print(f"\n{category}:")
        for point in points:
            print(f"  {point}")

def protein_logic_gates():
    """蛋白质逻辑门"""
    print("\n" + "=" * 80)
    print("蛋白质逻辑门 - 生物计算的基础")
    print("=" * 80)
    
    print("""
1. AND门 (与门)
   机制: 双底物酶
   ┌─────────────────────────────┐
   │  底物A + 底物B + 酶 → 产物   │
   │  需要A和B同时存在            │
   └─────────────────────────────┘
   实例: 限制性内切酶 (识别特定序列)

2. OR门 (或门)
   机制: 多途径激活
   ┌─────────────────────────────┐
   │  信号A → 激活                │
   │  信号B → 激活                │
   │  A或B任一即可                │
   └─────────────────────────────┘
   实例: 多个转录因子激活同一基因

3. NOT门 (非门)
   机制: 抑制剂/阻遏蛋白
   ┌─────────────────────────────┐
   │  输入 → 阻遏蛋白 → 抑制输出  │
   │  输入高 → 输出低             │
   └─────────────────────────────┘
   实例: lac阻遏蛋白

4. 组合逻辑
   • NAND = NOT + AND
   • NOR = NOT + OR
   • XOR = (A AND NOT B) OR (NOT A AND B)
   
   可以构建任意逻辑电路！

5. 实际案例: 基因振荡器 (Repressilator)
   
   基因A → 蛋白A → 抑制基因B
   基因B → 蛋白B → 抑制基因C
   基因C → 蛋白C → 抑制基因A
   
   结果: 周期性振荡 (类似时钟)
   周期: ~150分钟

6. 生物计算机
   • 2013: 斯坦福大学 - 双核生物计算机
   • 使用大肠杆菌
   • 实现简单逻辑运算
   • 速度: 小时级

7. 优势
   • 在活细胞内工作
   • 可感知生物信号
   • 可执行生物功能
   • 自我复制

8. 局限
   • 速度极慢
   • 噪声大
   • 难以扩展
   • 需要营养供应
    """)

def turing_completeness_protein():
    """蛋白质CPU的图灵完备性"""
    print("\n" + "=" * 80)
    print("蛋白质CPU是否图灵完备？")
    print("=" * 80)
    
    print("""
答案: ✓ 是图灵完备的

证明：

1. 细胞本身就是图灵完备的
   • 细胞 = 通用计算机
   • DNA = 程序
   • 蛋白质 = 处理器
   • 代谢 = 计算过程

2. 逻辑门
   • AND: 双底物酶
   • OR: 多途径激活
   • NOT: 阻遏蛋白
   • 可构建任意逻辑

3. 存储
   • DNA: 长期存储
   • mRNA: 中期存储
   • 蛋白质浓度: 短期存储
   • 表观遗传: 可遗传存储

4. 控制流
   • 条件: 转录因子响应信号
   • 循环: 正反馈/负反馈
   • 分支: 信号通路选择

5. 实际证明
   • 细胞能执行复杂计算
   • 发育: 单细胞→多细胞生物
   • 免疫: 抗体多样性生成
   • 神经: 学习和记忆

6. 合成生物学实例
   • 基因线路: 实现逻辑功能
   • 生物振荡器: 时钟
   • 生物开关: 记忆
   • 边缘检测: 图像处理

局限性：
• 速度: 分钟-小时级
• 精度: 随机性强
• 规模: 难以扩展到复杂程序
• 调试: 极其困难

结论：
蛋白质CPU是图灵完备的，
但不适合通用计算。

最适合：
• 生物传感
• 体内诊断
• 靶向治疗
• 生物制造

"生命是最古老的计算机"
38亿年的进化 = 38亿年的编程
    """)

def main():
    cpu = ProteinCPU()
    cpu.display()
    demonstrate_protein_computing()
    analyze_protein_cpu()
    protein_logic_gates()
    turing_completeness_protein()
    
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)
    print("""
蛋白质CPU：生命的计算本质

核心洞察：
• 生命 = 计算
• 细胞 = 计算机
• DNA = 程序
• 蛋白质 = 处理器
• 代谢 = 执行

惊人的能力：
• 自我复制 (DNA复制)
• 自我修复 (DNA修复)
• 自我组装 (蛋白质折叠)
• 自我进化 (突变+选择)

Levinthal悖论：
• 100个氨基酸 → 3¹⁰⁰种构象
• 随机搜索需10⁷⁷年
• 实际折叠仅需1秒
• 加速10⁸⁴倍！

信号放大：
• MAPK级联: 1个信号 → 10⁶个响应
• 指数级放大
• 灵敏度极高

合成生物学：
• 2000: 基因振荡器
• 2004: 生物开关
• 2010: 合成基因组
• 2020: AlphaFold革命

未来展望：
• 活细胞计算机
• 体内诊断芯片
• 智能药物递送
• 生物-电子接口

哲学意义：
"我们不是在研究计算机，
 我们本身就是计算机。
 每个细胞都在执行程序，
 这个程序已经运行了38亿年。"

蛋白质CPU证明：
计算不是人类的发明，
而是生命的本质。
    """)

if __name__ == '__main__':
    main()
