from langchain.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import requests
from app.config import settings

class WeatherQueryInput(BaseModel):
    city: str = Field(description="Nome da cidade para consulta do tempo")
    country_code: Optional[str] = Field(default=None, description="Código do país (opcional)")

class WeatherTool(BaseTool):
    name = "weather_query"
    description = "Consulta informações do tempo atual para uma cidade específica"
    args_schema: Type[BaseModel] = WeatherQueryInput
    
    def _run(self, city: str, country_code: Optional[str] = None) -> str:
        # if not settings.openweather_api_key:
        #     return "API key do OpenWeatherMap não configurada. Usando dados simulados: Tempo ensolarado, 25°C em " + city
        
        try:
            location = f"{city},{country_code}" if country_code else city
            base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={settings.openweather_api_key}"
            
            print(f"Consultando: {base_url}")
            
            
            response = requests.get(base_url, timeout=20)
            data = response.json()
            
            if response.status_code == 200:
                weather = data["weather"][0]
                main = data["main"]
                wind = data.get("wind", {})

                return f"""🌤️ **Tempo em {data['name']}**

                    📊 **Condições atuais:**
                    - Clima: {weather['description'].capitalize()}
                    - Temperatura: {main['temp']:.1f}°C
                    - Sensação térmica: {main['feels_like']:.1f}°C
                    - Temperatura mínima: {main['temp_min']:.1f}°C
                    - Temperatura máxima: {main['temp_max']:.1f}°C
                    - Umidade: {main['humidity']}%
                    - Pressão: {main['pressure']} hPa
                    - Vento: {wind.get('speed', 0):.1f} m/s

                    🌍 Coordenadas: {data['coord']['lat']}, {data['coord']['lon']}
                    """
            else:
                return f"Erro ao consultar tempo para {city}: {data.get('message', 'Erro desconhecido')}"
            
        except requests.Timeout:
            return f"Timeout ao consultar API do OpenWeatherMap para {city}"
        except Exception as e:
            return f"Erro na consulta do tempo: {str(e)}"