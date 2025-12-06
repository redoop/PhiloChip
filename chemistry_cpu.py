#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
化学CPU - Chemistry-Driven CPU
基于元素周期表和化学反应的计算架构

核心思想：
- 化学反应作为计算
- 元素性质映射指令
- 分子结构存储信息
- 反应速率控制时序
"""

import math

class ChemistryCPU:
    def __init__(self):
        self.instructions = self._define_instructions()
        self.elements = self._define_elements()
        # 化学寄存器 (浓度 mol/L)
        self.reagents = {
            'H': 0.0, 'O': 0.0, 'C': 0.0, 'N': 0.0,
            'Na': 0.0, 'Cl': 0.0, 'Fe': 0.0, 'Cu': 0.0
        }
        self.temperature = 298.15  # K (25°C)
        self.pH = 7.0
        
    def _define_elements(self):
        """定义关键元素"""
        return {
            # 第1周期
            'H': {'Z': 1, 'group': 1, 'period': 1, 'valence': 1, 'property': '还原剂'},
            'He': {'Z': 2, 'group': 18, 'period': 1, 'valence': 0, 'property': '惰性'},
            
            # 第2周期
            'C': {'Z': 6, 'group': 14, 'period': 2, 'valence': 4, 'property': '有机骨架'},
            'N': {'Z': 7, 'group': 15, 'period': 2, 'valence': 3, 'property': '碱性'},
            'O': {'Z': 8, 'group': 16, 'period': 2, 'valence': 2, 'property': '氧化剂'},
            'F': {'Z': 9, 'group': 17, 'period': 2, 'valence': 1, 'property': '强氧化'},
            
            # 第3周期
            'Na': {'Z': 11, 'group': 1, 'period': 3, 'valence': 1, 'property': '强还原'},
            'Mg': {'Z': 12, 'group': 2, 'period': 3, 'valence': 2, 'property': '还原剂'},
            'Si': {'Z': 14, 'group': 14, 'period': 3, 'valence': 4, 'property': '半导体'},
            'P': {'Z': 15, 'group': 15, 'period': 3, 'valence': 3, 'property': '生命元素'},
            'S': {'Z': 16, 'group': 16, 'period': 3, 'valence': 2, 'property': '硫化'},
            'Cl': {'Z': 17, 'group': 17, 'period': 3, 'valence': 1, 'property': '氧化剂'},
            
            # 过渡金属
            'Fe': {'Z': 26, 'group': 8, 'period': 4, 'valence': '2/3', 'property': '催化剂'},
            'Cu': {'Z': 29, 'group': 11, 'period': 4, 'valence': '1/2', 'property': '导电'},
            'Ag': {'Z': 47, 'group': 11, 'period': 5, 'valence': 1, 'property': '贵金属'},
            'Au': {'Z': 79, 'group': 11, 'period': 6, 'valence': '1/3', 'property': '惰性贵金属'}
        }
    
    def _define_instructions(self):
        """定义化学指令集"""
        return {
            # 基于元素周期律
            'ALKALI': {'desc': '碱金属反应', 'elements': 'Li,Na,K', 'property': '强还原性'},
            'HALOGEN': {'desc': '卤素反应', 'elements': 'F,Cl,Br,I', 'property': '强氧化性'},
            'NOBLE': {'desc': '惰性气体', 'elements': 'He,Ne,Ar', 'property': '不反应'},
            'TRANSITION': {'desc': '过渡金属', 'elements': 'Fe,Cu,Ag', 'property': '催化'},
            
            # 化学反应类型
            'OXIDIZE': {'desc': '氧化反应', 'example': '2H₂+O₂→2H₂O', 'ΔG': '负'},
            'REDUCE': {'desc': '还原反应', 'example': 'Fe₂O₃+3CO→2Fe+3CO₂', 'ΔG': '负'},
            'ACID_BASE': {'desc': '酸碱中和', 'example': 'HCl+NaOH→NaCl+H₂O', 'ΔH': '负'},
            'PRECIPITATE': {'desc': '沉淀反应', 'example': 'AgNO₃+NaCl→AgCl↓', 'ΔS': '负'},
            'COMPLEX': {'desc': '配位反应', 'example': 'Cu²⁺+4NH₃→[Cu(NH₃)₄]²⁺', 'K': '大'},
            
            # 有机反应
            'ADDITION': {'desc': '加成反应', 'example': 'C₂H₄+H₂→C₂H₆', 'type': '有机'},
            'SUBSTITUTION': {'desc': '取代反应', 'example': 'CH₄+Cl₂→CH₃Cl+HCl', 'type': '有机'},
            'ELIMINATION': {'desc': '消除反应', 'example': 'C₂H₅OH→C₂H₄+H₂O', 'type': '有机'},
            'POLYMERIZE': {'desc': '聚合反应', 'example': 'nC₂H₄→(C₂H₄)ₙ', 'type': '高分子'},
            
            # 电化学
            'ELECTROLYSIS': {'desc': '电解', 'example': '2H₂O→2H₂+O₂', 'E': '1.23V'},
            'GALVANIC': {'desc': '原电池', 'example': 'Zn+Cu²⁺→Zn²⁺+Cu', 'E': '1.10V'},
            'CORROSION': {'desc': '腐蚀', 'example': '4Fe+3O₂→2Fe₂O₃', 'spontaneous': True},
            
            # 催化
            'CATALYZE': {'desc': '催化反应', 'catalyst': 'Pt,Pd,Fe', 'effect': '降低Ea'},
            'ENZYME': {'desc': '酶催化', 'catalyst': '生物酶', 'specificity': '高'},
            'AUTOCATALYSIS': {'desc': '自催化', 'example': 'A+B→2A', 'exponential': True},
            
            # 平衡
            'EQUILIBRIUM': {'desc': '化学平衡', 'law': 'K=[C]ᶜ[D]ᵈ/[A]ᵃ[B]ᵇ', 'dynamic': True},
            'LE_CHATELIER': {'desc': '勒夏特列原理', 'principle': '平衡移动', 'adaptive': True},
            'BUFFER': {'desc': '缓冲溶液', 'example': 'HAc/NaAc', 'pH_stable': True},
            
            # 动力学
            'RATE': {'desc': '反应速率', 'formula': 'v=k[A]ᵐ[B]ⁿ', 'unit': 'mol/(L·s)'},
            'ARRHENIUS': {'desc': '阿伦尼乌斯', 'formula': 'k=Ae^(-Ea/RT)', 'temp_dep': True},
            'ACTIVATION': {'desc': '活化能', 'symbol': 'Ea', 'barrier': True},
            
            # 热力学
            'ENTHALPY': {'desc': '焓变', 'symbol': 'ΔH', 'unit': 'kJ/mol'},
            'ENTROPY': {'desc': '熵变', 'symbol': 'ΔS', 'unit': 'J/(mol·K)'},
            'GIBBS': {'desc': '吉布斯自由能', 'formula': 'ΔG=ΔH-TΔS', 'spontaneous': 'ΔG<0'},
            
            # 分子结构
            'BOND': {'desc': '化学键', 'types': '共价/离子/金属', 'energy': 'kJ/mol'},
            'ISOMER': {'desc': '同分异构', 'types': '结构/立体', 'same_formula': True},
            'CHIRALITY': {'desc': '手性', 'property': '光学活性', 'mirror': True},
            
            # 量子化学
            'ORBITAL': {'desc': '轨道', 'types': 's,p,d,f', 'quantum': True},
            'HYBRID': {'desc': '杂化', 'types': 'sp,sp²,sp³', 'geometry': True},
            'RESONANCE': {'desc': '共振', 'example': '苯环', 'delocalized': True},
            
            # 胶体
            'COLLOID': {'desc': '胶体', 'size': '1-100nm', 'tyndall': True},
            'EMULSION': {'desc': '乳化', 'example': '油水', 'surfactant': True},
            
            # 控制
            'HALT': {'desc': '停机', 'method': '淬灭反应', 'T': '0K'}
        }
    
    def oxidation_reduction(self, reductant, oxidant):
        """氧化还原反应"""
        # 简化：电子转移
        # 例：2H₂ + O₂ → 2H₂O
        if reductant == 'H' and oxidant == 'O':
            product = 'H2O'
            delta_G = -237.1  # kJ/mol
            return product, delta_G
        return None, 0
    
    def acid_base_neutralization(self, acid_conc, base_conc):
        """酸碱中和"""
        # H⁺ + OH⁻ → H₂O
        neutralized = min(acid_conc, base_conc)
        remaining_acid = acid_conc - neutralized
        remaining_base = base_conc - neutralized
        
        # 计算pH
        if remaining_acid > 0:
            pH = -math.log10(remaining_acid)
        elif remaining_base > 0:
            pOH = -math.log10(remaining_base)
            pH = 14 - pOH
        else:
            pH = 7.0
        
        return pH, neutralized
    
    def reaction_rate(self, k, concentrations, orders):
        """反应速率方程 v = k[A]^m[B]^n"""
        rate = k
        for conc, order in zip(concentrations, orders):
            rate *= conc ** order
        return rate
    
    def arrhenius_equation(self, A, Ea, T):
        """阿伦尼乌斯方程 k = A·e^(-Ea/RT)"""
        R = 8.314  # J/(mol·K)
        k = A * math.exp(-Ea / (R * T))
        return k
    
    def gibbs_free_energy(self, delta_H, delta_S, T):
        """吉布斯自由能 ΔG = ΔH - TΔS"""
        delta_G = delta_H - T * delta_S
        spontaneous = delta_G < 0
        return delta_G, spontaneous
    
    def equilibrium_constant(self, products, reactants):
        """平衡常数 K = [C]^c[D]^d / [A]^a[B]^b"""
        K = 1.0
        for conc, coeff in products:
            K *= conc ** coeff
        for conc, coeff in reactants:
            K /= conc ** coeff
        return K
    
    def periodic_trend(self, element1, element2, property_name):
        """周期律趋势"""
        e1 = self.elements[element1]
        e2 = self.elements[element2]
        
        if property_name == 'electronegativity':
            # 同周期从左到右增大
            if e1['period'] == e2['period']:
                return e1['Z'] < e2['Z']
        elif property_name == 'atomic_radius':
            # 同周期从左到右减小
            if e1['period'] == e2['period']:
                return e1['Z'] > e2['Z']
        
        return None
    
    def display(self):
        """展示化学CPU设计"""
        print("=" * 80)
        print("化学CPU - Chemistry-Driven CPU")
        print("基于元素周期表和化学反应的计算架构")
        print("=" * 80)
        
        print(f"\n总指令数: {len(self.instructions)}")
        print(f"元素库: {len(self.elements)}种元素")
        print(f"温度: {self.temperature}K ({self.temperature-273.15:.1f}°C)")
        print(f"pH: {self.pH}")
        
        print("\n关键元素:")
        for symbol, props in list(self.elements.items())[:8]:
            print(f"  {symbol:<3} (Z={props['Z']:2d}) - {props['property']}")
        
        print("\n指令分类:")
        categories = {
            '周期律': ['ALKALI', 'HALOGEN', 'NOBLE', 'TRANSITION'],
            '反应类型': ['OXIDIZE', 'REDUCE', 'ACID_BASE', 'PRECIPITATE', 'COMPLEX'],
            '有机反应': ['ADDITION', 'SUBSTITUTION', 'ELIMINATION', 'POLYMERIZE'],
            '电化学': ['ELECTROLYSIS', 'GALVANIC', 'CORROSION'],
            '催化': ['CATALYZE', 'ENZYME', 'AUTOCATALYSIS'],
            '平衡': ['EQUILIBRIUM', 'LE_CHATELIER', 'BUFFER'],
            '动力学': ['RATE', 'ARRHENIUS', 'ACTIVATION'],
            '热力学': ['ENTHALPY', 'ENTROPY', 'GIBBS'],
            '结构': ['BOND', 'ISOMER', 'CHIRALITY'],
            '量子': ['ORBITAL', 'HYBRID', 'RESONANCE']
        }
        
        for cat, instrs in categories.items():
            print(f"\n{cat}:")
            for instr in instrs[:3]:  # 只显示前3个
                if instr in self.instructions:
                    info = self.instructions[instr]
                    print(f"  {instr:<20} - {info['desc']}")

def demonstrate_chemistry_computing():
    """演示化学计算"""
    cpu = ChemistryCPU()
    
    print("\n" + "=" * 80)
    print("化学计算演示")
    print("=" * 80)
    
    # 1. 酸碱中和
    print("\n1. 酸碱中和反应:")
    test_cases = [
        (0.1, 0.1, "等量中和"),
        (0.1, 0.05, "酸过量"),
        (0.05, 0.1, "碱过量")
    ]
    for acid, base, desc in test_cases:
        pH, neutralized = cpu.acid_base_neutralization(acid, base)
        print(f"  {desc}: [H⁺]={acid}M, [OH⁻]={base}M → pH={pH:.2f}, 中和={neutralized:.2f}mol")
    
    # 2. 反应速率
    print("\n2. 反应速率计算:")
    k = 0.5  # 速率常数
    test_cases = [
        ([1.0, 1.0], [1, 1], "一级+一级"),
        ([2.0, 1.0], [1, 1], "浓度加倍"),
        ([1.0, 1.0], [2, 1], "二级+一级")
    ]
    for concs, orders, desc in test_cases:
        rate = cpu.reaction_rate(k, concs, orders)
        print(f"  {desc}: v = {rate:.3f} mol/(L·s)")
    
    # 3. 阿伦尼乌斯方程
    print("\n3. 温度对反应速率的影响:")
    A = 1e10  # 指前因子
    Ea = 50000  # 活化能 J/mol
    temperatures = [273, 298, 323, 373]
    print(f"  活化能: {Ea/1000:.0f} kJ/mol")
    for T in temperatures:
        k = cpu.arrhenius_equation(A, Ea, T)
        print(f"  T={T}K ({T-273:.0f}°C): k={k:.2e} s⁻¹")
    
    # 4. 吉布斯自由能
    print("\n4. 反应自发性判断:")
    reactions = [
        (-100, -50, 298, "放热+熵增"),
        (-100, 50, 298, "放热+熵减"),
        (100, 200, 298, "吸热+熵增"),
        (100, -50, 298, "吸热+熵减")
    ]
    for dH, dS, T, desc in reactions:
        dG, spont = cpu.gibbs_free_energy(dH*1000, dS, T)
        print(f"  {desc}: ΔG={dG/1000:.1f}kJ/mol, 自发={spont}")
    
    # 5. 化学平衡
    print("\n5. 化学平衡常数:")
    # 例：N₂ + 3H₂ ⇌ 2NH₃
    products = [(0.5, 2)]  # [NH₃]^2
    reactants = [(1.0, 1), (2.0, 3)]  # [N₂]^1 [H₂]^3
    K = cpu.equilibrium_constant(products, reactants)
    print(f"  N₂ + 3H₂ ⇌ 2NH₃")
    print(f"  [NH₃]=0.5M, [N₂]=1.0M, [H₂]=2.0M")
    print(f"  K = {K:.4f}")
    
    # 6. 周期律
    print("\n6. 元素周期律:")
    comparisons = [
        ('Na', 'Cl', 'electronegativity', '电负性'),
        ('Na', 'Cl', 'atomic_radius', '原子半径')
    ]
    for e1, e2, prop, name in comparisons:
        result = cpu.periodic_trend(e1, e2, prop)
        print(f"  {name}: {e1} {'<' if result else '>'} {e2}")

def analyze_chemistry_cpu():
    """分析化学CPU特性"""
    print("\n" + "=" * 80)
    print("化学CPU特性分析")
    print("=" * 80)
    
    analysis = {
        '核心优势': [
            '• 大规模并行: 10²³个分子同时反应 (阿伏伽德罗常数)',
            '• 自组装: 分子自动形成结构',
            '• 低能耗: 室温反应，无需高温',
            '• 信息密度高: DNA存储 10¹⁹ bit/cm³',
            '• 可编程: 改变反应物即改变功能',
            '• 生物兼容: 可在生物体内工作'
        ],
        '关键挑战': [
            '• 速度慢: 秒-分钟级 (vs 电子ns级)',
            '• 精度低: 受温度、浓度影响',
            '• 不可逆: 多数反应难以逆转',
            '• 副反应: 非目标产物',
            '• 难以小型化: 需要宏观容器',
            '• 环境敏感: pH、温度、压力'
        ],
        '实际应用': [
            '• DNA计算: 解决NP完全问题 (Adleman 1994)',
            '• 化学神经网络: 振荡反应',
            '• 分子逻辑门: AND/OR/NOT',
            '• 生物传感器: 酶反应检测',
            '• 药物筛选: 组合化学',
            '• 自组装纳米结构'
        ],
        '历史里程碑': [
            '• 1994: Adleman DNA计算 (哈密顿路径)',
            '• 2002: 分子计算机 (Weizmann研究所)',
            '• 2013: DNA存储 (哈佛大学)',
            '• 2016: 化学神经网络 (格拉斯哥大学)'
        ]
    }
    
    for category, points in analysis.items():
        print(f"\n{category}:")
        for point in points:
            print(f"  {point}")

def turing_completeness_chemistry():
    """化学CPU的图灵完备性"""
    print("\n" + "=" * 80)
    print("化学CPU是否图灵完备？")
    print("=" * 80)
    
    print("""
