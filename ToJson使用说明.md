# ToJson 转换工具使用说明

## 📋 功能说明

`ToJson.py` 是一个通用的煤矿采空区数据集转换工具，能够：

1. ✅ **自动检测煤矿** - 扫描目录中的所有煤矿CSV文件
2. ✅ **单矿转换** - 将一个煤矿的10个表合并为1个JSON文件
3. ✅ **批量转换** - 自动转换目录中的所有煤矿
4. ✅ **容错处理** - 部分表缺失时仍能正常转换
5. ✅ **生成报告** - 自动生成转换报告

---

## 🚀 快速开始

### 安装依赖

```bash
pip install pandas
```

### 使用方式

#### 方式1: 批量转换（推荐）

```bash
# 自动检测并转换当前目录下的所有煤矿
python ToJson.py
```

**输出**:
```
🚀 批量转换模式
🔍 自动检测到 3 个煤矿: 河西联办煤矿, 盛博煤矿, 王才伙盘煤矿

📋 正在转换: 河西联办煤矿
  ✅ 采空区基本信息: 30条记录
  ✅ 采空区积水信息: 17条记录
  ✅ 采空区积气信息: 124条记录
  ...
✅ 已生成: ./json_output/河西联办煤矿-采空区数据集.json

📋 正在转换: 盛博煤矿
  ✅ 采空区基本信息: 15条记录
  ⚠️ 采空区积水信息: 读取失败 - 文件不存在
  ...
✅ 已生成: ./json_output/盛博煤矿-采空区数据集.json
```

#### 方式2: 转换单个煤矿

```bash
# 转换指定煤矿
python ToJson.py 河西联办煤矿
```

#### 方式3: Python代码调用

```python
from ToJson import ToJson

# 创建转换器
converter = ToJson(data_dir=".")

# 转换单个煤矿
converter.convert_mine("河西联办煤矿", "河西联办煤矿-采空区数据集.json")

# 批量转换
converter.batch_convert(output_dir="./json_output")

# 指定煤矿列表
converter.batch_convert(
    mine_names=["河西联办煤矿", "盛博煤矿"],
    output_dir="./json_output"
)
```

---

## 📁 文件组织

### 输入文件（CSV）

```
当前目录/
├── 河西联办煤矿-采空区基本信息.csv
├── 河西联办煤矿-采空区积水信息.csv
├── 河西联办煤矿-采空区积气信息.csv
├── ...
├── 盛博煤矿-采空区基本信息.csv
├── 盛博煤矿-采空区积水信息.csv
└── ...
```

### 输出文件（JSON）

```
json_output/
├── 河西联办煤矿-采空区数据集.json
├── 盛博煤矿-采空区数据集.json
├── 王才伙盘煤矿-采空区数据集.json
└── 转换报告.txt
```

---

## 📊 输出JSON格式

```json
{
  "mine_info": {
    "mine_id": "HX001",
    "mine_name": "河西联办煤矿",
    "survey_date": "",
    "standard": "KAT 22.2-2024",
    "data_version": "1.0.0"
  },
  "statistics": {
    "goaf_basic_info": 30,
    "goaf_water_info": 17,
    "goaf_gas_info": 124,
    "fire_info": 0,
    "suspended_roof_info": 10,
    "collapse_info": 0,
    "crack_info": 10,
    "abandoned_shaft_info": 2,
    "seal_wall_info": 25,
    "treatment_info": 4
  },
  "data": {
    "goaf_basic_info": [...],
    "goaf_water_info": [...],
    "goaf_gas_info": [...],
    "fire_info": [],
    "suspended_roof_info": [...],
    "collapse_info": [],
    "crack_info": [...],
    "abandoned_shaft_info": [...],
    "seal_wall_info": [...],
    "treatment_info": [...]
  }
}
```

---

## ✨ 特色功能

### 1. 自动检测煤矿

工具会自动扫描目录中的CSV文件，识别所有煤矿：

```python
converter = ToJson()
mines = converter.auto_detect_mines()
print(mines)  # ['河西联办煤矿', '盛博煤矿', '王才伙盘煤矿']
```

### 2. 容错处理

- ✅ 表文件不存在 → 该表记录为空数组
- ✅ 表文件读取失败 → 该表记录为空数组，输出警告
- ✅ 部分表缺失 → 仍能生成完整JSON结构

**示例**:
```
盛博煤矿只有5个表 → 生成的JSON中其他5个表为空数组
```

### 3. 自动生成mine_id

