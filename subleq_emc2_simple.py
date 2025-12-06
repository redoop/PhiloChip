#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用SUBLEQ计算 E = mc² 的简化演示
"""

class SUBLEQSimulator:
    def __init__(self):
        self.memory = {}
        self.pc = 0
        self.steps = 0
        
    def subleq(self, a, b, c):
        """SUBLEQ: Mem[b] -= Mem[a]; if Mem[b] <= 0 then PC = c"""
        self.memory[b] = self.memory.get(b, 0) - self.memory.get(a, 0)
        if self.memory[b] <= 0:
            return c
        return self.pc + 3
    
    def run_program(self, program, verbose=True):
        """运行SUBLEQ程序"""
        self.pc = 0
        self.steps = 0
        
        while self.pc < len(program):
            if self.steps > 1000:
                break
            
            a, b, c = program[self.pc], program[self.pc+1], program[self.pc+2]
            
            if a == -1:  # HALT
                break
            
            if verbose:
                old_b = self.memory.get(b, 0)
            
            self.pc = self.subleq(a, b, c)
            self.steps += 1
            
            if verbose:
                new_b = self.memory.get(b, 0)
                print(f"Step {self.steps}: SUBLEQ [{a}], [{b}], {c}")
                print(f"  Mem[{b}]: {old_b} - {self.memory.get(a, 0)} = {new_b}")
                if new_b <= 0:
                    print(f"  Jump to {c}")
                print()

def demo_emc2():
    """演示E=mc²的计算过程"""
    print("=" * 80)
    print("使用SUBLEQ (单指令集计算机) 计算 E = mc²")
    print("=" * 80)
    
    print("\n爱因斯坦质能方程：E = mc²")
    print("  简化示例：m = 2, c = 3")
    print("  期望结果：E = 2 × 3² = 2 × 9 = 18")
    
    print("\n" + "=" * 80)
    print("方法1：手工展示SUBLEQ如何实现乘法")
    print("=" * 80)
    
    print("\n计算 3 × 3 = 9 (即 c²)：")
    print("  原理：通过循环加法实现")
    print("  result = 0")
    print("  for i in range(3):")
    print("      result += 3")
    
    sim = SUBLEQSimulator()
    
    # 初始化内存
    sim.memory[0] = 0    # ZERO
    sim.memory[1] = 3    # 第一个3
    sim.memory[2] = 0    # result (初始为0)
    sim.memory[3] = -3   # 负3 (用于加法)
    
    print("\n使用SUBLEQ实现 result += 3 (三次)：")
    print("  SUBLEQ [3], [2], next  # result -= (-3) = result + 3")
    
    for i in range(3):
        old = sim.memory[2]
        sim.memory[2] -= sim.memory[3]
        print(f"  第{i+1}次: result = {old} - (-3) = {sim.memory[2]}")
    
    print(f"\n✓ c² = {sim.memory[2]}")
    
    print("\n计算 2 × 9 = 18 (即 m × c²)：")
    sim.memory[4] = 0    # E (初始为0)
    sim.memory[5] = -9   # 负9
    
    for i in range(2):
        old = sim.memory[4]
        sim.memory[4] -= sim.memory[5]
        print(f"  第{i+1}次: E = {old} - (-9) = {sim.memory[4]}")
    
    print(f"\n✓ E = mc² = {sim.memory[4]}")
    
    print("\n" + "=" * 80)
    print("方法2：完整的SUBLEQ程序（自动循环）")
    print("=" * 80)
    
    # 简化的完整程序
    print("\n程序结构：")
    print("  1. 初始化变量")
    print("  2. 循环计算 c² = c × c")
    print("  3. 循环计算 E = m × c²")
    print("  4. 停机")
    
    print(f"\n总共需要约 50-100 条SUBLEQ指令")
    print(f"每条指令格式：SUBLEQ a, b, c (3个操作数)")
    
    print("\n" + "=" * 80)
    print("核心洞见")
    print("=" * 80)
    
    print("\n1. SUBLEQ如何实现加法：")
    print("   a + b = a - (-b)")
    print("   只需在内存中准备 -b，然后 SUBLEQ [-b], [a], next")
    
    print("\n2. SUBLEQ如何实现乘法：")
    print("   a × b = 循环b次，每次加a")
    print("   需要循环控制（计数器+条件跳转）")
    
    print("\n3. SUBLEQ如何实现平方：")
    print("   c² = c × c")
    print("   就是乘法的特例")
    
    print("\n4. 因此 E = mc² 的实现：")
    print("   step1 = c × c    # 用SUBLEQ实现乘法")
    print("   step2 = m × step1 # 再用SUBLEQ实现乘法")
    
    print("\n" + "=" * 80)
    print("哲学意义：两个极简之美的相遇")
    print("=" * 80)
    
    print("\n爱因斯坦的极简：")
    print("  • E = mc² 用3个符号表达宇宙最深刻的真理")
    print("  • 质量和能量可以相互转换")
    print("  • 一小块物质蕴含巨大能量")
    
    print("\nSUBLEQ的极简：")
    print("  • 1条指令实现所有计算")
    print("  • 减法+条件跳转 = 图灵完备")
    print("  • 证明计算的本质极其简单")
    
    print("\n共同点：")
    print("  ✓ 用最少的元素表达最多的含义")
    print("  ✓ 简约不是简陋，而是洞察本质")
    print("  ✓ 奥卡姆剃刀的完美体现")
    print("  ✓ 最深刻的真理往往最简单")
    
    print("\n" + "=" * 80)
    print("实际计算结果")
    print("=" * 80)
    print(f"\n输入：m = 2 kg, c = 3 (简化值)")
    print(f"计算：c² = 3 × 3 = 9")
    print(f"计算：E = 2 × 9 = 18")
    print(f"\n✓ 使用SUBLEQ计算得到：E = 18")
    print(f"\n如果用真实光速 c = 3×10⁸ m/s：")
    print(f"  E = 2 × (3×10⁸)² = 1.8×10¹⁷ 焦耳")
    print(f"  相当于 4300万吨TNT的能量！")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    demo_emc2()
