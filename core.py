import re
from engines.reference_engine import resolve_reference
from engines.conversation_memory import add_message
from engines.pipeline import PIPELINE
from engines.activity_engine import log as activity_log
from engines.self_correction_engine import record as correction_record
from engines.knowledge_engine import begin_learning
from engines.personality_style_engine import transform as apply_personality
from engines.router import route
from engines.context_engine import set_topic
from pathlib import Path
import json

def _save_agent_trace(trace):
    try:
        path=Path("agent_history.json")
        history=json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        history.append(trace)
        path.write_text(json.dumps(history[-20:], indent=2), encoding="utf-8")
    except Exception as exc:
        print("Agent history error:", exc)


def respond(message, allow_planning=True):

    print("Message:", message)
    activity_log("request", message)

    message = message.strip()
    normalized_message = message.lower()

    # NLU
    data = route(normalized_message)

    from engines.nlu_context import set_analysis
    set_analysis(data)

    # Keep the exact normalized message available to every engine.
    data["message"] = normalized_message

    # Reference resolution
    reference = resolve_reference(normalized_message)

    if reference:

        print("Reference detected:", reference)

        message = re.sub(
            r"\b(it|that|this)\b",
            reference,
            message,
            flags=re.IGNORECASE
        )
        data["message"] = message.lower()

        print("Rewritten message:", message)

    # Save user's message
    add_message("user", message)

    # Run engines
    for engine in PIPELINE:

        # Nested task steps should use the normal pipeline without creating
        # another multi-step plan recursively.
        if not allow_planning and engine.__name__ == "handle" and engine.__module__.endswith("planning_engine"):
            continue

        print("Running:", engine.__module__)
        activity_log("engine_start", engine.__module__)

        try:
            handled, reply = engine(data)
        except Exception as exc:
            correction_record(message, engine.__module__, exc)
            activity_log("engine_error", f"{engine.__module__}: {exc}")
            continue

        print("handled =", handled)
        print("reply =", reply)

        if handled:

            if data.get("topic"):
                set_topic(data["topic"])

            reply = apply_personality(reply)
            add_message("assistant", reply)
            activity_log("response", engine.__module__)

            return reply

    reply = begin_learning(message)

    reply = apply_personality(reply)
    add_message("assistant", reply)

    return reply