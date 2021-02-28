/* Core logic payment flow for this comes from here:
https://stripe.com/docs/payments/accept-a-payment

CSS from here:
https://stripe.com/docs/stripe-js */ 

/*get the stripe public key and client secret from the template those script elements there
contain the values we need as their text.So we can get them just by getting their ids and using the .text function.
Also slice off the first and last character on each since they'll have quotation marks which we don't want. */
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
/* to set up stripe create a variable using our stripe public key.*/ 
var stripe = Stripe(stripe_public_key);
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