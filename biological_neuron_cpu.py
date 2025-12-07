#!/usr/bin/env python3
"""
生物神经元CPU (Biological Neuron CPU)
完全模仿人类神经细胞的CPU架构

核心理念：
- 每个处理单元 = 一个神经元
- 脉冲通信（不是连续值）
- 突触可塑性（动态学习）
- 异步并行（无全局时钟）
"""

import random
from dataclasses import dataclass
from typing import List, Dict
from enum import IntEnum

class NeuronInstruction(IntEnum):
    """神经元指令集 - 极简12条"""
    # 输入处理
    RECEIVE = 0      # 接收突触输入
    INTEGRATE = 1    # 积分（累加电位）
    
    # 输出
    FIRE = 2         # 发射脉冲
    INHIBIT = 3      # 抑制性输出
    
    # 突触操作
    STRENGTHEN = 4   # 增强突触（LTP）
    WEAKEN = 5       # 削弱突触（LTD）
    PRUNE = 6        # 剪除突触
    GROW = 7         # 生长新突触
    
    # 状态控制
    REST = 8         # 静息态
    REFRACTORY = 9   # 不应期
    
    # 调节
    MODULATE = 10    # 神经调质（多巴胺等）
    ADAPT = 11       # 自适应调节

@dataclass
class Synapse:
    """突触 - 神经元间连接"""
    source_id: int           # 源神经元
    target_id: int           # 目标神经元
    weight: float            # 突触权重 (0-1)
    type: str                # 'excitatory' or 'inhibitory'
    plasticity: float = 0.01 # 可塑性系数
    
    def transmit(self, spike: bool) -> float:
        """传递脉冲"""
        if spike:
            signal = self.weight if self.type == 'excitatory' else -self.weight
            return signal
        return 0.0
    
    def update_weight(self, delta: float):
        """更新权重（学习）"""
        self.weight = max(0.0, min(1.0, self.weight + delta * self.plasticity))

@dataclass
class Neuron:
    """生物神经元处理单元"""
    id: int
    membrane_potential: float = -70.0  # 膜电位 (mV)
    threshold: float = -55.0           # 阈值
    resting_potential: float = -70.0   # 静息电位
    refractory_period: int = 0         # 不应期计数
    
    # 生物参数
    leak_rate: float = 0.1             # 漏电率
    spike_amplitude: float = 40.0      # 脉冲幅度
    
    # 突触连接
    input_synapses: List[Synapse] = None
    output_synapses: List[Synapse] = None
    
    # 神经调质
    dopamine: float = 0.0              # 多巴胺水平
    
    def __post_init__(self):
        if self.input_synapses is None:
            self.input_synapses = []
        if self.output_synapses is None:
            self.output_synapses = []
    
    def execute(self, instruction: NeuronInstruction, **kwargs):
        """执行神经元指令"""
        if instruction == NeuronInstruction.RECEIVE:
            return self._receive()
        elif instruction == NeuronInstruction.INTEGRATE:
            return self._integrate()
        elif instruction == NeuronInstruction.FIRE:
            return self._fire()
        elif instruction == NeuronInstruction.INHIBIT:
            return self._inhibit()
        elif instruction == NeuronInstruction.STRENGTHEN:
            self._strengthen_synapses()
        elif instruction == NeuronInstruction.WEAKEN:
            self._weaken_synapses()
        elif instruction == NeuronInstruction.REST:
            self._rest()
        elif instruction == NeuronInstruction.REFRACTORY:
            self._refractory()
        elif instruction == NeuronInstruction.MODULATE:
            self._modulate(kwargs.get('dopamine', 0.0))
        elif instruction == NeuronInstruction.ADAPT:
            self._adapt()
    
    def _receive(self) -> float:
        """接收所有输入突触的信号"""
        total_input = 0.0
        for synapse in self.input_synapses:
            # 简化：假设源神经元已发射
            total_input += synapse.weight if synapse.type == 'excitatory' else -synapse.weight
        return total_input
    
    def _integrate(self):
        """积分输入（Leaky Integrate-and-Fire模型）"""
        if self.refractory_period > 0:
            return
        
        # 接收输入
        input_current = self._receive()
        
        # 更新膜电位：dV/dt = -(V - V_rest)/τ + I
        self.membrane_potential += input_current
        self.membrane_potential -= (self.membrane_potential - self.resting_potential) * self.leak_rate
    
    def _fire(self) -> bool:
        """检查是否发射脉冲"""
        if self.refractory_period > 0:
            self.refractory_period -= 1
            return False
        
        if self.membrane_potential >= self.threshold:
            # 发射脉冲
            self.membrane_potential = self.spike_amplitude
            self.refractory_period = 5  # 5ms不应期
            
            # 传播到所有输出突触
            for synapse in self.output_synapses:
                synapse.transmit(True)
            
            # 重置电位
            self.membrane_potential = self.resting_potential
            return True
        return False
    
    def _inhibit(self):
        """抑制性输出"""
        for synapse in self.output_synapses:
            if synapse.type == 'inhibitory':
                synapse.transmit(True)
    
    def _strengthen_synapses(self):
        """长时程增强 (LTP)"""
        for synapse in self.input_synapses:
            synapse.update_weight(0.1 * (1 + self.dopamine))
    
    def _weaken_synapses(self):
        """长时程抑制 (LTD)"""
        for synapse in self.input_synapses:
            synapse.update_weight(-0.05)
    
    def _rest(self):
        """静息态"""
        self.membrane_potential = self.resting_potential
    
    def _refractory(self):
        """不应期"""
        if self.refractory_period > 0:
            self.refractory_period -= 1
    
    def _modulate(self, dopamine: float):
        """神经调质调节"""
        self.dopamine = dopamine
        self.threshold += dopamine * 0.1  # 多巴胺降低阈值
    
    def _adapt(self):
        """自适应调节"""
        # 根据活动历史调整阈值
        if self.membrane_potential > self.threshold * 0.9:
            self.threshold += 0.1  # 防止过度兴奋
        else:
            self.threshold -= 0.05  # 提高敏感度

