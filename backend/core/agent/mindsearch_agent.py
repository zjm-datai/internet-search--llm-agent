

from .graph import WebSearchGraph 



class MindSearchAgent(StreamingAgentForInternLM):
    def __init__(
            self, 
            searcher_cfg: dict, 
            summary_prompt: str, 
            finish_condition=lambda m: "add_response_node" in m.content,
            max_turn: int = 10,
            **kwargs, 
    ): 
        WebSearchGraph.SEARCHER_CONFIG = searcher_cfg