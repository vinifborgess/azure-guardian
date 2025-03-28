import azure.cognitiveservices.speech as speechsdk

speech_key = "EZSJgz6Q70urJBDGSs1e0VezdYzmyap6U5uLn1u8pX3YpmFLRycqJQQJ99BCACYeBjFXJ3w3AAAYACOGs8iC"
speech_endpoint = "https://eastus.api.cognitive.microsoft.com"
print(f"Chave: {speech_key}")
print(f"Endpoint: {speech_endpoint}")

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region="eastus")
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

print("Fala algo (te dou tempo até parar de falar)...")

# Reconhecimento único, espera até você parar
result = speech_recognizer.recognize_once_async().get()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print(f"Texto reconhecido: {result.text}")
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("Nada reconhecido, falou baixo ou microfone tá mudo?")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Cancelado: {cancellation_details.reason}")
    print(f"Erro: {cancellation_details.error_details}")
else:
    print(f"Outro erro: {result.reason}")