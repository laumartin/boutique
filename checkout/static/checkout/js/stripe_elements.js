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
    // It uses the stripe.confirm card payment method to send the card information securely to stripe.
    // we call the confirm card payment method.Provide the card to stripe and then execute this function on the result.
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
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
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
            // and otherwise, if the status of the payment intent comes back is succeeded we'll submit the form.
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});