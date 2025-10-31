from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class Transcript(BaseModel):
    """Class to hold all the transcript messages and links used in the bot."""

    class Config:
        """Configuration for the Pydantic model."""

        extra = "forbid"

    program_name: str = Field(
        default="Construct", description="Name of the program"
    )
    program_owner: str = Field(
        default="U054VC2KM9P",
        description="Slack ID of the support manager",
    )
    help_channel: str = Field(
        default="",
        description="Slack channel ID for help requests",
    )
    ticket_channel: str = Field(
        default="",
        description="Slack channel ID for ticket creation",
    )
    team_channel: str = Field(
        default="",
        description="Slack channel ID for team discussions and stats",
    )
    ticket_reopen: str = Field(
        default="",
        description="Message when ticket is reopened",
    )

    @property
    def program_snake_case(self) -> str:
        """Snake case version of the program name."""
        return self.program_name.lower().replace(" ", "_")

    faq_link: str = Field(
        default="https://hackclub.slack.com/docs/T0266FRGM/F09Q2DS061J",
        description="FAQ link URL",
    )

    summer_help_channel: str = Field(
        default="C091D312J85", description="Summer help channel ID"
    )

    identity_help_channel: str = Field(
        default="C092833JXKK", description="Identity help channel ID"
    )

    first_ticket_create: str = Field(
        default="", description="Message for first-time ticket creators"
    )

    ticket_create: str = Field(default="", description="Message for ticket creation")

    ticket_resolve: str = Field(
        default="", description="Message when ticket is resolved"
    )

    ticket_resolve_stale: str = Field(
        default="",
        description="Message when ticket is resolved due to being stale",
    )

    thread_broadcast_delete: str = Field(
        default="heads up — please keep messages in a single thread so context stays intact. i've removed the duplicate message to keep the channel tidy.",
    )

    home_unknown_user_title: str = Field(
        default=":gear: hold up, {name} — access restricted!",
        description="Title for unknown user on home page",
    )

    home_unknown_user_text: str = Field(
        default="", description="Text for unknown user on home page"
    )

    not_allowed_channel: str = Field(
        default="", description="Message for unauthorized channel access"
    )

    # this stuff is only required for summer of making, but it's easier to keep it here :p
    dm_magic_link_no_user: str = Field(
        default="please provide the user (username or ID) you want me to DM",
        description="Message when no user provided for magic link DM",
    )

    dm_magic_link_error: str = Field(
        default="", description="Error message for magic link generation"
    )

    dm_magic_link_success: str = Field(
        default="magic link sent — tell them to check their DMs.",
        description="Success message for magic link DM",
    )

    dm_magic_link_message: str = Field(
        default="got stuck? here’s a quick link to get you back on track:\n{magic_link}",
        description="Magic link DM message",
    )

    dm_magic_link_no_permission: str = Field(
        default="", description="No permission message for magic link command"
    )

    @model_validator(mode="after")
    def set_default_messages(self):
        """Set default values for messages that reference other fields"""
        if not self.first_ticket_create:
            self.first_ticket_create = f"""hey — looks like this is your first post. welcome! someone will be by soon. meantime, check the FAQ <{self.faq_link}|here> to see if your question's already answered.
if your issue is resolved, please tap the button below to mark it resolved.
    """

        if not self.ticket_create:
            self.ticket_create = f"""someone will be along to help soon. meanwhile, please consult the FAQ <{self.faq_link}|here> to check for an existing answer. if your question's already resolved, tap the resolve button below.
    """

        if not self.ticket_resolve:
            self.ticket_resolve = f"""this post was marked resolved by <@{{user_id}}>. if you need further help, please open a new post in <#{self.help_channel}> and the team will assist. i've taken care of the status update.
    """

        if not self.ticket_resolve_stale:
            self.ticket_resolve_stale = f"""this thread looks stale. if you still need support, please open a new post in <#{self.help_channel}> and someone will help you.
        """

        if not self.home_unknown_user_text:
            self.home_unknown_user_text = f"can't show that here — you don't have permission. if you think this is wrong, contact <@{self.program_owner}> to sort access."

        if not self.not_allowed_channel:
            self.not_allowed_channel = f"that action isn't allowed in this channel. please contact <@{self.program_owner}> if you need access."

        if not self.dm_magic_link_error:
            self.dm_magic_link_error = f"failed to generate magic link (status: {{status}}). please contact <@{self.program_owner}>."

        if not self.dm_magic_link_no_permission:
            self.dm_magic_link_no_permission = f"you don't have permission to use that command. if this seems wrong, contact <@{self.program_owner}>."

        if not self.ticket_reopen:
            self.ticket_reopen = "update: <@{helper_slack_id}> reopened this post. someone will be with you shortly."

        return self
