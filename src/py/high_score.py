from storage import BaseStorageAdaptor

NUMBER_TOP_SCORES = 10


class HighScore:
    """Operations on the high score list"""

    def __init__(self, storage_adaptor: BaseStorageAdaptor):
        self.storage_adaptor = storage_adaptor
        # Load from persistent storage
        self.high_scores = self.storage_adaptor.load("high_score") or []

    def check_and_insert_score(self, name, score):
        """
        Check if the given score is one of the top N and add it into the high scores list if so. Returns -1 if not a
        high score, otherwise the index of where it was added.
        """
        if len(self.high_scores) < NUMBER_TOP_SCORES or score > self.high_scores[-1][1]:
            insertion_index = 0
            for _, existing_score in self.high_scores:
                if score > existing_score:
                    break
                insertion_index += 1
            self.high_scores.insert(insertion_index, (name, score))
            if len(self.high_scores) > NUMBER_TOP_SCORES:
                self.high_scores.pop()
            self.storage_adaptor.save("high_score", self.high_scores)
            return insertion_index
        return -1

    def get_top_scores(self):
        return self.high_scores
