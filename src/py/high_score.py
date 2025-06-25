from storage import BaseStorageAdaptor
from typing import List, Optional, Tuple

_HIGH_SCORES: Optional[List[Tuple[str, int]]] = None
NUMBER_TOP_SCORES = 10

class HighScore:

    def __init__(self, storage_adaptor: BaseStorageAdaptor):
        global _HIGH_SCORES

        self.storage_adaptor = storage_adaptor
        if _HIGH_SCORES is None:
            # Load from persistent storage
            _HIGH_SCORES = self.storage_adaptor.load('high_score') or []

    def check_and_insert_score(self, name, score):
        """
        Check if the given score is one of the top N and add it into the high scores list if so. Returns -1 if not a
        high score, otherwise the index of where it was added.
        """
        global _HIGH_SCORES

        if len(_HIGH_SCORES) < NUMBER_TOP_SCORES or score > _HIGH_SCORES[-1][1]:
            insertion_index = 0
            for _, existing_score in _HIGH_SCORES:
                if score > existing_score:
                    break
                else:
                    insertion_index += 1
            _HIGH_SCORES.insert(insertion_index, (name, score))
            if len(_HIGH_SCORES) > NUMBER_TOP_SCORES:
                _HIGH_SCORES.pop()
            self.storage_adaptor.save('high_score', _HIGH_SCORES)
            return insertion_index
        return -1

    def get_top_scores(self):
        return _HIGH_SCORES