"""
| Main Classes for packinit
"""
from argparse import ArgumentParser, RawTextHelpFormatter
import os
import sys
import datetime
import getpass
import socket
import logging
from .utils import PropertyFileManager, PackFileUpdater, PackManager, \
    BufferingSMTPHandler, MakeFileHandler, JavaRunner

DEFAULTS = {
    'dist_dirs': ['/dist'],
    'cache': '/tmp/packmaker',
    'server_dir': '/server',
    'no_update': 'false',
    'prop_file': '/server/server.properties',
    'game_type': 'modded',
    'minecraft_version': 'Unknown Minecraft Version',
    'pack_name': 'Modded Minecraft',
    'pack_creator': 'Super Modpack Dev',
    'server_host': 'Minecraft Admin',
    'dest_email': 'root@localhost',
    'src_email': '%s@%s' % (getpass.getuser(), socket.getfqdn()),
    'mail_server': 'localhost',
    'mail_port': '25',
    'log_level': 'INFO',
    'log_dir': '/var/log/packinit',
    'java_params': {
        'memory': '4096m',
        'fml_confirm': 'cancel',
        'log_level': 'warn',
        'log4j_xml': os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'extra_files/log4j2.xml'
        )
    },
    'server_props': {
        'motd': '',
        'server-port': '25565',
        'allow-nether': 'true',
        'announce-player-achievements': 'true',
        'enable-command-block': 'false',
        'spawn-animals': 'true',
        'spawn-monsters': 'true',
        'spawn-npcs': 'true',
        'generate-structures': 'true',
        'view-distance': '10',
        'hardcore': 'false',
        'max-build-height': '256',
        'force-gamemode': 'false',
        'max-tick-time': '-1',
        'enable-query': 'false',
        'query.port': '25565',
        'enable-rcon': 'false',
        'rcon.password': 'minecraft',
        'rcon.port': '25575',
        'max-players': '20',
        'max-world-size': '15000',
        'level-name': 'world',
        'level-seed': '',
        'pvp': 'true',
        'generator-settings': '',
        'online-mode': 'true',
        'allow-flight': 'true',
        'level-type': 'DEFAULT',
        'white-list': 'false',
        'spawn-protection': '0',
        'difficulty': '2',
        'gamemode': '0'
    }
}

