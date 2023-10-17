$("#btn_submit").click(function(){

    let userDetails ={
        username :"Emmanuel",
        email :"Admin@thetekgenius.com",
        password :"emmydavii"
    }

    $.ajax({
        type:"POST",
        contentType: "application/json",
        url:"http://localhost:5000/api/v1/users",
        data: {USERDETAILS: JSON.stringify(userDetails)},
        success: function (data) {
            console.log(data)
        },

        error: function(jqXHR, textStatus, errorThrown) {
            
            console.log("AJAX Request Failed");
            console.log(textStatus, errorThrown);
          }
    }); 
});

// Assuming you have a form with id="addressForm" and input fields with appropriate ids
$(document).ready(function() {
    $('#addressForm').submit(function(event) {
        event.preventDefault();

        // Get input values
        var street = $('#streetInput').val();
        var city = $('#cityInput').val();
        var state = $('#stateInput').val();
        var postalCode = $('#postalCodeInput').val();

        // Prepare data to send
        var postData = {
            street: street,
            city: city,
            state: state,
            postal_code: postalCode
        };

        // Send POST request using jQuery
        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/api/v1/addresses',  // Replace this with your Flask route
            contentType: 'application/json',
            data: JSON.stringify(postData),
            success: function(response) {
                // Handle success response from the server
                console.log('Data posted successfully:', response);
            },
            error: function(error) {
                // Handle error response from the server
                console.error('Error posting data:', error);
            }
        });
    });
});
