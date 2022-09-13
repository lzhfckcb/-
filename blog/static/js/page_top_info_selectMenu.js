// <!-- 下拉菜单 -->
window.addEventListener('load', function () {
    var info = document.querySelector('.page_top_info');
    var menu = document.querySelector('.page_top_info_selectMenu');
    info.addEventListener('mouseover', function () {
        menu.style.display = 'block';
    });
    info.addEventListener('mouseout', function () {
        menu.style.display = 'none';
    });
    menu.addEventListener('mouseover', function () {
        this.style.display = 'block';
    });
    menu.addEventListener('mouseout', function () {
        this.style.display = 'none';
    });
})
