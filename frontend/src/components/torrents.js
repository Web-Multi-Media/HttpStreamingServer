import React from 'react';

function TransmissionClient() {
  // Replace "YOUR_AUTH_TOKEN" with your actual authentication token
  const authToken = "YOUR_AUTH_TOKEN";
  // Replace "http://your-transmission-web-client-url:9091/" with the actual URL of your Transmission Web Client
  const transmissionUrl = `http://http://localhost:8000/transmission/web/`;

  return (
    <div>
      <iframe
        src={transmissionUrl}
        width="100%"
        height="600"
        title="Transmission Web Client"
        frameborder="0"
      ></iframe>
    </div>
  );
}

export default TransmissionClient;