<!--
 * @Author: Mr.Car
 * @Date: 2025-03-20 17:40:04
-->
# Weather MCP Tool

[![smithery badge](https://smithery.ai/badge/@MrCare/mcp_tool)](https://smithery.ai/server/@MrCare/mcp_tool)
[English](README.md) | [中文](README_zh.md)

A minimalist weather query MCP tool that allows you to check global weather with just one sentence. Perfectly integrated with Cursor editor, supporting both Chinese and English natural language interaction.

## Features

- 💡 Minimalist: One-line weather query
- 🤖 Smart: Natural language support in Chinese/English
- 🌏 Global: Support for all major cities
- 🔌 Plug & Play: Perfect Cursor integration

## Quick Start

### 1. Installation

#### Method 1: One-Click Installation (Recommended)

Install and configure with Smithery in one command (OpenWeather API Key required):

```bash
npx -y @smithery/cli@latest install @MrCare/mcp_tool --client cursor --config "{\"openweathermapApiKey\":\"your_api_key_here\",\"port\":8000}"
```

> For WindSurf and Cine installation, please visit our [Smithery repository](https://smithery.ai/server/@MrCare/mcp_tool).

#### Method 2: Manual Installation

```bash
git clone https://github.com/yourusername/weather-server.git && cd weather-server && pip install -e .
```

### 2. Configuration

> 🔑 [Get OpenWeather API Key](https://home.openweathermap.org/api_keys)

**Method 1: Quick Setup (Recommended)**

Copy the example configuration file and modify it:
```bash
cp env.example .env
```
Then edit the `.env` file, replace `your_api_key_here` with your API Key.

**Method 2: Environment Variables**

macOS/Linux:
```bash
export OPENWEATHERMAP_API_KEY="your_api_key"
```

Windows:
```cmd
set OPENWEATHERMAP_API_KEY=your_api_key
```

### 3. Enable Tool

Edit `~/.cursor/mcp.json` (Windows: `%USERPROFILE%\.cursor\mcp.json`):
```json
{
    "weather_fastmcp": {
        "command": "python",
        "args": ["-m", "weather_server.server"]
    }
}
```

Restart Cursor and you're ready to go!

## Usage Examples

Simply type in Cursor:
```
Show me the weather in Tokyo
What's the forecast for London?
How's the weather in New York?
Will it rain tomorrow in Paris?
```

That's it!

## Parameters

For more precise queries, you can specify these parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| city | City name (Chinese/English) | Required |
| days | Forecast days (1-5) | 5 |
| units | Temperature unit (metric/imperial) | metric |
| lang | Response language (zh_cn/en) | zh_cn |

## FAQ

1. **Not Working?**
   - Ensure API Key is set correctly
   - Restart Cursor
   - Check Python environment

2. **City Not Found?**
   - Try using English name
   - Check spelling
   - Use complete city name

## Author

- Mr.Car
- Email: 534192336car@gmail.com

## Acknowledgments

- [FastMCP](https://github.com/microsoft/fastmcp)
- [OpenWeatherMap](https://openweathermap.org/)
- [Cursor](https://cursor.sh/)
