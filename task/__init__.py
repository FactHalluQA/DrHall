from .common import *
from .task_answer_in_dutch import *
from .task_answer_in_english import *
from .task_answer_in_german import *
from .task_answer_in_spanish import *
from .task_fact import *
from .task_reconstruction import *
from .task_repeat import *
from .task_step_by_step import *
from .task_wiki import *

__all__ = [
    # _task_common
    "handle_question_only",
    "handle_task_except_english",
    "handle_wiki_only",
    "handle_translated_question",
    "mode_question",
    "mode_wiki",
    "mode_extra",
    "mode_full",

    # task_answer_in_dutch
    "answer_in_dutch",
    "answer_in_dutch_step_1",

    # task_answer_in_english
    "answer_in_english",
    "answer_in_english_step_1",

    # task_answer_in_german
    "answer_in_german",
    "answer_in_german_step_1",

    # task_answer_in_spanish
    "answer_in_spanish",
    "answer_in_spanish_step_1",

    # task_fact
    "fact",
    "fact_step_1",

    # task_reconstruction
    "reconstruction",
    "reconstruction_step_1",
    "reconstruction_step_2",
    "reconstruction_step_3",

    # task_repeat
    "repeat",
    "repeat_step_1",

    # task_step_by_step
    "step_by_step",
    "step_by_step_step_1",

    # task_wiki
    "wiki",
    "wiki_step_1",
]
