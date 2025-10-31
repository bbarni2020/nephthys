from nephthys.actions.resolve import resolve
from nephthys.macros.types import Macro
from nephthys.utils.env import env
from nephthys.utils.ticket_methods import reply_to_ticket


class Fraud(Macro):
    name = "fraud"

    async def run(self, ticket, helper, **kwargs):
        """
        A simple macro telling people to use Fraudpheus
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
            text=f"Oi {name} — got a fraud issue? Send it straight to <@U091HC53CE8>. I’ll keep the theatrics, they’ll handle the rest. Keeps things confidential and on the fraud team’s radar.",
            ticket=ticket,
            client=env.slack_client,
        )
        await resolve(
            ts=ticket.msgTs,
            resolver=helper.slackId,
            client=env.slack_client,
        )
