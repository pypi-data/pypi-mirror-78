(function($){
    $(document).ready(function(){
        $(".submit-row .cancellink").each(function(){
            var href = window.location.href;
            if(href.indexOf("&_edit_flag=1") >= 0){
                href = href.replace("&_edit_flag=1", "");
            }else if(href.indexOf("?_edit_flag=1&") >= 0){
                href = href.replace("?_edit_flag=1&", "?");
            }else if(href.indexOf("?_edit_flag=1") >=0){
                href = href.replace("?_edit_flag=1", "");
            }else if(href.indexOf("_edit_flag=1") >=0 ){
                href = href.replace("_edit_flag=1", "");
            }
            $(this).attr("href", href);
        });
        $(".submit-row .editlink").each(function(){
            var href = window.location.href;
            if(href.indexOf("?") < 0){
                href += "?";
            }
            href += "&_edit_flag=1";
            $(this).attr("href", href);
        })
    });
})(jQuery);
