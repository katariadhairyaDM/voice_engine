let bool = true;
let final_transcript = "";

if ("webkitSpeechRecognition" in window) {
    let speechRecognition = new webkitSpeechRecognition();
    

    speechRecognition.continuous = false;

    speechRecognition.onstart = () => {
        final_transcript = '';
        document.getElementById("start").style.color = 'red';
        bool = false;
        // document.getElementsByClassName("material-icons").style.color = 'red';
        // document.getElementsByClassName("material-icons").style.background = 'red';
        // document.querySelector("#status").style.display = "block";
    };
    speechRecognition.onerror = () => {
        // document.querySelector("#status").style.display = "none";
        console.log("Speech Recognition Error");
    };
    speechRecognition.onend = () => {
        // document.getElementById("start").style.background = '#07b825';
        document.getElementById("start").style.color = 'rgb(24 179 186 / 92%)';
        // document.querySelector("#status").style.display = "none";
        let value1 = document.getElementById("dropdown1");
        let gettext1 = value1.options[value1.selectedIndex].text;
        let value2 = document.getElementById("dropdown2");
        let gettext2 = value2.options[value2.selectedIndex].text;
        let value3 = document.getElementById("dropdown3");
        let gettext3 = value3.options[value3.selectedIndex].text;
        // let value4 = document.getElementById("dropdown4");
        // let gettext4 = value4.options[value4.selectedIndex].text;
        let accountID = 300301992;
        bool = true;
        ////////////////////////////////////////////
        // On right
        const newDivChatR = document.createElement("div");
        newDivChatR.classList.add('chat-r');
        const newDivSp = document.createElement("div");
        newDivSp.classList.add('sp');
        const newDivMess = document.createElement("div");
        newDivMess.classList.add('mess');
        newDivMess.classList.add('mess-r');
        newDivMess.classList.add('span-on-right');
        const newSpan = document.createElement("span");
        newSpan.innerHTML = final_transcript;
        newSpan.classList.add('div-shadow-right');
        
        newDivChatR.appendChild(newDivSp);
        newDivChatR.appendChild(newDivMess);
        newDivMess.appendChild(newSpan);
        newSpan.scrollIntoView();
        
        const newDivChatRAdd = document.querySelector(".chat-box");
        newDivChatRAdd.appendChild(newDivChatR);
        fetch('', {
            method: "POST",
            credentials: "same-origin",
            headers: {
              "X-Requested-With": "XMLHttpRequest",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            // body: JSON.stringify({payload: final_transcript, accName : gettext1, resultMetric : gettext2, CPR : gettext3})
            body: JSON.stringify({payload: "Get platform breakdown data", accName : gettext1, resultMetric : gettext2, CPR : gettext3})
            })
            .then(response => response.json())
            .then(data => {
                data = JSON.parse(data);
                console.log(data);
                ////////////////////////////////
                // On left

                drawChart(data);

            });
        

        console.log("Speech Recognition Ended");
    };

    speechRecognition.onresult = (event) => {
        let interim_transcript = "";

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            } else {
                interim_transcript += event.results[i][0].transcript;
            }
        }
        // document.querySelector("#final").innerHTML = final_transcript;

    };
    document.querySelector("#start").onclick = () => {

        if (bool){
            bool = false;
            final_transcript = '';
            // document.querySelector("#final").innerHTML = final_transcript;
            speechRecognition.start();
        }
        else{
            
            bool = true;
            speechRecognition.stop();
        }
    };
}

else {
    console.log("Speech Recognition Not Available");
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
