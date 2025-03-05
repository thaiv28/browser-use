import logging
import math

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from browser_use.critic.prompts import SYSTEM_MESSAGE, USER_MESSAGE

class CriticGPT:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini").bind(logprobs=True)
        self.logger = logging.getLogger(__name__)
    
    def score(self, input_messages, proposed_action) -> float:
        for i in reversed([0, 2, 3, 4]):
            input_messages.pop(i)
        
        system_message = SystemMessage(content=SYSTEM_MESSAGE)
        proposed_msg = HumanMessage(content=f"The proposed action is: {proposed_action}")
        query = SystemMessage(content=USER_MESSAGE)
        critic_input = [system_message] + input_messages + [proposed_msg] + [query]
       
        output = self.llm.invoke(critic_input)
      
        logprobs = output.response_metadata["logprobs"]["content"]
        for d in logprobs:
            if d["token"] == 'A':
                return math.exp(d["logprob"])
            
        self.logger.warning("Critic output unresolved. Returning score 1.0 from: %s", output.content)
        return 1.0
        

        
        