// Access video stream
const video = document.getElementById('video');
const statusDiv = document.getElementById('status');

// Start the video stream from the camera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    // Automatically capture the image when the video starts
    setInterval(captureImage, 3000); // Capture every 3 seconds (adjust as needed)
  })
  .catch(err => {
    console.error('Error accessing camera:', err);
    statusDiv.innerText = 'Error accessing camera.';
  });

// Function to capture an image from the video feed
function captureImage() {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  // Draw the current frame of the video on the canvas
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Convert the image to base64
  const imageData = canvas.toDataURL('image/jpeg');
  
  // Send the image to the backend API
  sendToBackend(imageData);
}

// Function to send the image to the backend API
async function sendToBackend(imageData) {
  try {
    const response = await fetch('http://localhost:8000/predict/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image: imageData }),
    });

    const result = await response.json();
    if (result.success) {
      // Process and display the result
      const prediction = result.prediction;
      statusDiv.innerText = `Prediction: ${prediction}`;
    } else {
      statusDiv.innerText = 'Error processing image.';
    }
  } catch (error) {
    console.error('Error:', error);
    statusDiv.innerText = 'Error communicating with the backend.';
  }
}