function submitForm(id) {
    // Get the form element by ID
    // var form = document.getElementsByClassName("form active");
    var form = id.parentNode;

    // Create an empty string to store form data
    var formDataString = "";

    // Loop through each form element
    for (var i = 0; i < form.elements.length; i++) {
        var element = form.elements[i];

        // Check if the element is an input, textarea, or select
        if (element.tagName === "INPUT" || element.tagName === "TEXTAREA" || element.tagName === "SELECT") {
            // Append the element's name and value to the formDataString
            formDataString += element.name + ": " + element.value + "\n";
        }
    }

    // Display or use the formDataString as needed
    console.log(formDataString);
}
