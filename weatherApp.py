import sys
import requests
from PyQt5.QtWidgets import QApplication , QWidget , QLabel ,QLineEdit ,QPushButton ,QVBoxLayout
from PyQt5.QtCore import Qt

class  WeatherApp(QWidget):
    def __init__(self):
        super ().__init__()
        self.city_label = QLabel ("Enter the name of City:",self)
        self.city_input = QLineEdit (self)
        self.get_weather_button = QPushButton("Get Button",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox  = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)              
        self.temperature_label.setAlignment(Qt.AlignCenter)       
        self.emoji_label.setAlignment(Qt.AlignCenter)       
        self.description_label.setAlignment(Qt.AlignCenter)     
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")  
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
            QLabel,QPushButton{
             font-family : 'calibri';    
            }
            QLabel#city_label {
                font-size: 40px;
                font-family:'TrebuchetMS';
                font-weight: bold;
                
            }
            Qlabel{
                font-weight: bold;
                font-style : italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size : 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size : 75px;
            }
            QLabel#emoji_label{
                font-size : 100px;
                font-family : Segoe UI emoji;
            }
            QLabel#description_label{
                font-size : 50px;
            }  
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
    def get_weather(self):
        
        api_key = "c60295445dac099cd20ac8e991db861e"
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city }&appid={api_key}"
        try:
            response =  requests.get(url)
            response.raise_for_status()
            data = response.json()
            if response.status_code == 200:
                self.display_weather(data)
            else:
                print("City  not found or API erro ")
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("UnAuthrized:\nInvalid Api Key")
                case 403:
                    self.display_error("Forbidden:\nAcess is deined")
                case 404:
                    self.display_error("Not found:\nCity is not found")                    
                case 500:
                    self.display_error("Internet serve error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\ninvalid resposne from serve")
                case 503:
                    self.display_error("Server unavaible:\nServer is Down")
                case 504:
                    self.display_error("Gateway timeout:\nNo resposne from server")
                case _:
                    self.display_error(f"Http error occour\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\n Check your network please")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error \n The request time out") 
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirect \n check your url")    
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error\n{req_error}")
            
    def display_error(self,message):
        # Resize font slightly and change color to red for errors
        self.temperature_label.setStyleSheet("font-size : 30px; color: red;")
        self.temperature_label.setText(message)
        self.emoji_label.setText("")
        self.description_label.setText("")
    def display_weather(self, data):
        # 1. Validation: Check if the API's picked city matches what the user actually searched for
       self.temperature_label.setStyleSheet("font-size: 75px;")
       temperature_k = data["main"]["temp"]
       temperature_c = temperature_k - 273.15
       temperature_f = (temperature_k * 9/5) - 459.67
       weather_id = data["weather"][0]["id"]
       weather_description = data["weather"][0]["description"]
    
       self.temperature_label.setText(f"{temperature_c:.0f}°C")
       self.emoji_label.setText(self.get_weather_emoji(weather_id))
       self.description_label.setText(weather_description)
    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id == 800:
            return "☀️"
        elif 200 <= weather_id >= 232:
            return "⛈️"
        elif 300 <= weather_id >= 321:
            return "🌦️"
        elif 500 <= weather_id >= 531:
            return   "🌧️"
        elif 600 <= weather_id >= 622:
            return   "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
             return "☁️"
        else:
            return ""
             
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_App = WeatherApp()
    weather_App.show()
    sys.exit(app.exec_())

    