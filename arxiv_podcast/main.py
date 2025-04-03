import yaml
import os
import json
from datetime import datetime
from arxiv_client import fetch_arxiv_papers
from summarizer import summarize_paper
from tts_generator import synthesize_speech

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    required_keys = ["search", "openai"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"配置文件缺少必要字段：`{key}`")
    return config

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_markdown(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for paper in data:
            f.write(f"# {paper['title']}\n\n")
            f.write(f"**作者：** {', '.join(paper['authors'])}\n\n")
            f.write(f"**发表日期：** {paper['published']}\n\n")
            f.write(f"**PDF链接：** [{paper['pdf_url']}]({paper['pdf_url']})\n\n")
            f.write(f"**摘要内容：**\n\n{paper['summary']}\n\n")
            f.write("---\n\n")

def main():
    config = load_config()
    output_format = config["openai"].get("output_format", "text")

    # Step 1: 获取论文
    papers = fetch_arxiv_papers(
        query=config["search"]["query"],
        max_results=config["search"]["max_results"],
        categories=config["search"]["categories"],
        sort_by=config["search"]["sort_by"],
        sort_order=config["search"]["sort_order"]
    )
    print(f"找到 {len(papers)} 篇论文")
    for i, paper in enumerate(papers):
        print(f"论文 {i+1}: {paper['title']}")

    # Step 2: 要约生成
    summaries = []
    for paper in papers:
        try:
            summary = summarize_paper(
                paper,
                system_prompt=config["openai"]["system_prompt"],
                model=config["openai"]["model"],
                output_format=output_format,
                api_key=config["openai"]["api_key"]
            )
        except Exception as e:
            print(f"[!] 要约失败：{paper['title']}\n{e}")
            summary = "要约失败：发生了错误。"

        # Step 2.5: Azure TTS（可选）
        if config.get("azure_tts", {}).get("use_azure_tts", False):
            audio_output_dir = config["azure_tts"]["output_dir"]
            voice = config["azure_tts"]["voice"]
            os.makedirs(audio_output_dir, exist_ok=True)

            audio_path = os.path.join(audio_output_dir, f"{paper['arxiv_id']}.mp3")
            try:
                synthesize_speech(summary, audio_path, voice=voice)
            except Exception as e:
                print(f"[!] 音声生成失败：{paper['title']}\n{e}")

        # Step 2.6: 保存信息
        summaries.append({
            "title": paper["title"],
            "authors": paper["authors"],
            "published": paper["published"],
            "pdf_url": paper["pdf_url"],
            "summary": summary
        })

    # Step 3: 保存结果
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    json_path = os.path.join(output_dir, f"{timestamp}.json")
    md_path = json_path.replace(".json", ".md")

    save_json(summaries, json_path)

    # 可选保存为 markdown
    if output_format == "markdown":
        save_markdown(summaries, md_path)
        print(f"[✓] 已保存 Markdown 文件：{md_path}")

    print(f"[✓] 完成：共处理 {len(summaries)} 篇论文摘要")
    print(f"[✓] JSON 文件保存在：{json_path}")

if __name__ == "__main__":
    main()
