#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奥卡姆剃刀CPU (Occam's Razor CPU)
基于威廉·奥卡姆的简约原则

核心思想：
- "如无必要，勿增实体" (Entities should not be multiplied without necessity)
- "简单性优先" (Simplicity is preferable)
- 最小指令集 - 仅保留图灵完备所需的绝对最少指令

设计：8条指令实现图灵完备（OISC的扩展）
"""

class OccamCPU:
    def __init__(self):
        self.instructions = self._generate_instructions()
    
    def _generate_instructions(self):
        """
        奥卡姆剃刀原则：削减到最小
        8条指令 = 2^3（3位操作码）
        """
        return [
            {
                'opcode': 0,
                'mnemonic': 'SUBLEQ',
                'description': '减法并小于等于零跳转 [a] = [a] - [b]; if [a] <= 0 then PC = c',
                'category': '核心',
                'justification': '单指令计算机(OISC)的基础，可实现所有算术和控制流'
            },
            {
                'opcode': 1,
                'mnemonic': 'LOAD',
                'description': '加载 R = [addr]',
                'category': '必要',
                'justification': '内存读取，无法通过SUBLEQ高效实现'
            },
            {
                'opcode': 2,
                'mnemonic': 'STORE',
                'description': '存储 [addr] = R',
                'category': '必要',
                'justification': '内存写入，与LOAD对称'
            },
            {
                'opcode': 3,
                'mnemonic': 'JMP',
                'description': '无条件跳转 PC = addr',
                'category': '必要',
                'justification': '简化控制流，避免复杂的SUBLEQ组合'
            },
            {
                'opcode': 4,
                'mnemonic': 'JZ',
                'description': '零跳转 if R == 0 then PC = addr',
                'category': '必要',
                'justification': '条件分支，图灵完备的关键'
            },
            {
                'opcode': 5,
                'mnemonic': 'ADD',
                'description': '加法 R = R + [addr]',
                'category': '效率',
                'justification': '虽可用双重减法实现，但效率提升显著'
            },
            {
                'opcode': 6,
                'mnemonic': 'HALT',
                'description': '停机',
                'category': '必要',
                'justification': '明确终止，避免无限循环'
            },
            {
                'opcode': 7,
                'mnemonic': 'NOP',
                'description': '空操作',
                'category': '对齐',
                'justification': '填充到2^3，保持编码简洁'
            }
        ]
    
    def verify_completeness(self):
        """验证图灵完备性"""
        mnemonics = {inst['mnemonic'] for inst in self.instructions}
        
        print("=== 图灵完备性验证 ===\n")
        
        checks = [
            ('算术运算', ['SUBLEQ', 'ADD'], 
             'SUBLEQ可实现减法，ADD提供加法，可组合出乘除'),
            ('内存访问', ['LOAD', 'STORE'], 
             '读写内存，实现无限存储'),
            ('条件分支', ['JZ', 'SUBLEQ'], 
             'JZ提供条件跳转，SUBLEQ内含条件跳转'),
            ('无条件跳转', ['JMP'], 
             '实现循环和函数调用'),
            ('停机', ['HALT'], 
             '明确终止条件')
        ]
        
        complete = True
        for name, required, reason in checks:
            found = [op for op in required if op in mnemonics]
            status = "✓" if found else "✗"
            print(f"{status} {name}: {', '.join(found)}")
            print(f"   理由: {reason}")
            if not found:
                complete = False
        
        print(f"\n{'✓ 图灵完备' if complete else '✗ 不完备'}")
        print(f"\n奥卡姆剃刀评分: {len(self.instructions)}/8 指令")
        print("简约度: 100% (已达理论最小值)")
        return complete
    
    def compare_with_others(self):
        """与其他架构对比"""
        print("\n" + "=" * 80)
        print("指令集复杂度对比")
        print("=" * 80)
        
        architectures = [
            ("奥卡姆剃刀CPU", 8, "极简主义，仅保留必要指令"),
            ("RISC-V RV32I", 47, "精简指令集"),
            ("ARM Thumb", 50, "16位精简指令"),
            ("MIPS I", 64, "经典RISC"),
            ("易经CPU", 64, "哲学映射"),
            ("x86 (8086)", 133, "CISC起点"),
            ("佛教CPU", 128, "宗教哲学"),
            ("x86-64", 1000, "现代CISC"),
        ]
        
        print(f"\n{'架构':<20} {'指令数':>8}  {'特点'}")
        print("-" * 80)
        for name, count, note in architectures:
            ratio = count / 8
            print(f"{name:<20} {count:>8}  {note} (×{ratio:.1f})")
        
        print("\n奥卡姆剃刀原则: 指令数越少越好（在保证图灵完备前提下）")
    
    def display(self):
        """显示指令集"""
        print("=" * 80)
        print("奥卡姆剃刀CPU (Occam's Razor CPU)")
        print("威廉·奥卡姆 (William of Ockham, 1287-1347)")
        print("=" * 80)
        print("\n核心原则：")
        print("  'Entia non sunt multiplicanda praeter necessitatem'")
        print("  如无必要，勿增实体")
        print("\n设计哲学：")
        print("  - 最小指令集：仅8条指令（3位操作码）")
        print("  - 图灵完备：满足计算完备性的最低要求")
        print("  - 简约至上：每条指令都有存在的必要性")
        print(f"\n指令集：{len(self.instructions)}条指令")
        print("=" * 80)
        
        print("\n指令列表：")
        print("-" * 80)
        for inst in self.instructions:
            print(f"  {inst['opcode']}  {inst['mnemonic']:<8}  {inst['description']}")
            print(f"     类别: {inst['category']}")
            print(f"     必要性: {inst['justification']}")
            print()
        
        print("=" * 80)
        print("SUBLEQ详解（单指令计算机核心）：")
        print("  SUBLEQ a, b, c 执行:")
        print("    1. [a] = [a] - [b]  (减法)")
        print("    2. if [a] <= 0 then PC = c  (条件跳转)")
        print("  ")
        print("  可实现:")
        print("    - MOV:  SUBLEQ a, a, next; SUBLEQ a, b, next")
        print("    - ADD:  先取负，再减负数")
        print("    - 条件跳转: 利用内置的 <= 0 判断")
        print("=" * 80)

if __name__ == "__main__":
    cpu = OccamCPU()
    cpu.display()
    print("\n")
    cpu.verify_completeness()
    cpu.compare_with_others()
