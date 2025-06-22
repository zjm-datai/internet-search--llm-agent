import asyncio 
import queue 


from typing import Dict, List

from lagent.schema import 

from .streaming import AsyncStreamingAgentForInternLM, StreamingAgentForInternLM


class SearcherAgent(StreamingAgentForInternLM):
    def __init__(
            self, 
            user_input_template: str = "{question}", 
            user_context_template: str = None, 
            **kwargs,
    ):
        self.user_input_template = user_input_template
        self.user_context_template = user_context_template 
        super().__init__(**kwargs)

    def forward(
            self, 
            question: str, 
            topic: str, 
            history: List[dict] = None, 
            session_id=0,
            **kwargs,
    ):
        message = [self.user_input_template.format(question=question, topic=topic)]
        if history and self.user_context_template:
            message = [self.user_context_template.format_map(item) for item in history] + message 
        message = "\n".join(message) 
        return super().forward(message, session_id=session_id, **kwargs)
    
class AsyncSearcherAgent(AsyncStreamingAgentForInternLM):
    def __init__(
            self, 
            user_input_template: str = "{question}", 
            user_context_template: str = None, 
            **kwargs,
    ):
        self.user_input_template = user_input_template
        self.user_context_template = user_context_template
        super().__init__(**kwargs)

    async def forward(
            self,
            question: str, 
            topic: str, 
            history: List[dict] = None, 
            session_id=0,
            **kwargs,
    ):
        message = [self.user_input_template.format(question=question, topic=topic)]
        if history and self.user_context_template:
            message = [self.user_context_template.format_map(item) for item in history] + message 
        message = "\n".join(message) 
        async for message in super().forward(message, session_id=session_id, **kwargs):
            yield message 



class WebSearchGraph: 
    is_async = False
    SEARCHER_CONFIG = {}
    _SEARCHER_LOOP = []
    _SEARCHER_THREAD = []

    def __init__(self):
        self.nodes: Dict[str, Dict[str, str]] = {}
        self.adjacency_list: Dict[str, List[dict]] = defaultdict(list) 
        self.future_to_query = dict() 
        self.searcher_resp_queue = queue.Queue() 
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.n_active_tasks = 0 

    def add_root_node(
            self, 
            node_content: str, 
            node_name: str = "root"
    ):
        """ 
        添加起始节点
        """
        self.nodes[node_name] = dict(content=node_content, type="root")
        self.adjacency_list[node_name] = []

    def add_node(
            self, 
            node_name: str, 
            node_content: str,
    ):
        """
        添加搜索子问题节点
        """

        self.nodes[node_name] = dict(content=node_content, type="searcher") 
        self.adjacency_list[node_name] = []

        parent_nodes = []
        for start_node, adj in self.adjacency_list.items():
            for neighbor in adj:
                if (
                    node_name == neighbor
                    and start_node in self.nodes 
                    and "response" in self.nodes[start_node]
                ):
                    parent_nodes.append(self.nodes[start_node]) 
        parent_response = [
            dict(question=node["content"], answer=node["response"]) for node in parent_nodes
        ]

        if self.is_async:
            async def _async_search_node_stream():
                cfg = {
                    **self.SEARCHER_CONFIG,
                    "plugins": deepcopy(self.SEARCHER_CONFIG.get("plugin")),
                }
                agent, session_id = AsyncSearcherAgent(**cfg), random.randint(0, 999999)
                searcher_message = AgentMessage(sender="SearcherAgent", content="")
                try:
                    async for searcher_message in agent(
                        question=node_content, 
                        topic=self.nodes["root"]["content"],
                        history=parent_response, 
                        session_id=session_id, 
                    ):
                        self.nodes[node_name]["response"] = searcher_message.model_dump()
                        self.nodes[node_name]["memory"] = agent.state_dict(session_id=session_id)
                        self.nodes[node_name]["session_id"] = session_id 
                        self.searcher_resp_queue.put((node_name, self.nodes[node_name], []))

                    self.searcher_resp_quque.put((None, None, None))
                except Exception as exc:
                    self.searcher_resp_queue.put((exc, None, None))

            self.future_to_query[
                asyncio.run_coroutine_threadsafe(
                    _async_search_node_stream(), random.choice(self._SEARCHER_LOOP)
                )
            ] = f"{node_name}-{node_content}"
        
        else:
            def _search_node_stream():
                cfg = {
                    **self.SEARCHER_CONFIG, 
                    "plugins": deepcopy(self.SEARCHER_CONFIG.get("plugins")),
                }
                agent, session_id = SearcherAgent(**cfg), random.randint(0, 999999)
                searcher_message = AgentMessage(sender="SearcherAgent", content="")
                

    def add_response_node(self, node_name="response"):
        """ 
        添加回复节点
        """

        self.nodes[node_name] = dict(type="end")
        self.searcher_resp_queue.put((node_name, self.nodes[node_name], []))

    def add_edge(self, start_node: str, end_node: str):
        """
        添加边
        """
        self.adjacency_list[start_node].append(dict(id(str(uuid.uuid4())), name=end_node, state=2))
        self.searcher_resp_queue.put(
            (start_node, self.nodes[start_node], self.adjacency_list[start_node])
        )

    def reset(self):
        self.nodes = {}
        self.adjacency_list = defaultdict(list)

    def node(self, node_name: str) -> str:
        return self.nodes[node_name].copy()


    @classmethod
    def start_loop(cls, n: int = 32):
        if not cls.is_async:
            raise RuntimeError("Event loop cannot be launched as `is_async` is disabled")
        
        