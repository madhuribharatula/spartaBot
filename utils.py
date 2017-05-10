from wit import Wit

access_token = "OYYCZ6TTHWRUDFBAF7CJMY6KAJRLNPUO"

client = Wit(access_token = access_token)


def wit_response(message_text):
    resp = client.message(message_text)
    #print resp
    try:
        categories = {}
        entities = list(resp['entities'])
        for entity in entities:
         categories[entity] = resp['entities'][entity][0]['value']
    except:
        pass
    return categories


