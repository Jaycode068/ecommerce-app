$('#a-logout').click(function(){
    // Perform an AJAX request to the logout route and redirect the user
    $.ajax({
        url: 'http://localhost:5000/auth/v1/logout', // Assuming this is the correct logout route
        type: 'POST', // Use the appropriate HTTP method (GET, POST, etc.)
        success: function(response) {
            console.log(response)
            // Check the response from the server
            if (response && response.success) {
                // The logout was successful, redirect the user to the login page
                window.location.href = '/login'; // Redirect to the login page after successful logout
            } else {
                // The server returned an error message, handle it as needed
                console.error('Logout error:', response.error);
                // Optionally, display an error message to the user
            }
        },
        error: function(error) {
            // Handle any errors that occur during the logout request, if needed
            console.error('Logout error:', error);
        }
    });
});

