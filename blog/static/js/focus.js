
    window.addEventListener('load', function () {
        var focus = document.querySelector('.focus');
        var arrow_l = document.querySelector('.arrow-l');
        var arrow_r = document.querySelector('.arrow-r');

        var focusWidth = focus.offsetWidth;

        //1.鼠标经过轮播图模块，左右按钮显示，离开隐藏左右按钮。
        focus.addEventListener('mouseover', function () {
            arrow_l.style.display = 'block';
            arrow_r.style.display = 'block';
            clearInterval(timer);
        });
        focus.addEventListener('mouseout', function () {
            arrow_l.style.display = 'none';
            arrow_r.style.display = 'none';
            timer = setInterval(function () {
                //手动调用事件
                arrow_r.click();

            }, 5000);
        })

        var ul = focus.querySelector('ul');
        var ol = focus.querySelector('ol');

        //2.动态生成小圆点,同时绑定小圆点 点击事件
        for (var i = 0; i < ul.children.length; i++) {
            var li = document.createElement('li');
            //设置自定义属性
            li.setAttribute('index', i);
            // 插入
            ol.appendChild(li);
            // 排他思想
            li.addEventListener('click', function () {
                for (var j = 0; j < ol.children.length; j++) {
                    ol.children[j].className = ' ';
                }
                this.className = 'current';
                // 移动代码
                var index = this.getAttribute('index');
                num = index;
                cir = index;
                //核心 动画代码
                animate(ul, -index * focusWidth);

            });

        }
        ol.children[0].className = 'current';
        var cir = 0;

        //3. 右侧按钮
        // 3.1 拷贝
        var li_2 = ul.children[0].cloneNode(1);
        ul.appendChild(li_2);

        // 3.2 点击事件设置
        var num = 0;
        arrow_r.addEventListener('click', function () {
            if (num == ul.children.length - 1) {
                ul.style.left = 0;
                num = 0;
            }
            num++;

            animate(ul, -num * focusWidth);

            // 3.3 和其他系统进行交互
            cir = num;
            if (cir == ul.children.length - 1) {
                cir = 0;
            }
            for (var i = 0; i < ol.children.length; i++) {
                ol.children[i].className = ' ';
            }
            ol.children[cir].className = 'current';

        })


        // 4.左侧按钮

        // 4.1 点击事件设置

        arrow_l.addEventListener('click', function () {
            if (num == 0) {
                num = ul.children.length - 1;
                ul.style.left = -(ul.children.length - 1) * focusWidth + 'px';
            }
            num--;

            animate(ul, -num * focusWidth);

            // 4.2 和其他系统进行交互
            cir = num;
            if (cir == ul.children.length - 1) {
                cir = 0;
            }
            for (var i = 0; i < ol.children.length; i++) {
                ol.children[i].className = ' ';
            }
            ol.children[cir].className = 'current';

        })

        // 5.自动播放
        var timer = setInterval(function () {
            //手动调用事件
            arrow_r.click();

        }, 5000);
    })
