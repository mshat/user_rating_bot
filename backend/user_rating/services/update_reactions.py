from .tg_client.client import MyClient, Message


def update_reactions():
    print('update_reactions - START')
    client = MyClient()
    messages_with_reactions = client.get_messages_with_reactions()
    # for msg in messages_with_reactions:
    #     update_message(msg.id_, msg.text, msg.reactions)
    return messages_with_reactions
