$(function(){

    $.getJSON("js/stats.json", function(data){

        console.log("Plugins: " + data.plugins.length)

        for (var i = 1; i <= data.plugins.length / 100; i++) {
            if (i > 0) {
                $('<li id="' + i + '" class="select">' +
                  '<a href="#">' + i + '01-</td>' +
                  '</li>'
                 ).appendTo('ul.nav');
            }
        }

        appendPluginRows(data.plugins)

    });

    /*
    var stats_th = $('table.stats thead'),
    offset = stats_th.offset();

    $(window).scroll(function () {
        if($(window).scrollTop() > offset.top) {
            nav.addClass('fixed');
        } else {
            nav.removeClass('fixed');
        }
    });
    */
});

function appendPluginRows(plugins){

    cnt = 0;

    $(plugins).each(function(){

        /*
        if (cnt % 50 == 0) {
            $('<tr>' +
              '<th>rank</th>' +
              '<th>plugin name</th>' +
              '<th>total installation</th>' +
              '</tr>'
             ).appendTo('table.stats tbody');
        }
        */

        $('<tr id="'+ cnt +'" class="plugin">' +
          '<td>' + (cnt + 1) + '</td>' +
          '<td><a href="' + this.plugin_info_url + '">' + this.name + '</a></td>' +
          '<td>' + this.total_installation + '</td>' +
          '</tr>'
         ).appendTo('table.stats tbody');

        cnt++;

    });
}

$(document).on("click", "li.select", function(e) {

    console.log("click: " + $(this).attr("id"))
    var i =  $(this).attr("id")
    var p = $("tr.plugin").eq(i*100).offset().top;
    $('html,body').animate({ scrollTop: p }, 'fast');

});