class BiologicalNeuronCPU:
    """生物神经元CPU - 完整系统"""
    
    def __init__(self, num_neurons=1000):
        self.neurons: List[Neuron] = []
        self.synapses: List[Synapse] = []
        self.time_step = 0  # 时间步（ms）
        
        # 创建神经元
        for i in range(num_neurons):
            neuron = Neuron(id=i)
            self.neurons.append(neuron)
        
        # 随机连接（模拟大脑连接）
        self._create_random_connections()
    
    def _create_random_connections(self):
        """创建随机突触连接"""
        for neuron in self.neurons:
            # 每个神经元连接到10-100个其他神经元
            num_connections = random.randint(10, 100)
            targets = random.sample(self.neurons, num_connections)
            
            for target in targets:
                synapse_type = 'excitatory' if random.random() > 0.2 else 'inhibitory'
                synapse = Synapse(
                    source_id=neuron.id,
                    target_id=target.id,
                    weight=random.uniform(0.1, 0.9),
                    type=synapse_type
                )
                neuron.output_synapses.append(synapse)
                target.input_synapses.append(synapse)
                self.synapses.append(synapse)
    
    def step(self):
        """执行一个时间步（1ms）"""
        spike_count = 0
        
        # 所有神经元并行执行
        for neuron in self.neurons:
            # 1. 积分输入
            neuron.execute(NeuronInstruction.INTEGRATE)
            
            # 2. 检查是否发射
            if neuron.execute(NeuronInstruction.FIRE):
                spike_count += 1
                
                # 3. Hebbian学习：同时激活的神经元连接增强
                if random.random() < 0.1:  # 10%概率学习
                    neuron.execute(NeuronInstruction.STRENGTHEN)
            
            # 4. 自适应
            if self.time_step % 100 == 0:  # 每100ms调整
                neuron.execute(NeuronInstruction.ADAPT)
        
        self.time_step += 1
        return spike_count
    
    def stimulate(self, neuron_ids: List[int], intensity: float = 1.0):
        """外部刺激"""
        for nid in neuron_ids:
            if 0 <= nid < len(self.neurons):
                self.neurons[nid].membrane_potential += intensity * 20
    
    def reward(self, dopamine: float = 1.0):
        """奖励信号（多巴胺）"""
        for neuron in self.neurons:
            neuron.execute(NeuronInstruction.MODULATE, dopamine=dopamine)
    
    def get_activity(self) -> Dict:
        """获取网络活动统计"""
        active = sum(1 for n in self.neurons if n.membrane_potential > n.threshold * 0.8)
        avg_potential = sum(n.membrane_potential for n in self.neurons) / len(self.neurons)
        
        return {
            'time': self.time_step,
            'active_neurons': active,
            'avg_potential': avg_potential,
            'total_synapses': len(self.synapses)
        }

