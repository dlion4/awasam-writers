document.addEventListener('scroll', load_script);
document.addEventListener('mousedown', load_script);
document.addEventListener('mousemove', load_script);
document.addEventListener('touchstart', load_script);
document.addEventListener('keydown', load_script);

function load_script () {

    // zopim code
    window.$zopim||(function(d,s){var z=$zopim=function(c){z._.push(c)},$=z.s=
        d.createElement(s),e=d.getElementsByTagName(s)[0];z.set=function(o){z.set.
    _.push(o)};z._=[];z.set._=[];$.async=!0;$.setAttribute('charset','utf-8');
        $.src='//v2.zopim.com/?2cNaiMpGahesGtbvnw4a0u5l9MFXmHoc';z.t=+new Date;$.
            type='text/javascript';e.parentNode.insertBefore($,e)})(document,'script');
    $zopim(function() {
        $zopim.livechat.theme.setColor('#2f4bff');
        $zopim.livechat.theme.reload();
        $zopim.livechat.departments.filter('1. I am a new customer', '2. I am an existing customer');
    });

    document.removeEventListener('scroll', load_script);
    document.removeEventListener('mousedown', load_script);
    document.removeEventListener('mousemove', load_script);
    document.removeEventListener('touchstart', load_script);
    document.removeEventListener('keydown', load_script);

}
