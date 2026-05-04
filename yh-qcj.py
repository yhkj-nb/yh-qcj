"""
配置加载前置插件
启动时自动加载 config/ 下所有 YAML 配置，并生成加载日志
其他插件调用: from plugins.yh-qcj import config_loader
"""

import yaml
import logging
from pathlib import Path

from core.plugin.decorators import on_load

__plugin_meta__ = {
    'name': '配置加载器',
    'author': '云痕',
    'description': '前置插件：统一加载 config/ 所有 YAML 配置，自动生成加载日志',
    'version': '1.0.0',
    'github': 'https://github.com/yhkj-nb/yh-qcj/'


class ConfigLoader:
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            self.config_dir = Path.cwd() / "config"
        else:
            self.config_dir = Path(config_dir)
        self.configs = {}
        self._loaded = False  # 加载标记，防止重复加载
        self._setup_logger()

    def _setup_logger(self):
        log_file = Path(__file__).resolve().parent / "yh-qcj.log"

        self.logger = logging.getLogger("ConfigLoader")
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        fmt = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def _log_bot_config(self, bot_index, bot):
        """记录单个机器人配置详情"""
        i = bot_index
        self.logger.info(f"  ┌─ 机器人 [{i}] ─────────────────────────────")
        self.logger.info(f"  │ appid: {bot.get('appid', '')}")
        self.logger.info(f"  │ secret: {'***' if bot.get('secret') else ''}")
        self.logger.info(f"  │ robot_qq: {bot.get('robot_qq', '')}")
        self.logger.info(f"  │ owner_ids: {bot.get('owner_ids', [])}")

        ws = bot.get('websocket', {})
        self.logger.info(f"  │ websocket.enabled: {ws.get('enabled', True)}")
        self.logger.info(f"  │ websocket.custom_url: {ws.get('custom_url', '')}")
        self.logger.info(f"  │ websocket.reconnect_interval: {ws.get('reconnect_interval', 5)}")
        self.logger.info(f"  │ websocket.max_reconnects: {ws.get('max_reconnects', -1)}")

        msg = bot.get('message', {})
        self.logger.info(f"  │ message.use_markdown: {msg.get('use_markdown', True)}")
        self.logger.info(f"  │ message.markdown_suffix: {msg.get('markdown_suffix', '')}")
        self.logger.info(f"  │ message.button_enter_to_send: {msg.get('button_enter_to_send', False)}")
        self.logger.info(f"  │ message.send_default_response: {msg.get('send_default_response', False)}")

        identity = bot.get('identity', {})
        self.logger.info(f"  │ identity.use_union_id_for_group: {identity.get('use_union_id_for_group', False)}")
        self.logger.info(f"  │ identity.use_union_id_for_channel: {identity.get('use_union_id_for_channel', False)}")

        welcome = bot.get('welcome', {})
        self.logger.info(f"  │ welcome.group_welcome: {welcome.get('group_welcome', False)}")
        self.logger.info(f"  │ welcome.new_user_welcome: {welcome.get('new_user_welcome', False)}")
        self.logger.info(f"  │ welcome.friend_add_message: {welcome.get('friend_add_message', False)}")

        maintenance = bot.get('maintenance', {})
        self.logger.info(f"  │ maintenance.enabled: {maintenance.get('enabled', False)}")

        blacklist = bot.get('blacklist', {})
        self.logger.info(f"  │ blacklist.user_enabled: {blacklist.get('user_enabled', False)}")
        self.logger.info(f"  │ blacklist.group_enabled: {blacklist.get('group_enabled', False)}")
        self.logger.info(f"  └──────────────────────────────────────────")

    def load(self):
        """加载配置，只执行一次"""
        if self._loaded:
            self.logger.info("配置已加载，跳过重复加载")
            return

        self.logger.info("=" * 60)
        self.logger.info("ConfigLoader 开始加载配置")
        self.logger.info(f"配置目录: {self.config_dir}")
        self.logger.info("=" * 60)

        if not self.config_dir.exists():
            self.logger.error(f"配置目录不存在: {self.config_dir}")
            return

        self.configs.clear()
        yaml_files = (
            sorted(self.config_dir.glob("*.yaml"))
            + sorted(self.config_dir.glob("*.yml"))
        )

        if not yaml_files:
            self.logger.warning("未找到任何 YAML 配置文件")
            return

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                self.configs[yaml_file.stem] = data
                self.logger.info(f"✔ {yaml_file.name} 加载成功")

                if yaml_file.stem == "bot":
                    bots = data.get("bots", [])
                    if bots:
                        self.logger.info(f"  共检测到 {len(bots)} 个机器人配置:")
                        for idx, bot in enumerate(bots):
                            self._log_bot_config(idx, bot)
                    else:
                        self.logger.warning("  bot.yaml 中未找到任何机器人配置")
                else:
                    self.logger.debug(f"\n{yaml.dump(data, allow_unicode=True, default_flow_style=False)}")

            except Exception as e:
                self.logger.error(f"✖ {yaml_file.name} 加载失败: {e}")

        self._loaded = True  # 标记已加载
        self.logger.info(f"共加载 {len(self.configs)} 个文件: {list(self.configs.keys())}")
        self.logger.info("配置加载完成，不再重复加载")
        self.logger.info("=" * 60)

    def reload(self):
        """手动重新加载配置"""
        self._loaded = False
        self.load()

    def get(self, file: str, key: str = None, default=None):
        config = self.configs.get(file, {})
        if key is None:
            return config if config else default
        for k in key.split('.'):
            if isinstance(config, dict):
                config = config.get(k)
                if config is None:
                    return default
            elif isinstance(config, list):
                try:
                    config = config[int(k)]
                except (IndexError, ValueError):
                    return default
            else:
                return default
        return config

    def get_all(self, file: str = None):
        return self.configs if file is None else self.configs.get(file, {})


config_loader = ConfigLoader()


@on_load
def load_config():
    """插件加载时自动读取所有配置"""
    config_loader.load()