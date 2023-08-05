from bot.action.core.command.throttler import Throttler
from bot.action.core.command.throttler.shortlyrepeatedcommand.command_key import CommandKeyFactory
from bot.action.standard import chatsettings
from bot.action.standard.chatsettings import ChatSettings
from bot.action.util.format import UserFormatter, ChatFormatter
from bot.action.util.textformat import FormattedText
from bot.api.api import Api


LOG_TAG = FormattedText().bold("THROTTLER")


class ShortlyRepeatedCommandThrottler(Throttler):
    def __init__(self, api: Api):
        self.api = api
        self.command_key_factory = CommandKeyFactory()
        self.recent_commands = {}

    def add_personal_command(self, command: str):
        self.command_key_factory.add_personal_command(command)

    def should_execute(self, event):
        current_date = event.message.date
        self.__cleanup_recent_commands(current_date)
        command_key = self.command_key_factory.get_command_key(event)
        if command_key not in self.recent_commands:
            throttling_state = CommandThrottlingState(event)
            if not throttling_state.has_expired(current_date):
                # it has not expired immediately, throttling is enabled
                self.recent_commands[command_key] = throttling_state
        else:
            throttling_state = self.recent_commands[command_key]
            throttling_state.add_invocation()
        if throttling_state.should_warn():
            self.__send_throttling_warning(event, throttling_state)
        return throttling_state.should_execute()

    def __cleanup_recent_commands(self, current_date):
        for key, state in self.recent_commands.copy().items():
            if state.has_expired(current_date):
                del self.recent_commands[key]

    def __send_throttling_warning(self, event, throttling_state):
        remaining_seconds = throttling_state.remaining_seconds(event.message.date)
        self.__log_throttling(event, remaining_seconds)
        message = FormattedText().bold("Ignoring repeated command.").normal(" Try again in ")\
            .code_inline(remaining_seconds).normal(" seconds.")\
            .build_message()
        message.to_chat_replying(event.message)
        self.api.async.send_message(message)

    @staticmethod
    def __log_throttling(event, remaining_seconds):
        event.logger.log(
            LOG_TAG,
            FormattedText().normal("{command} {args}").start_format()
                .bold(command=event.command, args=event.command_args).end_format(),
            FormattedText().normal("User: {user}").start_format()
                .bold(user=UserFormatter(event.message.from_).full_data).end_format(),
            FormattedText().normal("Chat: {chat}").start_format()
                .bold(chat=ChatFormatter(event.chat).full_data).end_format(),
            FormattedText().normal("Throttling for {seconds} seconds.").start_format()
                .bold(seconds=remaining_seconds).end_format()
        )


class CommandThrottlingState:
    def __init__(self, event):
        self.chat_settings = chatsettings.repository.get_for_event(event)
        self.first_invocation = event.message.date
        self.number_of_invocations = 1

    def add_invocation(self):
        self.number_of_invocations += 1

    def should_execute(self):
        return self.number_of_invocations <= 2

    def should_warn(self):
        return self.number_of_invocations == 3

    def has_expired(self, current_date):
        throttling_seconds = self.chat_settings.get(ChatSettings.THROTTLING_SECONDS)
        expiration_date = current_date - throttling_seconds
        return self.first_invocation <= expiration_date

    def remaining_seconds(self, current_date):
        throttling_seconds = self.chat_settings.get(ChatSettings.THROTTLING_SECONDS)
        expiration_date = current_date - throttling_seconds
        return self.first_invocation - expiration_date
