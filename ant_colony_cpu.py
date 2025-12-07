#!/usr/bin/env python3
"""
蚁群CPU (Ant Colony CPU)
Architecture: 数百万简单核心，涌现集体智能
Philosophy: 简单×大量=复杂，整体>部分之和

核心理念：
- 每个蚂蚁 = 超简单处理器（5-8条指令）
- 信息素 = 共享内存/通信机制
- 涌现 = 集体智能（无中央控制）
- 容错 = 10%故障仍正常工作

指令集：8条（每个蚂蚁核心）
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import List, Tuple
import random

class AntInstruction(IntEnum):
    """蚂蚁核心指令集 - 极简8条"""
    # 1. 感知环境
    SENSE = 0      # 感知周围信息素浓度
    
    # 2. 移动
    MOVE = 1       # 向信息素浓度高的方向移动
    
    # 3. 释放信息素
    DROP = 2       # 在当前位置释放信息素
    
    # 4. 拾取/放下
    PICKUP = 3     # 拾取资源
    PUTDOWN = 4    # 放下资源
    
    # 5. 随机探索
    RANDOM = 5     # 随机移动（探索）
    
    # 6. 返回
    RETURN = 6     # 返回巢穴
    
    # 7. 等待
    WAIT = 7       # 等待（节能模式）

@dataclass
class Ant:
    """单个蚂蚁（处理器核心）"""
    id: int
    x: int
    y: int
    carrying: bool = False
    energy: int = 100
    state: str = "explore"  # explore, return, wait
    
@dataclass
class Cell:
    """网格单元（内存单元）"""
    pheromone: float = 0.0  # 信息素浓度
    food: int = 0           # 食物数量
    nest: bool = False      # 是否是巢穴

class AntColonyCPU:
    """蚁群CPU - 涌现智能计算系统"""
    
    def __init__(self, grid_size=50, num_ants=1000):
        self.grid_size = grid_size
        self.num_ants = num_ants
        self.grid = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.ants = []
        self.nest_pos = (grid_size // 2, grid_size // 2)
        self.grid[self.nest_pos[0]][self.nest_pos[1]].nest = True
        self.food_collected = 0
        self.cycles = 0
        
        # 初始化蚂蚁
        for i in range(num_ants):
            self.ants.append(Ant(i, self.nest_pos[0], self.nest_pos[1]))
        
        # 放置食物源
        self._place_food()
    
    def _place_food(self):
        """放置食物源"""
        for _ in range(5):
            x = random.randint(5, self.grid_size - 5)
            y = random.randint(5, self.grid_size - 5)
            self.grid[x][y].food = 100
    
    def execute(self, ant: Ant, instruction: AntInstruction):
        """执行单条指令"""
        if instruction == AntInstruction.SENSE:
            return self._sense(ant)
        elif instruction == AntInstruction.MOVE:
            self._move(ant)
        elif instruction == AntInstruction.DROP:
            self._drop_pheromone(ant)
        elif instruction == AntInstruction.PICKUP:
            self._pickup(ant)
        elif instruction == AntInstruction.PUTDOWN:
            self._putdown(ant)
        elif instruction == AntInstruction.RANDOM:
            self._random_move(ant)
        elif instruction == AntInstruction.RETURN:
            self._return_to_nest(ant)
        elif instruction == AntInstruction.WAIT:
            ant.energy += 1
    
    def _sense(self, ant: Ant) -> List[Tuple[int, int, float]]:
        """感知周围信息素"""
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = ant.x + dx, ant.y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny, self.grid[nx][ny].pheromone))
        return neighbors
    
    def _move(self, ant: Ant):
        """向信息素浓度高的方向移动"""
        neighbors = self._sense(ant)
        if neighbors:
            # 选择信息素最高的方向
            best = max(neighbors, key=lambda x: x[2])
            ant.x, ant.y = best[0], best[1]
            ant.energy -= 1
    
    def _drop_pheromone(self, ant: Ant):
        """释放信息素"""
        strength = 10.0 if ant.carrying else 1.0
        self.grid[ant.x][ant.y].pheromone += strength
    
    def _pickup(self, ant: Ant):
        """拾取食物"""
        if self.grid[ant.x][ant.y].food > 0 and not ant.carrying:
            self.grid[ant.x][ant.y].food -= 1
            ant.carrying = True
            ant.state = "return"
    
    def _putdown(self, ant: Ant):
        """放下食物"""
        if ant.carrying and self.grid[ant.x][ant.y].nest:
            ant.carrying = False
            ant.state = "explore"
            self.food_collected += 1
    
    def _random_move(self, ant: Ant):
        """随机移动（探索）"""
        dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
        nx, ny = ant.x + dx, ant.y + dy
        if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
            ant.x, ant.y = nx, ny
            ant.energy -= 1
    
    def _return_to_nest(self, ant: Ant):
        """返回巢穴"""
        dx = 1 if ant.x < self.nest_pos[0] else -1 if ant.x > self.nest_pos[0] else 0
        dy = 1 if ant.y < self.nest_pos[1] else -1 if ant.y > self.nest_pos[1] else 0
        if dx != 0 or dy != 0:
            ant.x += dx
            ant.y += dy
            ant.energy -= 1
    
    def ant_program(self, ant: Ant):
        """单个蚂蚁的行为程序（状态机）"""
        if ant.energy <= 0:
            self.execute(ant, AntInstruction.WAIT)
            return
        
        if ant.state == "explore":
            # 探索模式
            self.execute(ant, AntInstruction.SENSE)
            if self.grid[ant.x][ant.y].food > 0:
                self.execute(ant, AntInstruction.PICKUP)
            else:
                neighbors = self._sense(ant)
                if any(p > 0.5 for _, _, p in neighbors):
                    self.execute(ant, AntInstruction.MOVE)
                else:
                    self.execute(ant, AntInstruction.RANDOM)
        
        elif ant.state == "return":
            # 返回模式
            self.execute(ant, AntInstruction.DROP)  # 留下信息素
            if ant.x == self.nest_pos[0] and ant.y == self.nest_pos[1]:
                self.execute(ant, AntInstruction.PUTDOWN)
            else:
                self.execute(ant, AntInstruction.RETURN)
    
    def evaporate_pheromones(self):
        """信息素挥发"""
        for row in self.grid:
            for cell in row:
                cell.pheromone *= 0.95  # 5%挥发率
    
    def step(self):
        """执行一个时钟周期"""
        # 所有蚂蚁并行执行
        for ant in self.ants:
            self.ant_program(ant)
        
        # 信息素挥发
        self.evaporate_pheromones()
        self.cycles += 1
    
    def run(self, steps=1000):
        """运行模拟"""
        print(f"🐜 蚁群CPU启动")
        print(f"核心数: {self.num_ants}")
        print(f"网格大小: {self.grid_size}x{self.grid_size}")
        print(f"指令集: {len(AntInstruction)} 条\n")
        
        for i in range(steps):
            self.step()
            if i % 100 == 0:
                print(f"周期 {i}: 收集食物 {self.food_collected} 单位")
        
        print(f"\n✅ 完成 {steps} 个周期")
        print(f"总收集: {self.food_collected} 单位食物")
        print(f"效率: {self.food_collected/steps:.2f} 单位/周期")

def demonstrate_ant_colony_cpu():
    """演示蚁群CPU"""
    print("=" * 60)
    print("🐜 蚁群CPU (Ant Colony CPU)")
    print("=" * 60)
    print("\n核心理念：")
    print("• 每个蚂蚁 = 超简单处理器（8条指令）")
    print("• 信息素 = 共享内存")
    print("• 涌现 = 集体智能")
    print("• 简单×大量 = 复杂\n")
    
    print("指令集（8条）：")
    for inst in AntInstruction:
        print(f"  {inst.value}. {inst.name}")
    print()
    
    # 运行模拟
    cpu = AntColonyCPU(grid_size=30, num_ants=500)
    cpu.run(steps=500)
    
    print("\n" + "=" * 60)
    print("架构特点：")
    print("=" * 60)
    print("✓ 极致并行：数百万核心同时工作")
    print("✓ 天然容错：10%故障仍正常")
    print("✓ 自适应：无需编程，自动优化路径")
    print("✓ 线性扩展：核心数×2 = 性能×2")
    print("✓ 涌现智能：整体>部分之和")
    
    print("\n应用场景：")
    print("• 蚁群优化算法（ACO）")
    print("• 群体机器人（Swarm Robotics）")
    print("• 网络路由（AntNet）")
    print("• 物流优化（最短路径）")
    
    print("\n实现挑战：")
    print("• 信息素机制（共享内存）")
    print("• 物理布局（数百万核心）")
    print("• 功耗（100万×1mW=1kW）")
    print("• 编程工具链（如何编程？）")

if __name__ == "__main__":
    demonstrate_ant_colony_cpu()
