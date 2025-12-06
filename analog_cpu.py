#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟电路CPU - Analog Circuit CPU
基于连续电压/电流的计算架构

核心思想：
- 连续值计算 (非离散0/1)
- 电压/电流表示数据
- 运算放大器实现运算
- 超低功耗
"""

import numpy as np
import math

class AnalogCPU:
    def __init__(self):
        self.instructions = self._define_instructions()
        # 模拟寄存器 (电压值 -10V ~ +10V)
        self.voltage_regs = {
            'V0': 0.0, 'V1': 0.0, 'V2': 0.0, 'V3': 0.0,
            'V4': 0.0, 'V5': 0.0, 'V6': 0.0, 'V7': 0.0
        }
        # 电流寄存器 (电流值 -10mA ~ +10mA)
        self.current_regs = {
            'I0': 0.0, 'I1': 0.0, 'I2': 0.0, 'I3': 0.0
        }
        self.vdd = 10.0  # 电源电压
        
    def _define_instructions(self):
        """定义模拟指令集"""
        return {
            # 基本运算放大器操作
            'SUM': {'desc': '求和放大器', 'circuit': 'Op-Amp加法器', 'formula': 'Vout = -(V1+V2+...)'},
            'DIFF': {'desc': '差分放大器', 'circuit': 'Op-Amp减法器', 'formula': 'Vout = V1-V2'},
            'GAIN': {'desc': '增益放大', 'circuit': '反相放大器', 'formula': 'Vout = -G*Vin'},
            'BUFFER': {'desc': '电压跟随器', 'circuit': '缓冲器', 'formula': 'Vout = Vin'},
            
            # 数学运算
            'MULTIPLY': {'desc': '模拟乘法', 'circuit': '乘法器IC', 'formula': 'Vout = V1*V2/10'},
            'DIVIDE': {'desc': '模拟除法', 'circuit': '除法器', 'formula': 'Vout = 10*V1/V2'},
            'SQRT': {'desc': '平方根', 'circuit': '开方电路', 'formula': 'Vout = √Vin'},
            'SQUARE': {'desc': '平方', 'circuit': '平方器', 'formula': 'Vout = Vin²/10'},
            'LOG': {'desc': '对数', 'circuit': '对数放大器', 'formula': 'Vout = log(Vin)'},
            'EXP': {'desc': '指数', 'circuit': '指数放大器', 'formula': 'Vout = exp(Vin)'},
            
            # 积分/微分
            'INTEGRATE': {'desc': '积分器', 'circuit': 'RC积分电路', 'formula': 'Vout = ∫Vin dt'},
            'DIFFERENTIATE': {'desc': '微分器', 'circuit': 'RC微分电路', 'formula': 'Vout = dVin/dt'},
            
            # 比较器
            'COMPARE': {'desc': '电压比较', 'circuit': '比较器', 'formula': 'Vout = (V1>V2)?Vdd:0'},
            'WINDOW': {'desc': '窗口比较', 'circuit': '窗口比较器', 'formula': '范围检测'},
            'SCHMITT': {'desc': '施密特触发', 'circuit': '施密特触发器', 'formula': '滞回比较'},
            
            # 滤波器
            'LOWPASS': {'desc': '低通滤波', 'circuit': 'RC低通', 'formula': 'fc = 1/(2πRC)'},
            'HIGHPASS': {'desc': '高通滤波', 'circuit': 'RC高通', 'formula': 'fc = 1/(2πRC)'},
            'BANDPASS': {'desc': '带通滤波', 'circuit': 'RLC带通', 'formula': 'f0 = 1/(2π√LC)'},
            'NOTCH': {'desc': '陷波滤波', 'circuit': '双T陷波', 'formula': '抑制特定频率'},
            
            # 非线性
            'RECTIFY': {'desc': '整流', 'circuit': '二极管整流', 'formula': 'Vout = |Vin|'},
            'CLIP': {'desc': '限幅', 'circuit': '限幅器', 'formula': 'Vout = clip(Vin)'},
            'SATURATE': {'desc': '饱和', 'circuit': '饱和放大器', 'formula': 'Vout = tanh(Vin)'},
            
            # 振荡器
            'OSCILLATE': {'desc': '振荡器', 'circuit': '文氏桥振荡', 'formula': 'f = 1/(2πRC)'},
            'VCO': {'desc': '压控振荡', 'circuit': 'VCO', 'formula': 'f = K*Vin'},
            'PLL': {'desc': '锁相环', 'circuit': 'PLL', 'formula': '频率锁定'},
            
            # 采样保持
            'SAMPLE': {'desc': '采样', 'circuit': 'S/H电路', 'formula': '采样Vin'},
            'HOLD': {'desc': '保持', 'circuit': '保持电容', 'formula': '保持电压'},
            
            # ADC/DAC
            'ADC': {'desc': '模数转换', 'circuit': 'ADC', 'formula': 'Digital = Vin/Vref*2^n'},
            'DAC': {'desc': '数模转换', 'circuit': 'DAC', 'formula': 'Vout = Digital*Vref/2^n'},
            
            # 电流模式
            'V2I': {'desc': '电压转电流', 'circuit': 'V-I转换器', 'formula': 'Iout = Vin/R'},
            'I2V': {'desc': '电流转电压', 'circuit': 'I-V转换器', 'formula': 'Vout = Iin*R'},
            'CURRENT_MIRROR': {'desc': '电流镜', 'circuit': '电流镜', 'formula': 'Iout = Iin'},
            
            # 神经网络
            'NEURON': {'desc': '神经元', 'circuit': '模拟神经元', 'formula': 'Vout = σ(ΣwiVi)'},
            'SYNAPSE': {'desc': '突触', 'circuit': '可变增益', 'formula': 'Vout = w*Vin'},
            
            # 控制
            'HALT': {'desc': '停机', 'circuit': 'N/A', 'formula': 'N/A'}
        }
    
    def sum_amplifier(self, *voltages):
        """求和放大器 (反相)"""
        # Vout = -(V1 + V2 + ... + Vn)
        result = -sum(voltages)
        return self._clip(result)
    
    def diff_amplifier(self, v1, v2):
        """差分放大器"""
        # Vout = V1 - V2
        result = v1 - v2
        return self._clip(result)
    
    def gain_amplifier(self, vin, gain):
        """增益放大器"""
        # Vout = -G * Vin (反相)
        result = -gain * vin
        return self._clip(result)
    
    def multiply(self, v1, v2):
        """模拟乘法器"""
        # Vout = V1 * V2 / 10 (归一化)
        result = v1 * v2 / 10.0
        return self._clip(result)
    
    def divide(self, v1, v2):
        """模拟除法器"""
        if abs(v2) < 0.01:
            return self.vdd  # 饱和
        result = 10.0 * v1 / v2
        return self._clip(result)
    
    def integrate(self, vin, dt=0.001, initial=0):
        """积分器"""
        # Vout = ∫Vin dt
        # 简化：Vout = Vout_prev + Vin * dt
        result = initial + vin * dt
        return self._clip(result)
    
    def differentiate(self, vin, vin_prev, dt=0.001):
        """微分器"""
        # Vout = dVin/dt
        result = (vin - vin_prev) / dt
        return self._clip(result)
    
    def compare(self, v1, v2):
        """电压比较器"""
        # Vout = (V1 > V2) ? Vdd : 0
        return self.vdd if v1 > v2 else 0.0
    
    def rectify(self, vin):
        """整流器 (全波整流)"""
        return abs(vin)
    
    def saturate(self, vin):
        """饱和函数 (tanh)"""
        return self.vdd * math.tanh(vin / self.vdd)
    
    def lowpass_filter(self, vin, vin_prev, alpha=0.1):
        """一阶低通滤波器"""
        # Vout = α*Vin + (1-α)*Vout_prev
        return alpha * vin + (1 - alpha) * vin_prev
    
    def _clip(self, voltage):
        """限幅到电源范围"""
        return max(-self.vdd, min(self.vdd, voltage))
    
    def display(self):
        """展示模拟CPU设计"""
        print("=" * 80)
        print("模拟电路CPU - Analog Circuit CPU")
        print("基于连续电压/电流的计算架构")
        print("=" * 80)
        
        print(f"\n总指令数: {len(self.instructions)}")
        print(f"电源电压: ±{self.vdd}V")
        print(f"电压范围: -{self.vdd}V ~ +{self.vdd}V")
        
        print("\n指令分类:")
        categories = {
            '运算放大器': ['SUM', 'DIFF', 'GAIN', 'BUFFER'],
            '数学运算': ['MULTIPLY', 'DIVIDE', 'SQRT', 'SQUARE', 'LOG', 'EXP'],
            '微积分': ['INTEGRATE', 'DIFFERENTIATE'],
            '比较器': ['COMPARE', 'WINDOW', 'SCHMITT'],
            '滤波器': ['LOWPASS', 'HIGHPASS', 'BANDPASS', 'NOTCH'],
            '非线性': ['RECTIFY', 'CLIP', 'SATURATE'],
            '振荡器': ['OSCILLATE', 'VCO', 'PLL'],
            '采样保持': ['SAMPLE', 'HOLD'],
            '转换器': ['ADC', 'DAC', 'V2I', 'I2V', 'CURRENT_MIRROR'],
            '神经网络': ['NEURON', 'SYNAPSE']
        }
        
        for cat, instrs in categories.items():
            print(f"\n{cat}:")
            for instr in instrs:
                if instr in self.instructions:
                    info = self.instructions[instr]
                    print(f"  {instr:<15} - {info['desc']:<15} [{info['circuit']}]")
                    print(f"                  公式: {info['formula']}")

def demonstrate_analog_computing():
    """演示模拟计算"""
    cpu = AnalogCPU()
    
    print("\n" + "=" * 80)
    print("模拟计算演示")
    print("=" * 80)
    
    # 1. 基本运算
    print("\n1. 基本运算放大器操作:")
    v1, v2 = 3.0, 2.0
    print(f"  输入: V1={v1}V, V2={v2}V")
    print(f"  求和: Vout = -(V1+V2) = {cpu.sum_amplifier(v1, v2):.2f}V")
    print(f"  差分: Vout = V1-V2 = {cpu.diff_amplifier(v1, v2):.2f}V")
    print(f"  增益: Vout = -2*V1 = {cpu.gain_amplifier(v1, 2):.2f}V")
    
    # 2. 模拟乘法
    print("\n2. 模拟乘法器:")
    test_cases = [(5, 2), (3, 3), (-4, 2), (8, -1)]
    for v1, v2 in test_cases:
        result = cpu.multiply(v1, v2)
        print(f"  {v1}V × {v2}V = {result:.2f}V")
    
    # 3. 积分器
    print("\n3. 积分器 (求面积):")
    print("  输入恒定电压 5V，积分0.1秒:")
    vin = 5.0
    dt = 0.001
    vout = 0.0
    for _ in range(100):  # 100ms
        vout = cpu.integrate(vin, dt, vout)
    print(f"  输出: {vout:.2f}V (理论: {vin*0.1:.2f}V)")
    
    # 4. 微分器
    print("\n4. 微分器 (求斜率):")
    print("  输入斜坡信号:")
    vin_prev = 0.0
    for t in [0, 0.001, 0.002, 0.003]:
        vin = 1000 * t  # 斜率=1000 V/s
        if t > 0:
            dvdt = cpu.differentiate(vin, vin_prev, 0.001)
            print(f"  t={t:.3f}s, Vin={vin:.2f}V, dV/dt={dvdt:.0f}V/s")
        vin_prev = vin
    
    # 5. 比较器
    print("\n5. 电压比较器:")
    test_voltages = [1.0, 2.5, 5.0, 7.5, 10.0]
    threshold = 5.0
    print(f"  阈值: {threshold}V")
    for v in test_voltages:
        result = cpu.compare(v, threshold)
        print(f"  Vin={v:.1f}V → Vout={result:.1f}V {'(HIGH)' if result > 0 else '(LOW)'}")
    
    # 6. 整流器
    print("\n6. 全波整流器:")
    test_voltages = [-5, -2.5, 0, 2.5, 5]
    for v in test_voltages:
        result = cpu.rectify(v)
        print(f"  Vin={v:+.1f}V → Vout={result:.1f}V")
    
    # 7. 饱和函数
    print("\n7. 饱和放大器 (tanh):")
    test_voltages = [-10, -5, 0, 5, 10, 15]
    for v in test_voltages:
        result = cpu.saturate(v)
        print(f"  Vin={v:+3.0f}V → Vout={result:+.2f}V")
    
    # 8. 低通滤波
    print("\n8. 低通滤波器 (平滑噪声):")
    noisy_signal = [5.0, 5.2, 4.8, 5.1, 4.9, 5.3, 4.7]
    filtered = noisy_signal[0]
    print(f"  原始信号: {noisy_signal}")
    filtered_signal = []
    for v in noisy_signal:
        filtered = cpu.lowpass_filter(v, filtered, alpha=0.3)
        filtered_signal.append(filtered)
    print(f"  滤波后:   {[f'{v:.2f}' for v in filtered_signal]}")

def analyze_analog_cpu():
    """分析模拟CPU特性"""
    print("\n" + "=" * 80)
    print("模拟CPU特性分析")
    print("=" * 80)
    
    analysis = {
        '核心优势': [
            '• 超低功耗: μW-mW级 (vs 数字CPU的W级)',
            '• 连续值计算: 无量化误差',
            '• 天然并行: 电路同时工作',
            '• 高速模拟运算: 微积分、滤波等',
            '• 简单电路: 少量元件即可',
            '• 低成本: 无需复杂工艺',
            '• 实时性: 无时钟周期'
        ],
        '关键劣势': [
            '• 精度低: 1-2% (vs 数字的精确)',
            '• 温度漂移: 受环境影响',
            '• 噪声敏感: 易受干扰',
            '• 难编程: 需改变电路',
            '• 不可重构: 固定功能',
            '• 难以存储: 电容漏电',
            '• 不图灵完备: 缺乏通用性'
        ],
        '适用场景': [
            '• 信号处理: 滤波、放大',
            '• 传感器接口: 模拟前端',
            '• 神经网络: 模拟神经元',
            '• 控制系统: PID控制',
            '• 音频处理: 均衡器、效果器',
            '• 射频: 混频、调制',
            '• 低功耗AI: 边缘计算'
        ],
        '历史地位': [
            '• 1940s: 模拟计算机黄金时代',
            '• 用于弹道计算、微分方程求解',
            '• 1960s-70s: 被数字计算机取代',
            '• 2010s: 模拟AI芯片复兴',
            '• 未来: 混合模拟-数字架构'
        ]
    }
    
    for category, points in analysis.items():
        print(f"\n{category}:")
        for point in points:
            print(f"  {point}")

def compare_analog_digital():
    """模拟vs数字对比"""
    print("\n" + "=" * 80)
    print("模拟CPU vs 数字CPU")
    print("=" * 80)
    
    comparison = [
        ['特性', '模拟CPU', '数字CPU'],
        ['数据表示', '连续电压/电流', '离散0/1'],
        ['精度', '1-2% (低)', '精确 (高)'],
        ['功耗', 'μW-mW (极低)', 'W-100W (高)'],
        ['速度', '极快 (无时钟)', '受时钟限制'],
        ['并行性', '天然并行', '需设计'],
        ['可编程性', '困难 (改电路)', '容易 (软件)'],
        ['存储', '困难 (电容)', '容易 (SRAM)'],
        ['噪声', '敏感', '抗噪声强'],
        ['温度漂移', '严重', '小'],
        ['成本', '低', '中高'],
        ['图灵完备', '否', '是'],
        ['适用', '特定任务', '通用计算']
    ]
    
    for row in comparison:
        print(f"{row[0]:<15} {row[1]:<25} {row[2]:<25}")

def hardware_implementation():
    """硬件实现"""
    print("\n" + "=" * 80)
    print("模拟CPU硬件实现")
    print("=" * 80)
    
    print("""
