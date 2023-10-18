function redirectToRegister() {
  window.location.href = "/register";
}

document.addEventListener("DOMContentLoaded", function() {
  const signUpLink = document.querySelector("#signup-link");

  if (signUpLink) {
      signUpLink.addEventListener("click", function(event) {
          event.preventDefault();
          redirectToRegister();
      });
  }
});

// Add an event listener to the form
document.getElementById('registrationForm').addEventListener('submit', function (event) {
  event.preventDefault(); // Prevent the default form submission
  const form = event.target;

  // Get user data from the form
  const formData = new FormData(form);

  // Send a POST request to the /api/users route
  fetch('/api/v1/users', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => response.json())
  .then(data => {
      // Handle the response from the server (e.g., show a success message or error message)
      console.log(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
});
