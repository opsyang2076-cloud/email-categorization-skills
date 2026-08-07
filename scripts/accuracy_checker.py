#!/usr/bin/env python3
"""
准确性检查器 - 验证分类准确性
将自动分类与地面真实值进行比较以测量准确性。
"""

import json
import argparse
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AccuracyChecker:
    """验证分类准确性并计算指标。"""
    
    def __init__(self):
        self.metrics = {}
    
    def compare_classifications(self, 
                                predicted: Dict[str, Dict],
                                ground_truth: Dict[str, Dict]) -> Dict:
        """将预测分类与真实标签进行比较。
        
        Args:
            predicted: 预测的分类结果
            ground_truth: 手动标注的真实类别
            
        Returns:
            包含准确性和指标的字典
        """
        if not predicted or not ground_truth:
            return self._empty_metrics()
        
        # 计算混淆矩阵
        tp = 0  # 真正例
        tn = 0  # 真负例
        fp = 0  # 假正例
        fn = 0  # 假负例
        
        total_samples = 0
        category_stats = {}
        
        for account_name, emails in predicted.items():
            if account_name not in ground_truth:
                continue
                
            for email_id, pred_category in emails.items():
                if email_id not in ground_truth[account_name]:
                    continue
                    
                true_category = ground_truth[account_name][email_id]
                total_samples += 1
                
                # 初始化类别统计
                if true_category not in category_stats:
                    category_stats[true_category] = {'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0}
                
                if pred_category == true_category:
                    tp += 1
                    category_stats[true_category]['tp'] += 1
                else:
                    fp += 1
                    category_stats[true_category]['fp'] += 1
                    fn += 1
                    category_stats[true_category]['fn'] += 1
        
        # 计算指标
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / total_samples if total_samples > 0 else 0
        
        self.metrics = {
            'total_samples': total_samples,
            'true_positives': tp,
            'false_positives': fp,
            'false_negatives': fn,
            'precision': round(precision, 4),
            'recall': round(recall, 4),
            'f1_score': round(f1_score, 4),
            'accuracy': round(accuracy, 4),
            'category_breakdown': category_stats
        }
        
        return self.metrics
    
    def _empty_metrics(self) -> Dict:
        """返回空的指标字典。"""
        return {
            'total_samples': 0,
            'true_positives': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'precision': 0,
            'recall': 0,
            'f1_score': 0,
            'accuracy': 0,
            'category_breakdown': {}
        }
    
    def generate_recommendations(self, metrics: Dict) -> List[str]:
        """基于准确性指标生成改进建议。"""
        recommendations = []
        
        if metrics['precision'] < 0.7:
            recommendations.append(
                "精确率较低 - 检查是否有太多邮件被错误分类到其他类别"
            )
        
        if metrics['recall'] < 0.7:
            recommendations.append(
                "召回率较低 - 检查是否有邮件被遗漏或未正确分类"
            )
        
        if metrics['f1_score'] < 0.6:
            recommendations.append(
                "F1 分数较低 - 建议重新检查分类规则和置信度阈值"
            )
        
        # 检查各类别的性能
        for category, stats in metrics.get('category_breakdown', {}).items():
            if stats['tp'] == 0 and (stats['fp'] > 0 or stats['fn'] > 0):
                recommendations.append(
                    f"类别 '{category}' 未被正确识别 - 检查该类别的关键词和模式"
                )
        
        if not recommendations:
            recommendations.append("分类准确性良好 - 继续监控以保持一致性")
        
        return recommendations
    
    def export_report(self, metrics: Dict, output_path: str):
        """导出准确性报告到 JSON 文件。"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)
        logger.info(f"准确性报告已保存到 {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='验证电子邮件分类准确性',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 比较预测与真实标签
  python accuracy_checker.py --predicted predictions.json --ground-truth labels.json
  
  # 导出报告
  python accuracy_checker.py --predicted predictions.json --ground-truth labels.json --output report.json
        """
    )
    
    parser.add_argument('--predicted', '-p', required=True, help='预测分类 JSON 文件')
    parser.add_argument('--ground-truth', '-g', required=True, help='真实标签 JSON 文件')
    parser.add_argument('--output', '-o', help='输出报告 JSON 文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 加载预测结果
        with open(args.predicted, 'r', encoding='utf-8') as f:
            predicted = json.load(f)
        
        # 加载真实标签
        with open(args.ground_truth, 'r', encoding='utf-8') as f:
            ground_truth = json.load(f)
        
        # 初始化检查器
        checker = AccuracyChecker()
        
        # 比较分类
        metrics = checker.compare_classifications(predicted, ground_truth)
        
        # 生成建议
        recommendations = checker.generate_recommendations(metrics)
        
        # 准备报告
        report = {
            'metrics': metrics,
            'recommendations': recommendations,
            'generated_at': __import__('datetime').datetime.now().isoformat()
        }
        
        # 保存报告
        output_path = args.output or 'accuracy_report.json'
        checker.export_report(report, output_path)
        
        # 打印摘要
        print("\n" + "="*60)
        print("准确性验证摘要")
        print("="*60)
        print(f"总样本数: {metrics['total_samples']}")
        print(f"精确率: {metrics['precision']:.2%}")
        print(f"召回率: {metrics['recall']:.2%}")
        print(f"F1 分数: {metrics['f1_score']:.2%}")
        print(f"准确率: {metrics['accuracy']:.2%}")
        
        print("\n改进建议:")
        for rec in recommendations:
            print(f"  • {rec}")
        
        print(f"\n报告已保存到: {output_path}")
        print("="*60)
        
    except FileNotFoundError:
        logger.error("未找到输入文件")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error("输入文件中的 JSON 无效")
        sys.exit(1)
    except Exception as e:
        logger.error(f"错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
