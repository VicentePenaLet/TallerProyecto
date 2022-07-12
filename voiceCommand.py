import speech_recognition as sr
import pyttsx3
import winsound
import pyaudio
# Speech to text function


class Speaker():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate',150)
        self.active = False

    def speak(self, text):
        self.active = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.active = False

    def stop(self):
        print("stoping")
        self.engine.stop()
        self.active = False


def speaker(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.setProperty('rate',150)
    engine.say(command)
    engine.runAndWait()

def listener(keys):
    detect = True
    while(detect):   
        print("Listening")
        try:
            r = sr.Recognizer()
            with sr.Microphone(device_index = 4) as source2:
                print(source2)
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("listening")
                audio2 = r.listen(source2)
                print("listening")
                # Using google to recognize audio
                MyText = r.recognize_google(audio2,language="es-ES")
                MyText = MyText.lower()
    
                print("Did you say "+MyText)
                if MyText[:2]=='si':
                    MyText='si'
                if MyText[:2]=='no':
                    MyText='no'
                if MyText in keys:
                    detect = False   
                else: 
                    speaker(f'No se reconoce este comando, las palabras claves son {",".join(keys)}')          
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occured")
    return MyText

if __name__=="__main__":
    keys_inicio=['instrucciones', 'comenzar','cerrar']
    keys_bool=['si', 'no']
    keys_atributos=['marca', 'cantidad', 'ingredientes','sellos', 'información nutricional', 'precio', 'fecha de vencimiento', \
                    'logos']

    #time.sleep(1)
    winsound.Beep(440, 500)
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))
    MyText=listener(keys_inicio)
