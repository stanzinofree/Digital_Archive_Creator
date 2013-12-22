/**
 * Created with PyCharm.
 * User: alessandro
 * Date: 17/07/13
 * Time: 12.41
 * To change this template use File | Settings | File Templates.
 */
jQuery(document).ready(function () {

    $('#search').autocomplete({
        source: "/sub_temp",
        messages: {
            noResults: '',
            results: function () {
            }
        }
    });
    $(".fancybox").fancybox();
    $('#submit_log').hide();
    $('#calc').hide();
    $('#log_list').autocomplete({
        source: "/log_list",
        messages: {
            noResults: '',
            results: function () {
            }
        }
    });
    $("prompt").keypress(function (e) {
        var keyCode = e.keyCode || e.which;
        var calc = $("#calc").val();

        if (keyCode == 13) {
            e.preventDefault();
            alert(calc);
        }
    });
    $("#remove").click(function () {
        var postdata = $("#remove").val()
        $.post('/admin/remove', postdata, function (data){
            $('#remove').html(data)
        });
        return false;
    });

    $("#command").submit(function () {
        // post the form values via AJAX…
        var postdata = {term: $("#prompt").val(), log: $("#log_list").val(), calc: $("#calc").val()};
        $.post('/log_sub', postdata, function (data) {
            // and set the title with the result
            $("#terminal").html(data);
        });
        return false;
    });
    $('#open_term').click(function() {
        dterm.dialog('open');
    });
    $("#testform").submit(function () {
        // post the form values via AJAX…
        var postdata = {term: $("#search").val()};
        $.post('/sub_calc', postdata, function (data) {
            // and set the title with the result
            $("#title").html(data);
        });
        $.post('/preview', postdata, function (data) {
            // and set the title with the result
            $("#preview").html(data);
        });
        $.post('/archive', postdata, function (data) {
            // and set the title with the result
            $("#archive").html(data);
        });
        return false;
    });
    //CAT SHOW_HIDE
    $("#cathide").click(function () {
        $(".catshow").toggle();
        return false;
    });
    //HEAD SHOW_HIDE
    $("#headhide").click(function () {
        $(".headshow").toggle();
        return false;
    });
    //TAIL SHOW_HIDE
    $("#tailhide").click(function () {
        $(".tailshow").toggle();
        return false;
    });
    //GREP SHOW_HIDE
    $("#grephide").click(function () {
        $(".grepshow").toggle();
        return false;
    });
    //DUMP SHOW_HIDE
    $("#dumphide").click(function () {
        $(".dumpshow").toggle();
        return false;
    });
    
});