1. 基本构建块

   运算放大器 (Op-Amp)
   ┌─────────────────┐
   │      +Vcc       │
   │        │        │
   │    ┌───▼───┐    │
   │ ───┤-      │    │
   │    │   Op  ├───→ Vout
   │ ───┤+   Amp│    │
   │    └───────┘    │
   │        │        │
   │      -Vcc       │
   └─────────────────┘
   
   • 核心器件: LM358, TL072, OPA2134
   • 增益: 100dB+
   • 带宽: MHz级
   • 功耗: mW级

2. 求和放大器电路
   
        R1
   V1 ──┬──┐
        │  │  Rf
   V2 ──┬──┼──┬──┐
        R2 │  │  │
          ─┴─ │  │
          │-\ │  │
          │  >┴──┴─→ Vout = -(V1+V2)
          │+/
          ─┬─
           │
          GND

3. 乘法器电路
   
   • IC: AD633 (模拟乘法器)
   • 公式: Vout = (V1×V2)/10 + V3
   • 精度: 0.1%
   • 带宽: 1MHz

4. 积分器电路
   
        R
   Vin ─┬──┐
        │  │  C
        │  ├──┬──┐
        │  │  │  │
       ─┴─ │  │  │
       │-\ │  │  │
       │  >┴──┴──→ Vout = -∫Vin dt / RC
       │+/
       ─┬─
        │
       GND

