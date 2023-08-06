# https://github.com/sacOO7/socketcluster-client-python
from socketclusterclient import Socketcluster
# https://github.com/titouandk/emitter.py
from emitter import Emitter

from uuid import uuid4
from threading import Thread
from . import constants
from . import proto
from . import __version__
import os
from google.protobuf import message as _message
import base64
import traceback
import time
import socket as sock
import json
import re
from inspect import signature

class RTI(Emitter):

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        if self.connected and not self.incognito:
            self._publish_state()

    def __init__(self, application_id="python", application_version=None, instance_id=None, federation_id=None, secret=None, user=None, password=None, incognito=False, suppress_own_messages=False, connect=True):
        super().__init__()

        self.subscriptions = {}
        self.known_channels = {}
        self.used_channels = {}
        self.known_clients = {}

        self._state = proto.UNKNOWN
        self.connected = False
        self.cluster_version = None

        url = None
        if not url:
            url = os.environ.get('GEISTT_RTI_URL')
        if not url:
            url = constants.default_url
        self.url = url

        self.application_id = application_id
        self.application_version = application_version
        self.instance_id = instance_id
        if not self.instance_id:
            self.instance_id = str(uuid4())
        self.federation_id = federation_id
        if not self.federation_id:
            self.federation_id = os.environ.get('GEISTT_RTI_FEDERATION')

        auth_secret = None
        if not auth_secret:
            auth_secret = os.environ.get('GEISTT_RTI_SECRET')
        if not auth_secret:
            auth_secret = secret
        self.user = user

        self._host = os.environ.get('GEISTT_RTI_HOST')
        if not self._host:
            self._host = sock.gethostname()
        self._station = os.environ.get('GEISTT_RTI_STATION')

        self.incognito = incognito

        auth_token = {
            'applicationId': self.application_id,
            'instanceId': self.instance_id,
            'clientLibraryVersion': __version__
        }
        if auth_secret:
            auth_token['secret'] = auth_secret
        if user:
            auth_token['user'] = user
        if password:
            auth_token['password'] = password
        if suppress_own_messages:
            auth_token['suppressOwnMessages'] = True
        if self.federation_id:
            auth_token['federationId'] = self.federation_id

        socket = Socketcluster.socket(url)
        socket.setdelay(2)
        socket.setreconnection(True)

        def on_connect(socket):
            pass

        def on_disconnect(socket):
            self.connected = False
            self.emit("disconnect")

        def on_fail(socket, error):
            self.emit("error", "fail", error, None)

        def on_connection_error(socket, error):
            self.emit("error", "connection", error, None)

        def on_set_auth(socket, token):
            self.connected = True
            socket.setAuthtoken(token)
            self.subscribe(constants.clients_channel,
                           proto.Clients, on_clients)
            self.subscribe(constants.channels_channel,
                           proto.Channels, on_channels)
            if self.federation_id:
                self.publish_text(
                    constants.federations_channel, self.federation_id)
                self.subscribe_text(
                    constants.federations_channel, on_federations)
            for channel_name in self.subscriptions:
                socket.subscribe(channel_name)
            if not self.incognito:
                self._publish_client()
            self.emit("connect")

        def on_auth(socket, is_authenticated):
            socket.emit("auth", auth_token)

        def on_clients(message: proto.Clients):
            if message.HasField("request_clients") and not self.incognito:
                self._publish_client()
            elif message.HasField("client"):
                self.known_clients[message.client.instance_id] = message.client

        def on_channels(message: proto.Channels):
            if message.HasField("request_channel_usage"):
                message = proto.Channels()
                message.channel_usage.instance_id = self.instance_id
                message.channel_usage.usage.extend(self.used_channels.values())
                if not self.incognito:
                    self.publish(constants.channels_channel, message)
            elif message.HasField("channel_usage"):
                for use in message.channel_usage.usage:
                    self.known_channels[use.channel.name] = use.channel
            elif message.HasField("channel"):
                self.known_channels[message.channel.name] = message.channel

        def on_federations(message: str):
            if message == "?":
                self.publish_text(
                    constants.federations_channel, self.federation_id)

        def on_cluster_version(channel: str, content: str):
            self.cluster_version = content

        socket.setBasicListener(on_connect, on_disconnect, on_connection_error)
        socket.setAuthenticationListener(on_set_auth, on_auth)
        socket.on("fail", on_fail)
        socket.on("cluster-version", on_cluster_version)
        self.socket = socket
        self.thread = None
        if connect:
            self.connect()

    def connect(self):
        self.thread = Thread(target=self.socket.connect)
        self.thread.daemon = True
        self.thread.start()

    def disconnect(self):
        self.socket.disconnect()
        self.connected = False
        self.emit("disconnect")

    def wait_until_connected(self):
        count = 0
        while count < 500 and not self.connected:
            count += 1
            time.sleep(0.01)
        return self.connected

    def subscribe(self, channel_name: str, message_class, handler):
        def handle_message(content):
            message = self.parse(message_class, content)
            if len(signature(handler).parameters) < 2:
                handler(message)
            else:
                handler(channel_name, message)
        return self.subscribe_text(channel_name, handle_message, str(message_class))

    @classmethod
    def parse(cls, message_class, content):
        message = message_class()
        message.ParseFromString(base64.b64decode(content))
        return message


    def subscribe_json(self, channel_name: str, handler):
        def handle_message(content):
            if len(signature(handler).parameters) < 2:
                handler(json.loads(content))
            else:
                handler(channel_name, json.loads(content))
        return self.subscribe_text(channel_name, handle_message, "json")

    def subscribe_text(self, channel_name: str, handler, data_type="text"):
        socket_channel_name = channel_name
        if self.federation_id and channel_name != constants.federations_channel:
            socket_channel_name = self.federation_id + "/" + channel_name
        if (socket_channel_name not in self.subscriptions):
            if self.connected:
                self.socket.subscribe(socket_channel_name)
            self.subscriptions[socket_channel_name] = []
            self._add_channel(channel_name, False, data_type)

            def handle_message(in_channel_name, content):
                for listener in self.subscriptions[socket_channel_name]:
                    try:
                        if len(signature(listener).parameters) < 2:
                            listener(content)
                        else:
                            listener(channel_name, content)
                    except Exception as e:
                        self.emit("error", channel_name, e,
                                  traceback.format_exc())
            self.socket.onchannel(socket_channel_name, handle_message)

        self.subscriptions[socket_channel_name].append(handler)
        return handler

    def unsubscribe(self, channel_name_or_handler):
        if (channel_name_or_handler is str):
            if self.federation_id and channel_name_or_handler != constants.federations_channel:
                channel_name_or_handler = self.federation_id + "/" + channel_name_or_handler
            self.socket.unsubscribe(channel_name_or_handler)
            if channel_name_or_handler in self.subscriptions:
                self.subscriptions.pop(channel_name_or_handler)
        else:
            for channel_name in self.subscriptions:
                if channel_name_or_handler in self.subscriptions[channel_name]:
                    self.subscriptions[channel_name].remove(
                        channel_name_or_handler)
                    if len(self.subscriptions[channel_name]) <= 0:
                        self.socket.unsubscribe(channel_name_or_handler)

    def publish(self, channel_name: str, message: _message.Message):
        try:
            self._add_channel(channel_name, True, data_type=str(type(message)))
            content = base64.b64encode(
                message.SerializeToString()).decode("utf8")
            if self.federation_id and not channel_name.startswith("@"):
                channel_name = self.federation_id + "/" + channel_name
            self.socket.publish(channel_name, content)
        except Exception as e:
            print(e)

    def publish_text(self, channel_name: str, content: str):
        try:
            self._add_channel(channel_name, True, data_type="text")
            if self.federation_id and not channel_name.startswith("@") and channel_name != constants.federations_channel:
                channel_name = self.federation_id + "/" + channel_name
            self.socket.publish(channel_name, content)
        except Exception as e:
            print(e)
    
    def publish_json(self, channel_name: str, message: object):
        try:
            self._add_channel(channel_name, True, data_type="json")
            if self.federation_id and not channel_name.startswith("@") and channel_name != constants.federations_channel:
                channel_name = self.federation_id + "/" + channel_name
            self.socket.publish(channel_name, json.dumps(message))
        except Exception as e:
            print(e)


    def publish_error(self, error_message, runtime_state: proto.RuntimeState = None):
        message = proto.RuntimeControl()
        message.error.application_id = self.application_id
        message.error.instance_id = self.instance_id
        message.error.message = error_message
        if runtime_state is not None:
            message.error.state = runtime_state
        self.publish(constants.control_channel, message)

    def _publish_client(self):
        message = proto.Clients()
        message.client.application_id = self.application_id
        message.client.instance_id = self.instance_id
        message.client.state = self._state
        message.client.client_library_version = __version__
        if self.application_version:
            message.client.application_version = self.application_version
        if self._host:
            message.client.host = self._host
        if self._station:
            message.client.station = self._station
        if self.user:
            message.client.user = self.user
        self.publish(constants.clients_channel, message)

    def _add_channel(self, channel_name, publish, data_type=None):
        if channel_name.startswith("@"): return
        channel = proto.Channels.Channel()
        channel.name = channel_name
        data_type = re.sub("<class.*_pb2\\.", "", data_type)
        data_type = re.sub("'>", "", data_type)
        channel.data_type = data_type
        use = None
        if channel_name not in self.used_channels:
            use = proto.Channels.ChannelUse()
            use.channel.CopyFrom(channel)
            self.used_channels[channel_name] = use
        else:
            use = self.used_channels[channel_name]
        if publish: use.publish = True
        else: use.subscribe = True
        if channel_name not in self.known_channels:
            self.known_channels[channel_name] = channel
            if self.connected and not self.incognito:
                message = proto.Channels()
                message.channel.CopyFrom(channel)
                self.publish(constants.channels_channel, message)

    def _publish_state(self):
        message = proto.RuntimeControl()
        message.state.application_id = self.application_id
        message.state.instance_id = self.instance_id
        message.state.state = self._state
        self.publish(constants.control_channel, message)