答案: ✓ 理论上是图灵完备的

证明：

1. DNA计算 (Adleman 1994)
   • 用DNA分子编码图问题
   • 通过生化反应求解哈密顿路径
   • 证明：化学反应可以进行通用计算

2. 化学图灵机
   • 状态: 不同分子种类
   • 纸带: DNA序列
   • 读写: 酶切割/连接
   • 转移: 化学反应规则

3. 逻辑门实现
   • AND: A + B → C (需要两种反应物)
   • OR: A → C 或 B → C (任一反应物)
   • NOT: 抑制反应 (竞争性抑制)
   • 组合可实现任意逻辑

4. 存储
   • DNA: 4种碱基 = 2 bit
   • 分子浓度: 模拟存储
   • 沉淀: 固态存储

5. 控制流
   • 条件: pH、温度触发
   • 循环: 自催化反应
   • 分支: 竞争反应

实例：DNA计算解决TSP

问题: 7个城市的旅行商问题
方法:
1. 合成所有可能路径的DNA (10¹⁴条)
2. 用酶筛选满足条件的路径
3. PCR扩增正确答案
4. 测序读取结果

时间: 7天 (vs 超级计算机数年)
并行度: 10¹⁴ (vs 电子计算机10⁶)

局限性：
• 速度慢 (天级)
• 错误率高 (1%)
• 难以通用化
• 需要人工干预

