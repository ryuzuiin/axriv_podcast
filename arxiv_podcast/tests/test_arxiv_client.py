import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from arxiv_client import fetch_arxiv_papers
from unittest.mock import MagicMock

def test_fetch_arxiv_papers_mocked():
    # 创建模拟结果对象
    mock_result = MagicMock()
    mock_result.title = "Test Paper Title"
    mock_result.summary = "This is a test paper summary."
    mock_result.published = datetime.datetime(2024, 12, 1)
    mock_result.authors = [MagicMock(name="Alice"), MagicMock(name="Bob")]
    mock_result.authors[0].name = "Alice"
    mock_result.authors[1].name = "Bob"
    mock_result.pdf_url = "http://arxiv.org/pdf/test.pdf"
    mock_result.entry_id = "http://arxiv.org/abs/1234.56789v1"
    
    # 模拟 Client 的 results 方法
    mock_client = MagicMock()
    mock_client.results.return_value = [mock_result]
    
    # 直接传入模拟的客户端，而不是使用 patch
    papers = fetch_arxiv_papers(
        query="test",
        max_results=1,
        categories=["cs.LG"],
        sort_by="submittedDate",
        sort_order="descending",
        client=mock_client  # 使用依赖注入方式传入模拟对象
    )
    
    assert isinstance(papers, list)
    assert len(papers) == 1
    paper = papers[0]
    assert paper["title"] == "Test Paper Title"
    assert paper["summary"].startswith("This is a test")
    assert paper["authors"] == ["Alice", "Bob"]
    assert paper["pdf_url"] == "http://arxiv.org/pdf/test.pdf"
    assert paper["published"] == "2024-12-01"
    assert paper["arxiv_id"] == "1234.56789v1"