5. 完整模拟计算机示例

   • Heathkit EC-1 (1960s)
   • PACE TR-48 (1970s)
   • 现代: Mythic AI芯片 (模拟AI)

6. 现代应用: 模拟AI芯片

   Mythic AI 架构:
   ┌─────────────────────────────────┐
   │  数字输入 (激活值)               │
   └──────────┬──────────────────────┘
              │ DAC
   ┌──────────▼──────────────────────┐
   │  模拟矩阵乘法 (Flash存储权重)    │
   │  • 电导表示权重                  │
   │  • 电流求和 = 矩阵乘法           │
   │  • 功耗: 1/10 数字              │
   └──────────┬──────────────────────┘
              │ ADC
   ┌──────────▼──────────────────────┐
   │  数字输出                        │
   └─────────────────────────────────┘
    """)

def turing_completeness_analog():
    """模拟CPU的图灵完备性"""
    print("\n" + "=" * 80)
    print("模拟CPU是否图灵完备？")
    print("=" * 80)
    
    print("""
答案: ✗ 不是图灵完备

原因：

1. 缺乏通用存储
   • 电容存储会漏电
   • 无法实现RAM
   • 不能保存程序状态

2. 不可编程
   • 功能由电路固定
   • 改变功能需改变电路
   • 无法执行任意程序

