


$(document).ready(function() {
    console.log("media.js");
    $('#defaultCheck1').change(function() {
        // Show div
        if ($(this).is(':checked')) {
            $('#model2_form').show();
            $('#model2_form').find('select').attr('required', true);

            $('#model2_card').show();
            // add required tag for select
        }
        // Hide div
        else {
            $('#model2_form').hide();
            $('#model2_card').hide();


        }
        
    });
   
    $('#submit').click(function(e) {
        
        e.preventDefault();
        e.stopPropagation();
        console.log("submit");
        // Get form data from select tag
        var formData = new FormData($("#form")[0]);
        console.log(formData.get('models'));
        console.log(formData.get('models2'));
        console.log(formData.get('defaultCheck1'));
     
        // get value from checkbox 
        var checkbox = $('#defaultCheck1').is(':checked');
        console.log(checkbox);
        // Use AJAX to post the data to our adduser service
        $.ajax({
            type: 'POST',
            
            data: JSON.stringify({
                models: formData.get('models'),
                models2: formData.get('models2'),
                checkbox: checkbox
            }),
                
            url: 'http://127.0.0.1:8000/med_data',
            contentType: "application/json",
            dataType: 'json',
            setTimeout: 5000,
            beforeSend: function() {
                $("#loader_info").show();
        $("#info_disorders").hide();
            },
           
            

            success: function(data) {
                // Check for successful (blank) response
                console.log(data);
                $("#loader_info").hide();
                $("#info_disorders").hide();
                if (checkbox!=true && data.response_msg==='OK') {
                    // Clear the form inputs
                    console.log("no Compare");
                    best_acc=data.best_acc;
                    img=data.img;
                    img='data:image/jpeg;base64,'+img;
                    random_pred=data.pred;
                    // update the p tag with id best_acc
                    $('#acc').html(best_acc+"%");
                    $('#img_model').attr('src',img);
                    $('#pred').html(random_pred);
                    
                }
                else if (checkbox==true && data.response_msg==='OK') {
                    // If something goes wrong, alert the error message that our service returned
                    console.log("Compare");
                    //return {"model1": model1, "model2": model2,"compare":{"model1":random_pred,"model2":random_pred2}}

                    model1=data.model1;
                    model2=data.model2;
                    model1_pred=data.compare.model1;
                    model2_pred=data.compare.model2;
                    model1_img=data.compare_img.model1;
                    model2_img=data.compare_img.model2;
                    img1='data:image/jpeg;base64,'+model1_img;
                    img2='data:image/jpeg;base64,'+model2_img;

                    best_acc=data.best_acc;
                    $('#acc').html(model1+"%");
                    $('#acc2').html(model2+"%");
                    $('#img_model').attr('src',img1);
                    $('#img_model2').attr('src',img2);

                    $('#pred').html(model1_pred);
                    $('#pred2').html(model2_pred);

                }
                else {
                    // Show error_message div
                    $('#error_message_body').html(data.response_msg);
                    $('#error_message').show();
                }
            },
            error: function(data) {
                // If error, alert the error message that our service returned
                alert('Error: ' + error);
            }
        });
    });
});
