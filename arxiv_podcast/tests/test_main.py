import sys
import os
import tempfile
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from main import main

@patch("main.fetch_arxiv_papers")
@patch("main.summarize_paper")
def test_main_pipeline(mock_summarize, mock_fetch):
    # 模拟 arxiv 返回
    mock_fetch.return_value = [{
        "title": "Test Paper",
        "summary": "Test summary",
        "published": "2024-01-01",
        "authors": ["Alice", "Bob"],
        "pdf_url": "http://arxiv.org/pdf/test.pdf"
    }]
    
    # 模拟 ChatGPT 返回摘要
    mock_summarize.return_value = "这是一篇测试论文的摘要内容。"
    
    # 替换 config.yaml 内容
    with patch("main.load_config") as mock_config:
        mock_config.return_value = {
            "search": {
                "query": "test",
                "max_results": 1,
                "categories": ["cs.LG"],
                "sort_by": "submittedDate",
                "sort_order": "descending"
            },
            "openai": {
                "model": "gpt-4",
                "system_prompt": "请用中文总结以下论文。",
                "output_format": "markdown"
            }
        }
        
        # 创建临时 outputs 目录
        temp_dir = tempfile.mkdtemp()
        
        # 模拟 os.makedirs 和保存函数，以便追踪保存的文件
        with patch("os.makedirs") as mock_makedirs:
            with patch("main.save_json") as mock_save_json:
                with patch("main.save_markdown") as mock_save_markdown:
                    # 执行主程序
                    main()
                    
                    # 验证调用
                    mock_makedirs.assert_called_once()
                    mock_save_json.assert_called_once()
                    mock_save_markdown.assert_called_once()
                    
                    # 可以进一步验证传递给保存函数的参数
                    args, _ = mock_save_json.call_args
                    data = args[0]
                    assert len(data) == 1
                    assert data[0]["title"] == "Test Paper"
                    assert data[0]["summary"] == "这是一篇测试论文的摘要内容。"
        
        # 清理临时目录
        shutil.rmtree(temp_dir)