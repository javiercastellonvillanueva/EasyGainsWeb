document.getElementById('upload-button').addEventListener('click', function() {
    var fileInput = document.getElementById('image-upload');
    var file = fileInput.files[0];

    if (!file) {
        alert('Please select an image file first!');
        return;
    }

    // Convert the image file to Base64 since OpenAI API expects Base64-encoded images
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        var base64ImageContent = reader.result.replace(/^data:image\/(png|jpeg|jpg);base64,/, '');
        sendImageToOpenAI(base64ImageContent);
    };
    reader.onerror = function (error) {
        console.log('Error converting image to Base64:', error);
    };
});

function sendImageToOpenAI(imageContentBase64) {
    const data = {
        model: "gpt-4-vision-preview",
        prompt: {
            // Provide the appropriate prompt for OpenAI's model to analyze the image
            "image": imageContentBase64,
            // Example prompt, adjust based on OpenAI's documentation and your needs
            "task": "Describe the image and provide nutrition facts."
        },
        temperature: 0.5,
        max_tokens: 100,
        top_p: 1.0,
        frequency_penalty: 0.0,
        presence_penalty: 0.0,
    };

    fetch('https://api.openai.com/v1/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer'
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle the API response here. Display the nutrition facts or handle errors.
        // This could involve parsing the response and updating the DOM to show the results.
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
