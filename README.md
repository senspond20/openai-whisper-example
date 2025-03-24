
## INSTALL

pip install torch torch-audio openai-whisper

## 실행예시

```
python main.py <오디오파일경로> --model <모델> --output <저장경로>
```

> sample_audio.mp3 오디오 파일을 medium 모델로 result.txt에 저장

```
python main.py sample_audio.mp3 --model medium --output result.txt
```
