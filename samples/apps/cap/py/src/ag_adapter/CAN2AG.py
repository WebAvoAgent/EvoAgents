from DebugLog import Debug, Error, Info, Warn, shorten
from LocalActorNetwork import LocalActorNetwork
from proto.Autogen_pb2 import GenReplyReq, GenReplyResp, PrepChat, ReceiveReq, Terminate
from autogen import Agent
from enum import Enum
from typing import Dict, List, Optional, Union
from ag_adapter.AG2CAN import AG2CAN
from CANActor import CANActor

class CAN2AG(CANActor):
    """
    A CAN actor that acts as an adapter for the AutoGen system.
    """
    States = Enum('States', ['INIT', 'CONVERSING'])

    def __init__(self,
                 ag_agent,
                 the_other_name,
                 init_chat,
                 self_recursive=True):
        super().__init__(ag_agent.name, ag_agent.description)
        self._the_ag_agent = ag_agent
        self._ag2can_other_agent:AG2CAN = None
        self._other_agent_name = the_other_name
        self._init_chat = init_chat
        self.STATE = self.States.INIT
        self._can2ag_name: str = self.agent_name+".can2ag"
        self._self_recursive = self_recursive
        self._network = None
        self._connectors = {}

    def connect(self, network):
        """
        Connect to the AutoGen system.
        """
        self._network = network
        self._ag2can_other_agent =  AG2CAN(self._network, self._other_agent_name)
        Debug(self._can2ag_name, "connected to {network}")

    def disconnect(self, network: LocalActorNetwork):
        """
        Disconnect from the AutoGen system.
        """
        super().disconnect(network)
#        self._the_other.close()
        Debug(self.agent_name, "disconnected")

    def process_txt_msg(self, msg, msg_type, topic, sender):
        """
        Process a text message received from the AutoGen system.
        """
        Info(self._can2ag_name, f"proc_txt_msg: [{topic}], [{msg_type}], {shorten(msg)}")
        if self.STATE == self.States.INIT:
            self.STATE = self.States.CONVERSING
            if self._init_chat:
                self._the_ag_agent.initiate_chat(self._ag2can_other_agent, message=msg)
            else:
                self._the_ag_agent.receive(msg, self._ag2can_other_agent, True)
        else:
            self._the_ag_agent.receive(msg, self._ag2can_other_agent, True)
        return True

    def _call_agent_receive(self, receive_params):
        request_reply: Optional[bool] = None
        silent: Optional[bool] = False

        if receive_params.HasField('request_reply'):
            request_reply = receive_params.request_reply
        if receive_params.HasField('silent'):
            silent = receive_params.silent

        save_name = self._ag2can_other_agent.name
        self._ag2can_other_agent.set_name(receive_params.sender)
        if receive_params.HasField('data_map'):
            data = dict(receive_params.data_map.data)
        else:
            data = receive_params.data
        self._the_ag_agent.receive(data, self._ag2can_other_agent, request_reply, silent)
        self._ag2can_other_agent.set_name(save_name)

    def receive_msgproc(self, msg):
        """
        Process a ReceiveReq message received from the AutoGen system.
        """
        receive_params = ReceiveReq()
        receive_params.ParseFromString(msg)
        
        self._ag2can_other_agent.reset_receive_called()
        
        if self.STATE == self.States.INIT:
            self.STATE = self.States.CONVERSING
            
            if self._init_chat:
                self._the_ag_agent.initiate_chat(self._ag2can_other_agent, message=receive_params.data)
            else:
                self._call_agent_receive(receive_params)
        else:
            self._call_agent_receive(receive_params)
                       
        if not self._ag2can_other_agent.was_receive_called() and self._self_recursive:
            Warn(self._can2ag_name, "TERMINATE")
            self._ag2can_other_agent.send_terminate(self._the_ag_agent)
            return False
        return True

    def get_actor_connector(self, topic: str):
        """
        Get the actor connector for the given topic.
        """
        if topic in self._connectors:
            return self._connectors[topic]
        else:
            connector = self._network.agent_connector_by_topic(topic)
            self._connectors[topic] = connector
            return connector

    def generate_reply_msgproc(self, msg, sender_topic):
        """
        Process a GenReplyReq message received from the AutoGen system and generate a reply.
        """
        generate_reply_params = GenReplyReq()
        generate_reply_params.ParseFromString(msg)
        reply = self._the_ag_agent.generate_reply(sender=self._ag2can_other_agent)
        connector = self.get_actor_connector(sender_topic)

        reply_msg = GenReplyResp()
        reply_msg.data = reply.encode("utf8")
        serialized_msg = reply_msg.SerializeToString()
        connector.send_bin_msg(type(reply_msg).__name__, serialized_msg)
        return True

    def prepchat_msgproc(self, msg, sender_topic):
        prep_chat = PrepChat()
        prep_chat.ParseFromString(msg)
        self._the_ag_agent._prepare_chat(self._ag2can_other_agent, prep_chat.clear_history, prep_chat.prepare_recipient)
        return True

    def process_bin_msg(self, msg: bytes, msg_type: str, topic: str, sender: str):
        """
        Process a binary message received from the AutoGen system.
        """
        Info(self._can2ag_name, f"proc_bin_msg: topic=[{topic}], msg_type=[{msg_type}]")
        if msg_type == ReceiveReq.__name__:
            return self.receive_msgproc(msg)
        elif msg_type == GenReplyReq.__name__:
            return self.generate_reply_msgproc(msg, sender)
        elif msg_type == PrepChat.__name__:
            return self.prepchat_msgproc(msg, sender)
        elif msg_type == Terminate.__name__:
            Warn(self._can2ag_name, f"TERMINATE received: topic=[{topic}], msg_type=[{msg_type}]")
            return False
        else:
            Error(self._can2ag_name,
                  f"Unhandled message type: topic=[{topic}], msg_type=[{msg_type}]")
        return True
