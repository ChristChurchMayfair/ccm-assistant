import intents


def on_launch():
    return intents.handle_welcome()


def on_intent(intent_request, session, context):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    # Dispatch to intent handlers
    irrelevant_audio_intents = ["AMAZON.LoopOffIntent", "AMAZON.LoopOnIntent",
                                "AMAZON.RepeatIntent", "AMAZON.ShuffleOffIntent",
                                "AMAZON.ShuffleOnIntent", "AMAZON.StartOverIntent",
                                "AMAZON.PreviousIntent", "AMAZON.NextIntent"]
    if intent_name == "GetSermonPassage":
        return intents.handle_get_passage(intent)
    elif intent_name == "PlaySermon":
        return intents.handle_play_sermon(intent)
    elif intent_name == "GetNextEvent":
        return intents.handle_get_next_event()
    elif intent_name == "AMAZON.HelpIntent":
        return intents.handle_welcome()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return intents.handle_session_end_request()
    # Audio player intents
    elif intent_name in irrelevant_audio_intents:
        return intents.handle_irrelevant_audio_intent()
    elif intent_name == "AMAZON.PauseIntent":
        return intents.handle_pause()
    elif intent_name == "AMAZON.ResumeIntent":
        return intents.handle_resume(context)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    pass
