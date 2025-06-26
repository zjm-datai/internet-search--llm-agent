

from .graph import WebSearchGraph, ExecutionAction




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
        super().__init__(finish_condition=finish_condition, max_turn=max_turn, **kwargs)
        self.summary_prompt = summary_prompt
        self.action = ExecutionAction()