'''
Author: Mr.Car
Date: 2025-03-20 20:18:33
'''
from fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import asyncio

from .models import WeatherData, ForecastData, WeatherForecast
from .utils import CityNameConverter

# 加载环境变量
load_dotenv()

# 初始化工具类
city_converter = CityNameConverter()

# 初始化 FastMCP 服务器
server = FastMCP()

# 设置响应头，添加Transfer-Encoding: chunked，支持SSE流式响应
@server.middleware("http")
async def add_chunked_encoding(request, call_next):
    response = await call_next(request)
    response.headers["Transfer-Encoding"] = "chunked"
    return response


@server.tool()
async def get_weather(city: str, units: str = "metric", lang: str = "zh_cn") -> WeatherData:
    english_city = city_converter.to_english(city)
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("缺少 OPENWEATHERMAP_API_KEY 环境变量")

    params = {
        "q": english_city,
        "appid": api_key,
        "units": units,
        "lang": lang
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://api.openweathermap.org/data/2.5/weather",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                description=data["weather"][0]["description"],
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                city=city
            )

    except httpx.TimeoutException:
        raise Exception("请求超时，请稍后重试")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise Exception(f"未找到城市 '{city}' ({english_city}) 的天气信息")
        raise Exception(f"HTTP错误: {e.response.status_code} - {e.response.text}")
    except KeyError as e:
        raise Exception(f"数据解析错误：缺少必要字段 {str(e)}")
    except Exception as e:
        raise Exception(f"获取天气信息时发生错误：{str(e)}")


@server.tool()
async def get_weather_forecast_stream(city: str, days: int = 5, units: str = "metric", lang: str = "zh_cn") -> StreamingResponse:
    """
    使用 SSE 流式返回天气预报
    """
    english_city = city_converter.to_english(city)
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("缺少 OPENWEATHERMAP_API_KEY 环境变量")

    params = {
        "q": english_city,
        "appid": api_key,
        "units": units,
        "lang": lang,
        "cnt": min(days * 8, 40)
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://api.openweathermap.org/data/2.5/forecast",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

        forecasts = {}
        for item in data["list"]:
            date = item["dt_txt"].split()[0]
            if date not in forecasts:
                forecasts[date] = {
                    "temp_min": float("inf"),
                    "temp_max": float("-inf"),
                    "descriptions": set(),
                    "humidity": [],
                    "wind_speed": []
                }

            daily = forecasts[date]
            daily["temp_min"] = min(daily["temp_min"], item["main"]["temp"])
            daily["temp_max"] = max(daily["temp_max"], item["main"]["temp"])
            daily["descriptions"].add(item["weather"][0]["description"])
            daily["humidity"].append(item["main"]["humidity"])
            daily["wind_speed"].append(item["wind"]["speed"])

        daily_forecasts = []
        for date, daily in list(forecasts.items())[:days]:
            daily_forecasts.append(ForecastData(
                date=date,
                description="/".join(daily["descriptions"]),
                temp_min=round(daily["temp_min"], 2),
                temp_max=round(daily["temp_max"], 2),
                humidity=round(sum(daily["humidity"]) / len(daily["humidity"])),
                wind_speed=round(sum(daily["wind_speed"]) / len(daily["wind_speed"]), 2),
                city=city
            ))

        async def forecast_stream():
            for forecast in daily_forecasts:
                await asyncio.sleep(1)  # 模拟处理时间
                yield f"data: {forecast.to_json()}\n\n"
            yield "event: done\ndata: [END]\n\n"

        return StreamingResponse(forecast_stream(), media_type="text/event-stream")

    except Exception as e:
        async def error_stream():
            yield f"event: error\ndata: {str(e)}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream")


@server.tool()
async def get_weather_forecast(city: str, days: int = 5, units: str = "metric", lang: str = "zh_cn") -> dict:
    """
    原有的普通非流式返回
    """
    english_city = city_converter.to_english(city)
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("缺少 OPENWEATHERMAP_API_KEY 环境变量")

    params = {
        "q": english_city,
        "appid": api_key,
        "units": units,
        "lang": lang,
        "cnt": min(days * 8, 40)
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://api.openweathermap.org/data/2.5/forecast",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

        forecasts = {}
        for item in data["list"]:
            date = item["dt_txt"].split()[0]
            if date not in forecasts:
                forecasts[date] = {
                    "temp_min": float("inf"),
                    "temp_max": float("-inf"),
                    "descriptions": set(),
                    "humidity": [],
                    "wind_speed": []
                }

            daily = forecasts[date]
            daily["temp_min"] = min(daily["temp_min"], item["main"]["temp"])
            daily["temp_max"] = max(daily["temp_max"], item["main"]["temp"])
            daily["descriptions"].add(item["weather"][0]["description"])
            daily["humidity"].append(item["main"]["humidity"])
            daily["wind_speed"].append(item["wind"]["speed"])

        result = []
        for date, daily in list(forecasts.items())[:days]:
            result.append(ForecastData(
                date=date,
                description="/".join(daily["descriptions"]),
                temp_min=round(daily["temp_min"], 2),
                temp_max=round(daily["temp_max"], 2),
                humidity=round(sum(daily["humidity"]) / len(daily["humidity"])),
                wind_speed=round(sum(daily["wind_speed"]) / len(daily["wind_speed"]), 2),
                city=city
            ))

        return WeatherForecast(forecasts=result).to_dict()

    except Exception as e:
        raise Exception(f"获取天气预报信息时发生错误：{str(e)}")


# 启动服务器
if __name__ == "__main__":
    server.run()
