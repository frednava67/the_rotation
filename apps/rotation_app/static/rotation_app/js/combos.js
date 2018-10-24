(function(a){var d=a.event,b,c;b=d.special.debouncedresize={setup:function(){a(this).on("resize",b.handler)},teardown:function(){a(this).off("resize",b.handler)},handler:function(a,f){var g=this,h=arguments,e=function(){a.type="debouncedresize";d.dispatch.apply(g,h)};c&&clearTimeout(c);f?e():c=setTimeout(e,b.threshold)},threshold:150}})(jQuery);

var $playlist1 = $('#playlist1'),
    numItem = $playlist1.children().length,
    widthItem = $playlist1.children().first().children().first().width(),
    numThumbs = function() {
        var num = Math.floor($(window).width() / widthItem);
        console.log('numThumbs', num);
        return num < numItem ? num : numItem - 1;
    },
    getNumScroll = function() {
        var num = numThumbs() > 3 ? Math.max(Math.floor(numThumbs() / 3), 1) : numThumbs();
        console.log('getNumScroll', num);
        return num;
    };

var $playlist2 = $('#playlist2'),
    numItem = $playlist2.children().length,
    widthItem = $playlist2.children().first().children().first().width(),
    numThumbs = function() {
        var num = Math.floor($(window).width() / widthItem);
        console.log('numThumbs', num);
        return num < numItem ? num : numItem - 1;
    },
    getNumScroll = function() {
        var num = numThumbs() > 3 ? Math.max(Math.floor(numThumbs() / 3), 1) : numThumbs();
        console.log('getNumScroll', num);
        return num;
    };

$playlist1.slick({
    dots            : false,
    arrows          : false,
    infinite        : true,
    lazyLoad        : 'ondemand',
    slidesToScroll  : getNumScroll(),
    slidesToShow    : numThumbs(),
    touchThreshold  : numThumbs(),
    focusOnSelect   : true,
    speed           : 600,
    centerMode      : true,
    cssEase         : 'linear',
    centerPadding   : 0,
});

$playlist2.slick({
    dots            : false,
    arrows          : false,
    infinite        : true,
    lazyLoad        : 'ondemand',
    slidesToScroll  : getNumScroll(),
    slidesToShow    : numThumbs(),
    touchThreshold  : numThumbs(),
    focusOnSelect   : true,
    speed           : 600,
    centerMode      : true,
    cssEase         : 'linear',
    centerPadding   : 0,
});


$(window).on('debouncedresize', function() {
    $playlist1
        .slick('slickSetOption', 'slidesToShow',   numThumbs())
        .slick('slickSetOption', 'touchThreshold', numThumbs())
        .slick('slickSetOption', 'slidesToScroll', getNumScroll(), true);

    $playlist2
    .slick('slickSetOption', 'slidesToShow',   numThumbs())
    .slick('slickSetOption', 'touchThreshold', numThumbs())
    .slick('slickSetOption', 'slidesToScroll', getNumScroll(), true);


});
    
    