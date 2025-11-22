from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest
from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse
from starlette.responses import Response
from starlette.routing import Route
from starlette_exporter import PrometheusMiddleware

from nephthys.__main__ import main
from nephthys.api.stats import stats
from nephthys.api.user import user_stats
from nephthys.utils.env import env
from nephthys.utils.slack import app as slack_app

req_handler = AsyncSlackRequestHandler(slack_app)


async def endpoint(req: Request):
    return await req_handler.handle(req)


async def health(req: Request):
    try:
        await env.slack_client.api_test()
        slack_healthy = True
    except Exception:
        slack_healthy = False

    db_healthy = env.db.is_connected()

    return JSONResponse(
        {
            "healthy": slack_healthy,
            "slack": slack_healthy,
            "database": db_healthy,
        }
    )


async def metrics(req: Request):
    """Prometheus metrics endpoint"""
    main_metrics: bytes = generate_latest()
    prisma_metrics = await env.db.get_metrics(format="prometheus")
    all_metrics = main_metrics + prisma_metrics.encode("utf-8")
    return Response(all_metrics, media_type=CONTENT_TYPE_LATEST)


async def project(req: Request):
    auth = req.query_params.get("authorization")
    if auth != env.auth_key:
        return JSONResponse({"error": "invalid authorization"}, status_code=401)
    slack_id = req.query_params.get("slack-id")
    project_url = req.query_params.get("project-url")
    if not slack_id or not project_url:
        return JSONResponse({"error": "slack-id and project-url required"}, status_code=400)
    try:
        user_info = await env.slack_client.users_info(user=slack_id)
        user_name = user_info["user"].get("real_name") or user_info["user"]["name"]
    except:
        user_name = "there"
    message = f"Hey {user_name}! Your project has been shipped on Construct! Check it out: {project_url} Yepee! 🎉"
    try:
        await env.slack_client.chat_postMessage(channel=slack_id, text=message)
    except Exception as e:
        return JSONResponse({"error": f"Failed to send DM: {str(e)}"}, status_code=500)
    return JSONResponse({"message": "Project endpoint", "slack-id": slack_id, "project-url": project_url})


async def shop(req: Request):
    auth = req.query_params.get("authorization")
    if auth != env.auth_key:
        return JSONResponse({"error": "invalid authorization"}, status_code=401)
    slack_id = req.query_params.get("slack-id")
    approved = req.query_params.get("approved")
    item = req.query_params.get("item")
    if not slack_id or approved is None or not item:
        return JSONResponse({"error": "slack-id, approved, and item required"}, status_code=400)
    try:
        user_info = await env.slack_client.users_info(user=slack_id)
        user_name = user_info["user"].get("real_name") or user_info["user"]["name"]
    except:
        user_name = "there"
    if approved.lower() == "true":
        message = f"Congrats {user_name}! Your {item} has been approved on Construct! 🎉"
    else:
        message = f"Sorry {user_name}, your {item} request was not approved this time."
    try:
        await env.slack_client.chat_postMessage(channel=slack_id, text=message)
    except Exception as e:
        return JSONResponse({"error": f"Failed to send DM: {str(e)}"}, status_code=500)
    return JSONResponse({"message": "Shop endpoint", "slack-id": slack_id, "approved": approved, "item": item})


async def review(req: Request):
    auth = req.query_params.get("authorization")
    if auth != env.auth_key:
        return JSONResponse({"error": "invalid authorization"}, status_code=401)
    slack_id = req.query_params.get("slack-id")
    project_url = req.query_params.get("project-url")
    status = req.query_params.get("status")
    reason = req.query_params.get("reason")
    if not slack_id or not project_url or not status or not reason:
        return JSONResponse({"error": "slack-id, project-url, status, and reason required"}, status_code=400)
    try:
        user_info = await env.slack_client.users_info(user=slack_id)
        user_name = user_info["user"].get("real_name") or user_info["user"]["name"]
    except:
        user_name = "there"
    status_lower = status.lower()
    if status_lower == "approved":
        message = f"Great news {user_name}! Your project review is approved on Construct! Check it out: {project_url} Reason: {reason} 🎉"
    elif status_lower == "rejected":
        message = f"Sorry {user_name}, your project review was rejected on Construct. Reason: {reason}"
    elif status_lower == "pending":
        message = f"Hey {user_name}, your project review is pending on Construct. Reason: {reason}"
    elif status_lower == "hour_deduction":
        message = f"Hey {user_name}, your hours have been deducted on Construct. Reason: {reason}"
    else:
        message = f"Hey {user_name}, your project review status: {status}. Reason: {reason}"
    try:
        await env.slack_client.chat_postMessage(channel=slack_id, text=message)
    except Exception as e:
        return JSONResponse({"error": f"Failed to send DM: {str(e)}"}, status_code=500)
    return JSONResponse({"message": "Review endpoint", "slack-id": slack_id, "project-url": project_url, "status": status, "reason": reason})


async def root(req: Request):
    return RedirectResponse(url="https://construct.hackclub.com")


app = Starlette(
    debug=True if env.environment != "production" else False,
    routes=[
        Route(path="/", endpoint=root, methods=["GET"]),
        Route(path="/slack/events", endpoint=endpoint, methods=["POST"]),
        Route(path="/api/stats", endpoint=stats, methods=["GET"]),
        Route(path="/api/user", endpoint=user_stats, methods=["GET"]),
        Route(path="/health", endpoint=health, methods=["GET"]),
        Route(path="/metrics", endpoint=metrics, methods=["GET"]),
        Route(path="/project", endpoint=project, methods=["GET"]),
        Route(path="/shop", endpoint=shop, methods=["GET"]),
        Route(path="/review", endpoint=review, methods=["GET"]),
    ],
    lifespan=main,
)

app.add_middleware(
    PrometheusMiddleware,
    app_name="nephthys",
    buckets=[
        0.001,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        1.5,
        2.5,
    ],
)
