"""工具函数测试。"""

import unittest
import os
import tempfile
from datetime import datetime
from pathlib import Path
import sys

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from utils import (
    load_config,
    save_config,
    format_email_date,
    sanitize_filename,
    generate_timestamp,
    truncate_string,
    merge_configs,
    calculate_statistics,
    validate_email
)


class TestUtils(unittest.TestCase):
    """工具函数测试类。"""
    
    def test_validate_email(self):
        """测试电子邮件验证。"""
        self.assertTrue(validate_email('test@example.com'))
        self.assertTrue(validate_email('user.name@domain.co.uk'))
        self.assertFalse(validate_email('invalid-email'))
        self.assertFalse(validate_email('@example.com'))
        self.assertFalse(validate_email(''))
        
    def test_truncate_string(self):
        """测试字符串截断。"""
        # 测试截断
        long_text = 'a' * 1000
        result = truncate_string(long_text, 500)
        self.assertEqual(len(result), 503)  # 500 + '...'
        
        # 测试不截断
        short_text = 'short'
        result = truncate_string(short_text, 500)
        self.assertEqual(result, 'short')
        
    def test_sanitize_filename(self):
        """测试文件名清理。"""
        # 测试清理不安全字符
        self.assertEqual(sanitize_filename('test/file:*.txt'), 'test_file_*.txt')
        self.assertEqual(sanitize_filename('normal.txt'), 'normal.txt')
        
        # 测试长度限制
        long_name = 'a' * 200
        result = sanitize_filename(long_name)
        self.assertEqual(len(result), 100)
        
    def test_format_email_date(self):
        """测试日期格式化。"""
        # 测试标准格式
        result = format_email_date('2024-01-15T10:00:00')
        self.assertIn('2024-01-15', result)
        
        # 测试无效日期
        result = format_email_date('invalid-date')
        self.assertEqual(result, 'invalid-date')
        
        # 测试空日期
        result = format_email_date('')
        self.assertIn('1970', result)  # 返回当前时间
        
    def test_generate_timestamp(self):
        """测试时间戳生成。"""
        timestamp = generate_timestamp()
        self.assertIn('-', timestamp)  # ISO 格式应包含 '-'
        self.assertIn('T', timestamp)  # ISO 格式应包含 'T'
        
    def test_merge_configs(self):
        """测试配置合并。"""
        base = {'a': 1, 'b': 2, 'nested': {'x': 1}}
        override = {'b': 3, 'c': 4}
        result = merge_configs(base, override)
        
        self.assertEqual(result['a'], 1)
        self.assertEqual(result['b'], 3)  # override 优先
        self.assertEqual(result['c'], 4)
        
    def test_calculate_statistics(self):
        """测试统计计算。"""
        # 测试非空列表
        values = [1, 2, 3, 4, 5]
        stats = calculate_statistics(values)
        self.assertEqual(stats['count'], 5)
        self.assertEqual(stats['sum'], 15)
        self.assertEqual(stats['mean'], 3.0)
        self.assertEqual(stats['min'], 1)
        self.assertEqual(stats['max'], 5)
        
        # 测试空列表
        stats = calculate_statistics([])
        self.assertEqual(stats['count'], 0)
        
    def test_load_config(self):
        """测试配置加载。"""
        # 测试文件不存在
        result = load_config('/nonexistent/path.yaml')
        self.assertEqual(result, {})
        
        # 测试有效文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('key: value\n')
            temp_path = f.name
        
        try:
            result = load_config(temp_path)
            self.assertEqual(result['key'], 'value')
        finally:
            os.unlink(temp_path)
            
    def test_save_config(self):
        """测试配置保存。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, 'test.yaml')
            save_config({'test': 'data'}, config_path)
            
            self.assertTrue(os.path.exists(config_path))
            
            with open(config_path, 'r') as f:
                content = f.read()
            self.assertIn('test: data', content)


if __name__ == '__main__':
    unittest.main()
