import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from summarizer import summarize_paper
from unittest.mock import patch, MagicMock

def test_summarize_paper_basic():
    sample_paper = {
        "title": "Time Series Forecasting with Deep Learning",
        "summary": "This paper discusses novel transformer architectures for forecasting."
    }

    system_prompt = "Please summarize the following paper in one or two sentences."

    # 构造 mock 的返回结构，模拟 .choices[0].message.content
    mock_choice = MagicMock()
    mock_choice.message.content = "This paper introduces transformer-based models for improved time series forecasting."

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    with patch("summarizer.openai.ChatCompletion.create", return_value=mock_response) as mock_create:
        result = summarize_paper(sample_paper, system_prompt)

    assert isinstance(result, str)
    assert "transformer" in result.lower()
    assert mock_create.called
