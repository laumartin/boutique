/* get the value of the country field when the page loads and store it in a variable.
(the value will be an empty string if the first option is selected)*/
let countrySelected = $('#id_default_country').val();
/*if that's selected we can use this as a boolean.So if country selected is false then we want the colour
of this element to be that grey placeholder colour.*/
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
/*Then we need to capture the change event and every time the box changes we'll get the value of it
and then determine the proper colour.*/
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected){
        $(this).css('color', '#aab7c4');
    } else{
        $(this).css('color', '#000');
    }
});