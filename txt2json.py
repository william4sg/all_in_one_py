import re
import json
import os
import argparse

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="Process a novel text file and split it into a JSON format.")
parser.add_argument('--input_file', type=str, required=True, help='未经处理的小说txt文件路径')
parser.add_argument('--output_file', type=str, required=True, help='要输出的json文件路径')
parser.add_argument('--novel_name', type=str, required=True, help='小说名称')

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
novel_name = args.novel_name

# 检查并创建输出文件夹（如果不存在）
output_dir = os.path.dirname(output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 打开并读取文件内容
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# 正则表达式匹配章节标题
chapter_pattern = r'(第\d+章 .+?)(?=第\d+章 |\Z)'

# 查找所有章节
chapters = re.findall(chapter_pattern, content, re.S)

# 存储所有章节信息的列表
chapter_list = []

# 处理每一章并存入列表
for chapter in chapters:
    # 章节标题
    title_match = re.match(r'(第\d+章 .+)', chapter)
    instruction = title_match.group(1) if title_match else 'Unknown Instruction'
    
    # 在 instruction 最前面加上小说名称
    instruction = f"小说名称《{novel_name}》" + instruction
    
    # 章节内容
    content = chapter[len(instruction) - len(f"小说名称《{novel_name}》"):].strip()
    
    # 计算分割点（20%的位置）
    split_point = max(1, len(content) // 5)  # 确保至少有一个字符分配给 input
    
    # 将 content 拆分为两部分
    input_part = content[:split_point].strip()  # 去掉两端的空白字符
    output_part = content[split_point:].strip()
    
    # 如果 input_part 为空，跳过当前循环
    if not input_part:
        continue
    
    # 在 input 最前面加上“续写小说”
    input_part = "续写小说：" + input_part
    
    # 构建字典
    chapter_dict = {
        'instruction': instruction,
        'input': input_part,
        'output': output_part
    }
    
    # 添加到章节列表
    chapter_list.append(chapter_dict)

# 将所有章节信息保存到JSON文件中
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(chapter_list, json_file, ensure_ascii=False, indent=4)

print(f'Saved all chapters to {output_file}')
