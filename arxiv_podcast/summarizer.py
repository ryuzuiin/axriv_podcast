import openai

def summarize_paper(paper, system_prompt, model="gpt-4", output_format=None, api_key=None):
    """
    使用 OpenAI 模型对 arXiv 论文进行摘要。
    参数:
    paper (dict): 包含论文标题和摘要的字典。
    system_prompt (str): 系统角色设定，用于控制摘要风格。
    model (str): 使用的 OpenAI 模型名称。
    output_format (str): 可选，控制输出格式，支持 "markdown", "bullet", "text"。
    api_key (str): 可选，OpenAI API 密钥。
    返回:
    str: 生成的中文摘要内容。
    """
    # 如果提供了 API 密钥，就设置它
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = openai.OpenAI()  # 使用环境变量中的 API 密钥
        
    # 根据 format 参数附加额外说明
    format_hint = {
        "markdown": "请用 Markdown 格式输出。",
        "bullet": "请用项目符号列出要点。",
        "text": ""
    }.get(output_format, "")
    
    prompt = f"""
论文标题：{paper['title']}
论文摘要：
{paper['summary']}
{format_hint}
"""
    
    # 使用新的 API 格式
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    
    # 新 API 返回格式也有变化
    return response.choices[0].message.content.strip()