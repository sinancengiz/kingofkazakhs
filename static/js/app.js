

$('#header_message').hide(5000);


$('#army_info_table').hide();
$('#city_info_table').hide();
$('#economic_info_table').hide();

$('#population_info_button').click( function(){
    $('#army_info_table').hide();
    $('#city_info_table').hide();
    $('#economic_info_table').hide();
    $('#population_info_table').show();
});

$('#army_info_button').click( function(){
    $('#population_info_table').hide();
    $('#city_info_table').hide();
    $('#economic_info_table').hide();
    $('#army_info_table').show();
});


$('#city_info_button').click( function(){
    $('#army_info_table').hide();
    $('#population_info_table').hide();
    $('#economic_info_table').hide();
    $('#city_info_table').show();
});

$('#economic_info_button').click( function(){
    $('#army_info_table').hide();
    $('#population_info_table').hide();
    $('#city_info_table').hide();
    $('#economic_info_table').show();
});


$('#castle_info_table').hide();

$('#castle_info_button').click( function(){
        $('#castle_info_table').toggle();
});

