
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
            window.location.href = 'http://localhost:5000/my-account'; // Replace with your accounts page URL
        },
        error: function(response) {
            //alert(response);
        }
    });

    return false
});

$('#btn-register').click(function(){

    let first_name = $('#fname').val();
    let last_name = $('#lname').val();
    let username = $('#username').val();
    let email = $('#email').val();
    let password = $('#password').val();
    let confirmpasswd = $('#cpassword');

    let postData = {

        first_name: first_name,
        last_name :last_name,
        username :username,
        email :email,
        password:password,
        confirmpasswd:confirmpasswd

    };

    $.ajax({
        type: 'POST',
        url: 'http://localhost:5000/api/v1/user', // Replace with your API endpoint URL
        contentType: 'application/json',
        data: JSON.stringify(postData),
        
        success: function(response) {
            console.log(response)
        },
        error: function(response) {
            console.log(response)
        }
    });

    return false
});
