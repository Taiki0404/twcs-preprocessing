class TwcsDialogExtractor:
    def __init__(self):
        pass

    def __split_res_tweet_id(self, tweet_ids: str) -> list:
        if not tweet_ids:
            return []

        return [int(i) for i in tweet_ids.split(",")]

    def __extract_dialog_paths(
        self,
        graph: dict,
        start_node: int,
        twcs_dict: dict[int, dict],
    ) -> list:
        stack: list[tuple[int, list[int]]] = [(start_node, [])]
        paths = []

        while stack:
            node, path = stack.pop()
            path.append(node)

            if node not in graph:
                record = twcs_dict.get(node, {})
                res_tweet_id = record.get("response_tweet_id", "")
                if isinstance(res_tweet_id, str):
                    graph[node] = self.__split_res_tweet_id(res_tweet_id)
                else:
                    graph[node] = []

            if not graph[node]:  # 隣接ノードがない場合
                paths.append(list(path))
            else:
                for neighbor in graph[node]:
                    if neighbor not in path:  # サイクルを防ぐ
                        stack.append((neighbor, list(path)))

        return paths

    def extract_dialog_branching(self, start: int, twcs_dict: dict) -> list[list[int]]:
        graph: dict[int, list[int]] = {}
        return self.__extract_dialog_paths(graph, start, twcs_dict)

    def extract_all_dialog_branching(self, starts: list[int], twcs_dict: dict) -> list[list[int]]:
        all_paths = []
        for start in starts:
            paths = self.extract_dialog_branching(start, twcs_dict)
            all_paths.extend(paths)

        return all_paths
