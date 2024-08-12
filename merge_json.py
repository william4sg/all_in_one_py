import os
import json
import random
import argparse

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="Merge JSON files into a single JSON file with shuffled data.")
parser.add_argument('--json_dir', type=str, required=True, help='存放 JSON 文件的目录路径')
parser.add_argument('--output_file', type=str, required=True, help='合并后输出的 JSON 文件路径')

args = parser.parse_args()

json_dir = args.json_dir
output_file = args.output_file

# 初始化一个空列表来存储合并的数据
merged_data = []

# 遍历指定目录中的所有 JSON 文件
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(json_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 将每个 JSON 文件的列表数据合并到 merged_data 列表中
            merged_data.extend(data)

# 随机打乱 merged_data 列表的顺序
random.shuffle(merged_data)

# 将合并并打乱的数据保存到一个新的 JSON 文件中
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, ensure_ascii=False, indent=4)

print(f'Merged JSON data from {len(os.listdir(json_dir))} files into {output_file}')