如果CSV中没有mine_id字段，工具会自动生成：

```python
河西联办煤矿 → HXLBMK001
盛博煤矿 → SBMK001
```

### 4. 详细的转换报告

```
================================================================================
煤矿采空区数据集批量转换报告
================================================================================

总煤矿数: 3
成功: 3
失败: 0
总记录数: 450

--------------------------------------------------------------------------------

✅ 河西联办煤矿
   记录数: 222
   表数: 8/10
   文件: ./json_output/河西联办煤矿-采空区数据集.json

✅ 盛博煤矿
   记录数: 150
   表数: 5/10
   文件: ./json_output/盛博煤矿-采空区数据集.json

✅ 王才伙盘煤矿
   记录数: 78
   表数: 6/10
   文件: ./json_output/王才伙盘煤矿-采空区数据集.json
```

---

## 🎯 使用场景

### 场景1: 新煤矿数据转换

```bash
# 1. 准备CSV文件
新煤矿-采空区基本信息.csv
新煤矿-采空区积水信息.csv
...

# 2. 运行转换
python ToJson.py 新煤矿

# 3. 获得JSON
新煤矿-采空区数据集.json
```

### 场景2: 批量转换多个煤矿

```bash
# 1. 准备多个煤矿的CSV文件
河西联办煤矿-*.csv
盛博煤矿-*.csv
王才伙盘煤矿-*.csv

# 2. 批量转换
python ToJson.py

# 3. 获得多个JSON
json_output/
├── 河西联办煤矿-采空区数据集.json
├── 盛博煤矿-采空区数据集.json
└── 王才伙盘煤矿-采空区数据集.json
```

### 场景3: 部分表缺失

```bash
# 盛博煤矿只有5个表
盛博煤矿-采空区基本信息.csv
盛博煤矿-采空区积水信息.csv
盛博煤矿-采空区积气信息.csv
盛博煤矿-地裂缝信息.csv
盛博煤矿-密闭墙信息.csv

# 仍能正常转换
python ToJson.py 盛博煤矿

# 生成的JSON中，缺失的表为空数组
{
  "data": {
    "goaf_basic_info": [...],
    "goaf_water_info": [...],
    "goaf_gas_info": [...],
    "fire_info": [],              // 缺失
    "suspended_roof_info": [],    // 缺失
    "collapse_info": [],          // 缺失
    "crack_info": [...],
    "abandoned_shaft_info": [],   // 缺失
    "seal_wall_info": [...],
    "treatment_info": []          // 缺失
  }
}
```

---

## ⚠️ 注意事项

### 1. 文件命名规范

CSV文件必须遵循命名规范：

```
{煤矿名称}-{表名}.csv

✅ 正确:
- 河西联办煤矿-采空区基本信息.csv
- 盛博煤矿-采空区积水信息.csv

❌ 错误:
- 河西联办煤矿_采空区基本信息.csv  (使用下划线)
- 采空区基本信息-河西联办煤矿.csv  (顺序错误)
```

### 2. 编码格式

CSV文件必须使用**UTF-8编码**，否则可能出现乱码。

### 3. 表名必须完整匹配

表名必须与Schema定义的10个表名完全一致：

```
✅ 采空区基本信息
✅ 采空区积水信息
✅ 采空区积气信息
✅ 自燃发火信息
✅ 采空区悬顶信息
✅ 采空区塌陷信息
✅ 地裂缝信息
✅ 废弃井筒信息
✅ 密闭墙信息
✅ 采空区治理信息
```

---

## 🔧 高级用法

### 自定义输出目录

```python
converter = ToJson(data_dir="./csv_data")
converter.batch_convert(output_dir="./my_json_output")
```

### 只转换指定煤矿

```python
converter = ToJson()
converter.batch_convert(
    mine_names=["河西联办煤矿", "盛博煤矿"],
    output_dir="./json_output"
)
```

### 获取转换结果

```python
results = converter.batch_convert()

for result in results:
    if result['success']:
        print(f"{result['mine_name']}: {result['record_count']}条记录")
    else:
        print(f"{result['mine_name']}: 失败 - {result['error']}")
```

---

## 📚 相关文档

- **Schema定义**: 煤矿采空区普查数据集Schema.json
- **JSON格式说明**: JSON格式规范-大模型训练版.md
- **单位规范**: 单位规范说明.md

---

**版本**: 1.0.0  
**更新日期**: 2024-12-26  
**维护单位**: 煤矿采空区普查数据标准化工作组

