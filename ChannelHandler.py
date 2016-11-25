import uuid
import json

class ChannelHandler(object):
    def __init__(self):
        self.client_info = {}
        self.channel_info = {}
        self.channel_users = {}

    def generate_channel(self, channel, client):
        client_id = uuid.uuid4().hex
        if not channel in self.channel_info:
            self.channel_info[channel] = []
        counter = 1
        user = client
        clients_list = self.registered_client(channel)
        while True:
            if user in clients_list:
                user = client + str(counter)
            else:
                break
            counter += 1

        self.client_info[client_id] = {'channel': channel, 'client': user}  # we still don't know the WS connection for this client
        self.channel_info[channel].append({'client_id': client_id, 'client': user})
        return client_id

    def generate_connection(self, client_id, conn):
        self.client_info[client_id]['socket_conn'] = conn
        client_channel = self.client_info[client_id]['channel']

        if client_channel in self.channel_users:
            self.channel_users[client_channel].add(conn)
        else:
            self.channel_users[client_channel] = {conn}

        for user in self.channel_info[client_channel]:
            if user['client_id'] == client_id:
                user['socket_conn'] = conn
                break
        self.send_pong_on_join(client_id)
        clients_list = self.registered_client(client_channel)
        connections = self.channel_connection(client_id)
        self.send_message(connections, clients_list)

    def remove_client(self, client_id):
        client_channel = self.client_info[client_id]['channel']
        client = self.client_info[client_id]['client']
        client_conn = self.client_info[client_id]['socket_conn']
        if client_conn in self.channel_users[client_channel]:
            self.channel_users[client_channel].remove(client_conn)
            if len(self.channel_users[client_channel]) == 0:
                del(self.channel_users[client_channel])
        remotely_connected_clients = self.channel_connection(client_id)
        remotely_connected_clients = [conn for conn in remotely_connected_clients if conn != self.client_info[client_id]['socket_conn']]
        self.client_info[client_id] = None
        for user in self.channel_info[client_channel]:
            if user['client_id'] == client_id:
                self.channel_info[client_channel].remove(user)
                break
        self.send_pong_on_leave(client, remotely_connected_clients)
        clients_list = self.registered_client(client_channel)
        self.send_message(remotely_connected_clients, clients_list)
        if len(self.channel_info[client_channel]) == 0:
            del(self.channel_info[client_channel])
            print "Removed empty channel %s" % client_channel

    def registered_client(self, channel):
        clients_list = []
        for user in self.channel_info[channel]:
            clients_list.append(user['client'])
        return clients_list

    def channel_connection(self, client_id):
        client_channel = self.client_info[client_id]['channel']
        remotely_connected = []
        if client_channel in self.channel_users:
            remotely_connected = self.channel_users[client_channel]
        return remotely_connected


    def send_pong_on_join(self, client_id):
        client = self.client_info[client_id]['client']
        remotely_connected_clients = self.channel_connection(client_id)
        msg = {"msgtype": "join", "username": client, "payload": " joined the chat channel."}
        pmessage = json.dumps(msg)
        for conn in remotely_connected_clients:
            conn.write_message(pmessage)

    @staticmethod
    def send_message(connections, clients_list):
        message = {"msgtype": "nick_list", "payload": clients_list}
        pmessage = json.dumps(message)
        for connected in connections:
            connected.write_message(pmessage)

    @staticmethod
    def send_pong_on_leave(client, remote_connected):
        message = {"msgtype": "leave", "username": client, "payload": " left the chat channel."}
        pmessage = json.dumps(message)
        for conn in remote_connected:
            conn.write_message(pmessage)