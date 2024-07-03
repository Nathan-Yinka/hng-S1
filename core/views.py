from rest_framework.response import Response
from rest_framework.views import APIView
import requests

from django.conf import settings


response = requests.get('https://ifconfig.me')
public_ip = response.text.strip()
print(public_ip)


class HelloView(APIView):
    def get(self, request):
        
        client_ip = self.get_ip_address()
        city = self.get_city()
        temp = self.get_temp()
        name = self.request.GET.get('visitor_name', 'Guest')
        
        return Response({
            "client_ip": client_ip,
            "location": city,
            "greeting": f"Hello, {name}!, the temperature is {temp} degrees Celsius in {city}"
        })
        
    
    def get_ip_address(self):
        client_ip = self.request.ipinfo.ip,
        return client_ip[0]
    
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
        except requests.RequestException as e:
            return "Unknown"
            
        
        