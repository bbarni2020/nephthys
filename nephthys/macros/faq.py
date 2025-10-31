from nephthys.actions.resolve import resolve
from nephthys.macros.types import Macro
from nephthys.utils.env import env
from nephthys.utils.ticket_methods import reply_to_ticket


class FAQ(Macro):
    name = "faq"

    async def run(self, ticket, helper, **kwargs):
        """
        A simple macro reminding people to check the FAQ.
        """
        sender = await env.db.user.find_first(where={"id": ticket.openedById})
        if not sender:
            return
        user_info = await env.slack_client.users_info(user=sender.slackId)
        name = (
            user_info["user"]["profile"].get("display_name")
            or user_info["user"]["profile"].get("real_name")
            or user_info["user"]["name"]
        )
        await reply_to_ticket(
            text=f"that's in the FAQ, {name}. Read it here — <{env.transcript.faq_link}|FAQ>",
            ticket=ticket,
            client=env.slack_client,
        )
        await resolve(
            ts=ticket.msgTs,
            resolver=helper.slackId,
            client=env.slack_client,
        )
