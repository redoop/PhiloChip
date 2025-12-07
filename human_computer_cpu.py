#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Human Computer CPU - 人体计算机CPU架构
致敬历史上的人肉计算机（1880s-1950s）

核心理念：
1. 人类是图灵完备的计算设备
2. 通过组织和协调，人类可以执行任何算法
3. "Computer"原本就是指做计算的人，不是机器

历史案例：
- 哈佛天文台计算员（1880s-1920s）：女性分类30万颗恒星
- 曼哈顿计划（1943-1945）：费曼组织数百人计算原子弹模拟
- 弹道计算（1940s）：80名女性计算炮弹弹道表
- ENIAC之前：所有复杂计算都由人完成

设计目标：
- 可实际执行（教学、艺术）
- 可视化算法过程
- 理解并行计算本质
- 致敬计算历史
"""

from enum import Enum
from typing import List, Tuple
from dataclasses import dataclass

class HumanInstruction(Enum):
    """人体计算机指令集 (32条指令)"""
    
    # === 1. 基础指令 (8条) ===
    SHOW = "举牌显示数值"
    HIDE = "放下牌子"
    LOOK_LEFT = "看左边邻居的牌"
    LOOK_RIGHT = "看右边邻居的牌"
    LOOK_UP = "看上方邻居的牌"
    LOOK_DOWN = "看下方邻居的牌"
    REMEMBER = "记住当前值"
    FORGET = "清除记忆"
    
    # === 2. 算术指令 (8条) ===
    ADD = "加法（用手指或计算器）"
    SUB = "减法"
    MUL = "乘法"
    DIV = "除法"
    INC = "加1"
    DEC = "减1"
    NEGATE = "取负"
    ABS = "取绝对值"
    
    # === 3. 逻辑指令 (4条) ===
    AND = "逻辑与（两个邻居都是1才是1）"
    OR = "逻辑或"
    NOT = "逻辑非（翻转牌子）"
    XOR = "异或"
    
    # === 4. 比较指令 (4条) ===
    EQUAL = "相等判断"
    GREATER = "大于判断"
    LESS = "小于判断"
    COMPARE = "比较并举牌显示结果"
    
    # === 5. 移动指令 (4条) ===
    PASS_LEFT = "把牌传给左边"
    PASS_RIGHT = "把牌传给右边"
    SWAP = "与邻居交换位置"
    ROTATE = "旋转队列"
    
    # === 6. 控制指令 (4条) ===
    WAIT = "等待信号"
    SIGNAL = "发出信号（举手/喊叫）"
    IF_ZERO = "如果是0则执行"
    REPEAT = "重复N次"

@dataclass
class HumanProcessor:
    """人类处理器（一个人）"""
    id: int
    name: str
    current_value: int = 0
    memory: int = 0
    card_color: str = "white"  # 举的牌子颜色
    position: Tuple[int, int] = (0, 0)  # 在阵列中的位置
    
    def execute(self, instruction: HumanInstruction, *args):
        """执行指令"""
        if instruction == HumanInstruction.SHOW:
            return f"{self.name} 举牌显示: {self.current_value}"
        elif instruction == HumanInstruction.ADD:
            self.current_value += args[0]
            return f"{self.name} 计算: {self.current_value}"
        elif instruction == HumanInstruction.INC:
            self.current_value += 1
            return f"{self.name} +1 = {self.current_value}"
        # ... 其他指令实现
        
    def look_at_neighbor(self, neighbor):
        """看邻居的牌子"""
        return neighbor.current_value
    
    def show_card(self):
        """举牌"""
        if self.current_value == 0:
            self.card_color = "white"
        else:
            self.card_color = "black"
        return self.card_color

class HumanComputerArray:
    """人体计算机阵列"""
    
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = []
        
        # 创建人类处理器阵列
        person_id = 0
        for i in range(rows):
            row = []
            for j in range(cols):
                person = HumanProcessor(
                    id=person_id,
                    name=f"Person_{i}_{j}",
                    position=(i, j)
                )
                row.append(person)
                person_id += 1
            self.grid.append(row)
    
    def get_neighbors(self, i: int, j: int):
        """获取邻居"""
        neighbors = {}
        if i > 0:
            neighbors['up'] = self.grid[i-1][j]
        if i < self.rows - 1:
            neighbors['down'] = self.grid[i+1][j]
        if j > 0:
            neighbors['left'] = self.grid[i][j-1]
        if j < self.cols - 1:
            neighbors['right'] = self.grid[i][j+1]
        return neighbors
    
    def broadcast(self, instruction: HumanInstruction):
        """广播指令给所有人"""
        print(f"\n📢 指挥官: 所有人执行 {instruction.value}")
        results = []
        for i in range(self.rows):
            for j in range(self.cols):
                person = self.grid[i][j]
                result = person.execute(instruction)
                results.append(result)
        return results

class HistoricalScenarios:
    """历史场景重现"""
    
    @staticmethod
    def manhattan_project_simulation():
        """曼哈顿计划：费曼的流水线计算"""
        print("=" * 70)
        print("🔬 曼哈顿计划场景（1943-1945）")
        print("任务：计算原子弹爆炸的微分方程")
        print("=" * 70)
        
        # 10个人排成流水线
        pipeline = [HumanProcessor(i, f"计算员_{i}") for i in range(10)]
        
        print("\n费曼的流水线设计：")
        print("每个人负责方程的一个步骤")
        
        # 输入数据
        input_data = 100
        print(f"\n输入: {input_data}")
        
        # 流水线处理
        current = input_data
        for i, person in enumerate(pipeline):
            # 每个人做一个简单操作
            if i % 3 == 0:
                person.current_value = current * 2
                print(f"  {person.name}: {current} × 2 = {person.current_value}")
            elif i % 3 == 1:
                person.current_value = current + 10
                print(f"  {person.name}: {current} + 10 = {person.current_value}")
            else:
                person.current_value = current - 5
                print(f"  {person.name}: {current} - 5 = {person.current_value}")
            
            current = person.current_value
        
        print(f"\n最终结果: {current}")
        print("✓ 计算完成！传递给物理学家...")
    
    @staticmethod
    def harvard_computers_simulation():
        """哈佛天文台：恒星分类"""
        print("\n" + "=" * 70)
        print("🌟 哈佛天文台场景（1880s-1920s）")
        print("任务：分类恒星光谱")
        print("=" * 70)
        
        # 5名女性计算员
        computers = [
            HumanProcessor(0, "安妮·坎农"),
            HumanProcessor(1, "亨丽埃塔·勒维特"),
            HumanProcessor(2, "威廉敏娜·弗莱明"),
            HumanProcessor(3, "安东尼娅·莫里"),
            HumanProcessor(4, "塞西莉亚·佩恩")
        ]
        
        # 模拟分类恒星
        star_types = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
        
        print("\n并行处理照相底片：")
        for i, person in enumerate(computers):
            star_type = star_types[i % len(star_types)]
            print(f"  {person.name}: 分析底片 #{i+1} → 恒星类型 {star_type}")
        
        print("\n✓ 今日完成5颗恒星分类")
        print("📊 安妮·坎农一生分类了30万颗恒星！")

class ModernApplications:
    """现代应用"""
    
    @staticmethod
    def sorting_algorithm_demo():
        """排序算法可视化"""
        print("\n" + "=" * 70)
        print("🎓 教学演示：冒泡排序")
        print("=" * 70)
        
        # 8个人，每人举着数字牌
        people = [
            HumanProcessor(0, "Alice", current_value=5),
            HumanProcessor(1, "Bob", current_value=2),
            HumanProcessor(2, "Carol", current_value=8),
            HumanProcessor(3, "Dave", current_value=1),
            HumanProcessor(4, "Eve", current_value=9),
            HumanProcessor(5, "Frank", current_value=3),
            HumanProcessor(6, "Grace", current_value=7),
            HumanProcessor(7, "Henry", current_value=4)
        ]
        
        print("\n初始状态:")
        print("  " + " ".join([f"{p.name}({p.current_value})" for p in people]))
        
        # 冒泡排序
        n = len(people)
        for i in range(n):
            for j in range(n - 1 - i):
                # 比较相邻两人
                if people[j].current_value > people[j+1].current_value:
                    # 交换位置
                    print(f"\n  {people[j].name}({people[j].current_value}) 和 "
                          f"{people[j+1].name}({people[j+1].current_value}) 交换位置")
                    people[j], people[j+1] = people[j+1], people[j]
        
        print("\n排序后:")
        print("  " + " ".join([f"{p.name}({p.current_value})" for p in people]))
        print("\n✓ 排序完成！观众看到了算法的每一步")
    
    @staticmethod
    def game_of_life_demo():
        """生命游戏演示"""
        print("\n" + "=" * 70)
        print("🎨 艺术装置：康威生命游戏")
        print("=" * 70)
        
        # 5×5人阵列
        array = HumanComputerArray(5, 5)
        
        # 初始状态（滑翔机）
        glider = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        
        print("\n初始状态（滑翔机）:")
        for i in range(5):
            row = ""
            for j in range(5):
                if (i, j) in glider:
                    array.grid[i][j].current_value = 1
                    row += "⬛ "
                else:
                    array.grid[i][j].current_value = 0
                    row += "⬜ "
            print("  " + row)
        
        print("\n每个人的任务：")
        print("  1. 数周围8个邻居中有多少黑牌")
        print("  2. 根据规则决定下一轮举黑牌还是白牌")
        print("  3. 听到信号后，所有人同时翻牌")
        
        print("\n规则：")
        print("  - 活细胞：邻居2-3个 → 存活，否则死亡")
        print("  - 死细胞：邻居=3个 → 复活")
        
        print("\n✓ 观众看到图案在人群中'移动'！")

class PerformanceAnalysis:
    """性能分析"""
    
    @staticmethod
    def compare_with_electronic():
        """与电子计算机对比"""
        print("\n" + "=" * 70)
        print("📊 性能对比：人体 vs 电子计算机")
        print("=" * 70)
        
        comparison = {
            "计算速度": {
                "人体": "1-10 ops/秒",
                "电子": "10^9 ops/秒",
                "差距": "10^8倍"
            },
            "延迟": {
                "人体": "200-500 ms（人类反应时间）",
                "电子": "1 ns",
                "差距": "10^6倍"
            },
            "并行度": {
                "人体": "可以很高（数百人）",
                "电子": "数千核心",
                "差距": "相当"
            },
            "功耗": {
                "人体": "100W/人（2000大卡/天）",
                "电子": "100-500W（整机）",
                "差距": "人体更耗能"
            },
            "成本": {
                "人体": "工资（持续成本）",
                "电子": "一次性购买",
                "差距": "电子更便宜"
            },
            "可靠性": {
                "人体": "低（会累、出错、生病）",
                "电子": "高",
                "差距": "电子更可靠"
            },
            "灵活性": {
                "人体": "高（可以理解新任务）",
                "电子": "中（需要编程）",
                "差距": "人体更灵活"
            }
        }
        
        for metric, data in comparison.items():
            print(f"\n{metric}:")
            print(f"  人体: {data['人体']}")
            print(f"  电子: {data['电子']}")
            print(f"  差距: {data['差距']}")
        
        print("\n结论：")
        print("  ✓ 电子计算机在速度、成本、可靠性上完胜")
        print("  ✓ 但人体计算机有教育、艺术、历史价值")
        print("  ✓ 证明了计算的本质与物理实现无关")

def demonstrate_human_computer():
    """演示人体计算机"""
    print("=" * 70)
    print("👥 Human Computer CPU - 人体计算机架构")
    print("=" * 70)
    print()
    
    # 1. 历史场景
    print("【第一部分：历史重现】")
    HistoricalScenarios.manhattan_project_simulation()
    HistoricalScenarios.harvard_computers_simulation()
    
    # 2. 现代应用
    print("\n【第二部分：现代应用】")
    ModernApplications.sorting_algorithm_demo()
    ModernApplications.game_of_life_demo()
    
    # 3. 性能分析
    print("\n【第三部分：性能分析】")
    PerformanceAnalysis.compare_with_electronic()
    
    # 4. 指令集总结
    print("\n" + "=" * 70)
    print("【第四部分：指令集总结】")
    print("=" * 70)
    
    categories = {
        "基础指令": 8,
        "算术指令": 8,
        "逻辑指令": 4,
        "比较指令": 4,
        "移动指令": 4,
        "控制指令": 4
    }
    
    total = sum(categories.values())
    print(f"\n总指令数: {total}条")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}条")
    
    # 5. 核心洞察
    print("\n" + "=" * 70)
    print("【核心洞察】")
    print("=" * 70)
    
    insights = [
        "💡 'Computer'原本就是指做计算的人，不是机器",
        "📜 1880s-1950s，所有复杂计算都由人完成",
        "👩‍🔬 哈佛天文台的女性计算员分类了30万颗恒星",
        "⚛️ 曼哈顿计划：费曼组织数百人计算原子弹",
        "🎓 人体计算机证明：计算与物理实现无关",
        "🎨 今天仍有教育、艺术、理论价值",
        "🤝 人类是图灵完备的计算设备",
        "⚡ 电子计算机快10^8倍，但原理相同",
        "🌟 致敬那些被遗忘的女性计算员",
        "∞ 计算的本质是逻辑，不是硅片"
    ]
    
    for insight in insights:
        print(f"  {insight}")
    
    print("\n" + "=" * 70)
    print("Human Computer CPU: 致敬计算的人类起源")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_human_computer()
