function    guirandom() {
			return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (function(e) {
				var t = 16 * Math.random() | 0,
					n = "x" == e ? t : 3 & t | 8;
				return n.toString(16)
			})).toUpperCase()
		};
		
function    callback(e) {
				return  e + Math.floor(2147483648 * Math.random()).toString(36)
};

function    escapeSymbol(a){
		return String(a).replace(/[#%&+=\/\\\ \　\f\r\n\t\]]/g,
		(function(b) {
			return "%" + (256 + b.charCodeAt()).toString(16).substring(1).toUpperCase()
		}))
	};

function    traceid() {

					t = (new Date).getTime() + (parseInt(90 * Math.random() + 10, 10)).toString();
					n = Number(t).toString(16);
					r = n.length;
					i = n.slice(r - 6, r).toUpperCase();
				    return i + "01";
			};

var s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/~！@#￥%……&";
u = String.fromCharCode;
l = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;
w = function(n, e) {
			return e ? h(String(n)).replace(/[+\/]/g, function(n) {
				return "+" == n ? "-" : "_"
			}).replace(/=/g, "") : h(String(n))
		};
h = function() {
			return m(d((new Date).getTime()))
		};
m = function(n) {
			return n.replace(/[\s\S]{1,3}/g, g)
		};
d = function(n) {
			return (n + "" + Math.random()).replace(l, f)
		};
f = function(n) {
    if (n.length < 2) {
        var e = n.charCodeAt(0);
        return 128 > e ? n : 2048 > e ? u(192 | e >>> 6) + u(128 | 63 & e) : u(224 | e >>> 12 & 15) + u(128 | e >>> 6 & 63) + u(128 | 63 & e)
    }
    var e = 65536 + 1024 * (n.charCodeAt(0) - 55296) + (n.charCodeAt(1) - 56320);
    return u(240 | e >>> 18 & 7) + u(128 | e >>> 12 & 63) + u(128 | e >>> 6 & 63) + u(128 | 63 & e)
};
g = function(n) {
			var e = [0, 2, 1][n.length % 3],
				o = n.charCodeAt(0) << 16 | (n.length > 1 ? n.charCodeAt(1) : 0) << 8 | (n.length > 2 ? n.charCodeAt(2) : 0),
				t = [s.charAt(o >>> 18), s.charAt(o >>> 12 & 63), e >= 2 ? "=" : s.charAt(o >>> 6 & 63), e >= 1 ? "=" : s.charAt(63 & o)];
			return t.join("")
		};
ddvv = function(){
    Re.prototype = {
            "int": function(e) {
                return Te(e, this.dict)
            },
            iary: function(e) {
                for (var t = "", n = 0; n < e.length; n++) {
                    var r = Te(e[n], this.dict2);
                    t += r.length > 1 ? r.length - 2 + r : r
                }
                return t
            },
            bary: function(e) {
                for (var t = 0, n = {}, r = 0; r < e.length; r++)
                    e[r] > t && (t = e[r],
                    n[e[r]] = !0);
                var o = parseInt(t / 6);
                o += t % 6 ? 1 : 0;
                for (var a = "", r = 0; r < o; r++) {
                    for (var d = 6 * r, i = 0, h = 0; h < 6; h++)
                        n[d] && (i += Math.pow(2, h)),
                        d++;
                    a += this.dict[i]
                }
                return a
            },
            str: function(e) {
                for (var t = [], n = 0; n < e.length; n++) {
                    var r = e.charCodeAt(n);
                    r >= 1 && r <= 127 ? t.push(r) : r > 2047 ? (t.push(224 | r >> 12 & 15),
                    t.push(128 | r >> 6 & 63),
                    t.push(128 | r >> 0 & 63)) : (t.push(192 | r >> 6 & 31),
                    t.push(128 | r >> 0 & 63))
                }
                for (var o = "", n = 0, a = t.length; n < a; ) {
                    var d = t[n++];
                    if (n >= a) {
                        o += this.dict[d >> 2],
                        o += this.dict[(3 & d) << 4],
                        o += "__";
                        break
                    }
                    var i = t[n++];
                    if (n >= a) {
                        o += this.dict[d >> 2],
                        o += this.dict[(3 & d) << 4 | (240 & i) >> 4],
                        o += this.dict[(15 & i) << 2],
                        o += "_";
                        break
                    }
                    var h = t[n++];
                    o += this.dict[d >> 2],
                    o += this.dict[(3 & d) << 4 | (240 & i) >> 4],
                    o += this.dict[(15 & i) << 2 | (192 & h) >> 6],
                    o += this.dict[63 & h]
                }
                return o
            }
        };
    function dv(){
    var e = new Object;
    e.browserInfo = "1,2,62",
    e.flashInfo = undefined,
    e.keyDown = "97,0,TANGRAM__PSP_4__userName,529587,307|99,0,TANGRAM__PSP_4__userName,540787,307|104,0,TANGRAM__PSP_4__userName,549698,307|102,0,TANGRAM__PSP_4__userName,556138,307|103,0,TANGRAM__PSP_4__userName,559042,307|",
    e.loadTime = (new Date).getTime() / 1e3,
    e.location = "https://pan.baidu.com/,undefined",
    e.mouseDown = "",
    e.mouseMove = "892,657,374818,,307|1308,323,509512,TANGRAM__PSP_4__userName,307|1382,406,576843,TANGRAM__PSP_4__submitWrapper,307|1363,443,764718,TANGRAM__PSP_4__submit,307|",
    e.screenInfo = "0,0,2046,918,1920,1080,1858,1858,1080",
    e.token = "tk" + Math.random() + (new Date).getTime(),
    e.version = 25,
    e.powAnsw = "0,17,22,25,54,55,62,66,75,90,109,134,140,145,159,192,194,234,236,261,307";
    var x = e.token + "@" + Ue(e, e.token);
    return x;
    }
    function Ue(e, t) {
            var n = new Re(t)
              , r = {
                flashInfo: 0,
                mouseDown: 1,
                keyDown: 2,
                mouseMove: 3,
                version: 4,
                loadTime: 5,
                browserInfo: 6,
                token: 7,
                location: 8,
                screenInfo: 9,
                powAnsw: 10
            }

              , o = [n.iary([2])];

            for (var a in e) {
                var d = e[a];
                if (void 0 !== d && void 0 !== r[a]) {
                    var i;
                    "number" == typeof d ? (i = d >= 0 ? 1 : 2,
                    d = n["int"](d)) : "boolean" == typeof d ? (i = 3,
                    d = n["int"](d ? 1 : 0)) : "object" == typeof d && d instanceof Array ? (i = 4,
                    d = n.bary(d)) : (i = 0,
                    d = n.str(d + "")),
                    d && o.push(n.iary([r[a], i, d.length]) + d)
                }
            }
            return o.join("")
        }
    function Ae(e) {
            for (var t = [], n = 0; n < e.length; n++)
                for (var r = e[n][0]; r <= e[n][1]; r++)
                    t.push(String.fromCharCode(r));
            return t
        }
    function Se(e, t) {
            for (var n = t.split(""), r = 0; r < e.length; r++) {
                var o = r % n.length;
                o = n[o].charCodeAt(0),
                o %= e.length;
                var a = e[r];
                e[r] = e[o],
                e[o] = a
            }
            return e
        }
    function Re(e) {
            var t = [[48, 57], [65, 90], [97, 122], [45, 45], [126, 126]]
              , n = Ae(t)
              , r = Ae(t.slice(1));
            e && (n = Se(n, e),
            r = Se(r, e)),
            this.dict = n,
            this.dict2 = r
        }
    function Te(e, t) {
            var n = ""
              , r = Math.abs(parseInt(e));
            if (r)
                for (; r; )
                    n += t[r % t.length],
                    r = parseInt(r / t.length);
            else
                n = t[0];
            return n
        }
    return dv();
};