3. 精度限制
   • 连续值有噪声
   • 无法精确表示整数
   • 不适合逻辑运算

4. 无条件分支
   • 比较器只能简单判断
   • 难以实现复杂控制流
   • 无法实现循环计数

但是：

模拟计算机可以解决特定类型的问题：
• 微分方程 (天然积分器)
• 线性代数 (矩阵运算)
• 信号处理 (滤波、变换)
• 优化问题 (模拟退火)

类比：
• 模拟计算机 ≈ 专用加速器
• 数字计算机 ≈ 通用处理器

结论：
模拟CPU不是图灵完备的通用计算机，
但在特定领域有独特优势，
尤其是低功耗AI推理。

未来趋势：混合模拟-数字架构
• 数字: 控制、存储、精确计算
• 模拟: 高速、低功耗、并行计算
    """)

def main():
    cpu = AnalogCPU()
    cpu.display()
    demonstrate_analog_computing()
    analyze_analog_cpu()
    compare_analog_digital()
    hardware_implementation()
    turing_completeness_analog()
    
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)
    print("""
模拟电路CPU：被遗忘的计算范式

历史：
• 1940s-1960s: 模拟计算机的黄金时代
• 用于弹道计算、飞行模拟、核反应堆设计
• 1970s: 被数字计算机全面取代

复兴：
• 2010s: 模拟AI芯片重新兴起
• Mythic AI, Analog Devices等公司
• 功耗仅为数字芯片的1/10

核心优势：
1. 超低功耗 (μW级)
2. 天然并行
3. 高速模拟运算
4. 简单电路

核心劣势：
1. 精度低
2. 不可编程
3. 不图灵完备
4. 温度漂移

最佳应用：
• 边缘AI推理
• 传感器信号处理
• 低功耗IoT
• 混合模拟-数字系统

"模拟计算不是数字计算的竞争者，
 而是在特定领域的完美补充"

未来属于混合架构：
数字的精确性 + 模拟的高效性 = 最优解
    """)

if __name__ == '__main__':
    main()
