#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BioC - 基因编程语言
类似C语言的生物计算高级语言

核心思想：
- 用类C语法编写生物程序
- 编译为DNA序列
- 在活细胞中执行
"""

class BioCLanguage:
    """BioC语言设计"""
    
    def __init__(self):
        self.syntax = self._define_syntax()
        self.stdlib = self._define_stdlib()
        self.examples = self._define_examples()
    
    def _define_syntax(self):
        """定义BioC语法"""
        return {
            '数据类型': {
                'gene': '基因',
                'protein': '蛋白质',
                'promoter': '启动子',
                'rbs': '核糖体结合位点',
                'terminator': '终止子',
                'plasmid': '质粒',
                'concentration': '浓度 (float)',
                'sequence': 'DNA序列 (string)'
            },
            
            '控制结构': {
                'if (condition)': '条件判断 (基于浓度/信号)',
                'while (condition)': '循环 (反馈环路)',
                'for (i=0; i<n; i++)': '计数循环',
                'switch (signal)': '多路选择'
            },
            
            '运算符': {
                'express()': '表达基因',
                'repress()': '抑制基因',
                'activate()': '激活基因',
                'degrade()': '降解蛋白质',
                'bind()': '结合',
                'phosphorylate()': '磷酸化',
                'sense()': '感知信号'
            },
            
            '函数': {
                'gene_circuit()': '基因线路',
                'feedback_loop()': '反馈环路',
                'oscillator()': '振荡器',
                'toggle_switch()': '开关',
                'logic_gate()': '逻辑门'
            },
            
            '标准库': {
                '#include <biostdlib.h>': '标准生物库',
                '#include <sensors.h>': '传感器库',
                '#include <actuators.h>': '执行器库',
                '#include <logic.h>': '逻辑门库'
            }
        }
    
    def _define_stdlib(self):
        """标准库函数"""
        return {
            # 基本操作
            'express(gene)': '表达基因',
            'repress(gene, repressor)': '抑制基因',
            'activate(gene, activator)': '激活基因',
            'degrade(protein, rate)': '降解蛋白质',
            
            # 传感器
            'sense_light(wavelength)': '光传感器',
            'sense_chemical(molecule)': '化学传感器',
            'sense_temperature(temp)': '温度传感器',
            'sense_pH(value)': 'pH传感器',
            
            # 执行器
            'produce_fluorescence(color)': '产生荧光',
            'produce_enzyme(type)': '产生酶',
            'produce_signal(molecule)': '产生信号分子',
            'kill_cell()': '细胞凋亡',
            
            # 逻辑门
            'AND(input1, input2)': '与门',
            'OR(input1, input2)': '或门',
            'NOT(input)': '非门',
            'XOR(input1, input2)': '异或门',
            
            # 时序
            'delay(time)': '延迟',
            'oscillate(period)': '振荡',
            'pulse(duration)': '脉冲',
            
            # 通信
            'send_signal(molecule)': '发送信号',
            'receive_signal(molecule)': '接收信号',
            'quorum_sensing()': '群体感应'
        }
    
    def _define_examples(self):
        """示例程序"""
        return {
            '1. Hello World (荧光蛋白)': '''
// BioC程序：表达绿色荧光蛋白
#include <biostdlib.h>

int main() {
    gene gfp = "GFP";  // 绿色荧光蛋白基因
    
    express(gfp);      // 表达GFP
    
    return 0;
}

// 编译为：
// Promoter-RBS-GFP-Terminator
''',
            
            '2. 条件表达': '''
// 根据信号表达不同蛋白质
#include <biostdlib.h>
#include <sensors.h>

int main() {
    gene gfp = "GFP";
    gene rfp = "RFP";
    
    float signal = sense_chemical("IPTG");
    
    if (signal > 0.1) {
        express(gfp);   // 高信号→绿色
    } else {
        express(rfp);   // 低信号→红色
    }
    
    return 0;
}

// 编译为：
// IPTG诱导启动子 + GFP
// 组成型启动子 + 阻遏蛋白 + RFP
''',
            
            '3. 逻辑门': '''
// AND门：需要两个信号
#include <logic.h>

int main() {
    float input1 = sense_chemical("AHL");
    float input2 = sense_chemical("Arabinose");
    
    float output = AND(input1, input2);
    
    if (output > 0.5) {
        produce_fluorescence("green");
    }
    
    return 0;
}

// 编译为：
// 双启动子系统
// 需要AHL和Arabinose同时存在
''',
            
            '4. 振荡器': '''
// 基因振荡器 (Repressilator)
#include <biostdlib.h>

void oscillator() {
    gene lacI = "lacI";
    gene tetR = "tetR";
    gene cI = "cI";
    
    // 循环抑制
    while (1) {
        express(lacI);
        repress(tetR, lacI);
        
        express(tetR);
        repress(cI, tetR);
        
        express(cI);
        repress(lacI, cI);
        
        delay(50);  // 50分钟周期
    }
}

int main() {
    oscillator();
    return 0;
}

// 编译为：
// 三个基因相互抑制的环路
''',
            
            '5. 开关': '''
// 双稳态开关 (Toggle Switch)
#include <biostdlib.h>

int main() {
    gene lacI = "lacI";
    gene tetR = "tetR";
    
    // 互相抑制
    repress(tetR, lacI);
    repress(lacI, tetR);
    
    // 外部信号切换状态
    float iptg = sense_chemical("IPTG");
    float atc = sense_chemical("aTc");
    
    if (iptg > 0.1) {
        activate(tetR);  // 切换到状态1
    }
    if (atc > 0.1) {
        activate(lacI);  // 切换到状态2
    }
    
    return 0;
}

// 编译为：
// 双稳态基因线路
// 具有记忆功能
''',
            
            '6. 边缘检测': '''
// 图像边缘检测 (细菌群体)
#include <biostdlib.h>
#include <sensors.h>

int main() {
    // 感知邻居信号
    float left = receive_signal("AHL_left");
    float right = receive_signal("AHL_right");
    float up = receive_signal("AHL_up");
    float down = receive_signal("AHL_down");
    
    // 计算梯度
    float gradient = abs(left - right) + abs(up - down);
    
    // 边缘处产生荧光
    if (gradient > 0.5) {
        produce_fluorescence("green");
    }
    
    return 0;
}

// 编译为：
// 群体感应 + 信号处理线路
''',
            
            '7. 计数器': '''
// 细胞分裂计数器
#include <biostdlib.h>

int main() {
    static int count = 0;
    
    // 每次细胞分裂
    count++;
    
    // 达到阈值后执行
    if (count >= 10) {
        produce_enzyme("cellulase");
        kill_cell();  // 程序性死亡
    }
    
    return 0;
}

// 编译为：
// 基于重组酶的计数器
// 不可逆DNA重排
''',
            
            '8. 定时炸弹': '''
// 定时释放药物
#include <biostdlib.h>

int main() {
    float time = 0;
    
    while (time < 24.0) {  // 24小时
        delay(1.0);  // 1小时
        time += 1.0;
    }
    
    // 时间到，释放药物
    produce_enzyme("therapeutic_protein");
    
    return 0;
}

// 编译为：
// 基于蛋白质降解的计时器
''',
        }
    
    def display(self):
        """展示BioC语言"""
        print("=" * 80)
        print("BioC - 基因编程语言")
        print("类似C语言的生物计算高级语言")
        print("=" * 80)
        
        print("\n语法特性:")
        for category, items in self.syntax.items():
            print(f"\n{category}:")
            for key, value in list(items.items())[:4]:
                print(f"  {key:<30} - {value}")
        
        print("\n\n标准库函数 (部分):")
        for func, desc in list(self.stdlib.items())[:8]:
            print(f"  {func:<35} - {desc}")

def show_examples():
    """展示示例程序"""
    lang = BioCLanguage()
    
    print("\n" + "=" * 80)
    print("BioC示例程序")
    print("=" * 80)
    
    for title, code in list(lang.examples.items())[:4]:
        print(f"\n{title}")
        print("-" * 80)
        print(code)

def existing_languages():
    """现有的基因编程语言"""
    print("\n" + "=" * 80)
    print("现有的基因编程语言")
    print("=" * 80)
    
    languages = {
        'Cello (MIT)': {
            'year': '2016',
            'description': 'Verilog风格的基因线路设计语言',
            'features': [
                '• 类似硬件描述语言',
                '• 自动设计基因线路',
                '• 输入逻辑规范，输出DNA序列',
                '• 已实现复杂逻辑电路'
            ],
            'example': '''
module sensor(input light, output gfp);
    assign gfp = light;
endmodule
'''
        },
        
        'GEC (Genetic Engineering of Cells)': {
            'year': '2011',
            'description': '基于规则的基因线路设计',
            'features': [
                '• 声明式语言',
                '• 基于约束求解',
                '• 自动优化设计',
                '• 考虑生物约束'
            ],
            'example': '''
circuit AND_gate {
    inputs: IPTG, Arabinose
    output: GFP
    logic: GFP = IPTG AND Arabinose
}
'''
        },
        
        'BioJava/BioPython': {
            'year': '2000s',
            'description': '生物信息学编程库',
            'features': [
                '• 序列操作',
                '• 基因注释',
                '• 系统生物学建模',
                '• 不直接编译为DNA'
            ],
            'example': '''
from Bio.Seq import Seq
seq = Seq("ATGGCCATTGTAATGGGCCGC")
protein = seq.translate()
'''
        },
        
        'Eugene': {
            'year': '2009',
            'description': '合成生物学设计语言',
            'features': [
                '• 声明DNA部件',
                '• 定义组装规则',
                '• 约束求解',
                '• 自动化设计'
            ],
            'example': '''
Device MyDevice(
    Promoter p,
    RBS r,
    CDS c,
    Terminator t
) {
    p BEFORE r
    r BEFORE c
    c BEFORE t
}
'''
        },
        
        'SBOL (Synthetic Biology Open Language)': {
            'year': '2011',
            'description': '合成生物学数据标准',
            'features': [
                '• XML/RDF格式',
                '• 描述生物部件',
                '• 数据交换标准',
                '• 不是编程语言'
            ],
            'example': '''
<Component>
    <displayId>GFP</displayId>
    <type>CDS</type>
    <sequence>ATGAGTAAAGGA...</sequence>
</Component>
'''
        }
    }
    
    for name, info in languages.items():
        print(f"\n{name} ({info['year']})")
        print(f"  {info['description']}")
        for feature in info['features']:
            print(f"  {feature}")
        print(f"\n  示例:")
        for line in info['example'].strip().split('\n'):
            print(f"    {line}")

def compilation_process():
    """编译过程"""
    print("\n" + "=" * 80)
    print("BioC编译过程")
    print("=" * 80)
    
    print("""