ENVIRONMENT = {
    'dist_dirs': None if not os.getenv('DIST') else os.getenv('DIST').split(','), #
    'cache': os.getenv('CACHE'), #
    'server_dir': os.getenv('SERVER_DIR'), #
    'no_update': os.getenv('NO_UPDATE'), #
    'prop_file': os.getenv('PROP_FILE'), #
    'game_type': os.environ.get('PACK_NAME', os.environ.get('GAME_TYPE'.lower())), #
    'minecraft_version': os.environ.get('VERSION'),
    'pack_name': os.environ.get('PACK_NAME'), #
    'pack_creator': os.environ.get('PACK_CREATOR'), #
    'server_host': os.environ.get('SERVER_HOST'), #
    'dest_email': os.environ.get('DEST_EMAIL'), #
    'src_email': os.environ.get('SRC_EMAIL'), #
    'mail_server': os.environ.get('MAIL_SERVER'), #
    'mail_port': os.environ.get('MAIL_PORT'), #
    'log_level': os.environ.get('LOG_LEVEL'), #
    'log_dir': os.environ.get('LOG_DIR'), #
    'java_params': {
        'memory': os.getenv('JAVA_MEM'), #
        'fml_confirm': os.getenv('FML_CONFIRM'), #
        'log_level': os.getenv('MINECRAFT_LOG_LEVEL'), #
        'log4j_xml': os.getenv('MINECRAFT_LOG4J_CONF') #
    },
    'server_props': {
        'motd': os.getenv('MOTD'), #
        'server-port': os.getenv('SERVER_PORT'), #
        'allow-nether': os.getenv('ALLOW_NETHER'), #
        'announce-player-achievements': os.getenv('ANNOUNCE_PLAYER_ACHIEVEMENTS'), #
        'enable-command-block': os.getenv('ENABLE_COMMAND_BLOCK'), #
        'spawn-animals': os.getenv('SPAWN_ANIMALS'), #
        'spawn-monsters': os.getenv('SPAWN_MONSTERS'), #
        'spawn-npcs': os.getenv('SPAWN_NPCS'), #
        'generate-structures': os.getenv('GENERATE_STRUCTURES'), #
        'view-distance': os.getenv('VIEW_DISTANCE'), #
        'hardcore': os.getenv('HARDCORE'), #
        'max-build-height': os.getenv('MAX_BUILD_HEIGHT'), #
        'force-gamemode': os.getenv('FORCE_GAMEMODE'), #
        'max-tick-time': os.getenv('MAX_TICK_TIME'), #
        'enable-query': os.getenv('ENABLE_QUERY'), #
        'query.port': os.getenv('QUERY_PORT'), #
        'enable-rcon': os.getenv('ENABLE_RCON'), #
        'rcon.password': os.getenv('RCON_PASSWORD'), #
        'rcon.port': os.getenv('RCON_PORT'), #
        'max-players': os.getenv('MAX_PLAYERS'), #
        'max-world-size': os.getenv('MAX_WORLD_SIZE'), #
        'level-name': os.getenv('LEVEL_NAME'), #
        'level-seed': os.getenv('LEVEL_SEED'), #
        'pvp': os.getenv('PVP'), #
        'generator-settings': os.getenv('GENERATOR_SETTINGS'), #
        'online-mode': os.getenv('ONLINE_MODE'), #
        'allow-flight': os.getenv('ALLOW_FLIGHT'), #
        'level-type': os.getenv('LEVEL_TYPE'.upper()), #
        'white-list': os.getenv('WHITELIST'), #
        'spawn-protection': os.getenv('SPAWN_PROTECTION'), #
        'difficulty': os.getenv('DIFFICULTY'),
        'gamemode': os.getenv('GAMEMODE')
    }
}


class Configuration:
    """
    | The main configuration class for unifying configuration sources in a predictable way.
    """

    def __getattribute__(self, name):
        return object.__getattribute__(self, name)

    def __init__(self, *defaults, **kwargs):
        config = {}
        for dictionary in defaults:
            clean_dictionary = self.clear_none_values(dictionary)
            config = {**config, **clean_dictionary}

        for key in config:
            if config[key]:
                setattr(self, key, config[key])
        for key in kwargs:
            if kwargs[key]:
                setattr(self, key, kwargs[key])
        setattr(self, 'motd', self.motd_generate)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def motd_generate(self):
        """
        | Check for the MOTD property and return, else auto-generate and return.
        | :return: `string` Message of the day.
        """

        if self.motd:
            return self.motd

        generated_motd = 'A %s %s Minecraft server by %s. Hosted by %s' % (
            self.game_type,
            self.minecraft_version,
            self.pack_creator,
            self.server_host
        )

        return generated_motd

    def clear_none_values(self, dictionary):
        """
        Strips `None` values from incoming dictionaries before merge.
        :param dictionary:
        :return:
        """
        clean = {}
        for key, value in dictionary.items():
            if isinstance(value, dict):
                nested = self.clear_none_values(value)
                if len(nested.keys()) > 0:
                    clean[key] = nested
            elif value is not None:
                clean[key] = value
        return clean


