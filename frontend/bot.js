const botui = new BotUI('shoppy-app');

const botName = "Shoppy";
let msg, data;

const ws = new ReconnectingWebSocket("ws://127.0.0.1:5678/");

const startText = `<b>${botName}</b>: Hi available commands: add [product] (example: <code>add chips</code>), <br>
<code>items count</code>, alias total <br>
<code>groceries status</code>, alias gs <br>
<code>show list</code>, alias sl <br>
<code>remove list</code>, alias rl,`;

function userInput() {

    return botui.action.text({
        delay: 1000,
        action: {
            size: 30

        }

    });
}

function sendMsg(res) {
    msg = res.value;

    console.log('send: ' + msg);

    ws.send(msg);
    return msg;
}

function enterMessage() {

    botui.message
        .bot({
            delay: 500,
            content: 'enter command'
        })

}

function addedMsg() {
    product = msg.substring(4);
    botui.message
        .bot({
            delay: 500,
            content: `added ${product} and ${bonusProduct}`
        })
}


function receivedMsg() {
    function socketMessageListener(event) {
        botMsg = event.data;

        botui.message
            .bot({
                delay: 500,
                type: 'html',
                content: botMsg
            });

    }

    ws.addEventListener('message', socketMessageListener);

}

botui.message
    .bot({
        type: 'html',
        content: startText
    })
    .then(enterMessage)
    .then(userInput)
    .then(sendMsg)
    // optional action
    .then(() => {



        if (msg.includes("add")) {

            return botui.action.button({
                delay: 1000,
                action: [
                    {
                        text: 'Yes',
                        value: 'yes'
                    },
                    {
                        text: 'No',
                        value: 'no'
                    }
                ]
            });
        }

    })
    // optional action

    .then((res) => {
        if (msg.includes("add")) {

            if (res.value == 'yes') {
                productLastLetter = botMsg.length - 1;
                bonusProduct = botMsg.substring(24, productLastLetter);

                ws.send(`add ${bonusProduct}`);



                addedMsg();
            }
        }
    })
    .then(userInput)
    .then(receivedMsg());

