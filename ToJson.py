"""
煤矿采空区数据集转换工具 - ToJson
将一个煤矿的多个CSV表转换为一个完整的JSON文件，用于大模型训练

符合: 煤矿采空区普查数据集Schema v1.0.0
版本: 1.0.0
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
import glob

class ToJson:
    """煤矿数据集转换器：CSV → JSON"""
    
    # 表名映射（中文 → 英文）
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
    
    def __init__(self, data_dir: str = "."):
        """
        初始化转换器
        
        Args:
            data_dir: CSV文件所在目录
        """
        self.data_dir = Path(data_dir)
    
    def auto_detect_mines(self) -> List[str]:
        """
        自动检测目录中的煤矿
        
        Returns:
            煤矿名称列表
        """
        mines = set()
        for csv_file in self.data_dir.glob("*-采空区*.csv"):
            # 提取煤矿名称（文件名中第一个"-"之前的部分）
            mine_name = csv_file.stem.split('-')[0]
            mines.add(mine_name)
        
        return sorted(list(mines))
    
    def convert_mine(self, mine_name: str, output_path: Optional[str] = None) -> Dict:
        """
        转换单个煤矿的数据
        
        Args:
            mine_name: 煤矿名称（如"河西联办煤矿"、"盛博煤矿"）
            output_path: 输出JSON文件路径，如果为None则只返回字典
            
        Returns:
            完整的JSON数据字典
        """
        # 初始化结果结构
        result = {
            "mine_info": {
                "mine_name": mine_name,
                "survey_date": "",
                "standard": "KAT 22.2-2024",
                "data_version": "1.0.0"
            },
            "statistics": {},
            "data": {}
        }
        
        # 读取所有表
        mine_id = None
        for table_cn, table_en in self.TABLE_MAPPING.items():
            file_pattern = f"{mine_name}-{table_cn}.csv"
            file_path = self.data_dir / file_pattern
            
            if file_path.exists():
                try:
                    # 尝试多种编码和解析方式
                    df = None
                    for encoding in ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'gb18030']:
                        try:
                            # 使用quoting参数处理字段中的逗号
                            df = pd.read_csv(
                                file_path,
                                encoding=encoding,
                                on_bad_lines='skip',
                                quoting=1,  # QUOTE_ALL
                                skipinitialspace=True
                            )
                            break
                        except:
                            try:
                                # 如果失败，尝试不使用quoting
                                df = pd.read_csv(
                                    file_path,
                                    encoding=encoding,
                                    on_bad_lines='skip'
                                )
                                break
                            except:
                                continue

                    if df is None:
                        raise Exception("无法读取文件，尝试了多种编码和解析方式")

                    # 从第一个表获取mine_id
                    if mine_id is None and 'mine_id' in df.columns and len(df) > 0:
                        mine_id = df['mine_id'].iloc[0]
                        result["mine_info"]["mine_id"] = mine_id

                    # 转换为字典列表，处理NaN值
                    # 将NaN、NaT等转换为None（JSON中的null）
                    records = df.replace({pd.NA: None, pd.NaT: None}).to_dict('records')
                    # 再次确保NaN转为None
                    records = [{k: (None if pd.isna(v) else v) for k, v in record.items()}
                              for record in records]

                    result["data"][table_en] = records
                    result["statistics"][table_en] = len(records)

                    print(f"  ✅ {table_cn}: {len(records)}条记录")

                except Exception as e:
                    print(f"  ⚠️ {table_cn}: 读取失败 - {e}")
                    result["data"][table_en] = []
                    result["statistics"][table_en] = 0
            else:
                # 表不存在，记录为空
                result["data"][table_en] = []
                result["statistics"][table_en] = 0
        
        # 如果没有找到mine_id，使用煤矿名称生成
        if mine_id is None:
            result["mine_info"]["mine_id"] = self._generate_mine_id(mine_name)
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ 已生成: {output_path}")
        
        return result
    
    def batch_convert(self, mine_names: Optional[List[str]] = None, 
                     output_dir: str = "./json_output") -> List[Dict]:
        """
        批量转换多个煤矿
        
        Args:
            mine_names: 煤矿名称列表，如果为None则自动检测
            output_dir: 输出目录
            
        Returns:
            转换结果列表
        """
        # 自动检测煤矿
        if mine_names is None:
            mine_names = self.auto_detect_mines()
            print(f"🔍 自动检测到 {len(mine_names)} 个煤矿: {', '.join(mine_names)}")
        
        if not mine_names:
            print("❌ 未找到任何煤矿数据")
            return []
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        results = []
        for mine_name in mine_names:
            print(f"\n📋 正在转换: {mine_name}")
            try:
                output_file = output_path / f"{mine_name}-采空区数据集.json"
                result = self.convert_mine(mine_name, str(output_file))
                
                total_records = sum(result["statistics"].values())
                results.append({
                    "mine_name": mine_name,
                    "success": True,
                    "file": str(output_file),
                    "record_count": total_records,
                    "tables": len([v for v in result["statistics"].values() if v > 0])
                })
                
            except Exception as e:
                print(f"  ❌ 转换失败: {e}")
                results.append({
                    "mine_name": mine_name,
                    "success": False,
                    "error": str(e)
                })
        
        # 生成批量转换报告
        self._generate_report(results, output_path)
        
        return results
    
    def _generate_mine_id(self, mine_name: str) -> str:
        """
        根据煤矿名称生成mine_id
        
        Args:
            mine_name: 煤矿名称
            
        Returns:
            mine_id
        """
        # 简单实现：取前3个字符的拼音首字母
        # 实际使用时可以根据需要调整
        import re
        # 移除特殊字符
        clean_name = re.sub(r'[^\w]', '', mine_name)
        # 取前几个字符作为ID
        return clean_name[:6].upper() + "001"
    
    def _generate_report(self, results: List[Dict], output_path: Path):
        """生成转换报告"""
        report = []
        report.append("=" * 80)
        report.append("煤矿采空区数据集批量转换报告")
        report.append("=" * 80)
        report.append("")
        
        success_count = sum(1 for r in results if r.get('success'))
        total_count = len(results)
        total_records = sum(r.get('record_count', 0) for r in results if r.get('success'))
        
        report.append(f"总煤矿数: {total_count}")
        report.append(f"成功: {success_count}")
        report.append(f"失败: {total_count - success_count}")
        report.append(f"总记录数: {total_records}")
        report.append("")
        report.append("-" * 80)
        report.append("")
        
        for result in results:
            mine_name = result.get('mine_name')
            if result.get('success'):
                record_count = result.get('record_count', 0)
                tables = result.get('tables', 0)
                file = result.get('file', '')
                report.append(f"✅ {mine_name}")
                report.append(f"   记录数: {record_count}")
                report.append(f"   表数: {tables}/10")
                report.append(f"   文件: {file}")
                report.append("")
            else:
                error = result.get('error', 'Unknown error')
                report.append(f"❌ {mine_name}")
                report.append(f"   错误: {error}")
                report.append("")
        
        report_text = "\n".join(report)
        print("\n" + report_text)
        
        # 保存报告
        with open(output_path / "转换报告.txt", 'w', encoding='utf-8') as f:
            f.write(report_text)


def main():
    """主函数"""
    import sys
    
    # 创建转换器
    converter = ToJson(data_dir=".")
    
    # 如果提供了命令行参数，转换指定煤矿
    if len(sys.argv) > 1:
        mine_name = sys.argv[1]
        output_file = f"{mine_name}-采空区数据集.json"
        print(f"📋 转换单个煤矿: {mine_name}")
        converter.convert_mine(mine_name, output_file)
    else:
        # 否则批量转换所有煤矿
        print("🚀 批量转换模式")
        converter.batch_convert(output_dir="./json_output")


if __name__ == "__main__":
    main()