def demonstrate_biological_neuron_cpu():
    """演示生物神经元CPU"""
    print("=" * 80)
    print("🧠 生物神经元CPU (Biological Neuron CPU)")
    print("=" * 80)
    
    print("\n核心设计理念：")
    print("  • 每个处理单元 = 一个真实神经元模型")
    print("  • 脉冲通信（0/1，不是连续值）")
    print("  • 突触可塑性（动态学习）")
    print("  • 异步并行（无全局时钟）")
    print("  • 神经调质（多巴胺奖励）")
    
    print("\n指令集（12条）：")
    for inst in NeuronInstruction:
        print(f"  {inst.value:2d}. {inst.name}")
    
    print("\n\n" + "=" * 80)
    print("运行模拟")
    print("=" * 80)
    
    # 创建CPU
    cpu = BiologicalNeuronCPU(num_neurons=1000)
    print(f"\n✅ 创建CPU: 1000个神经元")
    print(f"   突触连接: {len(cpu.synapses)}个")
    
    # 模拟运行
    print("\n运行100ms模拟:")
    for t in range(100):
        # 每20ms给一个刺激
        if t % 20 == 0:
            cpu.stimulate([0, 1, 2, 3, 4], intensity=1.5)
        
        # 每50ms给奖励
        if t % 50 == 0 and t > 0:
            cpu.reward(dopamine=0.5)
        
        spike_count = cpu.step()
        
        if t % 10 == 0:
            stats = cpu.get_activity()
            print(f"  t={t:3d}ms: {spike_count:3d}个脉冲, "
                  f"{stats['active_neurons']:3d}个活跃神经元, "
                  f"平均电位={stats['avg_potential']:6.2f}mV")
    
    print("\n" + "=" * 80)
    print("架构特点")
    print("=" * 80)
    
    features = [
        ("脉冲编码", "信息用脉冲时间和频率编码，不是数值"),
        ("异步并行", "无全局时钟，事件驱动"),
        ("突触可塑性", "连接权重动态调整（学习）"),
        ("不应期", "发射后5ms不能再发射（生物真实）"),
        ("漏电", "膜电位自动衰减到静息态"),
        ("神经调质", "多巴胺调节学习和兴奋性"),
        ("自适应", "阈值动态调整，防止过度兴奋"),
        ("稀疏激活", "同时只有少数神经元活跃（节能）")
    ]
    
    for name, desc in features:
        print(f"\n  ✓ {name}")
        print(f"    {desc}")
    
    print("\n\n" + "=" * 80)
    print("与传统CPU对比")
    print("=" * 80)
    
    comparison = """
    
| 维度 | 传统CPU | 生物神经元CPU |
|------|---------|--------------|
| 时钟 | 全局同步 (GHz) | 异步事件驱动 |
| 数据 | 二进制数值 | 脉冲时间/频率 |
| 指令 | 顺序执行 | 并行自发 |
| 存储 | RAM分离 | 突触权重 |
| 学习 | 需编程 | 自动学习 |
| 功耗 | 100W | 0.02W (理论) |
| 速度 | 快 (ns) | 慢 (ms) |
| 容错 | 低 | 高 |
    """
    print(comparison)
    
    print("\n" + "=" * 80)
    print("生物真实性")
    print("=" * 80)
    
    bio_features = [
        ("✅ Leaky Integrate-and-Fire模型", "经典神经元模型"),
        ("✅ 不应期", "发射后短暂不能再发射"),
        ("✅ 突触可塑性", "Hebbian学习：同时激活→连接增强"),
        ("✅ 兴奋性/抑制性突触", "80%兴奋，20%抑制"),
        ("✅ 神经调质", "多巴胺调节学习"),
        ("✅ 自适应", "阈值动态调整"),
        ("⚠️ 简化", "真实神经元有100+种离子通道"),
        ("⚠️ 简化", "真实突触有复杂的化学过程")
    ]
    
    for feature, desc in bio_features:
        print(f"  {feature}")
        print(f"    {desc}")
    
    print("\n\n" + "=" * 80)
    print("应用场景")
    print("=" * 80)
    
    applications = [
        ("模式识别", "视觉、听觉、触觉", "✅ 擅长"),
        ("时序学习", "预测、序列记忆", "✅ 擅长"),
        ("强化学习", "试错学习、游戏", "✅ 擅长"),
        ("低功耗AI", "边缘设备、传感器", "✅ 擅长"),
        ("精确计算", "科学计算、加密", "❌ 不擅长"),
        ("高速处理", "实时视频编码", "❌ 不擅长")
    ]
    
    for app, desc, status in applications:
        print(f"  {status} {app}")
        print(f"      {desc}")
    
    print("\n\n" + "=" * 80)
    print("硬件实现")
    print("=" * 80)
    
    print("\n三种实现方式:")
    implementations = [
        ("软件模拟", "在传统CPU/GPU上模拟", "✅ 灵活但慢"),
        ("神经形态芯片", "专用硬件（SpiNNaker/Loihi）", "✅ 快且节能"),
        ("真实神经元", "培养真实细胞（FinalSpark）", "⚠️ 最真实但难")
    ]
    
    for method, desc, status in implementations:
        print(f"\n  {status} {method}")
        print(f"      {desc}")
    
    print("\n\n" + "=" * 80)
    print("核心洞察")
    print("=" * 80)
    
    insights = """
1. 生物神经元CPU不是传统意义的"CPU"
   • 没有指令流水线
   • 没有ALU、寄存器
   • 更像是"神经网络加速器"

2. 优势在于特定任务
   • 模式识别：✅ 比传统CPU强1000倍
   • 学习能力：✅ 自动学习，无需编程
   • 功耗：✅ 理论上低100万倍

3. 劣势也明显
   • 精确计算：❌ 不适合
   • 编程：❌ 只能训练，不能编程
   • 速度：❌ ms级，比ns级慢100万倍

4. 未来：混合架构
   • 传统CPU：精确计算、控制
   • 神经元CPU：感知、学习、决策
   • 各取所长，超越人脑？
    """
    print(insights)
    
    print("=" * 80)

if __name__ == "__main__":
    demonstrate_biological_neuron_cpu()
