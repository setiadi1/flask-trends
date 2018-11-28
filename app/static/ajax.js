
$(document).ready(function() {
    $("#trend-submit").on("click", function(event) {
        $("#contentx").hide();
        $.ajax({
            data: {
                category: $("#item-category").val(),
                state: $("#state").val(),
                start: $("#order-date-start").val(),
                end: $("#order-date-end").val(),
                granularity: $("#granularity").val()
            },
            type: 'POST',
            url: '/_trends',
            beforeSend: function () {
                $('#loader-x').show();
                $("#graphx").hide();
            },
            complete: function () {
                $("#loader-x").hide();
            },
            success: function(data) {
                if (data) {
                    $("#contentx").slideDown(1000);
                    // console.log(data)
                    var vplot1 = 'data:image/png;base64,' + data.plot1;
                    var vplot2 = 'data:image/png;base64,' + data.plot2;
                    var vplot3 = 'data:image/png;base64,' + data.plot3;
                    // console.log(vplot1)
                    // console.log(vplot2)
                    // console.log(vplot3)
                    $('#plot1').attr('src', vplot1);
                    $('#plot2').attr('src', vplot2);
                    $('#plot3').attr('src', vplot3);
                    $("#text1").text(data.text1);
                    $("#text2").text(data.text2);
                    $("#text3").text(data.text3);
                    $("#text4").text(data.text4);
                } else {
                    $("#contentx").hide();
                    $("#graphx").show();
                }
            },
            error: function() {
                $("#graphx").show();
            }
        })
        event.preventDefault();
    })
})
