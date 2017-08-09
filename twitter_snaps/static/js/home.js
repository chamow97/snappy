
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
            // document.getElementById("tweet-content").innerHTML = "";
            var data = JSON.parse(data);
            var gallery = [];
            var text = "<br><div style='text-align: center; font-size: 20px;'>Search results for: " +
                "<span style='background-color: #8cff77; border-radius: 5px; font-family: ";
            text += "Lobster', cursive'; > ";
            text += search;
            text += "</span></div><br><br>";
            document.getElementById("tweet-content").innerHTML += text;

            for(var i = 0; i < data["images"].length; i++)
            {
                var html = "<a href='";
                html += data.images[i];
                html += "' class='big' title='";
                html += data.user[i] + " - " + data.text[i];
                html += "'> <img style='border-radius: 30px; width: 300px; height: 300px; margin: 10px 10px 10px 10px'; class='tweet-images' src='";
                html += data.images[i];
                html += "' >";
                document.getElementById("tweet-content").innerHTML += html;
                gallery.push({'name': data.user[i], 'url':data.images[i], 'description':data.text[i]});
            }
            $(".loader").hide();
            var gallery = $('#tweet-content a').simpleLightbox();
            document.getElementById("search-text").value = "";
        },
        error: function () {
            $(".loader").hide();
            toastr.error("Something went wrong! Make sure you are connected to the internet!");
            return;
        }

    });
}

function twitterOrInsta()
{
    $(".twitter-btn").toggleClass("selected");
    $(".insta-btn").toggleClass("selected");
}