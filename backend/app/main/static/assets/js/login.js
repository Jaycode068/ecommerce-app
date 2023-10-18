
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