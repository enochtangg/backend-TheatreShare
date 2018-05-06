import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from .settings import MSG_TYPE_LEAVE, MSG_TYPE_ENTER, NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS
from .models import Theatre
from .utils import get_room_or_error, catch_client_error
from .exceptions import ClientError


@channel_session_user_from_http
def ws_connect(message):
    message.channel_session['theatres'] = []


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@channel_session_user
def ws_disconnect(message):
    for theatre_id in message.channel_session.get("theatre", set()):
        try:
            theatre = Theatre.objects.get(pk=theatre_id)
            theatre.websocket_group.discard(message.reply_channel)
        except Theatre.DoesNotExist:
            pass


@channel_session_user
@catch_client_error
def chat_join(message):
    theatre = get_room_or_error(message["theatre"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        theatre.send_message(None, message.user, MSG_TYPE_ENTER)

        theatre.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['theatres']).union([theatre.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(theatre.id),
            "title": theatre.name,
        }),
    })


@channel_session_user
@catch_client_error
def chat_leave(message):
    theatre = get_room_or_error(message["theatre"], message.user)

    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        theatre.send_message(None, message.user, MSG_TYPE_LEAVE)

    theatre.websocket_group.discard(message.reply_channel)
    message.channel_session['theatres'] = list(set(message.channel_session['theatres']).difference([theatre.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(theatre.id),
        }),
    })


@channel_session_user
@catch_client_error
def chat_send(message):
    if int(message['theatre']) not in message.channel_session['theatres']:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["theatre"], message.user)
    room.send_message(message["message"], message.user)
