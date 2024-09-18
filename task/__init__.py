from .common import *
from .task_AMR1 import *
from .task_AMR2 import *
from .task_Consistency import *
from .task_QMR1 import *
from .task_QMR2_Dutch import *
from .task_QMR2_German import *
from .task_QMR2_Spanish import *
from .task_QMR3 import *
from .task_QMR4 import *
from .task_Source_Answer import *

__all__ = [
    # _task_common
    "handle_question_only",
    "handle_task_except_english",
    "handle_wiki_only",
    "handle_consistency_only",
    "handle_translated_question",
    "mode_question",
    "mode_wiki",
    "mode_extra",
    "mode_full",

    # task_Source_Answer
    "Source_Answer",
    "Source_Answer_step_1",

    # task_QMR1
    "QMR1",
    "QMR1_step_1",

    # task_QMR2_Spanish
    "QMR2_Spanish",
    "QMR2_Spanish_step_1",
    # task_QMR2_German
    "QMR2_German",
    "QMR2_German_step_1",
    # task_QMR2_Dutch
    "QMR2_Dutch",
    "QMR2_Dutch_step_1",

    # task_QMR3
    "QMR3",
    "QMR3_step_1",
    "QMR3_step_2",

    # task_QMR4
    "QMR4",
    "QMR4_step_1",

    # task_AMR1
    "AMR1",
    "AMR1_step_1",

    # task_AMR2
    "AMR2",
    "AMR2_step_1",
    "AMR2_step_2",
    "AMR2_step_3",

    # task_Consistency
    "Consistency",
    "Consistency_step_1",
]
