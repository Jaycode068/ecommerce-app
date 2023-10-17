const htmlCode = ``

const apiUrl = 'https://';

const formData = new FormData();
formData.append('html', new Blob([htmlCode], { type: 'text/html' }));

// Create a new Headers object and set the Content-Type header to multipart/form-data
const headers = new Headers();
headers.set('Content-Type', 'multipart/form-data');

// Send a POST request to your API with the headers object
fetch(apiUrl, {
  method: 'POST',
  headers,
  body: formData
})
  .then(response => {
    if (response.ok) {
      console.log('HTML code uploaded successfully.');
    } else {
      console.error('Failed to upload HTML code.');
    }
  })
  .catch(error => {
    console.error('An error occurred:', error);
  });
