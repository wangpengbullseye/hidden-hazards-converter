"""
ToDataJson 单元测试
测试ToJson和Validator工具的功能

版本: 1.0.0
"""

import unittest
import json
import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ToJson import ToJson
from Validator import Validator


class TestToJson(unittest.TestCase):
    """测试ToJson转换工具"""
    
    @classmethod
    def setUpClass(cls):
        """测试前准备"""
        cls.mine_name = "河西联办煤矿"
        cls.output_file = f"{cls.mine_name}-采空区数据集.json"
        cls.converter = ToJson()
    
    def test_01_auto_detect_mines(self):
        """测试自动检测煤矿"""
        mines = self.converter.auto_detect_mines()
        self.assertIn(self.mine_name, mines)
        print(f"✅ 检测到煤矿: {mines}")
    
    def test_02_convert_mine(self):
        """测试转换单个煤矿"""
        result = self.converter.convert_mine(self.mine_name, self.output_file)
        
        # 检查结果结构
        self.assertIn("mine_info", result)
        self.assertIn("statistics", result)
        self.assertIn("data", result)
        
        # 检查mine_info
        self.assertEqual(result["mine_info"]["mine_name"], self.mine_name)
        self.assertEqual(result["mine_info"]["standard"], "KAT 22.2-2024")
        
        # 检查是否有数据
        total_records = sum(result["statistics"].values())
        self.assertGreater(total_records, 0)
        
        print(f"✅ 转换成功: {total_records}条记录")
    
    def test_03_json_file_exists(self):
        """测试JSON文件是否生成"""
        self.assertTrue(os.path.exists(self.output_file))
        print(f"✅ JSON文件已生成: {self.output_file}")
    
    def test_04_json_structure(self):
        """测试JSON结构"""
        with open(self.output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查顶层结构
        self.assertIn("mine_info", data)
        self.assertIn("statistics", data)
        self.assertIn("data", data)
        
        # 检查10个表
        expected_tables = [
            "goaf_basic_info", "goaf_water_info", "goaf_gas_info",
            "fire_info", "suspended_roof_info", "collapse_info",
            "crack_info", "abandoned_shaft_info", "seal_wall_info",
            "treatment_info"
        ]
        
        for table in expected_tables:
            self.assertIn(table, data["data"])
        
        print(f"✅ JSON结构正确")
    
    def test_05_no_nan_values(self):
        """测试JSON中不包含NaN"""
        with open(self.output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertNotIn('NaN', content)
        print(f"✅ 无NaN值")
    
    def test_06_null_values(self):
        """测试空值正确转换为null"""
        with open(self.output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查第一条记录
        if data["data"]["goaf_basic_info"]:
            record = data["data"]["goaf_basic_info"][0]
            # 检查是否有None值（JSON中的null）
            has_null = any(v is None for v in record.values())
            self.assertTrue(has_null)
            print(f"✅ 空值正确转换为null")


class TestValidator(unittest.TestCase):
    """测试Validator验证工具"""
    
    @classmethod
    def setUpClass(cls):
        """测试前准备"""
        cls.mine_name = "河西联办煤矿"
        cls.json_file = f"{cls.mine_name}-采空区数据集.json"
        cls.validator = Validator()
    
    def test_01_validate_csv(self):
        """测试CSV验证"""
        result = self.validator.validate_csv(self.mine_name)
        
        self.assertEqual(result["mine_name"], self.mine_name)
        self.assertGreater(result["found_tables"], 0)
        self.assertGreater(result["total_records"], 0)
        
        print(f"✅ CSV验证: {result['found_tables']}/10表, {result['total_records']}条记录")
    
    def test_02_validate_json(self):
        """测试JSON验证"""
        result = self.validator.validate_json(self.json_file)
        
        self.assertTrue(result["valid"])
        self.assertGreater(result["total_records"], 0)
        
        print(f"✅ JSON验证: 有效, {result['total_records']}条记录")
    
    def test_03_compare_csv_json(self):
        """测试CSV与JSON比对"""
        result = self.validator.compare_csv_json(self.mine_name, self.json_file)
        
        self.assertTrue(result["match"])
        
        print(f"✅ CSV与JSON比对: 一致")
    
    def test_04_generate_report(self):
        """测试生成报告"""
        csv_result = self.validator.validate_csv(self.mine_name)
        json_result = self.validator.validate_json(self.json_file)
        compare_result = self.validator.compare_csv_json(self.mine_name, self.json_file)
        
        report = self.validator.generate_report(csv_result, json_result, compare_result)
        
        self.assertIn("数据集验证报告", report)
        self.assertIn("CSV文件验证", report)
        self.assertIn("JSON文件验证", report)
        
        print(f"✅ 报告生成成功")


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        mine_name = "河西联办煤矿"
        json_file = f"{mine_name}-采空区数据集.json"
        
        # 1. 转换
        converter = ToJson()
        result = converter.convert_mine(mine_name, json_file)
        total_records = sum(result["statistics"].values())
        
        # 2. 验证
        validator = Validator()
        csv_result = validator.validate_csv(mine_name)
        json_result = validator.validate_json(json_file)
        compare_result = validator.compare_csv_json(mine_name, json_file)
        
        # 3. 断言
        self.assertGreater(total_records, 0)
        self.assertTrue(json_result["valid"])
        self.assertTrue(compare_result["match"])
        
        print(f"✅ 完整工作流程测试通过")
        print(f"   - 转换: {total_records}条记录")
        print(f"   - 验证: JSON有效")
        print(f"   - 比对: CSV与JSON一致")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestToJson))
    suite.addTests(loader.loadTestsFromTestCase(TestValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print("\n❌ 部分测试失败！")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())

