
$('#btn-login').click(function(evt) {

    var username = $('#username').val();
    var password = $('#password').val();

    var postData = {
        username: username,
        password: password
    };
   
    // Make a POST request to the authentication API endpoint
    $.ajax({
        type: 'POST',
        url: 'auth/v1/login', // Replace with your API endpoint URL
        contentType: 'application/json',
        data: JSON.stringify(postData),
        
        success: function(response) {
            //Redirect to the accounts page after successful authentication
            window.location.href = 'http://localhost:5000/main'; // Replace with your accounts page URL
        },
        error: function(response) {
            $('#login-msg').html('Invalid credentials')
            //alert(response);
        }
    });

    return false
});

$('#btn-register').click(function(){
    let first_name = $('#fname').val();
    let last_name = $('#lname').val();
    let username = $('#rusername').val();
    let email = $('#email').val();
    let password = $('#rpassword').val();
    let confirmpasswd = $('#cpassword').val();

    // Validate empty fields
    if (!first_name || !last_name || !username || !email || !password || !confirmpasswd) {
        $("#signup-msg").text("All fields are required.");
        return false;
    }

    // Validate password length
    if (password.length < 6) {
        $("#signup-msg").text("Password must be at least 6 characters long.");
        $('#signup-msg').focus();
        return false;
    }

    // Validate password and confirm password match
    if (password !== confirmpasswd) {
        $("#signup-msg").text("Password and Confirm Password do not match.");
        return false;
    }

    // If all validations pass, proceed with the AJAX request
    let postData = {
        first_name: first_name,
        last_name: last_name,
        username: username,
        email: email,
        password: password,
        confirmpasswd: confirmpasswd
    };

    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/api/v1/users', // Replace with your API endpoint URL
        contentType: 'application/json',
        data: JSON.stringify(postData),
        
        success: function(response) {
            $('#signup-msg').text('Registered successfully')
            // Handle success response if necessary
        },
        error: function(xhr) {
            // Handle error response here
            if (xhr.responseJSON && xhr.responseJSON.error) {
                let errorMessage = xhr.responseJSON.error;
                // Update the h2 element with the error message
                $("#signup-msg").text(errorMessage);
            } else {
                // Handle other types of errors if necessary
                $("#signup-msg").text("An error occurred.");
            }
        }
    });

    return false;
});