1. 词法分析 (Lexical Analysis)
   BioC源代码 → Token流
   
   express(gfp); → [KEYWORD:express, LPAREN, ID:gfp, RPAREN, SEMICOLON]

2. 语法分析 (Syntax Analysis)
   Token流 → 抽象语法树 (AST)
   
   if (signal > 0.1) { express(gfp); }
   →
   IfStatement
   ├── Condition: signal > 0.1
   └── Body: express(gfp)

3. 语义分析 (Semantic Analysis)
   检查类型、作用域、生物约束
   
   • gfp是否已定义？
   • 启动子强度是否合适？
   • 是否有资源冲突？

4. 中间代码生成
   AST → 生物中间表示 (BIR)
   
   express(gfp)
   →
   Promoter(strength=0.5) + RBS(efficiency=0.8) + GFP + Terminator

5. 优化
   • 密码子优化 (提高表达)
   • 去除重复序列
   • 平衡代谢负担
   • 避免二级结构

6. DNA序列生成
   BIR → 实际DNA序列
   
   TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGCGGATAACAATTTCACACAGG
   AAACAGCTATGACCATGATTACGAATTCGAGCTCGGTACCCGGGGATCCTCTAGAGTCGACCTGC
   ...

7. 物理实现
   • DNA合成 (化学合成或PCR)
   • 质粒构建
   • 转化到细胞
   • 验证功能

