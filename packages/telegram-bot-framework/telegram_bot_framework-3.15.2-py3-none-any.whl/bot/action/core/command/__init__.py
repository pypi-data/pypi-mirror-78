import time

from bot.action.core.action import IntermediateAction
from bot.action.core.command.parser import UnderscoredCommandParser, CommandParser
from bot.action.core.command.throttler import NoThrottler
from bot.action.core.command.throttler.shortlyrepeatedcommand.throttler import ShortlyRepeatedCommandThrottler
from bot.action.util.format import UserFormatter, ChatFormatter, TimeFormatter
from bot.action.util.textformat import FormattedText
from bot.api.domain import MessageEntityParser


COMMAND_LOG_TAG = FormattedText().normal("COMMAND")


class CommandAction(IntermediateAction):
    def __init__(self, command, underscores_as_spaces=True, is_personal=False):
        """
        :param is_personal: If True, results are different depending on the user executing it.
            If False, different users executing it on the same chat will return the same result.
        """
        super().__init__()
        self.command = command
        self.parser = (UnderscoredCommandParser if underscores_as_spaces else CommandParser)(command)
        self.throttler = NoThrottler()  # overridden on post_setup where we have access to api
        self.is_personal = is_personal

    def post_setup(self):
        self.parser.build_command_matcher(self.cache.bot_info.username)
        self.throttler = self._get_throttler()
        if self.is_personal:
            self.throttler.add_personal_command(self.command)

    def _get_throttler(self):
        shared_throttler = self.cache.command_throttler
        if shared_throttler is None:
            shared_throttler = self.cache.command_throttler = ShortlyRepeatedCommandThrottler(self.api)
        return shared_throttler

    def process(self, event):
        for entity in self.get_entities(event):
            if self.is_valid_command(entity):
                parser = MessageEntityParser(event.message)
                command_text = parser.get_entity_text(entity)
                if self.parser.matches_command(command_text):
                    event.command = self.parser.get_command_name(command_text)
                    additional_text = parser.get_text_after_entity(entity)
                    event.command_args = self.parser.get_command_args(command_text, additional_text).lstrip(" ")
                    if self.throttler.should_execute(event):
                        start_time = time.time()
                        try:
                            self._continue(event)
                        finally:
                            self.__log_command_execution(event, time.time() - start_time)

    @staticmethod
    def get_entities(event):
        entities = event.message.entities
        return entities if entities is not None else []

    @staticmethod
    def is_valid_command(entity):
        return entity.type == "bot_command" and entity.offset == 0

    @staticmethod
    def __log_command_execution(event, elapsed_seconds: float):
        event.logger.log(
            COMMAND_LOG_TAG,
            FormattedText().normal("{command} {args}").start_format()
                .bold(command=event.command, args=event.command_args).end_format(),
            FormattedText().normal("User: {user}").start_format()
                .bold(user=UserFormatter(event.message.from_).full_data).end_format(),
            FormattedText().normal("Chat: {chat}").start_format()
                .bold(chat=ChatFormatter(event.chat).full_data).end_format(),
            FormattedText().normal("Execution time: {time}").start_format()
                .bold(time=TimeFormatter.format(elapsed_seconds)).end_format()
        )


class UnderscoredCommandBuilder:
    @staticmethod
    def build_command(command, *args):
        underscored_args = "_" + "_".join(args)
        at_start = command.find("@")
        if at_start != -1:
            return command[:at_start] + underscored_args + command[at_start:]
        else:
            return command + underscored_args
