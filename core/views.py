from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from django.conf import settings


class HelloView(APIView):
    def get(self, request):
        
        client_ip = self.get_ip_address()
        city = self.get_city()
        temp = self.get_temp()
        
        return Response({
            "client_ip": client_ip,
            "city": city,
            "temp": temp
        })
        
    
    def get_ip_address(self):
        response = requests.get('https://ifconfig.me')
        public_ip = response.text.strip()
        return public_ip
    
    def get_city(self):
        try:
            client_ip = self.get_ip_address()
            response = requests.get(f'http://ip-api.com/json/{client_ip}')
            response.raise_for_status()
            data = response.json()
            city = data.get('city', 'Unknown')
        except requests.RequestException:
            city = 'Unknown'
            
        return city
    
    def get_temp(self):
        city = self.get_city()

        if city == "Unknown":
            return "Unknown"
        
        try:
            api_key = settings.OPENWEATHERMAP_API_KEY
            response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
            response.raise_for_status()
            data = response.json()
            temp = data['main']['temp']
            return temp
        except requests.RequestException:
            return "Unknown"
            
        
        