编译流程图：

  BioC源代码
      ↓
  [词法分析器]
      ↓
   Token流
      ↓
  [语法分析器]
      ↓
    AST
      ↓
  [语义分析器]
      ↓
  类型检查的AST
      ↓
  [代码生成器]
      ↓
  生物中间表示
      ↓
  [优化器]
      ↓
  优化的BIR
      ↓
  [DNA序列生成器]
      ↓
  DNA序列 (FASTA)
      ↓
  [DNA合成]
      ↓
  物理质粒
      ↓
  [转化]
      ↓
  工程细菌
    """)

def challenges_and_future():
    """挑战与未来"""
    print("\n" + "=" * 80)
    print("挑战与未来展望")
    print("=" * 80)
    
    print("""
当前挑战：

1. 部件标准化
   • 生物部件不如电子元件标准
   • 上下文依赖性强
   • 难以预测行为

2. 调试困难
   • 无法单步执行
   • 观测手段有限
   • 时间尺度慢 (小时-天)

3. 可靠性
   • 突变
   • 环境敏感
   • 细胞异质性

4. 复杂度限制
   • 代谢负担
   • 资源竞争
   • 串扰

5. 工具链不完善
   • 编译器不成熟
   • 仿真器精度低
   • 缺乏IDE

未来展望：

