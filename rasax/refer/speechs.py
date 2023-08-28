#https://pypi.org/project/SpeechRecognition/

import speech_recognition as sr
# speech_recognition là phương thức tốt nhất
#-----------------------------------------------------------------------------------------
def C1():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
            print("Hãy nói gì đó...")
            audio = r.listen(source)
            text = r.recognize_google(audio,show_all=True, language='vi-VN')
            print(text)
            
#-----------------------------------------------------------------------------------------
def C2():
    r = sr.Recognizer()
    # Callback function được gọi mỗi khi có giọng nói được nhận diện
    def callback(recognizer, audio):
        try:
            # Nhận diện giọng nói từ tín hiệu âm thanh
            text = recognizer.recognize_google(audio,show_all=True, language='vi-VN')
            print(text)
        except sr.UnknownValueError:
            print("Không nhận diện được giọng nói")
        except sr.RequestError as e:
            print("Không thể kết nối đến Google API; {0}".format(e))
    # Lắng nghe tín hiệu âm thanh từ microphone trong nền
    stop_listening = r.listen_in_background(sr.Microphone(), callback)
    # Dừng quá trình lắng nghe bằng cách gọi hàm stop_listening()
    input("Nhấn Enter để dừng quá trình lắng nghe...")
    stop_listening(wait_for_stop=False)
    
#-----------------------------------------------------------------------------------------
def C3():
    #Tải API google cloud dưới dạng file json
    # Google Cloud Speech-to-Text API
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hãy nói gì đó...")
        audio = r.listen(source)
    text = r.recognize_google_cloud(audio_data=audio,
                                    credentials_json="path//.json",
                                    language="vi-VN",
                                    preferred_phrases="one",
                                    show_all=False)
    print(text)
    
#-----------------------------------------------------------------------------------------
def C4():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Hãy nói gì đó...")
        audio = r.record(source)
        text = r.recognize_google(audio,show_all=True, language='vi-VN')
        print(text)
        
#-----------------------------------------------------------------------------------------
def C5():
    #Không hỗ trợ vi-VN
    r = sr.Recognizer()
    with sr.Microphone() as source:
            print("Hãy nói gì đó...")
            audio = r.listen(source)
    try:
            text = r.recognize_sphinx(audio, language='en-US')
            print("Tôi: ",end="")
            print(text)
    except sr.UnknownValueError:
            print("Không thể nhận dạng giọng nói")
    except sr.RequestError as e:
            print("Lỗi kết nối tới API: {0}".format(e))
            
#-----------------------------------------------------------------------------------------
def C6():
    #API của Amazon
    r = sr.Recognizer()
    with sr.AudioFile('audio_file.wav') as source:
        audio_data = r.record(source)  
        # Thiết lập thông tin chứng thực Amazon Web Services
        aws_access_key_id = 'your_aws_access_key_id'
        aws_secret_access_key = 'your_aws_secret_access_key'
        region_name = 'your_aws_region'
        
        # Sử dụng hàm recognize_amazon() để chuyển đổi âm thanh thành văn bản
        text = r.recognize_amazon(audio_data=audio_data, 
                                  access_key_id= aws_access_key_id, 
                                  secret_access_key= aws_secret_access_key, 
                                  region=region_name, 
                                  language='en-US')

        print(text)
            
#-----------------------------------------------------------------------------------------
def C7():
    # API
    # Thiết lập subscription key cho dịch vụ nhận dạng giọng nói của Microsoft Bing Speech API
    subscription_key = 'your_subscription_key'
    r = sr.Recognizer()
    with sr.AudioFile('audio_file.wav') as source:
        audio_data = r.record(source)  
         # Sử dụng hàm recognize_bing() để chuyển đổi âm thanh thành văn bản
        text = r.recognize_bing(audio_data, key=subscription_key, language='en-US')
        # In văn bản
        print(text)
#-----------------------------------------------------------------------------------------
def C8():
    # API
    r = sr.Recognizer()
    with sr.AudioFile('audio_file.wav') as source:
        audio_data = r.record(source) 
        #Sử dụng Houndify API cho việc nhận dạng giọng nói tiếng Việt
        #Lưu ý rằng bạn cần thay thế giá trị của client_id và client_key bằng giá trị tương ứng của tài khoản Houndify của bạn
        text = r.recognize_houndify(audio_data, client_id='<your-client-id>', client_key='<your-client-key>', language='vi-VN')

#-----------------------------------------------------------------------------------------
def C9():
    #Ngôn ngữ en-US
    from pocketsphinx import LiveSpeech
    for phrase in LiveSpeech(): print(phrase)
    
    #Nhận diện key
    for phrase in LiveSpeech(lm=False, keyphrase='hello', kws_threshold=1e-20, verbose=False, sampling_rate=16000):
        print(phrase.segments(detailed=True))

        
# def C10():
#      Lệnh trên cmd
#     pip install git+https://github.com/openai/whisper.git
#     sudo apt update && sudo apt install ffmpeg
#     whisper "/content/Hello.mp3" --model medium.en       
#-----------------------------------------------------------------------------------------

# DeepSpeech: Đây là một dự án mã nguồn mở của Mozilla, cung cấp một mô hình chuyển đổi giọng nói thành văn bản có thể được huấn luyện lại cho các mục đích cụ thể. DeepSpeech sử dụng mạng nơ-ron học sâu để chuyển đổi âm thanh thành văn bản và có thể được sử dụng trên nhiều nền tảng khác nhau.

#-----------------------------------------------------------------------------------------

# Kaldi: Đây là một nền tảng mã nguồn mở và công cụ để thực hiện các nhiệm vụ xử lý tiếng nói, bao gồm chuyển đổi âm thanh thành văn bản. Kaldi có thể được sử dụng để xây dựng các ứng dụng nhận dạng giọng nói cho các mục đích khác nhau.
#-----------------------------------------------------------------------------------------   