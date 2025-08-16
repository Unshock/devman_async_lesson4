import configargparse


def parse_base_args():
    parser = configargparse.ArgParser(
        default_config_files=['./config.yaml']
    )
    parser.add_argument('--host', help='Host for the chat server')
    parser.add_argument('--read_port', help='Port for reading messages')
    parser.add_argument('--write_port', help='Port for writing messages')
    parser.add_argument('--history', help='File to store message history')
    subparsers = parser.add_subparsers(dest='command')

    return parser, subparsers


def parse_view_args():
    parser, subparsers = parse_base_args()
    config = _get_base_config(parser)

    view = subparsers.add_parser('view', help='Connect chat to view messages')
    view.add_argument(
        '--host',
        '--CHAT_HOST',
        required=False,
        default=config.host,
        env_var='CHAT_HOST',
    )
    view.add_argument(
        '--port',
        '--CHAT_READ_PORT',
        required=False,
        default=config.read_port,
        env_var='CHAT_READ_PORT',
    )
    view.add_argument(
        '--history',
        '--CHAT_HISTORY_FILE',
        required=False,
        default=config.history,
        env_var='CHAT_HISTORY_FILE',
    )

    return view.parse_args()


def parse_messaging_args():
    parser, subparsers = parse_base_args()
    config = _get_base_config(parser)

    messaging = subparsers.add_parser(
        'messaging',
        help='Connect chat to send messages'
    )
    messaging.add_argument(
        '--host',
        '--CHAT_HOST',
        required=False,
        default=config.host,
        env_var='CHAT_HOST',
    )
    messaging.add_argument(
        '--port',
        '--CHAT_WRITE_PORT',
        required=False,
        default=config.write_port,
        env_var='CHAT_WRITE_PORT',
    )
    messaging.add_argument(
        '--user_token',
        '--CHAT_USER_TOKEN',
        required=False,
        env_var='CHAT_USER_TOKEN',
    )
    messaging.add_argument(
        '--user_name',
        '--CHAT_USER_NAME',
        required=False,
        env_var='CHAT_USER_NAME',
    )

    return messaging.parse_args()


def parse_send_message_args():
    parser, subparsers = parse_base_args()
    config = _get_base_config(parser)

    send_message = subparsers.add_parser(
        'send_message',
        help='Send single message to chat'
    )
    send_message.add_argument(
        '-m',
        '--message',
        required=True
    )
    send_message.add_argument(
        '--host',
        '--CHAT_HOST',
        required=False,
        default=config.host,
        env_var='CHAT_HOST',
    )
    send_message.add_argument(
        '--port',
        '--CHAT_WRITE_PORT',
        required=False,
        default=config.write_port,
        env_var='CHAT_WRITE_PORT',
    )
    send_message.add_argument(
        '--user_token',
        '--CHAT_USER_TOKEN',
        required=False,
        env_var='CHAT_USER_TOKEN',
    )
    send_message.add_argument(
        '--user_name',
        '--CHAT_USER_NAME',
        required=False,
        env_var='CHAT_USER_NAME',
    )

    return send_message.parse_args()


def parse_register_user_args():
    parser, subparsers = parse_base_args()
    config = _get_base_config(parser)

    register_user = subparsers.add_parser(
        'register_user',
        help='Register new user'
    )
    register_user.add_argument(
        '--host',
        '--CHAT_HOST',
        required=False,
        default=config.host,
        env_var='CHAT_HOST',
    )
    register_user.add_argument(
        '--port',
        '--CHAT_WRITE_PORT',
        required=False,
        default=config.write_port,
        env_var='CHAT_WRITE_PORT',
    )
    register_user.add_argument(
        '--user_name',
        '--CHAT_USER_NAME',
        required=True,
        env_var='CHAT_USER_NAME',
    )

    return register_user.parse_args()


def _get_base_config(parser):
    config, _ = parser.parse_known_args()
    return config
