var base_url = 'http://localhost:8000/visualise/'

$(document).ready(function () {

    $("#btnSubmit").click(function (event) {
	
        //stop submit the form, we will post it manually.
        event.preventDefault();

        // Get form
        var form = $('#fileUploadForm')[0];

	// Create an FormData object
        var data = new FormData(form);

	// If you want to add an extra field for the FormData
        // data.append("CustomField", "This is some extra data, testing");
	
	// disabled the submit button
        $("#btnSubmit").prop("disabled", true);

        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            url: base_url + "image/upload/",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 600000,
            success: function (data) {

                $("#result").text(data);
                $("#btnSubmit").prop("disabled", false);
		if (data.success == true) {
		    alert('data is true')
		    window.location.reload();
	    }
            },
            error: function (e) {

                $("#result").text(e.responseText);
                console.log("ERROR : ", e);
                $("#btnSubmit").prop("disabled", false);
            }
        });
	window.location.reload();
    });

});

var visualise = function () {
    $("#url_submit").prop("disabled", true);
    var image_url = document.getElementById("url_input").value;
    if (image_url != null) {
	var upload_data = {image_url: image_url};
    } else {
	alert('Input url missing')
    }
    $.ajax({
	url: base_url + "image/upload/",
	type: "POST",
	data: upload_data,
	dataType: "text",
	timeout: 600000,
	async: false,
	success: function(resultData) {
	},
	error: function() {alert('Something went wrong');},
    })
    window.location.reload();
};


var image_listing = function () {
    $.ajax({
        url: base_url + "image/",
        type: "GET",
        success: function(result) {
	    html = ``
	    nav_html = ``
	    t_html = ``
	    var list_images = function () {
		$.each(result, function(index) {
		    var image_url = result[index].url
		    var labels = result[index].labels
		    var text = result[index].text
		    table_html = ``
		    header = `<table><tr><th>Feature</th><th>Score</th></tr>`
		    var label_table = $.each(labels, function(index) {
			table_html += `
			    <tr>
			    <td>` + labels[index].description + `</td>
			    <td>` + labels[index].score + `</td>
			    </tr>
			    <table>`
		    })
			table_html = header + table_html
			nav_html = `<nav><img src=`+image_url+`></nav>`
		    t_html = `<div style="margin-bottom: 20px;"><article><p>`+table_html+`</p><p>Text: `+text+`</p></article></div>`
		    t_html = `</div>` + nav_html + t_html
		    html += t_html
		    console.log(html);
		}
		      );
		return html
	    }
	    var content_html = list_images()
            $("#image-listing").append(content_html);
	}
    })}


function bs_input_file() {
    $(".input-file").before(
	function() {
	    if ( ! $(this).prev().hasClass('input-ghost') ) {
		var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
		element.attr("name",$(this).attr("name"));
		element.change(function(){
		    element.next(element).find('input').val((element.val()).split('\\').pop());
		});
		$(this).find("button.btn-choose").click(function(){
		    element.click();
		});
		$(this).find("button.btn-reset").click(function(){
		    element.val(null);
		    $(this).parents(".input-file").find('input').val('');
		});
		$(this).find('input').css("cursor","pointer");
		$(this).find('input').mousedown(function() {
		    $(this).parents('.input-file').prev().click();
		    return false;
		});
		return element;
	    }
	}
    );
}
$(function() {
    bs_input_file();
});
