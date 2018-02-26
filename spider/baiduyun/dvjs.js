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
    function Fp() {
        r =  {
			availableResolution: 0,
			canvasEnabled: 1,
			canvasFingerprint: 2,
			colorDepth: 3,
			cookieEnabled: 4,
			cpuClass: 5,
			cpuNumber: 6,
			currentResolution: 7,
			doNotTrack: 8,
			flashEnabled: 9,
			flashVersion: 10,
			fonts: 11,
			indexedDBEnabled: 12,
			javaEnabled: 13,
			language: 14,
			localStorageEnabled: 15,
			maxTouchPoints: 16,
			mimeTypes: 17,
			mimeTypesEnabled: 18,
			pixelRatio: 19,
			platform: 20,
			plugins: 21,
			sessionStorageEnabled: 22,
			silverlightEnabled: 23,
			silverlightVersion: 24,
			systemLanguage: 25,
			timezone: 26,
			uaSign: 27,
			xDPI: 28,
			yDPI: 29,
			touchSupport: 30,
			hasIndexedDB: 31,
			hasLocalStorage: 32,
			hasSessionStorage: 33,
			adBlock: 34,
			webGlFp: 35,
			liedLanguages: 36,
			liedResolution: 37,
			liedOs: 38,
			liedBrowser: 39,
			sessionStorage: 40,
			indexDb: 41,
			localStorage: 42,
			swfFonts: 43,
			vcFp: 44,
			hybridFp: 45,
			ccFp: 46,
			PxiFp: 47,
			pxiFullBufferFp: 48,
			mathTan: 49
		};
		y = {
            cpuClass: undefined,
            cpuNumber: 4,
            platform: "Win32",
            colorDepth: 24,
            currentResolution: "1920x1080",
            availableResolution: "1856x1080",
            xDPI: 96,
            yDPI: 96,
            pixelRatio: 0.8999999761581421,
            uaSign: 30,
            plugins: "pl:4~p:4035067994~pls:C3907709119~N3564903099~W264751799~sl:false",
            flashEnabled: false,
            flashVersion: undefined,
            javaEnabled: false,
            silverlightEnabled: false,
            silverlightVersion: undefined,
            mimeTypesEnabled: true,
            mimeTypes: "PortableDocumentFormat,EnablesWidevinelicensesforplaybackofHTMLaudio/videocontent.(version:1.4.8.1029)",
            fonts: "default~communications~b9ab18b47765e84d4b131e4d40a2170e67b4543bd29469a08005e22767e358c6~8fc82a84a117852c12b70eda0f748124e8cc48ecddb1aa57ba7d79151b0d719b~default~communications~93adae905354237d6d906bc332e373473ecf216d97a3cc0742a912c338639335",
            localStorageEnabled: true,
            sessionStorageEnabled: true,
            cookieEnabled: true,
            indexedDBEnabled: true,
            timezone: (new Date).getTimezoneOffset() / -60,
            language: "zh-CN",
            systemLanguage: undefined,
            doNotTrack: "unknown",
            canvasEnabled: true,
            canvasFingerprint: "",
            maxTouchPoints: 0,
            touchSupport: [0, false, false],
            adBlock: false,
            webGlFp: "",
            liedLanguages: false,
            liedResolution: false,
            liedOs: false,
            liedBrowser: false,
            mathTan: "" + Math.tan(-1e300)
        };
		var t = "caf63250e538d16ab0c224afbc092087";
		var n = new Re(t),
            c = [n.iary([1])];
		for (var a in y) {
                var d = y[a];
                if (void 0 !== d && void 0 !== r[a]) {
                    var i;
                    "number" == typeof d ? (i = d >= 0 ? 1 : 2,
                    d = n["int"](d)) : "boolean" == typeof d ? (i = 3,
                    d = n["int"](d ? 1 : 0)) : "object" == typeof d && d instanceof Array ? (i = 4,
                    d = n.bary(d)) : (i = 0,
                    d = n.str(d + "")),
                    d && c.push(n.iary([r[a], i, d.length]) + d)
                }
            }
            var fp = "4c67bb02563915a4a35885811b33cf05" + "002~~~" + c.join("");
            return fp
        };


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
    return [x,Fp()];
};