结论：
化学CPU是图灵完备的，
但不适合通用计算，
适合特定的大规模并行问题。

"化学计算是自然界的计算方式"
生命本身就是化学计算机！
    """)

def main():
    cpu = ChemistryCPU()
    cpu.display()
    demonstrate_chemistry_computing()
    analyze_chemistry_cpu()
    turing_completeness_chemistry()
    
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)
    print("""
化学CPU：自然界的计算范式

核心思想：
• 化学反应 = 计算
• 分子 = 数据
• 反应速率 = 时钟
• 平衡常数 = 逻辑

惊人的并行性：
• 1摩尔 = 6.02×10²³个分子
• 同时进行10²³次"计算"
• 远超任何电子计算机

DNA计算突破：
• 1994年Adleman用DNA解决7城市TSP
• 10¹⁴条DNA同时尝试所有路径
• 证明化学计算的可行性

信息存储密度：
• DNA: 10¹⁹ bit/cm³
• 硬盘: 10¹² bit/cm³
• DNA密度是硬盘的1000万倍！

生命即计算：
• 细胞是化学计算机
• DNA是程序
• 蛋白质是处理器
• 代谢是计算过程

未来展望：
• 分子计算机
• DNA数据存储
• 化学神经网络
• 合成生物学

哲学意义：
"计算不仅存在于硅片中，
 更存在于每一个化学反应中。
 生命本身就是最精妙的化学计算机。"

元素周期表不仅是化学的基础，
更是一张计算的蓝图！
    """)

if __name__ == '__main__':
    main()
