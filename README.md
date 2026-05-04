# 云痕前置插件
[![Python](https://img.shields.io/badge/Python-3.6+-blue?logo=python&logoColor=white)](https://python.org)
[![QQ群](https://img.shields.io/badge/QQ交流群-985373528-blue)](https://qun.qq.com/universal-share/share?ac=1&authKey=93R53wEA4EQpWW5WmZlEkoBWLmr8OP%2FXNh3P05QAfD%2BlJksecR%2Bh6C%2BQ4etuwdmv&busi_data=eyJncm91cENvZGUiOiI5ODUzNzM1MjgiLCJ0b2tlbiI6ImJCMndSbFMvZEN4OHY2b3ZHckUvSWlnQ3NHZ3g5b1dDM2R5emplang5RU5uNndLREZmUER1S3d4TXBGbGpoc3QiLCJ1aW4iOiIzMDIxMjIwOTkwIn0%3D&data=GaAYD3hoxugGVkxjslmorguKaSU0tUAkbLn5s3AsO4DbHop3LqbLDkTCsWsOciUUNkwpzSXwy5y30d4leXuCWg&svctype=4&tempid=h5_group_info)


ElainaBot v2 框架前置插件，用于统一加载 `config/` 目录下所有 YAML 配置文件，并提供接口供其他插件调用。

## ✨ 功能

- 启动时自动扫描并加载 `config/` 目录下所有 `.yaml` / `.yml` 文件
- 支持点号分隔的嵌套键读取，如 `config_loader.get("bot", "bots.0.appid")`
- 支持列表索引读取，如 `bots.0` 表示第一个机器人、`bots.1` 表示第二个
- 自动生成 `云痕前置插件.log` 加载日志，详细记录每个机器人的配置项（密钥自动隐藏）
- 全局单例，其他插件直接 import 即可使用，无需重复读取文件
## 其他插件读取
```python
from plugins.yh-qcj import config_loader

# ===== 读取 bot.yaml 配置 =====

# 获取第一个机器人的基本信息
appid = config_loader.get("bot", "bots.0.appid")
secret = config_loader.get("bot", "bots.0.secret")
robot_qq = config_loader.get("bot", "bots.0.robot_qq")
owner_ids = config_loader.get("bot", "bots.0.owner_ids")

# 获取 WebSocket 配置
ws_enabled = config_loader.get("bot", "bots.0.websocket.enabled")
ws_url = config_loader.get("bot", "bots.0.websocket.custom_url")
reconnect_interval = config_loader.get("bot", "bots.0.websocket.reconnect_interval")
max_reconnects = config_loader.get("bot", "bots.0.websocket.max_reconnects")

# 获取消息配置
use_markdown = config_loader.get("bot", "bots.0.message.use_markdown")
markdown_suffix = config_loader.get("bot", "bots.0.message.markdown_suffix")
button_enter_to_send = config_loader.get("bot", "bots.0.message.button_enter_to_send")
send_default_response = config_loader.get("bot", "bots.0.message.send_default_response")
default_response_excluded_regex = config_loader.get("bot", "bots.0.message.default_response_excluded_regex")

# 获取身份配置
union_id_group = config_loader.get("bot", "bots.0.identity.use_union_id_for_group")
union_id_channel = config_loader.get("bot", "bots.0.identity.use_union_id_for_channel")

# 获取欢迎消息配置
group_welcome = config_loader.get("bot", "bots.0.welcome.group_welcome")
new_user_welcome = config_loader.get("bot", "bots.0.welcome.new_user_welcome")
friend_add = config_loader.get("bot", "bots.0.welcome.friend_add_message")

# 获取维护模式
maintenance = config_loader.get("bot", "bots.0.maintenance.enabled")

# 获取黑名单配置
blacklist_user = config_loader.get("bot", "bots.0.blacklist.user_enabled")
blacklist_group = config_loader.get("bot", "bots.0.blacklist.group_enabled")
blacklist_user_list = config_loader.get("bot", "bots.0.blacklist.user_list")
blacklist_group_list = config_loader.get("bot", "bots.0.blacklist.group_list")

# 如果有多个机器人，用索引 1、2、3... 访问
second_appid = config_loader.get("bot", "bots.1.appid", default="未配置第二个机器人")

# ===== 读取 settings.yaml 配置 =====

token = config_loader.get("settings", "web.token")
port = config_loader.get("settings", "server.port", default=5001)

# ===== 获取整个配置文件 =====

# 获取整个 bot.yaml 内容
bot_config = config_loader.get_all("bot")

# 获取整个 settings.yaml 内容
settings_config = config_loader.get_all("settings")

# 获取所有已加载的配置
all_configs = config_loader.get_all()


## 📦 依赖

| 依赖 | 版本 | 说明 | 安装 |
|------|------|------|------|
| Python | ≥ 3.10 | ElainaBot v2 框架要求 | - |
| pyyaml | ≥ 6.0 | YAML 配置文件解析 | `pip install pyyaml` |

其余 `logging`、`pathlib` 均为 Python 标准库，无需额外安装。

### 快速安装依赖

```bash
pip install pyyaml