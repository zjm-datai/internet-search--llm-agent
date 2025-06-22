import copy 
from typing import List, Union 

from lagent.agents import Agent, AgentForInternLM, AysncAgent, AsyncAgentForInternLM
from lagent.schema import AgentMessage, AgentStatusCode, ModelStatusCode

class StreamingAgentMixin:
    """ 
    Make agent calling output a streaming response.
    """

    def __call__(self, *message: Union[AgentMessage, List[AgentMessage]], session_id=0, **kwargs):
        for hook in self._hooks.values():
            message = copy.deepcopy(message)
            result = hook.before_agent(self, message, session_id)
            if result:
                message = result 

        self.update_memory(message, session_id=session_id)
        response_message = AgentMessage(sender=self.name, content="")
        for response_message in self.forward(*message, session_id=session_id, **kwargs):
            if not isinstance(response_message, AgentMessage):
                model_state, response = response_message
                response_message = AgentMessage(
                    sender=self.name, 
                    content=response, 
                    stream_state=model_state
                )
            yield response_message.model_copy() 

        self.update_memory(response_message, session_id=session_id)
        for hook in self._hooks.values():
            response_message = response_message.model_copy(deep=True) 
            result = hook.after_agent(self, response_message, session_id) 
            if result:
                response_message = result
        yield response_message

class AsyncStreamingAgentMixin:
    pass 

class StreamingAgent(StreamingAgentMixin, Agent):
    """ 
    Base streaming agent class
    """

    def forward(self, *message: AgentMessage, session_id=0, **kwargs):
        formatted_messages = self.aggregator.aggregate(
            
        )