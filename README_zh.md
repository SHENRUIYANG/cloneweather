<!--
 * @Author: Mr.Car
 * @Date: 2025-03-20 17:40:04
-->
# Weather MCP Tool

[![smithery badge](https://smithery.ai/badge/@MrCare/mcp_tool)](https://smithery.ai/server/@MrCare/mcp_tool)
[English](README.md) | [中文](README_zh.md)

一个极简的天气查询 MCP 工具，只需一句话即可查询全球天气。完美集成 Cursor 编辑器，支持中英文自然语言交互。

## 特性

- 💡 极简使用：一句话查询天气
- 🤖 智能交互：支持中英文自然语言
- 🌏 全球天气：支持所有主要城市
- 🔌 即插即用：完美集成 Cursor

## 快速开始

### 1. 安装

#### 方法一：一键安装（推荐）

使用 Smithery 一键安装并配置（需要提前准备好 OpenWeather API Key）：

```bash
npx -y @smithery/cli@latest install @MrCare/mcp_tool --client cursor --config "{\"openweathermapApiKey\":\"your_api_key_here\",\"port\":8000}"
```

> WindSurf 和 Cine 的安装方法请访问我们的 [Smithery 仓库](https://smithery.ai/server/@MrCare/mcp_tool)。

#### 方法二：手动安装

```bash
git clone https://github.com/yourusername/weather-server.git && cd weather-server && pip install -e .
```

### 2. 配置

> 🔑 [获取 OpenWeather API Key](https://home.openweathermap.org/api_keys)

**方法一：快速配置（推荐）**

复制示例配置文件并修改：
```bash
cp env.example .env
```
然后编辑 `.env` 文件，将 `your_api_key_here` 替换为您的 API Key。

**方法二：环境变量**

macOS/Linux:
```bash
export OPENWEATHERMAP_API_KEY="your_api_key"
```

Windows:
```cmd
set OPENWEATHERMAP_API_KEY=your_api_key
```

### 3. 启用工具

编辑 `~/.cursor/mcp.json`（Windows: `%USERPROFILE%\.cursor\mcp.json`）：
```json
{
    "weather_fastmcp": {
        "command": "python",
        "args": ["-m", "weather_server.server"]
    }
}
```

重启 Cursor 即可使用！

## 使用示例

直接在 Cursor 中输入：
```
查询东京天气
伦敦天气预报怎么样？
纽约现在天气如何？
明天巴黎会下雨吗？
```

就是这么简单！

## 参数说明

如果需要更精确的查询，可以指定以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| city | 城市名称（中/英文） | 必填 |
| days | 预报天数（1-5天） | 5 |
| units | 温度单位 (metric/imperial) | metric |
| lang | 返回语言 (zh_cn/en) | zh_cn |

## 常见问题

1. **无法使用？**
   - 确保 API Key 已正确设置
   - 重启 Cursor
   - 检查 Python 环境

2. **找不到城市？**
   - 尝试使用英文名
   - 检查拼写是否正确
   - 使用完整城市名

## 作者

- Mr.Car
- Email: 534192336car@gmail.com

## 致谢

- [FastMCP](https://github.com/microsoft/fastmcp)
- [OpenWeatherMap](https://openweathermap.org/)
- [Cursor](https://cursor.sh/) 