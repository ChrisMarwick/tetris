import pytest
from high_score import HighScore
from storage import InMemoryStorage


@pytest.fixture
def dummy_storage():
    return InMemoryStorage(
        {
            "high_score": [
                ("Chris", 1000),
                ("Albert", 900),
                ("Bob", 850),
                ("Dylan", 700),
                ("Edward", 400),
                ("Fred", 400),
                ("Greg", 300),
                ("Hilary", 250),
                ("Ilya", 210),
                ("Jack", 100),
            ]
        }
    )


class TestHighScore:
    """Tests for high score"""

    def test_add_score_not_in_high_score(self, dummy_storage):
        high_score = HighScore(dummy_storage)
        inserted_index = high_score.check_and_insert_score("Kiril", 50)
        assert inserted_index == -1
        assert high_score.get_top_scores() == [
            ("Chris", 1000),
            ("Albert", 900),
            ("Bob", 850),
            ("Dylan", 700),
            ("Edward", 400),
            ("Fred", 400),
            ("Greg", 300),
            ("Hilary", 250),
            ("Ilya", 210),
            ("Jack", 100),
        ]

    @pytest.mark.parametrize(
        "name,new_score,expected_index,expected_high_scores",
        [
            (
                "Luke",
                1100,
                0,
                [
                    ("Luke", 1100),
                    ("Chris", 1000),
                    ("Albert", 900),
                    ("Bob", 850),
                    ("Dylan", 700),
                    ("Edward", 400),
                    ("Fred", 400),
                    ("Greg", 300),
                    ("Hilary", 250),
                    ("Ilya", 210),
                ],
            ),
            (
                "Luke",
                500,
                4,
                [
                    ("Chris", 1000),
                    ("Albert", 900),
                    ("Bob", 850),
                    ("Dylan", 700),
                    ("Luke", 500),
                    ("Edward", 400),
                    ("Fred", 400),
                    ("Greg", 300),
                    ("Hilary", 250),
                    ("Ilya", 210),
                ],
            ),
            (  # If there's a tie then the high score should favour the first people to have attained that score
                "Luke",
                400,
                6,
                [
                    ("Chris", 1000),
                    ("Albert", 900),
                    ("Bob", 850),
                    ("Dylan", 700),
                    ("Edward", 400),
                    ("Fred", 400),
                    ("Luke", 400),
                    ("Greg", 300),
                    ("Hilary", 250),
                    ("Ilya", 210),
                ],
            ),
        ],
    )
    # pylint: disable-next=too-many-arguments,too-many-positional-arguments   # this is necessary
    def test_add_score_new_high_score(
        self, dummy_storage, name, new_score, expected_index, expected_high_scores
    ):
        high_score = HighScore(dummy_storage)
        inserted_index = high_score.check_and_insert_score(name, new_score)
        assert inserted_index == expected_index
        assert high_score.get_top_scores() == expected_high_scores

    def test_new_high_score_list(self):
        high_score = HighScore(InMemoryStorage())
        high_score.check_and_insert_score("Chris", 1000)
        high_score.check_and_insert_score("Bob", 900)
        high_score.check_and_insert_score("Albert", 1100)
        assert high_score.get_top_scores() == [
            ("Albert", 1100),
            ("Chris", 1000),
            ("Bob", 900),
        ]
