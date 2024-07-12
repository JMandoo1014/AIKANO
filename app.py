from flask import Flask, render_template, request
from playsound import playsound
from openai import OpenAI
import speech_recognition as sr
from datetime import datetime

# Flask 애플리케이션 생성
app = Flask(__name__)

# OpenAI 설정
client = OpenAI(
    api_key="your-api"
)
model = "gpt-3.5-turbo"

# STT 함수
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("말씀하세요...")
        audio = r.listen(source)
        try:
            said = r.recognize_google_cloud(audio, language='ko-KR')
            print('음성 인식: ' + said)
        except sr.UnknownValueError:
            print('오디오를 이해할 수 없습니다.')
            said = ""
        except sr.RequestError as e:
            print(f'오류 발생: {e}')
            said = ""
    return said

# TTS 함수
def synthesize_speech(text, filename):
    with client.audio.with_streaming_response.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format="mp3",
        speed="1.0"
    ) as response:
        response.stream_to_file(filename)

# 웹 페이지 라우팅
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    text = get_audio()
    conversation_history = [
    {"role": "system", "content": "너는 이름이 AIKANO(아이카노)인 대화형 챗봇이야. 진짜 사람처럼 대화 해줘"}
    ]

    if text.lower() in ["종료", "끝", "그만"]:
        response_text = "대화를 종료합니다."
    elif text:
        # 챗봇 대화
        conversation_history.append({"role": "user", "content": text})
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=conversation_history
            )
            response = completion.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": response})

            # TTS 실행
            date_string = datetime.now().strftime("%Y%m%d%H%M%S")
            speech_file_path = f"TTS/{date_string}.mp3"  # static 폴더에 저장
            synthesize_speech(response, speech_file_path)

            response_text = f"AI 응답: {response}"
            print(f"AI응답 : {response}")

            playsound(speech_file_path)
        except Exception as e:
            response_text = f'오류 발생: {e}'
    else:
        response_text = '음성 인식 실패로 AI 호출이 생략되었습니다.'

    return response_text

if __name__ == '__main__':
    app.run(debug=True)
