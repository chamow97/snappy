
$(".loader").hide();

function searchTweet()
{
    var search = document.getElementById("search-text").value;
    if(search == "")
    {
        toastr.error("The search cannot be empty!");
        return;
    }
    search = "#"+search;
    $(".loader").show();
    $.ajax({
        data: {'search':search},
        url: '/searchTweet',
        type: 'POST',
        success: function (data) {
            document.getElementById("tweet-content").innerHTML = "";
            var data = JSON.parse(data);
            var gallery = []
            for(var i = 0; i < data["images"].length; i++)
            {
                var html = "<a href='";
                html += data.images[i];
                html += "' class='big' > <img style='max-height: 300px; max-width: 300px;' class='tweet-images' src='";
                html += data.images[i];
                html += "' >";
                document.getElementById("tweet-content").innerHTML += html;
                gallery.push({'name': data.user[i], 'url':data.images[i], 'description':data.text[i]});
            }
            $(".loader").hide();
            var gallery = $('#tweet-content a').simpleLightbox();

            // $("#tweet-content").nsAwesomeGallery({
            //     images: gallery,
            //     columns: 2
            // });
            document.getElementById("search-text").value = "";
        },
        error: function () {
            $(".loader").hide();
            toastr.error("Something went wrong! Make sure you are connected to the internet!");
            return;
        }

    });
}