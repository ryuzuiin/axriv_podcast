# 🎧 arXiv論文自動音声化ツール｜個人開発メモ

## 🧠 これは何？

個人的に開発した、**arXiv論文を自動でTTS音声化するシステム**です。  
最新のAI論文を「読む」のではなく「聞く」ことで、**通勤中や移動中でも論文をインプットできるように**したいと思い、作り始めました。

---

## 🔁 現在の処理フロー

```mermaid
graph TD
A[arXivの最新論文を自動取得] --> B[要約＋中国語に翻訳]
B --> C[TTS（Text-to-Speech）で音声生成]
C --> D[音声ファイル（mp3）を保存]
論文は自動で毎日クロール（主にAI/ML/NLP分野）
要約・翻訳は日本語/中国語ベースで処理
TTSは中国語ナレーションに対応（現在）
🔊 サンプル

対象論文：Instruction Tuning for Mathematical Reasoning
生成音声：./output/instruction_tuning_math_cn.mp3
要約抜粋（中国語）：
本论文提出了一种使用指令微调提升大模型数学推理能力的方法……
🧩 改善したい点（今後やりたいこと）

1. 論文の選定ロジック
今は「新着順」取得のみ
有益でない論文（いわゆる水文）も多く含まれる
✅ 将来的には：
SNSや引用数に基づく注目度フィルタ
専門家や研究者の推薦論文リスト
自分用の「読みたいテーマ」キーワード抽出
2. 多言語対応
現在は中国語音声のみ
✅ 日本語TTS、英語TTSへの拡張予定
🤖 Whisperを使った日→英 or 英→中の自動補完も検討中
3. 要約精度
現在はChatGPT APIによる抽象的な要約
✅ 将来的に：
ペーパー構造を考慮したセクション別要約
より自然な「聴き言葉」への最適化
4. 配信手段
ローカルでMP3保存＋手動で再生
✅ Podcast形式で自動配信（RSS生成）
✅ Web UIで再生・履歴管理（Flask + React予定）
💡 想定ユースケース（自分用）

朝の通勤中に、前日に出た論文を1本聞く
論文の内容をざっくり把握して、読む価値があるか判断
ブログ記事や技術スライドの種を探す
毎週末、自分の論文音声ログをまとめる
🛠 技術スタック（参考）

arxiv + BeautifulSoup：論文自動取得
ChatGPT API：論文要約（テンプレあり）
TTS（Azure-TTSなど）：音声生成（中国語ナレーション）
ffmpeg：音声整形、長さ調整
cron：定期実行
今後：FastAPI / Flask + React でUI構築予定
🚀 これからどうしたい？

週1本の精読＋音声アーカイブを習慣にする
自分だけの「AI音声論文ライブラリ」を作りたい
精度・品質が安定すれば、身近な友人や同僚にもシェア予定
📬 おまけ（作ってよかったこと）

論文を読むハードルが下がった
英語のabstractに触れる頻度が自然と増えた
“読む前に聴く”という新しい習慣ができた
