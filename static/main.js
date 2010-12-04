$(function() {
	$.timeago.settings.strings = {
        prefixAgo: "לפני",
        prefixFromNow: "מעכשיו",
        seconds: "פחות מדקה",
        minute: "דקה",
        minutes: "%d דקות",
        hour: "שעה",
        hours: "%d שעות",
        day: "יום",
        days: "%d ימים",
        month: "חודש",
        months: "%d חודשים",
        year: "שנה",
        years: "%d שנים"
    };

    var page = 0;

    $(window).scroll(function() { 
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 1) {
            $.getJSON("/updates?page=" + (page + 1), function(json) {
                load(json, false);
                page++;
            });
        }
    });


    $.getJSON("/updates?page=0", function(json) {      
        load(json, false);
    });    
});
        
function load(json, prepend) {
    var delay = 0;
               
    $.each(prepend ? json.reverse() : json, function(index, value) {
        var data = $("<li></li>")
            .append($("<div></div")
                .addClass("title")
                .text(value.content))
                .append($("<div></div>")
                    .addClass("description")
                    .text(value.description))
                    .append($("<div></div>")
                        .addClass("datesource")
                        .append($("<abbr></abbr>")
                            .attr("title", value.date)
                            .timeago())
                        .append(" - ")
                        .append($("<a></a>")
                            .attr("href", value.source_url)
                            .text(value.source)))
                .addClass("item").hide();

            prepend ? $("ul").prepend(data) : $("ul").append(data);
    });
                
    $("ul > li").each(function() {
        $(this).delay(delay).fadeIn(1000);
            delay += 50;
        });
}
