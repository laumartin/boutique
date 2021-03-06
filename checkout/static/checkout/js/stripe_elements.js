/* Core logic payment flow for this comes from here:
https://stripe.com/docs/payments/accept-a-payment

CSS from here:
https://stripe.com/docs/stripe-js */ 

/*get the stripe public key and client secret from the template those script elements there
contain the values we need as their text.So we can get them just by getting their ids and using the .text function.
Also slice off the first and last character on each since they'll have quotation marks which we don't want. */
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
/* to set up stripe create a variable using our stripe public key.*/ 
var stripe = Stripe(stripePublicKey);
/* Now we can use it to create an instance of stripe elements.Use that to create a card element.*/
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
/* nd finally, mount the card element to the div we created.The card element can also accept a style argument.*/
var card = elements.create('card', {style: style});
card.mount('#card-element');

/* Handle realtime validation errors on the card element
listener on the card element for the change event and every time it changes we'll check to see if there are any errors.
If so we'll display them in the card errors div we created near the card element on the checkout page.*/
card.addEventListener('change', function(event){
    var errorDiv = document.getElementById('card-errors');
    if( event.error){
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    }else{
        errorDiv.textContent = '';
    }
});
// Handle form submit (from Stripe documentation site)
var form = document.getElementById('payment-form');

/* After getting the form element the first thing the listener does is prevent its default action which in our case is to post.
Instead, we'll execute this code.*/
form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    // disable both the card element and the submit button to prevent multiple submissions.
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // trigger the overlay and fade out the form when the user clicks the submit button and reverse that if there's any error.
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    //We can get the boolean value of the saved info box by just looking at its checked attribute
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    // From using {% csrf_token %} in the form
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    //let's create a small object to pass this information to the new view.
    //And also pass the client secret for the payment intent.
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    var url = '/checkout/cache_checkout_data/';

    //post this data to the view using post method built into jQuery. Telling it we're posting to the URL 
    // and that we want to post the post data above. We'll want to wait for a response that the payment intent was updated
    // before calling the confirmed payment method by just tacking on the .done method and executing the callback function.
    $.post(url, postData).done(function() {
    // It uses the stripe.confirm card payment method to send the card information securely to stripe.
    // we call the confirm card payment method.Provide the card to stripe and then execute this function on the result.
    // stripe could potentially confirm the payment but the user could close the page before the form is submitted
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line1: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
            shipping:{
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address:{
                    line1: $.trim(form.street_address1.value),
                    line1: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            }

        }).then(function(result) {
            // If there's an error put the error right into the card error div, 
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                // if there's an error. We'll also want to re-enable the card element and the submit button to allow the user to fix it.
                $(errorDiv).html(html);
                // the overlay and fade out reverse if there's any error.
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
                // and otherwise, if the status of the payment intent comes back is succeeded we'll submit the form.
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                     form.submit();
                }
            }
        });
    //failure function will be triggered if our view sends a 400 bad request response. And in that case, we'll just\
    //reload the page to show the user the error message from the view.
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    })
});