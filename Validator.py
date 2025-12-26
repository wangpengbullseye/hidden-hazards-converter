"""
数据集验证工具 - Validator
检查CSV文件和JSON文件是否符合Schema定义，以及转换是否正确

版本: 1.0.0
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys

class Validator:
    """数据集验证器"""
    
    # 表名映射
    TABLE_MAPPING = {
        "采空区基本信息": "goaf_basic_info",
        "采空区积水信息": "goaf_water_info",
        "采空区积气信息": "goaf_gas_info",
        "自燃发火信息": "fire_info",
        "采空区悬顶信息": "suspended_roof_info",
        "采空区塌陷信息": "collapse_info",
        "地裂缝信息": "crack_info",
        "废弃井筒信息": "abandoned_shaft_info",
        "密闭墙信息": "seal_wall_info",
        "采空区治理信息": "treatment_info"
    }
    
    def __init__(self, schema_path: str = "煤矿采空区普查数据集Schema.json"):
        """
        初始化验证器
        
        Args:
            schema_path: Schema文件路径
        """
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
        
        # 构建表定义字典
        self.tables = {table['table_id']: table for table in self.schema['tables']}
        self.table_name_map = {table['table_name']: table for table in self.schema['tables']}
    
    def validate_csv(self, mine_name: str, data_dir: str = ".") -> Dict:
        """
        验证CSV文件
        
        Args:
            mine_name: 煤矿名称
            data_dir: CSV文件目录
            
        Returns:
            验证结果
        """
        print(f"\n📋 验证CSV文件: {mine_name}")
        print("=" * 80)
        
        data_path = Path(data_dir)
        results = {
            "mine_name": mine_name,
            "total_tables": 10,
            "found_tables": 0,
            "total_records": 0,
            "errors": [],
            "warnings": [],
            "table_details": {}
        }
        
        for table_cn, table_en in self.TABLE_MAPPING.items():
            file_path = data_path / f"{mine_name}-{table_cn}.csv"
            
            if file_path.exists():
                try:
                    # 尝试读取CSV
                    df = None
                    for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']:
                        try:
                            df = pd.read_csv(file_path, encoding=encoding, on_bad_lines='skip')
                            break
                        except:
                            continue
                    
                    if df is None:
                        results["errors"].append(f"{table_cn}: 无法读取文件")
                        continue
                    
                    results["found_tables"] += 1
                    results["total_records"] += len(df)
                    
                    # 获取Schema定义
                    table_schema = self.table_name_map.get(table_cn)
                    if table_schema:
                        # 检查字段
                        schema_fields = {f['name'] for f in table_schema['fields']}
                        csv_fields = set(df.columns)
                        
                        missing = schema_fields - csv_fields
                        extra = csv_fields - schema_fields
                        
                        if missing:
                            results["warnings"].append(f"{table_cn}: 缺少字段 {missing}")
                        if extra:
                            results["warnings"].append(f"{table_cn}: 多余字段 {extra}")
                    
                    results["table_details"][table_cn] = {
                        "records": len(df),
                        "fields": len(df.columns),
                        "status": "✅"
                    }
                    
                    print(f"  ✅ {table_cn}: {len(df)}条记录, {len(df.columns)}个字段")
                    
                except Exception as e:
                    results["errors"].append(f"{table_cn}: {str(e)}")
                    print(f"  ❌ {table_cn}: {str(e)}")
            else:
                results["table_details"][table_cn] = {
                    "records": 0,
                    "fields": 0,
                    "status": "⚠️ 文件不存在"
                }
                print(f"  ⚠️ {table_cn}: 文件不存在")
        
        return results
    
    def validate_json(self, json_path: str) -> Dict:
        """
        验证JSON文件
        
        Args:
            json_path: JSON文件路径
            
        Returns:
            验证结果
        """
        print(f"\n📋 验证JSON文件: {json_path}")
        print("=" * 80)
        
        results = {
            "file": json_path,
            "valid": True,
            "total_records": 0,
            "errors": [],
            "warnings": [],
            "table_details": {}
        }
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查顶层结构
            required_keys = ['mine_info', 'statistics', 'data']
            for key in required_keys:
                if key not in data:
                    results["errors"].append(f"缺少顶层字段: {key}")
                    results["valid"] = False
            
            if not results["valid"]:
                return results
            
            # 检查每个表
            for table_cn, table_en in self.TABLE_MAPPING.items():
                if table_en in data['data']:
                    records = data['data'][table_en]
                    record_count = len(records)
                    results["total_records"] += record_count
                    
                    # 检查是否包含NaN
                    json_str = json.dumps(records)
                    if 'NaN' in json_str:
                        results["errors"].append(f"{table_cn}: 包含NaN值（应为null）")
                    
                    # 检查统计数是否一致
                    if table_en in data['statistics']:
                        stat_count = data['statistics'][table_en]
                        if stat_count != record_count:
                            results["warnings"].append(
                                f"{table_cn}: 统计数({stat_count})与实际记录数({record_count})不一致"
                            )
                    
                    results["table_details"][table_cn] = {
                        "records": record_count,
                        "status": "✅"
                    }
                    
                    print(f"  ✅ {table_cn}: {record_count}条记录")
                else:
                    results["warnings"].append(f"{table_cn}: 表不存在")
                    results["table_details"][table_cn] = {
                        "records": 0,
                        "status": "⚠️ 不存在"
                    }
                    print(f"  ⚠️ {table_cn}: 表不存在")
            
        except Exception as e:
            results["errors"].append(f"读取JSON失败: {str(e)}")
            results["valid"] = False
            print(f"  ❌ 读取失败: {str(e)}")
        
        return results
    
    def compare_csv_json(self, mine_name: str, json_path: str, csv_dir: str = ".") -> Dict:
        """
        比对CSV和JSON，检查转换是否正确
        
        Args:
            mine_name: 煤矿名称
            json_path: JSON文件路径
            csv_dir: CSV文件目录
            
        Returns:
            比对结果
        """
        print(f"\n🔍 比对CSV与JSON: {mine_name}")
        print("=" * 80)
        
        results = {
            "mine_name": mine_name,
            "match": True,
            "errors": [],
            "warnings": [],
            "table_comparison": {}
        }
        
        # 读取JSON
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except Exception as e:
            results["errors"].append(f"无法读取JSON: {str(e)}")
            results["match"] = False
            return results
        
        # 比对每个表
        csv_path = Path(csv_dir)
        for table_cn, table_en in self.TABLE_MAPPING.items():
            csv_file = csv_path / f"{mine_name}-{table_cn}.csv"
            
            csv_count = 0
            json_count = 0
            
            # CSV记录数
            if csv_file.exists():
                try:
                    df = None
                    for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']:
                        try:
                            df = pd.read_csv(csv_file, encoding=encoding, on_bad_lines='skip')
                            break
                        except:
                            continue
                    if df is not None:
                        csv_count = len(df)
                except:
                    pass
            
            # JSON记录数
            if table_en in json_data.get('data', {}):
                json_count = len(json_data['data'][table_en])
            
            # 比对
            match = (csv_count == json_count)
            if not match:
                results["match"] = False
                results["errors"].append(
                    f"{table_cn}: CSV({csv_count}条) != JSON({json_count}条)"
                )
                status = "❌"
            else:
                status = "✅"
            
            results["table_comparison"][table_cn] = {
                "csv_records": csv_count,
                "json_records": json_count,
                "match": match,
                "status": status
            }
            
            print(f"  {status} {table_cn}: CSV={csv_count}, JSON={json_count}")
        
        return results
    
    def generate_report(self, csv_result: Dict, json_result: Dict, compare_result: Dict) -> str:
        """生成验证报告"""
        report = []
        report.append("=" * 80)
        report.append("数据集验证报告")
        report.append("=" * 80)
        report.append("")
        
        # CSV验证结果
        report.append("📋 CSV文件验证")
        report.append("-" * 80)
        report.append(f"煤矿: {csv_result['mine_name']}")
        report.append(f"找到表: {csv_result['found_tables']}/{csv_result['total_tables']}")
        report.append(f"总记录数: {csv_result['total_records']}")
        if csv_result['errors']:
            report.append(f"错误: {len(csv_result['errors'])}个")
            for error in csv_result['errors']:
                report.append(f"  ❌ {error}")
        if csv_result['warnings']:
            report.append(f"警告: {len(csv_result['warnings'])}个")
            for warning in csv_result['warnings']:
                report.append(f"  ⚠️ {warning}")
        report.append("")
        
        # JSON验证结果
        report.append("📋 JSON文件验证")
        report.append("-" * 80)
        report.append(f"文件: {json_result['file']}")
        report.append(f"有效: {'✅ 是' if json_result['valid'] else '❌ 否'}")
        report.append(f"总记录数: {json_result['total_records']}")
        if json_result['errors']:
            report.append(f"错误: {len(json_result['errors'])}个")
            for error in json_result['errors']:
                report.append(f"  ❌ {error}")
        if json_result['warnings']:
            report.append(f"警告: {len(json_result['warnings'])}个")
            for warning in json_result['warnings']:
                report.append(f"  ⚠️ {warning}")
        report.append("")
        
        # 比对结果
        report.append("🔍 CSV与JSON比对")
        report.append("-" * 80)
        report.append(f"转换正确: {'✅ 是' if compare_result['match'] else '❌ 否'}")
        if compare_result['errors']:
            report.append(f"差异: {len(compare_result['errors'])}个")
            for error in compare_result['errors']:
                report.append(f"  ❌ {error}")
        report.append("")
        
        # 总结
        report.append("=" * 80)
        all_ok = (
            not csv_result['errors'] and 
            json_result['valid'] and 
            compare_result['match']
        )
        if all_ok:
            report.append("✅ 验证通过！CSV和JSON数据一致，转换正确。")
        else:
            report.append("❌ 验证失败！请检查上述错误和警告。")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python Validator.py <煤矿名称>")
        print("  python Validator.py 河西联办煤矿")
        sys.exit(1)
    
    mine_name = sys.argv[1]
    json_file = f"{mine_name}-采空区数据集.json"
    
    # 创建验证器
    validator = Validator()
    
    # 验证CSV
    csv_result = validator.validate_csv(mine_name)
    
    # 验证JSON
    json_result = validator.validate_json(json_file)
    
    # 比对CSV和JSON
    compare_result = validator.compare_csv_json(mine_name, json_file)
    
    # 生成报告
    report = validator.generate_report(csv_result, json_result, compare_result)
    print("\n" + report)
    
    # 保存报告
    with open(f"{mine_name}-验证报告.txt", 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📄 报告已保存: {mine_name}-验证报告.txt")


if __name__ == "__main__":
    main()

