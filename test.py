import requests
import json
import os


FIM_PREFIX = "<PRE> "
FIM_MIDDLE = " <MID>"
FIM_SUFFIX = " <SUF>"

FIM_INDICATOR = "<FILL_ME>"

EOS_STRING = "</s>"
EOT_STRING = "<EOT>"

def testCurl(url, prompt, config):
    curl_data = f'"prompt":"{prompt}", "c":{config["context"]}, "temperature":{config["temperature"]} , "repeat_penalty":{config["repeat_penalty"]}, "top_p":{config["top_p"]}, "n_predict": {config["n_predict"]}'
    llama_curl = f'''
    curl --request POST \
        --url {url} \
        --header "Content-Type: application/json" \
        --data \'{{{curl_data}}}\'
        '''
    # print(llama_curl)
    os.system(llama_curl)


def testPyRequest(prompt, config, url="http://100.71.162.51:9090/completion"):
    def fetch_data(url, prompt, config):
        headers = {
            'Content-Type': 'application/json',
        }
        fim_mode = False
        if FIM_INDICATOR in prompt:
            fim_mode = True
            try:
                prefix, suffix = prompt.split(FIM_INDICATOR)
            except:
                raise ValueError(f"Only one {FIM_INDICATOR} allowed in prompt!")
            prompt = f"{FIM_PREFIX}{prefix}{FIM_SUFFIX}{suffix}{FIM_MIDDLE}"
        data = {
            'prompt': prompt,
            'temperature': config["temperature"],
            'top_k': config["top_k"],
            'top_p': config["top_p"],
            'repeat_penalty': config["repeat_penalty"],
            'n_predict': config["n_predict"],
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        res = response.status_code

        if response.status_code == 200:
            # content = response.json()['content']
            # print(content)
            res = json.loads(response.text)['content']
            #print(res)
            if fim_mode:
                output = prefix
                fill_me = res.split(EOT_STRING)[0]
                if(fill_me):
                    output += fill_me
                output += suffix
            else:
                output = prompt
                output += res
            print(output)
            return output
            
        else:
            print("Error:", response.status_code)

        return -1

    res = fetch_data(url, prompt, config)


def testHFModels(prompt, config):
    API_TOKEN = "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"
    API_URL = "https://api-inference.huggingface.co/models/codellama/CodeLlama-13b-hf"

    headers = {"Authorization": f"Bearer {API_TOKEN}",
               'Content-Type': 'application/json'}
    
    fim_mode = False
    if FIM_INDICATOR in prompt:
        fim_mode = True
        try:
            prefix, suffix = prompt.split(FIM_INDICATOR)
        except:
            raise ValueError(f"Only one {FIM_INDICATOR} allowed in prompt!")
        prompt = f"{FIM_PREFIX}{prefix}{FIM_SUFFIX}{suffix}{FIM_MIDDLE}"

    payload = {
        'inputs': prompt,
        "parameters": {
            'temperature': config["temperature"],
            'top_k': config["top_k"],
            'top_p': config["top_p"],
            'repetition_penalty': config["repeat_penalty"],
            'max_new_tokens': config["n_predict"],
        }
    }
    response = requests.post(API_URL, headers=headers,
                             data=json.dumps(payload))
    res = response.status_code

    if response.status_code == 200:
        #content = response.json()[0]['generated_text']
        #print(content.split(FIM_MIDDLE))
        #print(response)
        #res = json.loads(response.text)['content']
        #print(res)
        if fim_mode:
            output = prefix
        else:
            output = prompt

        previous_token = ""
        for r in response.json():
            content = r['generated_text']
            if any([end_token in content for end_token in [EOS_STRING, EOT_STRING]]):
                if fim_mode:
                    fill_me = content.split(FIM_MIDDLE)[1]
                    if fill_me:
                        output += fill_me.split(EOT_STRING)[0]
                    output += suffix
                    yield output
                    print("output:\n", output)
                    return output
                else:
                    return output
            else:
                output += content
            previous_token = r['generated_text']
            yield output
    else:
        print("Error:", response.status_code)


if __name__ == "__main__":
    url = "http://100.71.162.51:9090/completion"
    config = {
        "temperature": 0.1,
        "top_k": 40,
        "top_p": 0.9,
        "repeat_penalty": 1.05,
        "n_predict": 256,
        "context": 2048,
    }
    prompts = ["Tell me a joke", "Compute the sqrt of 1+8", "Write a DFS function in Python",
               "Write a fibonacci sequence algorithm", "Write a binary search in Python"]
    autoCompletes = ["def dfs(\n <FILL_ME> \n return", "def bfs(\n <FILL_ME> \n return", "def findDuplicate(\n <FILL_ME> \n return","def dedup(\n <FILL_ME> \n return",]
    
    test = autoCompletes

    for p in test:
        if FIM_INDICATOR not in p:
            print(f"==================== {p} =========================")
        else:
            print("====================")
            print(p)
            print("====================")
        testPyRequest(p, config, url)
        # testCurl(url, p, config)
        #testHFModels(p, config)
        # for result in testHFModels(p, config):
        #     print(result)  
        #break