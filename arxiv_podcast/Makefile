# Makefile for arxiv_podcast project

# 默认目标：运行测试
default: test

# 测试（自动发现 tests/ 中所有 test_*.py）
test:
	pytest -v --tb=short

# 清理 Python 缓存文件
clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -type f -name "*.pyc" -delete

# 格式化代码（可选：需安装 black）
format:
	black .

# 检查代码格式但不修改（只提示）
check-format:
	black --check .

# 一键运行主程序（需手动设置 main.py 路径）
run:
	python main.py
