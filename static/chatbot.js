
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const API_KEY = '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' ; // Paste your API key here
const inputInitHeight = chatInput.scrollHeight;


let pdfUP = false;
let pdfText = "";

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}

function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("pdfFile", file);
    document.querySelector("#r").style.background = "white";
    document.querySelector("#g").style.background = "white";
    document.querySelector("#y").style.background = "rgb(247, 247, 68)";
    
    
    
    fetch("/upload_pdf", {
      method: "POST",
      body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        chatbox.appendChild(createChatLi("PDF uploaded successfully", "incoming"));
        setTimeout(() => {
            
            document.querySelector("#r").style.background = "white";
            document.querySelector("#g").style.background = "rgb(84, 255, 84)";
            document.querySelector("#y").style.background = "white";
            chatbox.appendChild(createChatLi("You can now ask any questions regarding the PDF.", "incoming"));


        }, 1000);
        pdfUP = true;
        pdfText = data["data"];
        console.log(data);
    })
    .catch((error) => {
        
        pdfUP = false;
        pdfText = "";
        console.error("Error:", error);
        document.querySelector("#r").style.background = "rgb(247, 53, 53)";
            document.querySelector("#g").style.background = "white";
            document.querySelector("#y").style.background = "white";
      });
  }

const createChatLiWithInput = (className) => {
    // Create a chat <li> element with an input for uploading PDF and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").innerHTML = `
    <input type="file" id="pdfFile" accept=".pdf" required />
    <button onclick="uploadPDF()">Upload PDF</button>
    `;
    return chatLi; // return chat <li> element// return chat <li> element
}


function scanPDF(){
chatInput.value = "";
document.querySelector(".cmdContainer").innerHTML = "";

chatbox.appendChild(createChatLi("/scanPDF", "outgoing"));
setTimeout(() => {
    chatbox.appendChild(createChatLiWithInput("incoming"));
}, 1200);

}
function Locate(){

}
function createDoc(){

}
function About(){

}
function showHelp() {
    alert("help");
    chatInput.value = "";
    document.querySelector(".cmdContainer").innerHTML = "";
    chatbox.appendChild(createChatLi("/Help", "outgoing"));
    chatbox.appendChild(createChatLi(
      "Hello! I am an AI bot trained to handle data regarding legal documents and law. ",
      "incoming"
    ));
    const summary =`
    The features of this website are: \n
1. Create Business Contracts: Generate tailored contracts by selecting document types like Contracts & Agreements, Real Estate Plannings, Regulatory Compliance, Intellectual Properties, and Formation & Governance.\n

2. Legal AI Chatbot - Dexter: Get answers to legal questions and assistance with business-related legal documents through Dexter, our knowledgeable AI chatbot.
3. Find Certified Lawyers Nearby: Explore a database to locate certified lawyers in your vicinity, ensuring access to specialized legal expertise for your business needs. \n
4. Consultation with Lawyers: Schedule direct consultations with certified lawyers for personalized legal support, clarifying doubts, seeking advice, or addressing complex legal matters.\n
5. Chatbot Commands Simplification: Press "/" to access a menu of commands, streamlining interactions and providing quick navigation for creating contracts, consulting lawyers, and accessing essential features. \n

`;
setTimeout(() => {
    chatbox.appendChild(createChatLi(summary,"incoming"));
}, 1200);


  }
function checkCMD() {
    const cmd = document.querySelector(".cmdContainer");

    if (chatInput.value == '/') {
        // Creating buttons
        const helpButton = document.createElement("button");
        helpButton.textContent = "/Help";
        helpButton.addEventListener("click", showHelp);

        const scanPDFButton = document.createElement("button");
        scanPDFButton.textContent = "/ScanPDF";
        scanPDFButton.addEventListener("click", scanPDF);

        const locateButton = document.createElement("button");
        locateButton.textContent = "/Locate";
        locateButton.addEventListener("click", Locate);

        const createDocButton = document.createElement("button");
        createDocButton.textContent = "/Create";
        createDocButton.addEventListener("click", createDoc);

        const aboutButton = document.createElement("button");
        aboutButton.textContent = "/About";
        aboutButton.addEventListener("click", About);

        // Appending buttons to cmd container
        cmd.innerHTML = ''; // Clear existing content
        cmd.appendChild(helpButton);
        cmd.appendChild(scanPDFButton);
        cmd.appendChild(locateButton);
        cmd.appendChild(createDocButton);
        cmd.appendChild(aboutButton);

        cmd.style.opacity = 1;
    } else {
        cmd.style.opacity = 0;
        cmd.innerHTML = '';
    }
}



const generateResponse= (chatElement) => {
    const API_URL = "https://api.openai.com/v1/chat/completions";
    const messageElement = chatElement.querySelector("p");

    // Define the properties and message for the API request

    if(pdfUP === true)

        userMessage = `You are a Legal Ai Assistant and will only answer questions regarding, legal documents.\n The PDF is: { ${pdfText} }. \n User's Question: `+userMessage;    
    
    else
    userMessage = "You are a Legal Ai Assistant and will only answer questions related to legal documents and law. If the user asks you to provide a summary of pdf, ask them to upload the pdf file first using '/scanPDF' command. \n User: "+userMessage;
    
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${API_KEY}`
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{role: "user", content: userMessage}],
        })
    }

    // Send POST request to API, get response and set the reponse as paragraph text
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        messageElement.textContent = data.choices[0].message.content.trim();
    }).catch(() => {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    document.querySelector("#r").style.background = "white";
    document.querySelector("#g").style.background = "white";
    document.querySelector("#y").style.background = "rgb(247, 247, 68)";
    
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
         generateResponse(incomingChatLi);

         
         
         if(pdfUP === true)
         {
             
             document.querySelector("#g").style.background = "rgb(84, 255, 84)";
             document.querySelector("#y").style.background = "white";
            }
            else if(pdfUP === false){
                document.querySelector("#r").style.background = "rgb(247, 53, 53)";
                document.querySelector("#y").style.background = "white";
            }
        }, 600);
        }

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));