1. 自动化设计 (2025-2030)
   • AI辅助设计
   • 自动优化
   • 预测性建模

2. 标准化 (2030+)
   • 生物部件标准库
   • 即插即用
   • 可组合性

3. 高级抽象 (2030+)
   • 更高级的语言
   • 面向对象
   • 函数式编程

4. 云实验室 (已有)
   • 远程DNA合成
   • 自动化实验
   • 在线验证

5. 应用爆发 (2025-2040)
   • 智能药物
   • 环境监测
   • 生物制造
   • 活体计算机

示例：未来的BioC++

class Cell {
private:
    gene gfp;
    protein GFP;
    
public:
    Cell() {
        gfp = new gene("GFP");
    }
    
    void sense_and_respond(float signal) {
        if (signal > threshold) {
            GFP = express(gfp);
            GFP.fluoresce();
        }
    }
};

int main() {
    Cell myCell;
    myCell.sense_and_respond(0.5);
    return 0;
}
    """)

def main():
    lang = BioCLanguage()
    lang.display()
    show_examples()
    existing_languages()
    compilation_process()
    challenges_and_future()
    
    print("\n" + "=" * 80)
    print("总结")
    print("=" * 80)
    print("""
基因编程语言：从梦想到现实

答案：✓ 可以，而且已经存在！

现有语言：
• Cello (MIT, 2016): Verilog风格
• Eugene (2009): 声明式设计
• GEC (2011): 基于约束
• SBOL (2011): 数据标准

BioC的优势：
• 类C语法，程序员友好
• 高级抽象，隐藏生物细节
• 自动编译为DNA序列
• 标准库丰富

编译流程：
源代码 → AST → 优化 → DNA序列 → 物理实现

实际应用：
• 2016: Cello设计67个基因线路
• 2017: 自动设计AND/OR/NOT门
• 2020: 复杂逻辑电路 (16输入)

挑战：
• 部件标准化
• 调试困难
• 可靠性
• 复杂度限制

未来：
• AI辅助设计
• 标准化部件库
• 云实验室
• 活体计算机

哲学意义：
"编程不再局限于硅片，
 而是扩展到生命本身。
 我们正在学习用代码编写生命。"

从C语言到BioC：
• C语言: 编程电子计算机
• BioC: 编程生物计算机
• 本质相同: 都是指令序列
• 载体不同: 电子 vs 生命

基因编程语言证明：
生命是可编程的，
而我们正在成为生命的程序员。
    """)

if __name__ == '__main__':
    main()
