function writeCookie(name, value, days) {
	var date, expires;
	if (days) {
		date = new Date();
		date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
		expires = "; expires=" + date.toGMTString();
	} else {
		expires = "";
	}
	document.cookie = name + "=" + value + expires + "; path=/";
}

var common = {
	init: function() {
		common.fixNavigation();
		common.main();
		common.carousel();
		// common.select();
		// common.submit();
		common.menuActive();
	},
	fixNavigation: function(){
		// b-lazy

		var bLazy = new Blazy({});
		
		function fixPanel() {
			$('.main').css({'padding-top': $('.header').outerHeight()});
			$('.header').addClass('fixed');
		};

		// fixPanel();


		

		// rating item 


		$('.rating:not(.rating-static) label').click(function(event){
			event.preventDefault();
			$('.rating:not(.rating-static) label').removeClass('active')
			$(this).addClass('active')
		});


		function scrollScript(){

			if ($(window).width() > 1025) {
				$('.scroll-content').mCustomScrollbar({
					theme: "minimal-dark",
					callbacks:{
						whileScrolling:function(){
							if(this.mcs.top < 0){
								$('.header').addClass('fixed');
							}else{
								$('.header').removeClass('fixed')
							}

							if($('#animate1').hasClass('animate-blk')) {
								if($('#animate1').offset().top + 50 < 250){
									$('#animate1').addClass('animate-in');
								}
							}
						}
					}
				});
			}else {
				$('.scroll-content').mCustomScrollbar("destroy");
			}
		}


		// scrollScript()


		// $(window).scroll(function() {
		// 	fixPanel();
		// 	scrollScript()
		// });

		$( window ).resize(function() {
			// fixPanel();
			// scrollScript()
			var bLazy = new Blazy({});
		});

	},
	main: function(){


		// setTimeout(function(){
		// 	$('.cookies').addClass('show');
		// }, 2000);		
		
		// tabs 

		$('.tab-cnt-trigger').click(function(e){
			e.preventDefault();
			if(!$(this).hasClass('.active')) {
				var tabCnt = '.' + $(this).attr('data-cnt');
				$(this).closest('.tabs-block').find('.tabs-section a.active').removeClass('active')
				$(this).closest('.tabs-block').find('.tab-cnt').removeClass('active')
				$(tabCnt).addClass('active')
				$(this).addClass('active');
				var bLazy = new Blazy({});
			}
		});

		

		$('.accordion-head').click(function(){
			$('.accordion-row').not($(this).closest('.accordion-row')).removeClass('open');

			$(this).closest('.accordion-row').toggleClass('open');
			$(this).closest('.accordion-row').find('.accordion-content').slideToggle('fast');
			$('.accordion-content').not($(this).closest('.accordion-row').find('.accordion-content')).slideUp('fast');
		});

		$('.header-dis__close').click(function(event){
			event.preventDefault();
			writeCookie("superbpaper_dis_hide", !0, 30)
			$('.header-dis').remove();
			$('.header').addClass('dis-off');
		});


		$('.steps-item').click(function(event){
			event.preventDefault();
			var dataEl = '.' + $(this).attr('data-images')
			$('.steps-item').removeClass('active');
			$('.steps-img').removeClass('active');
			$(dataEl).addClass('active');
			$(this).addClass('active');
			var bLazy = new Blazy({});
		});

		// menu-trigger

		$('.menu-trigger').click(function(event){
			event.preventDefault();
			$('.header').toggleClass('open');
			$('body').toggleClass('hidden');
		});



		// click in another place

		// jQuery(function($){
		// 	$(document).mouseup(function (e){
		// 		var select = $(".custom-select");
		// 		var popup = $(".popup");
		//
		// 		if(!popup.is(e.target) && popup.has(e.target).length === 0){
		// 			if($("#disPopup").hasClass("active")){
		// 				$("#disPopup").addClass("only-one");
		// 			}
		// 			$('.popup-wrapper').removeClass('active');
		// 			$('body').removeClass('hidden');
		// 		}
		//
		// 		if(!select.is(e.target) && select.has(e.target).length === 0){
		// 			$('.select-row').removeClass('open');
		// 		}
		//
		// 	});
		// });

		$('.cookies-close').click(function(event){
			event.preventDefault();
			$('.cookies').removeClass('show');
		});

		$('.popup-close').click(function(event){
			event.preventDefault();
			$('.popup-wrapper').removeClass('active');
			$('body').removeClass('hidden');
		});

		// $(document).mouseleave(function(e){
		// 	if (e.clientY < 10) {
		// 		$("#disPopup").addClass("active");
		// 		$('body').addClass('hidden');
		// 	}
		// });
	},
	carousel: function(){
		$('.reviews-slider').slick({
			autoplay:true,
			autoplaySpeed:5000,
			slidesToShow: 5,
			slidesToScroll: 1,
			dots: false,
			arrows: true,
			speed: 500,
			centerMode: true,
			responsive: [
			  {
				breakpoint: 768,
				settings: {
				  slidesToShow: 1,
				  slidesToScroll: 1,
				  centerMode: true,
				}
			  },
			]
		  });

		  $('.rev-slider-in').slick({
			infinite: false,
			slidesToShow: 1,
			slidesToScroll: 1,
			dots: true,
			speed: 500,
			fade: true,
			cssEase: 'linear'
		  });
		  $('.blog-slider').slick({
			  infinite: false,
			  slidesToShow: 3,
			  slidesToScroll: 1,
			  dots: false,
			  arrows: false,
			  autoplay: true,
			  autoplaySpeed: 2000,
			  speed: 500,
		});

	},
	select: function(){
		var x, i, j, l, ll, selElmnt, a, b, c;
		/* Look for any elements with the class "custom-select": */
		x = document.getElementsByClassName("custom-select");
		l = x.length;
		for (i = 0; i < l; i++) {
		selElmnt = x[i].getElementsByTagName("select")[0];
		ll = selElmnt.length;
		/* For each element, create a new DIV that will act as the selected item: */
		a = document.createElement("DIV");
		a.setAttribute("class", "select-selected");
		a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
		x[i].appendChild(a);
		/* For each element, create a new DIV that will contain the option list: */
		b = document.createElement("DIV");
		b.setAttribute("class", "select-items select-hide");
		for (j = 1; j < ll; j++) {
			/* For each option in the original select element,
			create a new DIV that will act as an option item: */
			c = document.createElement("DIV");
			c.innerHTML = selElmnt.options[j].innerHTML;
			c.addEventListener("click", function(e) {
				/* When an item is clicked, update the original select box,
				and the selected item: */
				var y, i, k, s, h, sl, yl;
				s = this.parentNode.parentNode.getElementsByTagName("select")[0];
				sl = s.length;
				h = this.parentNode.previousSibling;
				for (i = 0; i < sl; i++) {
				if (s.options[i].innerHTML == this.innerHTML) {
					s.selectedIndex = i;
					h.innerHTML = this.innerHTML;
					y = this.parentNode.getElementsByClassName("same-as-selected");
					yl = y.length;
					for (k = 0; k < yl; k++) {
					y[k].removeAttribute("class");
					}
					this.setAttribute("class", "same-as-selected");
					break;
				}
				}
				h.click();
			});
			b.appendChild(c);
		}
		x[i].appendChild(b);
		a.addEventListener("click", function(e) {
			/* When the select box is clicked, close any other select boxes,
			and open/close the current select box: */
			e.stopPropagation();
			closeAllSelect(this);
			this.nextSibling.classList.toggle("select-hide");
			this.classList.toggle("select-arrow-active");
		});
		}

		function closeAllSelect(elmnt) {
			/* A function that will close all select boxes in the document,
			except the current select box: */
			var x, y, i, xl, yl, arrNo = [];
			x = document.getElementsByClassName("select-items");
			y = document.getElementsByClassName("select-selected");
			xl = x.length;
			yl = y.length;
			$('.select-row').removeClass('open');
			for (i = 0; i < yl; i++) {
				if (elmnt == y[i]) {
					arrNo.push(i)
				} else {
					y[i].classList.remove("select-arrow-active");
					if($(elmnt).closest('.select-row').find('.select-selected').hasClass('select-arrow-active')){
						$('.select-row').removeClass('open');
					}else {
						$(elmnt).closest('.select-row').addClass('open');
					}
					
				}
			}
			for (i = 0; i < xl; i++) {
				if (arrNo.indexOf(i)) {
					x[i].classList.add("select-hide");	
				}
			}
		}

		/* If the user clicks anywhere outside the select box,
		then close all select boxes: */
		document.addEventListener("click", closeAllSelect);
	},
	submit: function(){
		$("form#mail").submit(function(event){
			event.preventDefault();
			formField = $(this).find(".required-field")
			formField.each(function(){
				var thisEl = $(this);
				if (! thisEl.val().length) {
					thisEl.addClass('error')
					setTimeout(function(){
						thisEl.removeClass('error')
					}, 3000)
					thisEl.addClass('form-error')
				}else { thisEl.removeClass('form-error')}
			});
			if(formField.hasClass('form-error') == false){
				$('.popup-wrapper').removeClass('active')
				$('#thanksPopup').addClass('active')
				$("#disPopup").addClass("only-one");
				$('body').addClass('hidden');
				var bLazy = new Blazy({});
			}
		});


	},
	menuActive: function (){
		$(".nav-list a").each(function() {
			if(this.href == location.href){
				$(this).addClass("active")
			}

		});
	}
};

(function() {
	common.init();
}());