class MineInit:
    """
    | The main class for the packinit executable.
    """

    def __init__(self):
        self.hostname = socket.getfqdn()
        self.parser = self.build_parser()
        self.ppid = os.getppid()
        args = self.parser.parse_args()
        self.config = Configuration(DEFAULTS, ENVIRONMENT, self.arg_dict(args))
        self.logger = self.setup_logging()
        args.func()

    def setup_logging(self):
        """
        | Setup logging
        | :return: logging.Logger instance
        """
        log_dir = self.config.log_dir
        log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        logger = logging.getLogger('packinit')
        logger.setLevel(self.config.log_level)
        log_format = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.config.log_level)
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)

        file_handler = MakeFileHandler(filename=os.path.join(log_dir, log_filename))
        file_handler.setLevel(self.config.log_level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        self.smtp_handler = BufferingSMTPHandler(
            self.config.mail_server,
            self.config.mail_port,
            self.config.src_email,
            self.config.dest_email,
            1000
        )
        self.smtp_handler.setLevel(self.config.log_level)
        self.smtp_handler.setFormatter(log_format)
        logger.addHandler(self.smtp_handler)

        return logger

    # pylint: disable=too-many-statements
    def build_parser(self):
        """
        | Build the main argparser for the application and return as an object.
        | :return: `object` argparser
        """
        parser = ArgumentParser(
            description='A container friendly startup routine for Packmaker servers.',
            epilog='packinit is a Python based startup routine for Packmaker based modded'
                   ' Minecraft servers. It can be run on any Linux system and in any container'
                   ' at present. It can be configured via environment variables, flags, and soon'
                   ' config files. (ini, yaml and toml formats are being considered)\n\n'
                   'It works by using Packmaker to download all mods based on a Packmaker yaml'
                   ' and lock file. It will download the latest mods, and sync the updated'
                   ' configuration and mods into the server directory in a stateful way that'
                   ' preserves runtime data, like the world.\n\n'
                   'Like Packmaker, packinit can be given multiple pack files, which it'
                   ' will merge from first to last provided. This allows pack developers'
                   ' to release a server with pack related mods, and for server administrators'
                   ' to add their own maintenance packs, with mods for backup; sleep voting;'
                   ' and maps for example.\n\n'
                   'For full help documentation, and config file syntax, please visit our'
                   ' documentation pages on Read the Docs:'
                   ' https://packinit.readthedocs.io/en/stable/\n\n'
        )
        parser.formatter_class = RawTextHelpFormatter
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        parser.add_argument(
            '--dest-email',
            dest='dest_email',
            type=str,
            help='STRING: The email address to send the backup report to. Defaults to %s.\n\n'
                 'Environment: DEST_EMAIL\n\n' %
            (DEFAULTS.get('dest_email'))
        )

        parser.add_argument(
            '--source-email',
            dest='src_email',
            type=str,
            help='STRING: The email address to send the backup report from. Defaults to %s\n\n'
                 'Environment: SRC_EMAIL\n\n' %
            (DEFAULTS.get('src_email'))
        )

        parser.add_argument(
            '--mail-server',
            dest='mail_server',
            type=str,
            help='STRING: The mail server to use to send mail. Defaults to %s.\n\n'
                 'Environment: MAIL_SERVER\n\n' %
            (DEFAULTS.get('mail_server'))
        )

        parser.add_argument(
            '--mail-port',
            dest='mail_port',
            type=int,
            help='INT: The port on which to connect to the mail server. Defaults to %s.\n\n'
                 'Environment: MAIL_PORT\n\n' %
            (DEFAULTS.get('mail_port'))
        )

        parser.add_argument(
            '--log-level',
            dest='log_level',
            type=str,
            help='STRING: The logging level, defaults to %s\n\n'
                 'Environment: LOG_LEVEL\n\n' %
            (DEFAULTS.get('log_level'))
        )

        parser.add_argument(
            '--log-dir',
            dest='log_dir',
            type=str,
            help='STRING: The directory to place logs. Defaults to %s\n\n'
                 'Environment: LOG_DIR\n\n' %
            (DEFAULTS.get('log_dir'))
        )

        parser_start = subparsers.add_parser(
            'start',
            help='Starts, stops, and configures a Minecraft instance.',
            formatter_class=RawTextHelpFormatter
        )
        parser_start.set_defaults(func=self.start)
        parser_start.add_argument(
            '-x', '--no-update',
            action='store_true',
            dest='no_update',
            help='BOOLEAN: Disable update of the server directory from the distribution directory.'
                 ' Defaults to %s.\n\n'
                 'Environment: NO_UPDATE\n\n' %
            (DEFAULTS.get('no_update'))
        )
        parser_start.add_argument(
            '-d', '--dist', '--distribution-dir',
            dest='dist_dirs',
            action='append',
            help='STRING: The directory containing the distribution files, like default '
                 ' server.properties, configs, and as infrequently as possible '
                 ' (to prevent bloat and legal issues) mods. Defaults to "%s". To tell Packmaker '
                 ' to merge multiple directories, pass this argument multiple times.\n\n'
                 'Environment: DIST\n'
                 'Provide a comma seperated list of paths for the environment variable.\n\n' %
            (DEFAULTS.get('dist_dir')),
        )
        parser_start.add_argument(
            '-s', '--server', '--server-dir',
            type=str,
            dest='server_dir',
            help='STRING: The directory where the server root will be (or is).'
                 ' Defaults to "%s".\n\n'
                 'Environment: SERVER_DIR\n\n' %
            (DEFAULTS.get('server_dir'))
        )
        parser_start.add_argument(
            '-c', '--cache', '--cache-dir',
            type=str,
            dest='cache',
            help='STRING: The directory containing cached files, often files downloaded by the'
                 ' pack manager process. The cache is used to speed up subsequent server starts'
                 ' so that these files do not need to be downloaded on every start.'
                 ' Defaults to "%s".\n\n'
                 'Environment: CACHE\n\n' %
            (DEFAULTS.get('cache'))
        )
        parser_start.add_argument(
            '--java-mem',
            type=str,
            dest='java_mem',
            help='STRING: The amount of memory to pass to XMS and XMX for the Minecraft server'
                 ' process. This needs to be at least 4g (or 4090m) for most modded Minecraft'
                 ' servers. Defaults to "%s".\n\n'
                 'Environment: JAVA_MEM\n\n' %
            (DEFAULTS.get('java_params', {}).get('memory'))
        )
        parser_start.add_argument(
            '--fml-confirm',
            type=str,
            dest='fml_confirm',
            help='STRING: One of confirm/cancel. Tells FML to go ahead and remove missing'
                 ' blocks, or cancel and exit the game. Defaults to "%s".\n\n'
                 'Environment: FML_CONFIRM\n\n' %
            (DEFAULTS.get('java_params', {}).get('fml_confirm'))
        )
        parser_start.add_argument(
            '--minecraft-log-level',
            type=str,
            dest='minecraft_log_level',
            help='STRING: The level to set for LOG4J2 verbosity in the Minecraft JVM.'
                 ' Valid values are ALL/DEBUG/INFO/WARN/ERROR/FATAL/OFF/TRACE.'
                 ' Defaults to "%s".\n\n'
                 'Environment: MINECRAFT_LOG_LEVEL\n\n' %
            (DEFAULTS.get('java_params', {}).get('log_level'))
        )
        parser_start.add_argument(
            '--minecraft-log4j-conf',
            type=str,
            dest='minecraft_log4j_conf',
            help='STRING: The path to a custom log4j config file for the Minecraft JVM.'
                 ' May be relative to the Minecraft server directory. Full path is safer.'
                 ' By default, packinit includes a config that allows it to control the'
                 ' log level. Defaults to "%s".\n\n'
                 'Environment: MINECRAFT_LOG4J_CONF\n\n' %
            (DEFAULTS.get('java_params', {}).get('log4j_xml'))
        )
        parser_start.add_argument(
            '--pack-name',
            type=str,
            dest='pack_name',
            help='STRING: The name of the pack being launched. This is used for the MOTD, if'
                 ' autogenerated. Defaults to "%s".\n\n'
                 'Environment: PACK_NAME\n\n' %
            (DEFAULTS.get('pack_name'))
        )
        parser_start.add_argument(
            '--pack-creator',
            type=str,
            dest='pack_creator',
            help='STRING: The name modpack developer or team. This is used for the MOTD, if'
                 ' autogenerated. Defaults to "%s".\n\n'
                 'Environment: PACK_CREATOR\n\n' %
            (DEFAULTS.get('pack_creator'))
        )
        parser_start.add_argument(
            '--server-host',
            type=str,
            dest='server_host',
            help='STRING: The name of the admin or team hosting the game. This is used for'
                 ' the MOTD, if autogenerated. Defaults to "%s".\n\n'
                 'Environment: SERVER_HOST\n\n' %
            (DEFAULTS.get('server_host'))
        )
        parser_start.add_argument(
            '--minecraft-version',
            type=str,
            dest='minecraft_version',
            help='STRING: The version of Minecraft the pack is based on. This is used for the'
                 ' MOTD, if autogenerated. Defaults to "%s".\n\n'
                 'Environment: VERSION\n\n' %
            (DEFAULTS.get('minecraft_version'))
        )
        parser_start.add_argument(
            '--game-type',
            type=str,
            dest='game_type',
            help='STRING: The game type being played. If this is not specified the PACK_NAME'
                 ' will be used for the MOTD, however server admins can override pack name from'
                 ' server containers that have it set if they are deploying special rules'
                 ' for their game. This is used for the MOTD, if autogenerated.'
                 ' Defaults to "%s".\n\n'
                 'Environment: GAME_TYPE\n\n' %
            (DEFAULTS.get('game_type'))
        )
        parser_start.add_argument(
            '--prop-file',
            type=str,
            dest='prop_file',
            help='STRING: The path to the properties file. Defaults to "%s".\n\n'
                 'Environment: PROP_FILE\n\n' %
            (DEFAULTS.get('prop_file'))
        )
        parser_start.add_argument(
            '--motd',
            type=str,
            dest='motd',
            help='STRING: The MOTD string. This will disable/override the autogenerated'
                 ' MOTD. Defaults to an autogenerated MOTD based on GAME_TYPE/PACK_NAME,'
                 ' MINECRAFT_VERSION, PACK_CREATOR and SERVER_HOST.\n\n'
                 'Environment: MOTD\n\n'
        )
        parser_start.add_argument(
            '--server-port',
            type=str,
            dest='server_port',
            help='STRING: The port the server will listen on. Defaults to "%s".\n\n'
                 'Environment: SERVER_PORT\n\n' %
            (DEFAULTS.get('server_props', {}).get('server-port'))
        )
        parser_start.add_argument(
            '--allow-nether',
            type=str,
            dest='allow_nether',
            help='BOOLEAN: (true/false) Enables the Nether. Defaults to "%s".\n\n'
                 'Environment: ALLOW_NETHER\n\n' %
            (DEFAULTS.get('server_props', {}).get('allow-nether'))
        )
        parser_start.add_argument(
            '--announce-player-achievements',
            type=str,
            dest='announce_player_achievements',
            help='BOOLEAN: (true/false) Enables announcement of player achievements.'
                 ' Defaults to "%s".\n\n'
                 'Environment: ANNOUNCE_PLAYER_ACHIEVEMENTS\n\n' %
            (DEFAULTS.get('server_props', {}).get('announce-player-achievments'))
        )
        parser_start.add_argument(
            '--enable-command-block',
            type=str,
            dest='enable_command_block',
            help='BOOLEAN: (true/false) Enables command blocks. Defaults to "%s".\n\n'
                 'Environment: ENABLE_COMMAND_BLOCK\n\n' %
            (DEFAULTS.get('server_props', {}).get('enable-command-block'))
        )
        parser_start.add_argument(
            '--spawn-animals',
            type=str,
            dest='spawn_animals',
            help='BOOLEAN: (true/false) Enables the spawning of passive mobs. Defaults to "%s".\n\n'
                 'Environment: SPAWN_ANIMALS\n\n' %
            (DEFAULTS.get('server_props', {}).get('spawn-animals'))
        )
        parser_start.add_argument(
            '--spawn-monsters',
            type=str,
            dest='spawn_monsters',
            help='BOOLEAN: (true/false) Enables the spawning of hostile mobs. Defaults to "%s".\n\n'
                 'Environment: SPAWN_MONSTERS\n\n' %
            (DEFAULTS.get('server_props', {}).get('spawn-monsters'))
        )
        parser_start.add_argument(
            '--spawn-npcs',
            type=str,
            dest='spawn_npcs',
            help='BOOLEAN: (true/false) Enables the spawning of NPCs, like villagers.'
                 ' Defaults to "%s".\n\n'
                 'Environment: SPAWN_NPCS\n\n' %
            (DEFAULTS.get('server_props', {}).get('spawn-npcs'))
        )
        parser_start.add_argument(
            '--generate-structures',
            type=str,
            dest='generate_structures',
            help='BOOLEAN: (true/false) Enables the generation of structures, like villages.'
                 ' Defaults to "%s".\n\n'
                 'Environment: GENERATE_STRUCTURES\n\n' %
            (DEFAULTS.get('server_props', {}).get('generate-structures'))
        )
        parser_start.add_argument(
            '--view-distance',
            type=str,
            dest='view_distance',
            help='INTEGER: The radius of view (in number of chunks) that will be sent to the'
                 ' client. You need to strike a balance between performance and playability here.'
                 ' Defaults to "%s".\n\n'
                 'Environment: VIEW_DISTANCE\n\n' %
            (DEFAULTS.get('server_props', {}).get('view-distance'))
        )
        parser_start.add_argument(
            '--hardcore',
            type=str,
            dest='hardcore',
            help='BOOLEAN: (true/false) Enables hardcore mode. You die, it\'s over. '
                 'Defaults to "%s".\n\n'
                 'Environment: HARDCORE\n\n' %
            (DEFAULTS.get('server_props', {}).get('hardcore'))
        )
        parser_start.add_argument(
            '--max-build-height',
            type=str,
            dest='max_build_height',
            help='INTEGER: Sets the max build height. Defaults to "%s".\n\n'
                 'Environment: MAX_BUILD_HEIGHT\n\n' %
            (DEFAULTS.get('server_props', {}).get('max-build-height'))
        )
        parser_start.add_argument(
            '--force-gamemode',
            type=str,
            dest='force_gamemode',
            help='BOOLEAN: (true/false) Forces players to join in the default gamemode. If'
                 ' this is false player\'s game mode will be preserved between connections.'
                 ' Defaults to "%s".\n\n'
                 'Environment: FORCE_GAMEMODE\n\n' %
            (DEFAULTS.get('server_props', {}).get('force-gamemode'))
        )
        parser_start.add_argument(
            '--max-tick-time',
            type=str,
            dest='max_tick_time',
            help='INTEGER: (milliseconds) The max amount of time a tick can take to process'
                 ' before it is skipped. Minecraft defaults this to 60000 (or 60 seconds),'
                 ' however packinit sets this to -1 (disabled) to prevent skipped ticks on'
                 ' busy, heavily modded servers as the result of a skipped tick is rubber banding'
                 ' or block lag and will cause all automation to seem to stop.'
                 ' Defaults to "%s".\n\n'
                 'Environment: MAX_TICK_TICK\n\n' %
            (DEFAULTS.get('server_props', {}).get('max-tick-time'))
        )
        parser_start.add_argument(
            '--enable-query',
            type=str,
            dest='enable_query',
            help='BOOLEAN: (true/false) Enables GameSpy4 protocol server listener.'
                 ' Defaults to "%s".\n\n'
                 'Environment: ENABLE_QUERY\n\n' %
            (DEFAULTS.get('server_props', {}).get('enable-query'))
        )
        parser_start.add_argument(
            '--query-port',
            type=str,
            dest='query_port',
            help='INTEGER: The port to list on for GameSpy4. Defaults to "%s".\n\n'
                 'Environment: QUERY_PORT\n\n' %
            (DEFAULTS.get('server_props', {}).get('query-port'))
        )
        parser_start.add_argument(
            '--enable-rcon',
            type=str,
            dest='enable_rcon',
            help='BOOLEAN: (true/false) Enables remote access to the server console.'
                 ' Defaults to "%s".\n\n'
                 'Environment: ENABLE_RCON\n\n' %
            (DEFAULTS.get('server_props', {}).get('enable-rcon'))
        )
        parser_start.add_argument(
            '--rcon-password',
            type=str,
            dest='rcon_password',
            help='STRING: Sets the password for remote console access. Do not expose'
                 ' your RCON port to the internet without a very strong password.'
                 ' Defaults to "%s".\n\n'
                 'Environment: RCON_PASSWORD\n\n' %
            (DEFAULTS.get('server_props', {}).get('rcon-password'))
        )
        parser_start.add_argument(
            '--rcon-port',
            type=str,
            dest='rcon_port',
            help='INTEGER: Sets the port to listen on for remote console access.'
                 ' Defaults to "%s".\n\n'
                 'Environment: RCON_PORT\n\n' %
            (DEFAULTS.get('server_props', {}).get('rcon-port'))
        )
        parser_start.add_argument(
            '--max-players',
            type=str,
            dest='max_players',
            help='INTEGER: Sets the maximum number of players that can be connected at'
                 ' any given time. Defaults to "%s".\n\n'
                 'Environment: MAX_PLAYERS\n\n' %
            (DEFAULTS.get('server_props', {}).get('max-players'))
        )
        parser_start.add_argument(
            '--max-world-size',
            type=str,
            dest='max_world_size',
            help='INTEGER: Sets the maximum radius in blocks that the world can grown, centered'
                 ' on spawn. Defaults to "%s".\n\n'
                 'Environment: MAX_WORLD_SIZE\n\n' %
            (DEFAULTS.get('server_props', {}).get('max-world-size'))
        )
        parser_start.add_argument(
            '--level-name',
            type=str,
            dest='level_name',
            help='STRING: Sets the name of the world. Affects the save folder for the overworld'
                 ' in the server directory. Do not change this on an existing world without'
                 ' renaming the world folder.'
                 ' Defaults to "%s".\n\n'
                 'Environment: LEVEL_NAME\n\n' %
            (DEFAULTS.get('server_props', {}).get('level-name'))
        )
        parser_start.add_argument(
            '--level-seed',
            type=str,
            dest='level_seed',
            help='INTEGER: Sets the seed for map generation. Defaults to "%s".\n\n'
                 'Environment: LEVEL_SEED\n\n' %
            (DEFAULTS.get('server_props', {}).get('level-seed'))
        )
        parser_start.add_argument(
            '--pvp',
            type=str,
            dest='pvp',
            help='BOOLEAN: (true/false) Enables PVP mode. Defaults to "%s".\n\n'
                 'Environment: PVP\n\n' %
            (DEFAULTS.get('server_props', {}).get('pvp'))
        )
        parser_start.add_argument(
            '--generator-settings',
            type=str,
            dest='generator_settings',
            help='STRING: The settings used to customize world generation. Enter a JSON formatted'
                 ' string. See https://tinyurl.com/y54aaft7 for guidelines.'
                 ' Defaults to "%s".\n\n'
                 'Environment: GENERATOR_SETTINGS\n\n' %
            (DEFAULTS.get('server_props', {}).get('generator-settings'))
        )
        parser_start.add_argument(
            '--online-mode',
            type=str,
            dest='online_mode',
            help='BOOLEAN: (true/false) Enables Minecraft login for the server.'
                 ' Defaults to "%s".\n\n'
                 'Environment: ONLINE_MODE\n\n' %
            (DEFAULTS.get('server_props', {}).get('online-mode'))
        )
        parser_start.add_argument(
            '--allow-flight',
            type=str,
            dest='allow_flight',
            help='BOOLEAN: (true/false) Enables flight. Defaults to "%s".\n\n'
                 'Environment: ALLOW_FLIGHT\n\n' %
            (DEFAULTS.get('server_props', {}).get('allow-flight'))
        )
        parser_start.add_argument(
            '--level-type',
            type=str,
            dest='level_type',
            help='STRING: (DEFAULT/FLAT/etc.. Mods can add more.) Select the level type for mapgen'
                 '. Defaults to "%s".\n\n'
                 'Environment: LEVEL_TYPE\n\n' %
            (DEFAULTS.get('server_props', {}).get('level-type'))
        )
        parser_start.add_argument(
            '--white-list',
            type=str,
            dest='white_list',
            help='BOOLEAN: (true/false) Enables white list mode. Anyone not on the white list'
                 ' will have their connection rejected. Defaults to "%s".\n\n'
                 'Environment: WHITE_LIST\n\n' %
            (DEFAULTS.get('server_props', {}).get('white-list'))
        )
        parser_start.add_argument(
            '--spawn-protection',
            type=str,
            dest='spawn_protection',
            help='INTEGER: Sets the area to protect around the spawn block. The spawn block'
                 ' is always protected. Defaults to "%s".\n\n'
                 'Environment: SPAWN_PROTECTION\n\n' %
            (DEFAULTS.get('server_props', {}).get('spawn-protection'))
        )
        parser_start.add_argument(
            '--difficulty',
            type=str,
            dest='difficulty',
            help='INTEGER: (0: peacful, 1: easy, 2: normal, 3: hard) Sets the difficulty level'
                 '. Defaults to "%s".\n\n'
                 'Environment: DIFFICULTY\n\n' %
            (DEFAULTS.get('server_props', {}).get('difficulty'))
        )
        parser_start.add_argument(
            '--gamemode',
            type=str,
            dest='gamemode',
            help='INTEGER: (0: survival, 1: creative, 2: adventure, 3: spectator) Sets the game'
                 ' mode. Defaults to "%s".\n\n'
                 'Environment: GAMEMODE\n\n' %
            (DEFAULTS.get('server_props', {}).get('gamemode'))
        )
        parser_start.set_defaults(func=self.start)
        return parser

    @staticmethod
    def arg_dict(args):
        """
        | Arg dict generator.
        :return:
        """
        arg_config = {
            'verbose': args.verbose,
            'dist_dirs': args.dist_dirs,
            'cache': args.cache,
            'server_dir': args.server_dir,
            'no_update': args.no_update,
            'prop_file': args.prop_file,
            'game_type': args.game_type,
            'minecraft_version': args.minecraft_version,
            'pack_name': args.pack_name,
            'pack_creator': args.pack_creator,
            'server_host': args.server_host,
            'dest_email': args.dest_email,
            'src_email': args.src_email,
            'mail_server': args.mail_server,
            'mail_port': args.mail_port,
            'log_level': args.log_level,
            'log_dir': args.log_dir,
            'java_params': {
                'memory': args.java_mem,
                'fml_confirm': args.fml_confirm,
                'log_level': args.minecraft_log_level,
                'log4j_xml': args.minecraft_log4j_conf
            },
            'server_props': {
                'motd': args.motd,
                'server-port': args.server_port,
                'allow-nether': args.allow_nether,
                'announce-player-achievements': args.announce_player_achievements,
                'enable-command-block': args.enable_command_block,
                'spawn-animals': args.spawn_animals,
                'spawn-monsters': args.spawn_monsters,
                'spawn-npcs': args.spawn_npcs,
                'generate-structures': args.generate_structures,
                'view-distance': args.view_distance,
                'hardcore': args.hardcore,
                'max-build-height': args.max_build_height,
                'force-gamemode': args.force_gamemode,
                'max-tick-time': args.max_tick_time,
                'enable-query': args.enable_query,
                'query.port': args.query_port,
                'enable-rcon': args.enable_rcon,
                'rcon.password': args.rcon_password,
                'rcon.port': args.rcon_port,
                'max-players': args.max_players,
                'max-world-size': args.max_world_size,
                'level-name': args.level_name,
                'level-seed': args.level_seed,
                'pvp': args.pvp,
                'generator-settings': args.generator_settings,
                'online-mode': args.online_mode,
                'allow-flight': args.allow_flight,
                'level-type': args.level_type,
                'white-list': args.white_list,
                'spawn-protection': args.spawn_protection,
                'difficulty': args.difficulty,
                'gamemode': args.gamemode
            }
        }
        return arg_config

    def start(self):
        """
        | Starts and updates a Minecraft instance.
        | :param args: `object` argparse arguments object.
        | :return:
        """

        self.logger.info('Initializing start routine...')
        pack_manager = PackManager(self.config.dist_dirs, self.config.cache)
        pack_update = PackFileUpdater(self.config.dist_dirs[0], self.config.server_dir)
        prop_manager = PropertyFileManager(self.config.prop_file, self.config.server_props)

        self.logger.info('Syncing pack files to server directory and updating settings...')
        pack_manager.install_pack()
        pack_update.sync()
        prop_manager.read()
        prop_manager.update_properties()
        prop_manager.write()

        self.logger.info('Prepare for launch...')
        server = JavaRunner(
            self.config.server_dir,
            self.config.dist_dirs[0],
            self.config.java_params
        )
        server.main()

        sys.exit(0)
