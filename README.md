

## INSTALL

pip install torch torch-audio openai-whisper

또는 

pip install -r requirements.txt


## 실행예시 

```
python transcriber.py <오디오파일경로> --model <모델> --output <저장경로>
```

>  sample_audio.mp3 오디오 파일을 medium 모델로 result.txt에 저장

```
python transcriber.py sample_audio.mp3 --model medium --output result.txt
```
