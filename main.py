import whisper
import torch
import gc
import os
import argparse
from decorator import singleton

@singleton
class WhisperTranscriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(name=model_size)

    def format_time(self, time: float) -> str:
        minutes = int(time // 60)
        seconds = int(time % 60)
        return f"{minutes:02}:{seconds:02}"

    def transcribe(self, file_path: str):
        response = self.model.transcribe(audio=file_path)
        segments = response.get("segments", [])
        results = []

        if not segments:
            print("음성 데이터를 찾을 수 없습니다.")
            return

        for seg in segments:
            start = self.format_time(seg["start"])
            end = self.format_time(seg["end"])
            text = seg["text"]
            print(f"{start} ~ {end} : {text}")
            results.append(f"{start} ~ {end} : {text}")

        return results

    def save_file(self, results, output_path="transcription.txt"):
        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write("\n".join(results))
            print(f"✅ 결과가 {output_path}에 저장되었습니다.")
        except Exception as e:
            print(f"❗️ 파일 저장 중 오류 발생: {e}")

    def release_resources(self):
        """명시적 메모리 해제"""
        if hasattr(self, "model"):
            del self.model
        torch.cuda.empty_cache()
        gc.collect()

    def __del__(self):
        self.release_resources()


if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(description="Whisper Transcriber")

    parser.add_argument("audio_file", type=str, help="변환할 오디오 파일 경로")
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "medium", "large"],
        help="Whisper 모델 크기 선택",
    )
    parser.add_argument(
        "--output", type=str, default="transcription.txt", help="결과 파일 저장 경로"
    )

    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"❗️ 오디오 파일을 찾을 수 없습니다: {args.audio_file}")
        sys.exit(1)

    wc = WhisperTranscriber(model_size=args.model)
    results = wc.transcribe(args.audio_file)

    if results:
        wc.save_file(results, args.output)

    # 메모리 해제
    wc.release_resources()
