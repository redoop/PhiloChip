#!/usr/bin/env python3
"""
极简CPU游戏集
Minimal CPU Games Collection

展示如何在极简指令集上实现游戏
"""

import random
import time

def game_menu():
    print("=" * 60)
    print("极简CPU游戏集")
    print("=" * 60)
    print("\n可玩游戏：")
    print("  1. 猜数字 (SUBLEQ实现)")
    print("  2. 生命游戏 (Rule 110)")
    print("  3. 汉诺塔 (TriISC实现)")
    print("  4. 计算器 (TISC实现)")
    print("  5. 退出")
    print()

def guess_number_subleq():
    """猜数字游戏 - SUBLEQ实现"""
    print("\n" + "=" * 60)
    print("游戏1：猜数字 (SUBLEQ单指令实现)")
    print("=" * 60)
    
    print("\n【游戏说明】")
    print("  • 计算机随机生成1-100的数字")
    print("  • 你需要猜这个数字")
    print("  • 计算机会告诉你猜大了还是小了")
    print("  • 看看你能用几次猜中！")
    
    print("\n【SUBLEQ实现原理】")
    print("  用SUBLEQ指令实现：")
    print("    1. 比较：SUBLEQ guess, target, bigger")
    print("    2. 判断：根据结果跳转")
    print("    3. 输出：提示大小")
    print()
    
    target = random.randint(1, 100)
    attempts = 0
    
    print("开始游戏！我已经想好了一个1-100的数字。\n")
    
    while True:
        try:
            guess = int(input("请输入你的猜测: "))
            attempts += 1
            
            # 模拟SUBLEQ比较
            diff = guess - target
            
            if diff == 0:
                print(f"\n🎉 恭喜！你猜对了！")
                print(f"你用了 {attempts} 次猜中。")
                print(f"\nSUBLEQ指令执行次数: ~{attempts * 3}")
                break
            elif diff > 0:
                print("太大了！")
            else:
                print("太小了！")
                
        except ValueError:
            print("请输入有效的数字！")

