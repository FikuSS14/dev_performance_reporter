import argparse
import csv
from typing import List, Dict, Any

def parse_args():
    parser = argparse.ArgumentParser(description="Generate performance reports from CSV files.")
    parser.add_argument('--files', nargs='+', required=True, help='Paths to CSV files')
    parser.add_argument('--report', choices=['performance'], required=True, help='Type of report to generate')
    return parser.parse_args()

class ReportGenerator:
    def __init__(self):
        self.data = [] 

    def load_files(self, file_paths: List[str]):
        """Загружает данные из всех CSV-файлов"""
        for file_path in file_paths:
            try:
                with open(file_path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if 'performance' in row:
                            row['performance'] = float(row['performance'])
                        self.data.append(row)
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")
            except Exception as e:
                raise ValueError(f"Error reading file {file_path}: {e}")

    def generate_performance_report(self) -> List[Dict[str, Any]]:
        """Группирует данные по позиции и считает среднюю эффективность"""
        position_stats = {}
        for row in self.data:
            pos = row['position']
            perf = row['performance']
            if pos not in position_stats:
                position_stats[pos] = {'total': 0, 'count': 0}
            position_stats[pos]['total'] += perf
            position_stats[pos]['count'] += 1

        result = []
        for pos, stats in position_stats.items():
            avg_perf = stats['total'] / stats['count']
            result.append({
                'position': pos,
                'average_performance': round(avg_perf, 2)
            })

        result.sort(key=lambda x: x['average_performance'], reverse=True)
        return result

def main():
    args = parse_args()
    generator = ReportGenerator()

    try:
        generator.load_files(args.files)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    if args.report == 'performance':
        report_data = generator.generate_performance_report()
        headers = ["Position", "Average Performance"]
        table_data = [[row['position'], row['average_performance']] for row in report_data]
        
        from tabulate import tabulate
        print("\nPerformance Report:")
        print(tabulate(table_data, headers=headers, tablefmt="grid", floatfmt=".2f"))
    else:
        print(f"Unknown report type: {args.report}")

if __name__ == "__main__":
    main()