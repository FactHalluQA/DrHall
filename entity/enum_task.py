import enum

from entity import BaseTask


class EnumTask(enum.Enum):
    ANSWER_IN_ENGLISH: BaseTask = BaseTask(task_name="英语",
                                           function_name="answer_in_english",
                                           chat_round_number=1,
                                           opinion_field="success_multilanguage")
    ANSWER_IN_SPANISH: BaseTask = BaseTask(task_name="西班牙语",
                                           function_name="answer_in_spanish",
                                           chat_round_number=1,
                                           opinion_field="success_multilanguage")
    ANSWER_IN_GERMAN: BaseTask = BaseTask(task_name="德语",
                                          function_name="answer_in_german",
                                          chat_round_number=1,
                                          opinion_field="success_multilanguage")
    ANSWER_IN_DUTCH: BaseTask = BaseTask(task_name="荷兰语",
                                         function_name="answer_in_dutch",
                                         chat_round_number=1,
                                         opinion_field="success_multilanguage")
    REPEAT: BaseTask = BaseTask(task_name="重复",
                                function_name="repeat",
                                chat_round_number=2,
                                additional_fields=["polished_question"],
                                opinion_field="success_repeat")
    STEP_BY_STEP: BaseTask = BaseTask(task_name="一步步思考",
                                      function_name="step_by_step",
                                      chat_round_number=1,
                                      opinion_field="success_step_by_step")
    WIKI: BaseTask = BaseTask(task_name="wiki",
                              function_name="wiki",
                              chat_round_number=1,
                              opinion_field="success_wiki")
    FACT: BaseTask = BaseTask(task_name="这句话不符合事实吗？",
                              function_name="fact",
                              chat_round_number=1,
                              opinion_field="success_fact")
    RECONSTRUCTION: BaseTask = BaseTask(task_name="改造为选择问题",
                                        function_name="reconstruction",
                                        chat_round_number=3,
                                        additional_fields=["english_phrase", "similar_phrases"],
                                        opinion_field="success_reconstruction")
