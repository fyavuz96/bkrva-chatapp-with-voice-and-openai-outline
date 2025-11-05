from openai import OpenAI
import requests

openai_client = OpenAI()


def speech_to_text(audio_binary):
    # Set up Watson Speech-to-Text HTTP Api url
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    # Set up parameters for our HTTP request
    params = {
        'model': 'en-US_Multimedia',
    }
    # Set up the body of our HTTP request
    body = audio_binary
    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()
    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text

def text_to_speech(text, voice=""):
    # Watson Metinden Sese HTTP Api url'sini ayarlayın
    base_url = "https://sn-watson-tts.labs.skills.network"
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    # Kullanıcı tercih edilen bir ses seçtiyse api_url'ye ses parametresini ekleyin
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    # HTTP isteğimiz için başlıkları ayarlayın
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    # HTTP isteğimizin gövdesini ayarlayın
    json_data = {
        'text': text,
    }
    # Watson Metinden Sese Servisine bir HTTP Post isteği gönderin
    response = requests.post(api_url, headers=headers, json=json_data)
    print('metinden sese yanıt:', response)
    return response.content


def openai_process_message(user_message):
    # OpenAI Api için istemi ayarla
    prompt = "Kişisel asistan gibi davran. Sorulara yanıt verebilir, cümleleri çevirebilir, haberleri özetleyebilir ve önerilerde bulunabilirsin."
    # İstemimizi işlemek için OpenAI Api'yi çağır
    openai_response = openai_client.chat.completions.create(
        model="o3-mini", 
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_completion_tokens=4000
    )
    print("openai yanıtı:", openai_response)
    # İstemimize yanıt mesajını almak için yanıtı ayrıştır
    response_text = openai_response.choices[0].message.content
    return response_text