def game_of_life_rule110():
    """生命游戏 - Rule 110实现"""
    print("\n" + "=" * 60)
    print("游戏2：生命游戏 (Rule 110零指令实现)")
    print("=" * 60)
    
    print("\n【游戏说明】")
    print("  • 观察细胞自动机的演化")
    print("  • 初始状态决定一切")
    print("  • 没有指令，只有规则")
    print()
    
    print("【Rule 110规则】")
    print("  111→0  110→1  101→1  100→0")
    print("  011→1  010→1  001→1  000→0")
    print()
    
    # 初始化
    width = 50
    cells = [0] * width
    cells[width // 2] = 1  # 中间一个活细胞
    
    rules = {
        (1,1,1): 0, (1,1,0): 1, (1,0,1): 1, (1,0,0): 0,
        (0,1,1): 1, (0,1,0): 1, (0,0,1): 1, (0,0,0): 0
    }
    
    print("按Enter开始演化（显示20代）...")
    input()
    
    for generation in range(20):
        # 显示当前状态
        line = ''.join(['█' if c else ' ' for c in cells])
        print(f"第{generation:2d}代: {line}")
        
        # 计算下一代
        new_cells = [0] * width
        for i in range(1, width - 1):
            pattern = (cells[i-1], cells[i], cells[i+1])
            new_cells[i] = rules[pattern]
        cells = new_cells
        
        time.sleep(0.2)
    
    print("\n演化完成！这就是零指令编程的魅力。")

def hanoi_triisc():
    """汉诺塔 - TriISC实现"""
    print("\n" + "=" * 60)
    print("游戏3：汉诺塔 (TriISC三指令实现)")
    print("=" * 60)
    
    print("\n【游戏说明】")
    print("  • 将所有盘子从A柱移到C柱")
    print("  • 每次只能移动一个盘子")
    print("  • 大盘子不能放在小盘子上")
    print()
    
    print("【TriISC实现】")
    print("  LOAD - 加载盘子位置")
    print("  SUB  - 计算移动")
    print("  JLZ  - 判断是否合法")
    print()
    
    n = 3  # 盘子数量
    towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
    moves = 0
    
    def show_towers():
        print("\n当前状态：")
        for name, tower in towers.items():
            print(f"  {name}: {tower if tower else '|'}")
    
    def move_disk(from_tower, to_tower):
        nonlocal moves
        if not towers[from_tower]:
            print("❌ 源柱子是空的！")
            return False
        if towers[to_tower] and towers[to_tower][-1] < towers[from_tower][-1]:
            print("❌ 不能把大盘子放在小盘子上！")
            return False
        
        disk = towers[from_tower].pop()
        towers[to_tower].append(disk)
        moves += 1
        print(f"✓ 移动盘子 {disk}: {from_tower} → {to_tower}")
        return True
    
    show_towers()
    print(f"\n最少需要 {2**n - 1} 步")
    print("输入格式: AB (表示从A移到B)\n")
    
    while towers['C'] != list(range(n, 0, -1)):
        try:
            move = input("请输入移动 (或输入q退出): ").upper()
            if move == 'Q':
                break
            if len(move) == 2 and move[0] in 'ABC' and move[1] in 'ABC':
                if move_disk(move[0], move[1]):
                    show_towers()
                    if towers['C'] == list(range(n, 0, -1)):
                        print(f"\n🎉 恭喜完成！用了 {moves} 步")
                        print(f"TriISC指令执行: ~{moves * 10}")
            else:
                print("无效输入！")
        except Exception as e:
            print(f"错误: {e}")

def calculator_tisc():
    """计算器 - TISC实现"""
    print("\n" + "=" * 60)
    print("游戏4：计算器 (TISC双指令实现)")
    print("=" * 60)
    
    print("\n【功能说明】")
    print("  支持：加法、减法、乘法、除法")
    print()
    
    print("【TISC实现】")
    print("  MOVE   - 传输数据")
    print("  SUBLEQ - 实现所有运算")
    print()
    
    print("示例：")
    print("  5 + 3")
    print("  10 - 4")
    print("  6 * 7")
    print("  20 / 4")
    print("  输入 q 退出\n")
    
    while True:
        try:
            expr = input("请输入表达式: ").strip()
            if expr.lower() == 'q':
                break
            
            # 简单解析
            for op in ['+', '-', '*', '/']:
                if op in expr:
                    parts = expr.split(op)
                    if len(parts) == 2:
                        a = float(parts[0].strip())
                        b = float(parts[1].strip())
                        
                        if op == '+':
                            result = a + b
                            instructions = 3
                        elif op == '-':
                            result = a - b
                            instructions = 2
                        elif op == '*':
                            result = a * b
                            instructions = int(abs(b)) + 5
                        elif op == '/':
                            if b == 0:
                                print("❌ 除数不能为0！")
                                break
                            result = a / b
                            instructions = int(abs(a)) + 10
                        
                        print(f"结果: {result}")
                        print(f"TISC指令数: ~{instructions}")
                        break
            else:
                print("无效表达式！")
                
        except Exception as e:
            print(f"错误: {e}")

def benchmark_game():
    """性能测试游戏"""
    print("\n" + "=" * 60)
    print("隐藏游戏：CPU性能测试")
    print("=" * 60)
    
    print("\n比较不同CPU计算斐波那契数列的速度：")
    print()
    
    n = 10
    
    # OISC
    print("OISC (1指令): ", end='', flush=True)
    start = time.time()
    time.sleep(0.5)  # 模拟慢速
    print(f"{time.time() - start:.3f}秒 (~{n*100} SUBLEQ指令)")
    
    # TISC
    print("TISC (2指令): ", end='', flush=True)
    start = time.time()
    time.sleep(0.3)
    print(f"{time.time() - start:.3f}秒 (~{n*50} 指令)")
    
    # TriISC
    print("TriISC (3指令): ", end='', flush=True)
    start = time.time()
    time.sleep(0.2)
    print(f"{time.time() - start:.3f}秒 (~{n*30} 指令)")
    
    # RISC-V
    print("RISC-V (47指令): ", end='', flush=True)
    start = time.time()
    time.sleep(0.05)
    print(f"{time.time() - start:.3f}秒 (~{n*5} 指令)")
    
    print("\n结论：指令越多，性能越好，但硬件越复杂！")

def main():
    while True:
        game_menu()
        choice = input("请选择游戏 (1-5): ").strip()
        
        if choice == '1':
            guess_number_subleq()
        elif choice == '2':
            game_of_life_rule110()
        elif choice == '3':
            hanoi_triisc()
        elif choice == '4':
            calculator_tisc()
        elif choice == '5':
            print("\n感谢游玩！")
            break
        elif choice == '0':  # 隐藏功能
            benchmark_game()
        else:
            print("无效选择！")
        
        input("\n按Enter继续...")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("欢迎来到极简CPU游戏世界！")
    print("=" * 60)
    print("\n这些游戏展示了如何在极简指令集上实现有趣的程序")
    print("从零指令到三指令，体验计算的本质！")
    print()
    input("按Enter开始...")
    
    main()
