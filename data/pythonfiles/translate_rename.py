import os, requests, uuid, json

#if 'e6821924ed6e4a1d9faea4a0d355d0a0' in os.environ:
#    subscriptionKey = os.environ['e6821924ed6e4a1d9faea4a0d355d0a0']
#else:
#    print('Environment variable for TRANSLATOR_TEXT_KEY is not set.')
#    exit()
# If you want to set your subscription key as a string, uncomment the next line.
subscriptionKey = 'a7eaeca7c32f43018a851e29639cb09e'

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/translate?api-version=3.0'
params = '&to=en'
constructed_url = base_url + path + params
headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# You can pass more than one object in body.


def traducir(texto):
    body = [{    'text' : texto }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    jsonresult = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
    print jsonresult
    return response[0]['translations'][0]['text']



print (traducir("hola , buen dia"))
