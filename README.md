# ToDataJson - 煤矿采空区数据集转换工具包

## 📋 简介

ToDataJson是一个完整的煤矿采空区数据集转换和验证工具包，用于将CSV格式的采空区普查数据转换为JSON格式，并验证转换的正确性。

**符合标准**: KAT 22.2-2024 矿山隐蔽致灾因素普查规范 第2部分：煤矿

**🌐 现已支持Web界面！**

---

## 📦 文件清单

### 核心工具
- `ToJson.py` - CSV转JSON转换工具
- `Validator.py` - 数据验证工具
- `test.py` - 单元测试
- **`app.py` - Streamlit Web应用** ⭐新增

### Schema和文档
- `煤矿采空区普查数据集Schema.json` - 数据结构定义
- `README.md` - 本文档
- `DEPLOYMENT.md` - 部署指南 ⭐新增
- `ToJson使用说明.md` - ToJson工具使用文档
- `Validator使用说明.md` - Validator工具使用文档
- `JSON格式规范-大模型训练版.md` - JSON格式说明
- `单位规范说明.md` - 单位规范文档
- `requirements.txt` - Python依赖 ⭐新增

### 测试数据
- `TEST煤矿-采空区基本信息.csv`
- `TEST煤矿-采空区积水信息.csv`
- ... (共10个CSV文件)

---

## 🚀 快速开始

### 方式1: Web界面（推荐）⭐

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行Web应用
streamlit run app.py

# 3. 浏览器访问
# 自动打开 http://localhost:8501
```

### 方式2: 命令行

```bash
# 转换数据
python ToJson.py TEST煤矿

# 验证数据
python Validator.py TEST煤矿

# 运行测试
python test.py
```

---

## 🎯 主要功能

### 1. ToJson - 数据转换

**功能**:
- ✅ 自动检测目录中的煤矿
- ✅ 将10个CSV表合并为1个JSON文件
- ✅ 支持多种编码（UTF-8, GBK等）
- ✅ 容错处理（部分表缺失仍可转换）
- ✅ 正确处理空值（转换为null）

**输入**: 10个CSV文件
```
TEST煤矿-采空区基本信息.csv
TEST煤矿-采空区积水信息.csv
...
```

**输出**: 1个JSON文件
```
TEST煤矿-采空区数据集.json
```

### 2. Validator - 数据验证

**功能**:
- ✅ 验证CSV文件（存在性、可读性、字段完整性）
- ✅ 验证JSON文件（结构正确性、无NaN值）
- ✅ 比对CSV和JSON（记录数一致性）
- ✅ 生成详细验证报告

**输出**: 验证报告
```
TEST煤矿-验证报告.txt
```

### 3. test - 单元测试

**功能**:
- ✅ 测试ToJson转换功能
- ✅ 测试Validator验证功能
- ✅ 集成测试（完整工作流程）

---

## 📊 数据格式

### CSV格式（输入）

10个表，每个表一个CSV文件：

| 表名 | 文件名模式 |
|------|-----------|
| 采空区基本信息 | {煤矿名称}-采空区基本信息.csv |
| 采空区积水信息 | {煤矿名称}-采空区积水信息.csv |
| 采空区积气信息 | {煤矿名称}-采空区积气信息.csv |
| 自燃发火信息 | {煤矿名称}-自燃发火信息.csv |
| 采空区悬顶信息 | {煤矿名称}-采空区悬顶信息.csv |
| 采空区塌陷信息 | {煤矿名称}-采空区塌陷信息.csv |
| 地裂缝信息 | {煤矿名称}-地裂缝信息.csv |
| 废弃井筒信息 | {煤矿名称}-废弃井筒信息.csv |
| 密闭墙信息 | {煤矿名称}-密闭墙信息.csv |
| 采空区治理信息 | {煤矿名称}-采空区治理信息.csv |

### JSON格式（输出）

一个煤矿一个JSON文件：

```json
{
  "mine_info": {
    "mine_id": "HX001",
    "mine_name": "TEST煤矿",
    "standard": "KAT 22.2-2024"
  },
  "statistics": {
    "goaf_basic_info": 29,
    "goaf_water_info": 9,
    ...
  },
  "data": {
    "goaf_basic_info": [...],
    "goaf_water_info": [...],
    ...
  }
}
```

---

## 🔧 使用示例

### 示例1: 转换单个煤矿

```bash
# 1. 准备CSV文件
TEST煤矿-采空区基本信息.csv
TEST煤矿-采空区积水信息.csv
...

