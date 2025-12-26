# Validator 验证工具使用说明

## 📋 功能说明

`Validator.py` 是一个数据集验证工具，用于检查：

1. ✅ **CSV文件验证** - 检查CSV文件是否存在、可读、字段是否符合Schema
2. ✅ **JSON文件验证** - 检查JSON结构是否正确、是否包含NaN等错误
3. ✅ **转换正确性** - 比对CSV和JSON的记录数，确保转换无误
4. ✅ **生成报告** - 自动生成详细的验证报告

---

## 🚀 快速开始

### 基本用法

```bash
python Validator.py <煤矿名称>
```

### 示例

```bash
python Validator.py TEST煤矿
```

---

## 📊 验证内容

### 1. CSV文件验证

**检查项**:
- ✅ 文件是否存在
- ✅ 文件是否可读（支持多种编码）
- ✅ 字段是否符合Schema定义
- ✅ 记录数统计

**输出示例**:
```
📋 验证CSV文件: TEST煤矿
================================================================================
  ✅ 采空区基本信息: 29条记录, 19个字段
  ✅ 采空区积水信息: 9条记录, 16个字段
  ✅ 采空区积气信息: 124条记录, 12个字段
  ...
  ⚠️ 自燃发火信息: 缺少字段 {'gas_composition', 'fire_area'}
  ⚠️ 自燃发火信息: 多余字段 {'temperature_unit', 'has_fire'}
```

### 2. JSON文件验证

**检查项**:
- ✅ JSON结构是否完整（mine_info, statistics, data）
- ✅ 是否包含NaN值（应为null）
- ✅ 统计数与实际记录数是否一致
- ✅ 所有表是否存在

**输出示例**:
```
📋 验证JSON文件: TEST煤矿-采空区数据集.json
================================================================================
  ✅ 采空区基本信息: 29条记录
  ✅ 采空区积水信息: 9条记录
  ...
  ❌ 采空区基本信息: 包含NaN值（应为null）
```

### 3. CSV与JSON比对

**检查项**:
- ✅ 每个表的记录数是否一致
- ✅ 转换是否完整

**输出示例**:
```
🔍 比对CSV与JSON: TEST煤矿
================================================================================
  ✅ 采空区基本信息: CSV=29, JSON=29
  ✅ 采空区积水信息: CSV=9, JSON=9
  ...
  ❌ 采空区积气信息: CSV(124条) != JSON(120条)
```

---

## 📄 验证报告

### 报告内容

验证完成后会生成详细报告，包括：

1. **CSV文件验证结果**
   - 找到的表数量
   - 总记录数
   - 错误和警告列表

2. **JSON文件验证结果**
   - 文件有效性
   - 总记录数
   - 错误和警告列表

3. **CSV与JSON比对结果**
   - 转换是否正确
   - 差异列表

4. **总结**
   - ✅ 验证通过
   - ❌ 验证失败

### 报告示例

```
================================================================================
数据集验证报告
================================================================================

📋 CSV文件验证
--------------------------------------------------------------------------------
煤矿: TEST煤矿
找到表: 10/10
总记录数: 255
警告: 7个
  ⚠️ 自燃发火信息: 缺少字段 {'gas_composition', 'fire_area'}
  ⚠️ 地裂缝信息: 多余字段 {'crack_number', 'location'}

📋 JSON文件验证
--------------------------------------------------------------------------------
文件: TEST煤矿-采空区数据集.json
有效: ✅ 是
总记录数: 255

🔍 CSV与JSON比对
--------------------------------------------------------------------------------
转换正确: ✅ 是

================================================================================
✅ 验证通过！CSV和JSON数据一致，转换正确。
================================================================================
```

### 报告保存

报告会自动保存为：`{煤矿名称}-验证报告.txt`

---

## 🎯 使用场景

### 场景1: 转换前检查CSV

```bash
# 检查CSV文件是否符合Schema
python Validator.py TEST煤矿
```

**用途**: 
- 确认CSV文件可读
- 检查字段是否完整
- 发现数据问题

### 场景2: 转换后验证

```bash
# 1. 转换
python ToJson.py TEST煤矿

# 2. 验证
python Validator.py TEST煤矿
```

**用途**:
- 确认转换正确
- 检查记录数一致
- 验证无NaN值

### 场景3: 批量验证

```bash
# 验证多个煤矿
python Validator.py TEST煤矿
```

---

## ⚠️ 常见问题

### 1. 字段不匹配警告

```
⚠️ 自燃发火信息: 缺少字段 {'gas_composition', 'fire_area'}
⚠️ 自燃发火信息: 多余字段 {'has_fire', 'temperature_unit'}
```

**原因**: CSV字段与Schema定义不完全一致

**处理**:
- 如果是扩展字段，可以忽略警告
- 如果是必需字段缺失，需要补充CSV

### 2. 记录数不一致

```
❌ 采空区积气信息: CSV(124条) != JSON(120条)
```

**原因**: 转换过程中丢失了数据

**处理**:
- 检查CSV文件是否有格式问题
- 重新运行ToJson.py转换
- 检查是否有on_bad_lines='skip'导致的行跳过

### 3. 包含NaN值

```
❌ 采空区基本信息: 包含NaN值（应为null）
```

**原因**: 空值未正确转换

**处理**:
- 使用最新版本的ToJson.py（已修复）
- 重新转换

---

## 🔧 Python代码调用

### 单独验证CSV

```python
from Validator import Validator

validator = Validator()
result = validator.validate_csv("TEST煤矿")

print(f"找到表: {result['found_tables']}/10")
print(f"总记录数: {result['total_records']}")
```

### 单独验证JSON

```python
validator = Validator()
result = validator.validate_json("TEST煤矿-采空区数据集.json")

print(f"有效: {result['valid']}")
print(f"总记录数: {result['total_records']}")
```

### 比对CSV和JSON

```python
validator = Validator()
result = validator.compare_csv_json(
    "TEST煤矿",
    "TEST煤矿-采空区数据集.json"
)

print(f"转换正确: {result['match']}")
```

### 完整验证流程

```python
validator = Validator()

# 验证CSV
csv_result = validator.validate_csv("TEST煤矿")

# 验证JSON
json_result = validator.validate_json("TEST煤矿-采空区数据集.json")

# 比对
compare_result = validator.compare_csv_json(
    "TEST煤矿",
    "TEST煤矿-采空区数据集.json"
)

# 生成报告
report = validator.generate_report(csv_result, json_result, compare_result)
print(report)
```

---

## 📚 相关工具

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| **ToJson.py** | CSV转JSON | 数据转换 |
| **Validator.py** | 验证工具 | 质量检查 |
| **Schema.json** | 数据结构定义 | 标准参考 |

---

## 💡 最佳实践

### 推荐工作流程

```bash
# 1. 准备CSV文件
TEST煤矿-采空区基本信息.csv
TEST煤矿-采空区积水信息.csv
...

# 2. 验证CSV（可选）
python Validator.py TEST煤矿

# 3. 转换为JSON
python ToJson.py TEST煤矿

# 4. 验证转换结果
python Validator.py TEST煤矿

# 5. 检查报告
cat TEST煤矿-验证报告.txt
```

### 质量保证

- ✅ 转换前验证CSV
- ✅ 转换后验证JSON
- ✅ 检查验证报告
- ✅ 修复所有错误
- ✅ 评估警告影响

---

**版本**: 1.0.0  
**更新日期**: 2024-12-26  
**维护单位**: 煤矿采空区普查数据标准化工作组

