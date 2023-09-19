const prompt = `Implement binary search in Python`;

async function Test() {
    let response = await fetch("http://100.71.162.51:9090/completion", {
        method: 'POST',
        body: JSON.stringify({
            prompt,
            temperature: 0.1,
            top_k: 40,
            top_p: 0.9,
            repeat_penalty: 1.05,
            // large n_predict significantly slows down the server, thus use a small value for testing purposes
            n_predict: 32,
            stream: false,
        }),
        headers: {
            'Content-Type': 'application/json'
          }
    })
    resJSON = JSON.parse((await response.text()));
    console.log(resJSON);
    return resJSON['content'];
}

Test()