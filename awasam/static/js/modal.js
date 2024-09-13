function ModalClass() {
  function e() {
    document.getElementsByTagName("html")[0].onmouseleave = function (e) {
      void 0 == o(i.COOKIE_NAME) && f === !1 && e.clientY < 10 && i.beforeShow() && (i.showPopup(), n(!0, i.COOKIE_NAME, i.getCookieExpires()), s("post", "/modal/modal.php", "method=show"));
    };
  }

  function t(e) {
    var t = !0;
    return u.length <= 0
      ? t
      : (u.forEach(function (o, n, s) {
        e.indexOf(o) >= 0 && (t = !1);
      }), t);
  }

  function o(e) {
    var t = document.cookie.match(new RegExp("(?:^|; )" + e.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, "\\$1") + "=([^;]*)"));
    return t
      ? decodeURIComponent(t[1])
      : void 0;
  }

  function n(e, t, o) {
    document.cookie = t + "=" + e + "; path=/; expires=" + o;
  }

  function s(e, t, o) {
    var n = new XMLHttpRequest();
    return (
      n.open(e, t), "post" == e && "undefined" != typeof o
      ? (n.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"), n.send(o))
      : n.send(),
    n);
  }
  var i = this;
  (i.COOKIE_NAME = "popupemail_hide"),
  (i.COOKIE_EXPIRE = 90),
  (i.waitSubmitResult = !1),
  (i.sendAbort = !1),
  (i.inited = !1);
  var r,
    a,
    l = 15,
    u = [],
    d = !1,
    f = !1,
    m = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i,
    c = /^[a-zA-Z ]*$/i,
    h = /\D/;
  (this.init = function () {
    if (void 0 == o(i.COOKIE_NAME) && ((d = !0), this.inited === !1)) {
      // update here later
      var t = s("post", "/", "method=init");
      (this.init = !0),
      (t.onreadystatechange = function () {
        if (4 == this.readyState) {
          if (200 != this.status) 
            return (console.log("Error: " + this.status + ". " + this.statusText), void(f = !0));
          if (this.responseText.length <= 0) 
            return void(f = !0);
          var t = JSON.parse(this.responseText);
          if ("undefined" != typeof t.location) {
            if ("undefined" == typeof t.template || t.template.length <= 0) 
              return void(f = !0);
            i.setModalToBody(t.template);
          }
          r = setInterval(e, 1e3 * l);
        }
      });
    }
  }),
  (this.setTimeout = function (t) {
    void 0 == o(i.COOKIE_NAME) && ("undefined" != typeof r && clearTimeout(r), (l = t), (r = setInterval(e, 1e3 * l)));
  }),
  (this.setBanEmail = function (e) {
    return !(e.length <= 0) && void(u = e);
  }),
  (this.getCookieExpires = function () {
    var e = new Date(),
      t = e.getTime(),
      o = t + 1e3 * (60 * i.COOKIE_EXPIRE * 60 * 24);
    return e.setTime(o),
    e.toGMTString();
  }),
  (this.setModalToBody = function (e) {
    a = setInterval(function () {
      var t = document.getElementsByTagName("body");
      t.length > 0 && (clearInterval(a), (t[0].innerHTML += e));
    }, 500);
  }),
  (this.closePopup = function (e) {
    this.beforeClose() && ((e = i.getParentElement(e, "popup__discount")), 0 != e && ((e.style.display = "none"), 1 != this.sendAbort && s("post", "/modal/modal.php", "method=close"), (document.getElementsByTagName("body")[0].style.overflow = "auto"), this.afterClose()));
  }),
  (this.showPopup = function () {
    var e = document.getElementsByClassName("popup__discount");
    e.length > 0
      ? ((document.getElementsByTagName("body")[0].style.overflow = "hidden"), (e[0].style.display = "block"), (f = !0), this.afterShow())
      : (a = setInterval(function () {
        document.getElementsByTagName("body")[0].style.overflow = "hidden";
        var e = document.getElementsByClassName("popup__discount");
        e.length > 0 && (clearInterval(a), (e[0].style.display = "block"), (f = !0), i.afterShow());
      }, 500));
  }),
  (this.getParentElement = function (e, t) {
    for (; (e = e.parentElement) && !e.classList.contains(t);) 
    ;
    return null != e && e;
  }),
  (this.removeFieldError = function (e) {
    if ("undefined" == typeof e) {
      var t = document.getElementsByClassName("popup__discount");
      if (t.length <= 0) 
        return !1;
      var o = t[0].getElementsByClassName("field-error");
      if (o.length <= 0) 
        return !1;
      for (var n = 0; n < o.length; n++) 
        o[n].className = i.replaceString(o[n].className, " field-error", "");
      }
    else {
      this.latineOnly(e);
      var s = e.getAttribute("data-type"),
        r = e.value;
      if ("number" == s) {
        r = r.replace(/^\D+/g, "");
        var a = r.match(/\d+/g);
        if (null != a && a.length > 0) {
          r = "";
          for (var n = 0; n < a.length; n++) 
            r += a[n];
          }
        e.value = r;
      }
      (e = i.getParentElement(e, "field-error")),
      "undefined" != typeof e.className && (e.className = i.replaceString(e.className, " field-error", ""));
    }
  }),
  (this.replaceString = function (e, t, o) {
    return e.replace(t, o);
  }),
  (this.submitForm = function (e) {
    var o = !0;
    if ((i.removeFieldError(), 0 != d)) {
      var n = e.getElementsByTagName("input"),
        r = "";
      if (n.length <= 0) 
        return !1;
      for (var a = 0; a < n.length; a++) {
        var l = n[a].getAttribute("data-required"),
          u = n[a].getAttribute("data-type"),
          f = n[a].getAttribute("name"),
          c = n[a].value,
          p = i.getParentElement(n[a], "popup__discount__form-row-group");
        1 == Boolean(l) && c.length <= 0
          ? ((o = !1), (p.className += " field-error"))
          : !(c.length > 0 && "email" == u) || (m.test(c) && t(c))
            ? c.length > 0 && "number" == u && h.test(c)
              ? ((o = !1), (p.className += " field-error"))
              : (r += "&" + f + "=" + encodeURIComponent(c))
            : ((o = !1), (p.className += " field-error"));
      }
      if (1 == o) {
        if (this.beforeFormSubmit(e)) {
          var g = s("post", "/", "method=send" + r);
          this.waitSubmitResult && (g.onreadystatechange = function () {
            4 == this.readyState && (
              200 != this.status
              ? i.showErrorMessage()
              : i.showSuccesMessage());
          });
        }
        this.waitSubmitResult || this.showSuccesMessage();
      }
    }
  }),
  (this.latineOnly = function (e) {
    var t = e.value;
    return ("undefined" == typeof t || t.length <= 0 || void(c.test(t) || "name" != e.getAttribute("name") || (e.value = t.replace(/[\u0400-\u04FF]/gi, ""))));
  }),
  (this.beforeShow = function () {
    return !0;
  }),
  (this.afterShow = function () {
    return !0;
  }),
  (this.beforeClose = function () {
    return !0;
  }),
  (this.afterClose = function () {
    return !0;
  }),
  (this.beforeFormSubmit = function (e) {
    return !0;
  }),
  (this.setOptions = function (e) {
    "undefined" != typeof e.beforeShow && (this.beforeShow = e.beforeShow),
    "undefined" != typeof e.afterShow && (this.afterShow = e.afterShow),
    "undefined" != typeof e.beforeClose && (this.beforeClose = e.beforeClose),
    "undefined" != typeof e.afterClose && (this.afterClose = e.afterClose),
    "undefined" != typeof e.waitSubmitResult && (this.waitSubmitResult = e.waitSubmitResult),
    "undefined" != typeof e.customErrorMessage && (this.showErrorMessage = e.customErrorMessage),
    "undefined" != typeof e.customSuccessMessage && (this.showSuccesMessage = e.customSuccessMessage),
    "undefined" != typeof e.beforeFormSubmit && (this.beforeFormSubmit = e.beforeFormSubmit);
  }),
  (this.showErrorMessage = function () {
    var e = document.getElementsByClassName("popup__discount__modal-body");
    if (!(e.length <= 0)) {
      var t = e[0].getElementsByClassName("popup__discount__modal-body-success-text");
      t.length <= 0 || ((t[0].style.display = "block"), (e[0].innerHTML = t[0].outerHTML), (this.sendAbort = !0));
    }
  }),
  (this.showSuccesMessage = function () {
    var e = document.getElementsByClassName("popup__discount__modal-body");
    if (!(e.length <= 0)) {
      var t = e[0].getElementsByClassName("popup__discount__modal-body-success-text");
      t.length <= 0 || ((t[0].style.display = "block"), (e[0].innerHTML = t[0].outerHTML), (this.sendAbort = !0));
    }
  }),
  (this.resetProperty = function (e) {
    var t = !1;
    for (var o in e) 
      void 0 !== typeof i[o] && ((i[o] = e[o]), "COOKIE_NAME" == o && (t = !0));
    t && i.init();
  });
}
var modalPopupDiscount = new ModalClass();
modalPopupDiscount.init();
