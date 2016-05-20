
// fades flash message after four seconds 
setTimeout(
    function() {
        $('.alert').fadeOut('fast');
    }, 4000);

// populates the add interaction modal with contact's name and id data
function getContact(evt) {
    var contactName = $(this).data('name');
    var contactId = $(this).data('contact-id');
    $('#contact-name-for-form').text(contactName);
    $('#contact-id').attr('value', contactId);
}

$('.add-int').on('click', getContact);


// UPDATE PROFILE MODAL
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
// displays interesting metrics about a specific relationship
function displayRelationshipData(data) {
    var name = data.first_name + " " + data.last_name;

    if (data.street) {
        var address = (data.street + ", " + data.city + ", " +data.state + " " + data.zipcode);
        $('#address.relationship').text(address);
    }


    // populate contact contact information
    $('#name.relationship').text(name);
    $('#email.relationship').text(data.email);
    $('#cell-phone.relationship').text(data.cell_phone);

    // populate relationship frienergy stats
    $('#total-ints.relationship').text("Total interactions: " + data.total_interactions);
    $('#total-frienergy.relationship').text("Total frienergy: " + data.total_frienergy);
    $('#avg-power.relationship').text("Average frienergy per day: " + data.avg_power);
    $('#avg-t-btwn-ints.relationship').text("Average time between interactions: " + data.avg_t_btwn_ints);
    $('#t-since-last-int.relationship').text("Time since last interaction: " + data.t_since_last_int);
    $('#avg-frienergy-each-interaction.relationship').text("Average frienergy per interaction: " + data.avg_frienergy_each_interaction);
    $('#notes.relationship').text("Notes: " + data.notes);
}

// populates the contact relationship modal with contact info
function getRelationship(evt) {
    var contactName = $(this).data('name');
    var contactId = $(this).data('contact-id');
    $('#contact-name-for-relationship').text(contactName);
    $('#contact-id-for-relationship').data('contact-id', contactId);
    evt.preventDefault();
    $.post('/getContact.json', {'id': contactId}, displayRelationshipData);
}

$('.relationship-link').on('click', getRelationship);

// EDIT CONTACT
// populates edit contact form with current contact information from db
function populateContactForm(data) {
    $('#prepopulate-contact-id').val(data.contact_id);
    $('#prepopulate-first-name').val(data.first_name);
    $('#prepopulate-last-name').val(data.last_name);
    $('#prepopulate-email').val(data.email);
    $('#prepopulate-cell-phone').val(data.cell_phone);
    $('#prepopulate-street').val(data.street);
    $('#prepopulate-city').val(data.city);
    $('#prepopulate-state').val(data.sate);
    $('#prepopulate-zipcode').val(data.zipcode);
}

// gets contact info from server before showing the edit contact form
function getContactData(evt) {
    evt.preventDefault();
    // gets contact id from form
    var contactId = $(this).data('contact-id');
    $.post('/getContact.json', {'id': contactId}, populateContactForm);
}

$('.edit-contact').on('click', getContactData);


// EDIT INTERACTION
// prepopulates the edit-interaction form
function populateIntForm(data) {
    $('#prepopulate-int-id').val(data.interactionId);
    $('#prepopulate-note-id').val(data.noteId);
    $('#prepopulate-contact-name').text(data.contactName);
    $('#prepopulate-date').val(data.date);
    $('#prepopulate-frienergy').val(data.frienergy);
    $('#prepopulate-note').val(data.noteText);
}

// gets interaction info from server before showing edit interaction form
function getInteractionData(evt) {
    evt.preventDefault();
    var interactionId = $(this).data('int-id');
    $.post('/getInteraction.json', {'id': interactionId}, populateIntForm);
}

$('.interaction-link').on('click', getInteractionData);


// NOTE POPOVER
$('.note-popover').click( function (evt) {
    var interactionId = $(this).data('id');
    $.get('/getNote.json', {'id': interactionId}, function (data) {
        $('a[data-id=' + interactionId + ']').popover({content: data}).popover('toggle');
    });
});


