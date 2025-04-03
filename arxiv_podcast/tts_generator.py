
import azure.cognitiveservices.speech as speechsdk
import os

def synthesize_speech(text, filename, voice="zh-CN-XiaoxiaoNeural"):
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("Azure Speech Key or Region not set.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"[\u2713] 音声生成成功: {filename}")
    else:
        print("[!] 音声生成失败:", result.reason)
        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            print("详细:", cancellation.reason)
            if cancellation.reason == speechsdk.CancellationReason.Error:
                print("错误详情:", cancellation.error_details)
