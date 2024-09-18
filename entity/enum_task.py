import enum

from entity import BaseTask


class EnumTask(enum.Enum):
    Source_Answer: BaseTask = BaseTask(task_name="Source_Answer",
                                       function_name="Source_Answer",
                                       chat_round_number=1,
                                       opinion_field="Consistency_Source_Answer")
    QMR1: BaseTask = BaseTask(task_name="QMR1",
                              function_name="QMR1",
                              chat_round_number=1,
                              opinion_field="Consistency_QMR1")
    QMR2_Spanish: BaseTask = BaseTask(task_name="QMR2_Spanish",
                                      function_name="QMR2_Spanish",
                                      chat_round_number=1,
                                      opinion_field="Consistency_QMR2")
    QMR2_German: BaseTask = BaseTask(task_name="QMR2_German",
                                     function_name="QMR2_German",
                                     chat_round_number=1,
                                     opinion_field="Consistency_QMR2")
    QMR2_Dutch: BaseTask = BaseTask(task_name="QMR2_Dutch",
                                    function_name="QMR2_Dutch",
                                    chat_round_number=1,
                                    opinion_field="Consistency_QMR2")
    QMR3: BaseTask = BaseTask(task_name="QMR3",
                              function_name="QMR3",
                              chat_round_number=2,
                              additional_fields=["polished_question"],
                              opinion_field="Consistency_QMR3")
    QMR4: BaseTask = BaseTask(task_name="QMR4",
                              function_name="QMR4",
                              chat_round_number=1,
                              opinion_field="Consistency_QMR4")
    AMR1: BaseTask = BaseTask(task_name="AMR1",
                              function_name="AMR1",
                              chat_round_number=1,
                              opinion_field="Consistency_AMR1")
    AMR2: BaseTask = BaseTask(task_name="AMR2",
                              function_name="AMR2",
                              chat_round_number=3,
                              additional_fields=["english_phrase", "similar_phrases"],
                              opinion_field="Consistency_AMR2")
