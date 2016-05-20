
// fades flash message after four seconds 
setTimeout(
    function() {
        $('.alert').fadeOut('fast');
    }, 4000);

// ADD INTERACTION MODAL
// populates the add interaction modal with contact's name and id data
$('.add-int').on('click', function (evt) {
    var contactName = $(this).data('name');
    var contactId = $(this).data('contact-id');
    $('#contact-name-for-form').text(contactName);
    $('#contact-id').attr('value', contactId);
});


// POPULATES UPDATE PROFILE MODAL
$('#edit-profile-button').click(function (evt) {
    evt.preventDefault();
    $.get('/getUser.json', function (data) {
        var fullName = data.first_name + " " + data.last_name;
        $('#user-name.prepopulate').text(fullName);
        $('#first-name.prepopulate').val(data.first_name);
        $('#last-name.prepopulate').val(data.last_name);
        $('#email.prepopulate').val(data.email);
        $('#zipcode.prepopulate').val(data.zipcode);
    });
});


// DISPLAY RELATIONSHIP FOR SPECIFIC CONTACT
// populates the contact relationship modal with contact info
$('.relationship-link').on('click', function (evt) {
    var contactName = $(this).data('name');
    var contactId = $(this).data('contact-id');
    $('#contact-name-for-relationship').text(contactName);
    $('#contact-id-for-relationship').data('contact-id', contactId);
    evt.preventDefault();
    // displays interesting metrics about a specific relationship
    $.post('/getContact.json', {'id': contactId}, function (data) {
        // makes full name of contact
        var name = data.first_name + " " + data.last_name;
        // displays address in correct format
        if (data.street) {
            var address = (data.street + ", " + data.city + ", " +
                           data.state + " " + data.zipcode);
            $('#address.relationship').text(address);
        }
        // populates contact contact information
        $('#name.relationship').text(name);
        $('#email.relationship').text(data.email);
        $('#cell-phone.relationship').text(data.cell_phone);
        // populates relationship frienergy stats
        $('#total-ints.relationship').text("Total interactions: " +
            data.total_interactions);
        $('#total-frienergy.relationship').text("Total frienergy: " +
            data.total_frienergy);
        $('#avg-power.relationship').text("Average frienergy per day: " +
            data.avg_power);
        $('#avg-t-btwn-ints.relationship').text(
            "Average time between interactions: " + data.avg_t_btwn_ints);
        $('#t-since-last-int.relationship').text("Time since last interaction: "
            + data.t_since_last_int);
        $('#avg-frienergy-each-interaction.relationship').text(
            "Average frienergy per interaction: " +
            data.avg_frienergy_each_interaction);
        $('#notes.relationship').text("Notes: " + data.notes);
    });
});


// EDIT CONTACT
// populates edit contact form with current contact information from db
$('.edit-contact').on('click', function (evt) {
    evt.preventDefault();
    // gets contact id from form
    var contactId = $(this).data('contact-id');
    // gets contact info from server before showing the edit contact form
    $.post('/getContact.json', {'id': contactId}, function (data) {
        $('#prepopulate-contact-id').val(data.contact_id);
        $('#prepopulate-first-name').val(data.first_name);
        $('#prepopulate-last-name').val(data.last_name);
        $('#prepopulate-email').val(data.email);
        $('#prepopulate-cell-phone').val(data.cell_phone);
        $('#prepopulate-street').val(data.street);
        $('#prepopulate-city').val(data.city);
        $('#prepopulate-state').val(data.sate);
        $('#prepopulate-zipcode').val(data.zipcode);
    });
});


// EDIT INTERACTION
// prepopulates the edit-interaction form
// gets interaction info from server before showing edit interaction form
$('.interaction-link').on('click', function (evt) {
    evt.preventDefault();
    var interactionId = $(this).data('int-id');
    $.post('/getInteraction.json', {'id': interactionId}, function (data) {
        $('#prepopulate-int-id').val(data.interactionId);
        $('#prepopulate-note-id').val(data.noteId);
        $('#prepopulate-contact-name').text(data.contactName);
        $('#prepopulate-date').val(data.date);
        $('#prepopulate-frienergy').val(data.frienergy);
        $('#prepopulate-note').val(data.noteText);
    });
});


// NOTE POPOVER
$('.note-popover').click( function (evt) {
    var interactionId = $(this).data('id');
    $.get('/getNote.json', {'id': interactionId}, function (data) {
        $('a[data-id=' + interactionId + ']').popover({content: data}).popover('toggle');
    });
});


