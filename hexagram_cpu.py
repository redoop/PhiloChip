#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
64 卦象与 CPU 指令集的语义映射
基于卦象的象征意义与指令的功能特性建立内在关联
"""

class HexagramCPU:
    """
    将 64 卦映射到 64 条 RISC 指令
    映射原则：卦象的哲学含义 → 指令的计算行为
    """
    
    def __init__(self):
        # 卦象到指令的映射表
        # 格式: (卦名, 二进制, 指令, 关联逻辑)
        self.mappings = [
            # ========== 八纯卦：基础操作 (000000-111111 的特殊位置) ==========
            ("坤", "000000", "NOP", "地，静止不动，无操作"),
            ("乾", "111111", "HALT", "天，终极完满，停机"),
            
            # ========== 数据传输类：涉及"交换、流动" ==========
            ("既济", "101010", "LOAD", "水火相交，已完成，取数据"),
            ("未济", "010101", "STORE", "火水未交，未完成，存数据"),
            ("泰", "000111", "MOV", "天地交泰，数据流通"),
            ("否", "111000", "SWAP", "天地不交，需要交换"),
            ("临", "000011", "PUSH", "地上有泽，向下压入"),
            ("观", "110000", "POP", "风行地上，向上取出"),
            
            # ========== 算术运算：涉及"增减、变化" ==========
            ("益", "110001", "ADD", "风雷益，增加"),
            ("损", "100011", "SUB", "山泽损，减少"),
            ("丰", "101100", "MUL", "雷火丰，丰盛，倍增"),
            ("旅", "001101", "DIV", "火山旅，分散，除法"),
            ("渐", "110100", "INC", "风山渐，渐进增长"),
            ("归妹", "001011", "DEC", "雷泽归妹，递减"),
            
            # ========== 逻辑运算：涉及"判断、组合" ==========
            ("同人", "111101", "AND", "天火同人，求同，与运算"),
            ("大有", "101111", "OR", "火天大有，包容，或运算"),
            ("睽", "101001", "XOR", "火泽睽，相异，异或"),
            ("革", "101110", "NOT", "泽火革，变革，取反"),
            ("比", "000010", "NAND", "水地比，亲比，与非"),
            ("师", "010000", "NOR", "地水师，众，或非"),
            
            # ========== 移位运算：涉及"移动、转换" ==========
            ("晋", "101000", "SLL", "火地晋，上升，左移"),
            ("明夷", "000101", "SRL", "地火明夷，下降，右移"),
            ("升", "000110", "SLA", "地风升，上升，算术左移"),
            ("萃", "011000", "SRA", "泽地萃，聚集下沉，算术右移"),
            ("困", "011101", "ROL", "泽水困，困顿循环，循环左移"),
            ("井", "010110", "ROR", "水风井，井水循环，循环右移"),
            
            # ========== 比较运算：涉及"对比、判断" ==========
            ("讼", "010111", "CMP", "天水讼，争讼，比较"),
            ("需", "111010", "TEST", "水天需，等待，测试"),
            ("小畜", "111011", "BEQ", "风天小畜，小有积蓄，相等分支"),
            ("履", "110111", "BNE", "天泽履，践履，不等分支"),
            ("大畜", "100111", "BLT", "山天大畜，大有积蓄，小于分支"),
            ("遁", "111100", "BGT", "天山遁，退避，大于分支"),
            ("咸", "011100", "BLE", "泽山咸，感应，小于等于"),
            ("恒", "001110", "BGE", "雷风恒，恒久，大于等于"),
            
            # ========== 跳转控制：涉及"行动、决策" ==========
            ("大壮", "111001", "JMP", "雷天大壮，强力前进，无条件跳转"),
            ("夬", "011111", "CALL", "泽天夬，决断，调用函数"),
            ("姤", "111110", "RET", "天风姤，相遇后返回"),
            ("随", "011001", "JMPR", "泽雷随，跟随，相对跳转"),
            
            # ========== 系统控制：涉及"管理、协调" ==========
            ("谦", "000100", "INT", "地山谦，谦逊请求，中断"),
            ("豫", "001000", "IRET", "雷地豫，愉悦返回，中断返回"),
            ("剥", "100000", "SYSCALL", "山地剥，剥落求助，系统调用"),
            ("复", "000001", "SYSRET", "地雷复，复归，系统返回"),
            
            # ========== I/O 操作：涉及"内外交互" ==========
            ("中孚", "110011", "IN", "风泽中孚，内心诚信，输入"),
            ("小过", "001100", "OUT", "雷山小过，小有过越，输出"),
            ("家人", "101011", "INTR", "风火家人，家内交流，读寄存器"),
            ("睽", "010100", "OUTR", "火风鼎，鼎器外用，写寄存器"),
            
            # ========== 内存管理：涉及"空间、容纳" ==========
            ("坎", "010010", "ALLOC", "坎为水，水聚成坎，分配内存"),
            ("离", "101101", "FREE", "离为火，火散，释放内存"),
            ("艮", "100100", "FENCE", "艮为山，山止，内存屏障"),
            ("震", "001001", "SYNC", "震为雷，雷动同步"),
            
            # ========== 位操作：涉及"细节、精微" ==========
            ("巽", "110110", "BSET", "巽为风，风入，置位"),
            ("兑", "011011", "BCLR", "兑为泽，泽泄，清位"),
            ("蒙", "010001", "BTST", "山水蒙，蒙昧测试位"),
            ("涣", "110010", "BFLIP", "风水涣，涣散翻转位"),
            
            # ========== 特殊运算：涉及"转化、特殊状态" ==========
            ("颐", "100001", "ABS", "山雷颐，养正，取绝对值"),
            ("大过", "011110", "NEG", "泽风大过，过度，取负"),
            ("噬嗑", "101001", "SIGN", "火雷噬嗑，咬合，取符号"),
            ("贲", "100101", "ZERO", "山火贲，装饰归零"),
            
            # ========== 扩展指令：涉及"发展、扩充" ==========
            ("无妄", "111001", "EXT", "天雷无妄，无妄扩展"),
            ("大壮", "001111", "TRUNC", "雷天大壮，截断"),
            ("鼎", "101110", "CAST", "火风鼎，鼎新，类型转换"),
            ("蛊", "100110", "PACK", "山风蛊，整治打包"),
            ("解", "001010", "UNPACK", "雷水解，解开"),
            
            # ========== 调试/保留：涉及"观察、预留" ==========
            ("大过", "011110", "BREAK", "泽风大过，过度中断"),
            ("小过", "001100", "TRACE", "雷山小过，小过追踪"),
            ("节", "010011", "WATCH", "水泽节，节制观察"),
            ("屯", "010001", "RESERVED", "水雷屯，屯积保留"),
        ]
        
        # 构建双向索引
        self.hex_to_inst = {}  # 二进制 -> (卦名, 指令, 含义)
        self.inst_to_hex = {}  # 指令 -> (卦名, 二进制, 含义)
        
        for gua, binary, inst, meaning in self.mappings:
            self.hex_to_inst[binary] = (gua, inst, meaning)
            self.inst_to_hex[inst] = (gua, binary, meaning)
    
    def hexagram_to_instruction(self, binary_6bit):
        """卦象 -> 指令"""
        if binary_6bit in self.hex_to_inst:
            gua, inst, meaning = self.hex_to_inst[binary_6bit]
            return {
                "hexagram": gua,
                "binary": binary_6bit,
                "instruction": inst,
                "meaning": meaning,
                "opcode": int(binary_6bit, 2)
            }
        return None
    
    def instruction_to_hexagram(self, instruction):
        """指令 -> 卦象"""
        if instruction in self.inst_to_hex:
            gua, binary, meaning = self.inst_to_hex[instruction]
            return {
                "instruction": instruction,
                "hexagram": gua,
                "binary": binary,
                "meaning": meaning,
                "opcode": int(binary, 2)
            }
        return None
    
    def print_instruction_set(self):
        """打印完整指令集"""
        categories = {
            "基础控制": ["NOP", "HALT"],
            "数据传输": ["LOAD", "STORE", "MOV", "SWAP", "PUSH", "POP"],
            "算术运算": ["ADD", "SUB", "MUL", "DIV", "INC", "DEC"],
            "逻辑运算": ["AND", "OR", "XOR", "NOT", "NAND", "NOR"],
            "移位运算": ["SLL", "SRL", "SLA", "SRA", "ROL", "ROR"],
            "比较运算": ["CMP", "TEST", "BEQ", "BNE", "BLT", "BGT", "BLE", "BGE"],
            "跳转控制": ["JMP", "CALL", "RET", "JMPR"],
            "系统控制": ["INT", "IRET", "SYSCALL", "SYSRET"],
            "I/O操作": ["IN", "OUT", "INTR", "OUTR"],
            "内存管理": ["ALLOC", "FREE", "FENCE", "SYNC"],
            "位操作": ["BSET", "BCLR", "BTST", "BFLIP"],
            "特殊运算": ["ABS", "NEG", "SIGN", "ZERO"],
            "扩展指令": ["EXT", "TRUNC", "CAST", "PACK", "UNPACK"],
            "调试保留": ["BREAK", "TRACE", "WATCH", "RESERVED"]
        }
        
        print("=" * 80)
        print("64 卦象 CPU 指令集")
        print("=" * 80)
        
        for category, instructions in categories.items():
            print(f"\n【{category}】")
            for inst in instructions:
                info = self.instruction_to_hexagram(inst)
                if info:
                    print(f"  {info['binary']} | {info['hexagram']:4s} | "
                          f"{info['instruction']:8s} | {info['meaning']}")
        
        print(f"\n总计: {len(self.mappings)} 条指令")
        print("=" * 80)


def demonstrate():
    """演示系统"""
    cpu = HexagramCPU()
    
    # 打印完整指令集
    cpu.print_instruction_set()
    
    # 示例：从卦象查指令
    print("\n\n示例 1: 从卦象查指令")
    print("-" * 40)
    result = cpu.hexagram_to_instruction("110001")
    if result:
        print(f"卦象: {result['hexagram']} ({result['binary']})")
        print(f"指令: {result['instruction']}")
        print(f"含义: {result['meaning']}")
        print(f"操作码: {result['opcode']}")
    
    # 示例：从指令查卦象
    print("\n\n示例 2: 从指令查卦象")
    print("-" * 40)
    result = cpu.instruction_to_hexagram("ADD")
    if result:
        print(f"指令: {result['instruction']}")
        print(f"卦象: {result['hexagram']} ({result['binary']})")
        print(f"含义: {result['meaning']}")
    
    # 示例：模拟指令执行
    print("\n\n示例 3: 模拟程序执行")
    print("-" * 40)
    program = ["LOAD", "ADD", "STORE", "HALT"]
    print("程序:")
    for inst in program:
        info = cpu.instruction_to_hexagram(inst)
        if info:
            print(f"  {info['hexagram']:4s} ({info['binary']}) -> {inst}")


if __name__ == "__main__":
    demonstrate()
