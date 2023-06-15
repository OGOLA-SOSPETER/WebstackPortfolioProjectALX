$(function() {
    $('#contact-form').validator();

    $('#send_message').on('click', function(e) {
        e.preventDefault();

        var form = $(this).closest('form');
        var messages = form.find('.messages');

        form.validator('validate');

        if (!form.has('.has-error').length) {
            var url = "contact.php";

            $.ajax({
                type: "POST",
                url: url,
                data: form.serialize(),
                success: function(data) {
                    var messageAlert = 'alert-' + data.type;
                    var messageText = data.message;

                    var alertBox = '<div class="alert ' + messageAlert + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + messageText + '</div>';

                    if (messageAlert && messageText) {
                        messages.html(alertBox);
                        form[0].reset();
                    }
                }
            });
        }
    });
});