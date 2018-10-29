
$(".loader").hide();
function checkBoxToggle() {
    $("#includeMore").toggleClass(this.checked);
}
function searchTags(selectedPlatform)
{
    var oldContent = "";
    var search = document.getElementById("search-text").value;
    search = search.split(" ")[0];
    var isChecked = $("#includeMore").is(':checked');
    if(isChecked === false)
    {
        document.getElementById("tweet-content").innerHTML = "";
    }
    else if(isChecked === true)
    {
        oldContent = document.getElementById("tweet-content").innerHTML;
        document.getElementById("tweet-content").innerHTML = "";
    }
    if(search == "")
    {
        toastr.error("The search cannot be empty!");
        return;
    }
    $(".loader").show();
    $.ajax({
        data: {'search':search, 'selectedPlatform':selectedPlatform },
        url: '/searchTags',
        type: 'POST',
        success: function (data) {
            console.log(JSON.parse(data));
            var data = JSON.parse(data);
            var gallery = [];
            if(selectedPlatform == 0){
                 var text = "<br/><br/><div style='text-align: center; font-size: 20px;'>Tweets tagged with: " +
                "<span style='background-color: #ff523f; border-radius: 5px; font-family: ";
                    text += "Lobster', cursive'; > #";
                    text += search;
                    text += "</span></div><br/><br/>";

            }
            else if(selectedPlatform == 1){
                var text = "<br/><br/><div style='text-align: center; font-size: 20px;'>Tumblr Images with tag: " +
                "<span style='background-color: #8cff77; border-radius: 5px; font-family: ";
                    text += "Lobster', cursive'; >";
                    text += search;
                    text += "</span></div><br/><br/>";
            }
            else{
                var text = "<br/><br/><div style='text-align: center; font-size: 20px;'>Twitter and Tumblr Images with tag: " +
                "<span style='background-color: #8cff77; border-radius: 5px; font-family: ";
                    text += "Lobster', cursive'; >";
                    text += search;
                    text += "</span></div><br/><br/>";
            }


            document.getElementById("tweet-content").innerHTML += text;

            for(var i = 0; i < data["images"].length; i++) {
                var html = "<a href='";
                html += data.images[i];
                html += "' class='big' title='";
                html += data.user[i] + " - " + data.text[i];
                html += "'> <img alt='Image Not Available' id='dummy1' style='border-radius: 30px; width: 300px; height: 300px; margin: 10px 10px 10px 10px'; class='tweet-images' src='";
                html += data.images[i];
                html += "' >";
                document.getElementById("tweet-content").innerHTML += html;
                gallery.push({'name': data.user[i], 'url': data.images[i], 'description': data.text[i]});
            }
            $.ajax({
                data: {'search':search, 'selectedPlatform':selectedPlatform },
                url: '/saveTerms',
                type: 'POST',
                success: function () {
                    console.log("Success");
                },
                error: function () {
                    console.log("Error");
                }

            });
            $(".loader").hide();
            document.getElementById("tweet-content").innerHTML += oldContent;
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

function twitterOrTumblrToggle(details) {
    var nodeId = details.id;
    $("#twitter").hasClass("selected") ? $("#twitter").removeClass("selected") : "";
    $("#tumblr").hasClass("selected") ? $("#tumblr").removeClass("selected") : "";
    $("#everything").hasClass("selected") ? $("#everything").removeClass("selected") : "";
    $("#" + nodeId).addClass("selected");
}

function twitterOrTumblr()
{
    var isTwitterChecked = $(".twitter-btn").hasClass("selected");
    var isTumblrChecked = $(".tumblr-btn").hasClass("selected");
    if(isTwitterChecked === true){
        searchTags(0);
    }
    else if(isTumblrChecked == true) {
        searchTags(1);
    }
    else {
        searchTags(2);
    }


}

function showWarning(){
    toastr.info('Login/Register to use the web app!');
}