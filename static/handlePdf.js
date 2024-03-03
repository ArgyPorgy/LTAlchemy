function sendDataToPythonAndDownload(stringToSend) {
    fetch("/receive_data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ string: stringToSend }),
    })
      .then((response) => response.blob())
      .then((blob) => {
        // Create a blob URL for the PDF blob
        const blobUrl = URL.createObjectURL(blob);

        // Create a link element
        const link = document.createElement("a");

        // Set the link's href to the blob URL
        link.href = blobUrl;

        // Set the download attribute with the desired file name
        link.download = "Generated_Contract.pdf";

        // Append the link to the document
        document.body.appendChild(link);

        // Programmatically click the link to trigger the download
        link.click();

        // Remove the link element from the document
        document.body.removeChild(link);

        // Revoke the blob URL to free up resources
        URL.revokeObjectURL(blobUrl);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
 

  function submitForm(id) {
    // Get the form element by ID
    const form = document.getElementById(`form${id}`);

    // Check if the form is found
    if (!form) {
        console.error("Form not found with ID:", `form${id}`);
        return;
    }

    // Create an empty string to store form data
    let formDataString = "";
    formDataString += `${id}\n`;

    // Loop through each form element
    for (var i = 0; i < form.elements.length; i++) {
        var element = form.elements[i];

        // Check if the element is an input, textarea, or select
        if (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.tagName === "SELECT") {
            // Append the element's name and value to the formDataString
            formDataString += `${element.name}: ${element.value}\n`;
        }
    }

    // Display or use the formDataString as needed
    console.log("Form data:\n", formDataString);

    // Call your function to send the form data to Python or perform other actions
    sendDataToPythonAndDownload(formDataString);
}
