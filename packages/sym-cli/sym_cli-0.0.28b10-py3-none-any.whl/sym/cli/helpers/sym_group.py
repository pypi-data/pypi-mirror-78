from contextlib import ExitStack
from typing import Any, Callable

from click import Command, Context, Group
from sentry_sdk.api import push_scope

from ..errors import get_active_env_vars
from ..saml_clients.chooser import choose_saml_client
from . import segment
from .tee import TeeStdErr, TeeStdOut


class AutoTagCommand(Command):
    """
    A command where each invocation sets the Sentry tag with the
    command's name automatically. Additionally, any CliErrors
    raised from the command are logged.
    """

    def invoke(self, ctx: Context) -> Any:
        segment.track(
            "Command Executed", command=ctx.info_name, options=ctx.obj.to_dict()
        )
        with ExitStack() as stack:
            scope = stack.enter_context(push_scope())
            scope.set_tag("command", ctx.info_name)
            scope.set_extra("options", ctx.obj.to_dict())

            if (log_path := ctx.parent.params.get("log_file")) :
                stack.enter_context(TeeStdOut(log_path))
                stack.enter_context(TeeStdErr(log_path))

            return super().invoke(ctx)

    def parse_args(self, ctx, args):
        if (
            self.params
            and (resource := ctx.parent.params.get("resource"))
            and self.params[0].name == "resource"
            and (
                not args
                or not choose_saml_client(
                    ctx.parent.params["saml_client_name"]
                ).validate_resource(args[0])
            )
        ):
            args = [resource] + args
        return super().parse_args(ctx, args)

    def format_epilog(self, ctx, formatter):
        if not self.epilog:
            formatter.write(get_active_env_vars())
        super().format_epilog(ctx, formatter)


class SymGroup(Group):
    """
    A group where any defined commands automatically use
    AutoTagCommand.
    """

    def __init__(self, *args: Any, **attrs: Any) -> None:
        super().__init__(*args, **attrs)

    def command(
        self, *args: Any, **kwargs: Any
    ) -> Callable[[Callable[..., Any]], AutoTagCommand]:
        return super().command(*args, **kwargs, cls=AutoTagCommand)  # type: ignore
