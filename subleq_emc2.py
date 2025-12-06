#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用SUBLEQ (单指令集计算机) 计算 E = mc²

展示如何用一条指令实现爱因斯坦最著名的公式
"""

class SUBLEQMachine:
    def __init__(self, memory_size=256):
        self.memory = [0] * memory_size
        self.pc = 0  # Program Counter
        self.halted = False
        self.steps = 0
        
    def load_program(self, program, data):
        """加载程序和数据到内存"""
        # 程序从地址0开始
        for i, val in enumerate(program):
            self.memory[i] = val
        # 数据从程序后开始
        data_start = len(program)
        for i, val in enumerate(data):
            self.memory[data_start + i] = val
        return data_start
    
    def subleq(self, a, b, c):
        """
        SUBLEQ指令：唯一的指令
        Mem[b] = Mem[b] - Mem[a]
        if (Mem[b] <= 0) then PC = c
        else PC = PC + 3
        """
        self.memory[b] = self.memory[b] - self.memory[a]
        if self.memory[b] <= 0:
            self.pc = c
        else:
            self.pc += 3
    
    def run(self, max_steps=1000, verbose=False):
        """运行程序"""
        while not self.halted and self.steps < max_steps:
            if self.pc >= len(self.memory) - 2:
                break
            
            a = self.memory[self.pc]
            b = self.memory[self.pc + 1]
            c = self.memory[self.pc + 2]
            
            if verbose:
                print(f"Step {self.steps}: PC={self.pc}, SUBLEQ {a}, {b}, {c}")
                print(f"  Before: Mem[{a}]={self.memory[a]}, Mem[{b}]={self.memory[b]}")
            
            # 检查停机条件
            if a == -1 or b == -1 or c == -1:
                self.halted = True
                break
            
            self.subleq(a, b, c)
            self.steps += 1
            
            if verbose:
                print(f"  After:  Mem[{b}]={self.memory[b]}, Next PC={self.pc}\n")
        
        return self.memory

def create_emc2_program():
    """
    创建计算 E = mc² 的SUBLEQ程序
    
    假设：
    - m = 2 (质量，单位：kg)
    - c = 3 (光速简化值，实际是3×10^8 m/s)
    - E = m × c × c = 2 × 3 × 3 = 18
    
    SUBLEQ实现乘法：
    result = a × b 通过循环加法实现
    """
    
    # 内存布局（数据区从地址100开始）
    ZERO = 100      # 常量0
    ONE = 101       # 常量1
    TEMP = 102      # 临时变量
    M = 103         # 质量 m
    C = 104         # 光速 c
    C_SQUARED = 105 # c²
    E = 106         # 能量 E = mc²
    COUNTER = 107   # 循环计数器
    NEG_ONE = 108   # 常量-1
    
    program = []
    
    # 初始化：E = 0
    # SUBLEQ E, E, next (E = 0)
    program.extend([E, E, len(program)+3])
    
    # 第一步：计算 c² = c × c
    # 使用循环加法：c² = 0; for i in range(c): c² += c
    
    # 初始化 c² = 0
    program.extend([C_SQUARED, C_SQUARED, len(program)+3])
    
    # 初始化 COUNTER = c
    program.extend([COUNTER, COUNTER, len(program)+3])  # COUNTER = 0
    program.extend([COUNTER, C, len(program)+3])        # COUNTER = 0 - c = -c
    program.extend([COUNTER, COUNTER, len(program)+3])  # COUNTER = 0 (清零)
    program.extend([COUNTER, NEG_ONE, len(program)+3])  # COUNTER = -(-c) = c
    
    # 循环：while COUNTER > 0: c² += c; COUNTER--
    loop1_start = len(program)
    # 检查 COUNTER <= 0，如果是则跳出循环
    program.extend([TEMP, TEMP, len(program)+3])        # TEMP = 0
    program.extend([TEMP, COUNTER, len(program)+3])     # TEMP = -COUNTER
    # 如果 TEMP <= 0 (即 COUNTER >= 0)，继续；否则跳到loop1_end
    # 这里简化：直接用COUNTER判断
    program.extend([COUNTER, ZERO, len(program)+15])    # 如果COUNTER<=0跳出
    
    # c² += c (通过 c² = c² - (-c) 实现)
    program.extend([C_SQUARED, NEG_ONE, len(program)+3]) # c² -= (-c) 需要先准备-c
    # 简化：直接减去负数
    program.extend([TEMP, TEMP, len(program)+3])         # TEMP = 0
    program.extend([TEMP, C, len(program)+3])            # TEMP = -c
    program.extend([C_SQUARED, TEMP, len(program)+3])    # c² -= TEMP = c² - (-c) = c² + c
    
    # COUNTER--
    program.extend([COUNTER, ONE, len(program)+3])       # COUNTER -= 1
    
    # 跳回循环开始
    program.extend([ZERO, ZERO, loop1_start])
    
    loop1_end = len(program)
    
    # 第二步：计算 E = m × c²
    # 初始化 COUNTER = m
    program.extend([COUNTER, COUNTER, len(program)+3])   # COUNTER = 0
    program.extend([COUNTER, M, len(program)+3])         # COUNTER = -m
    program.extend([COUNTER, COUNTER, len(program)+3])   # COUNTER = 0
    program.extend([COUNTER, NEG_ONE, len(program)+3])   # COUNTER = m
    
    # 循环：while COUNTER > 0: E += c²; COUNTER--
    loop2_start = len(program)
    program.extend([COUNTER, ZERO, len(program)+15])     # 如果COUNTER<=0跳出
    
    # E += c²
    program.extend([TEMP, TEMP, len(program)+3])
    program.extend([TEMP, C_SQUARED, len(program)+3])
    program.extend([E, TEMP, len(program)+3])
    
    # COUNTER--
    program.extend([COUNTER, ONE, len(program)+3])
    
    # 跳回循环开始
    program.extend([ZERO, ZERO, loop2_start])
    
    # 停机
    program.extend([-1, -1, -1])
    
    # 数据区
    data = [
        0,    # 100: ZERO
        1,    # 101: ONE
        0,    # 102: TEMP
        2,    # 103: M (质量 = 2)
        3,    # 104: C (光速 = 3)
        0,    # 105: C_SQUARED (结果)
        0,    # 106: E (能量，最终结果)
        0,    # 107: COUNTER
        -1,   # 108: NEG_ONE
    ]
    
    return program, data, E

def simplified_emc2():
    """
    简化版本：直接展示概念
    计算 E = 2 × 3² = 2 × 9 = 18
    """
    print("=" * 80)
    print("使用SUBLEQ计算 E = mc²")
    print("=" * 80)
    
    print("\n爱因斯坦质能方程：E = mc²")
    print("  E = 能量 (Energy)")
    print("  m = 质量 (Mass)")
    print("  c = 光速 (Speed of Light)")
    
    print("\n简化计算（演示用）：")
    print("  m = 2 kg")
    print("  c = 3 (简化值，实际是 3×10⁸ m/s)")
    print("  E = 2 × 3² = 2 × 9 = 18")
    
    print("\n" + "=" * 80)
    print("SUBLEQ程序执行")
    print("=" * 80)
    
    machine = SUBLEQMachine(memory_size=256)
    program, data, result_addr = create_emc2_program()
    machine.load_program(program, data)
    
    print(f"\n程序长度: {len(program)} 条SUBLEQ指令")
    print(f"数据区起始: 地址 {len(program)}")
    print(f"结果地址: {result_addr}")
    
    print("\n开始执行...")
    memory = machine.run(max_steps=10000, verbose=False)
    
    print(f"\n执行完成！")
    print(f"总步数: {machine.steps}")
    print(f"\n结果:")
    print(f"  c² = {memory[105]}")
    print(f"  E = mc² = {memory[result_addr]}")
    
    print("\n" + "=" * 80)
    print("验证：")
    print(f"  m = {memory[103]}")
    print(f"  c = {memory[104]}")
    print(f"  c² = {memory[104]}² = {memory[104]**2}")
    print(f"  E = {memory[103]} × {memory[104]**2} = {memory[103] * memory[104]**2}")
    print(f"  SUBLEQ计算结果: E = {memory[result_addr]}")
    print(f"  {'✓ 正确！' if memory[result_addr] == memory[103] * memory[104]**2 else '✗ 错误'}")
    
    print("\n" + "=" * 80)
    print("哲学意义：")
    print("  • 爱因斯坦用3个符号表达宇宙真理：E = mc²")
    print("  • SUBLEQ用1条指令实现所有计算")
    print("  • 两者都是'极简之美'的完美体现")
    print("  • 证明：最深刻的真理往往最简单")
    print("=" * 80)

def show_subleq_basics():
    """展示SUBLEQ基础操作"""
    print("\n" + "=" * 80)
    print("SUBLEQ指令详解")
    print("=" * 80)
    
    print("\n唯一指令：SUBLEQ a, b, c")
    print("  1. Mem[b] = Mem[b] - Mem[a]  (减法)")
    print("  2. if (Mem[b] <= 0) then PC = c  (条件跳转)")
    print("  3. else PC = PC + 3")
    
    print("\n如何实现加法 (a + b)：")
    print("  1. 准备 -b 在内存中")
    print("  2. SUBLEQ neg_b, result, next")
    print("  3. result = result - (-b) = result + b")
    
    print("\n如何实现乘法 (a × b)：")
    print("  1. result = 0")
    print("  2. for i in range(b):")
    print("  3.     result += a  (用上面的加法)")
    
    print("\n如何实现平方 (c²)：")
    print("  1. 就是 c × c")
    print("  2. 用乘法实现")
    
    print("\n因此 E = mc² 可以分解为：")
    print("  1. temp = c × c  (计算c²)")
    print("  2. E = m × temp  (计算m×c²)")
    print("=" * 80)

if __name__ == "__main__":
    show_subleq_basics()
    print("\n")
    simplified_emc2()