# 2. 转换
python ToJson.py TEST煤矿

# 3. 验证
python Validator.py TEST煤矿

# 4. 查看结果
TEST煤矿-采空区数据集.json
TEST煤矿-验证报告.txt
```

### 示例2: 批量转换

```bash
# 1. 准备多个煤矿的CSV文件
TEST煤矿-*.csv

# 2. 批量转换
python ToJson.py

# 3. 查看结果
json_output/
└── TEST煤矿-采空区数据集.json
```

### 示例3: Python代码调用

```python
from ToJson import ToJson
from Validator import Validator

# 转换
converter = ToJson()
converter.convert_mine("TEST煤矿", "output.json")

# 验证
validator = Validator()
result = validator.compare_csv_json("TEST煤矿", "output.json")
print(f"转换正确: {result['match']}")
```

---

## 🧪 测试

### 运行测试

```bash
python test.py
```

### 测试内容

**ToJson测试**:
- ✅ 自动检测煤矿
- ✅ 转换单个煤矿
- ✅ JSON文件生成
- ✅ JSON结构正确
- ✅ 无NaN值
- ✅ 空值转换为null

**Validator测试**:
- ✅ CSV验证
- ✅ JSON验证
- ✅ CSV与JSON比对
- ✅ 报告生成

**集成测试**:
- ✅ 完整工作流程（转换→验证→比对）

### 测试结果示例

```
test_01_auto_detect_mines (__main__.TestToJson) ... ok
test_02_convert_mine (__main__.TestToJson) ... ok
test_03_json_file_exists (__main__.TestToJson) ... ok
test_04_json_structure (__main__.TestToJson) ... ok
test_05_no_nan_values (__main__.TestToJson) ... ok
test_06_null_values (__main__.TestToJson) ... ok
test_01_validate_csv (__main__.TestValidator) ... ok
test_02_validate_json (__main__.TestValidator) ... ok
test_03_compare_csv_json (__main__.TestValidator) ... ok
test_04_generate_report (__main__.TestValidator) ... ok
test_full_workflow (__main__.TestIntegration) ... ok

================================================================================
测试总结
================================================================================
运行测试: 11
成功: 11
失败: 0
错误: 0

✅ 所有测试通过！
```

---

## 📚 文档

- **ToJson使用说明.md** - ToJson工具详细使用文档
- **Validator使用说明.md** - Validator工具详细使用文档
- **JSON格式规范-大模型训练版.md** - JSON格式详细说明
- **单位规范说明.md** - 字段单位规范说明

---

## ⚠️ 注意事项

1. **文件命名**: CSV文件必须遵循 `{煤矿名称}-{表名}.csv` 格式
2. **编码格式**: 推荐使用UTF-8编码（工具支持自动检测多种编码）
3. **表名匹配**: 表名必须与Schema定义的10个表名完全一致
4. **空值处理**: 空值会自动转换为JSON的null

---

## 🎯 适用场景

1. ✅ 煤矿采空区普查数据管理
2. ✅ 数据标准化转换
3. ✅ 大模型训练数据准备
4. ✅ 数据质量验证
5. ✅ 批量数据处理

---

## 📞 技术支持

如有问题或建议，请联系数据标准化工作组。

---

**版本**: 1.0.0  
**更新日期**: 2024-12-26  
**维护单位**: 煤矿采空区普查数据标准化工作组

