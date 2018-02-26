from fontTools.ttLib import TTFont
import woff2otf
import re
from pyquery import PyQuery as PQ
import requests

session = requests.Session()
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
}

def get_ttf():
    url = 'http://maoyan.com/'
    response = session.get(url , headers = header)
    doc = PQ(response.text)
    num = doc('.stonefont').text()
    re_font = re.compile(r'url\(\'(.*?)\'\)\sformat\(\'woff\'\)')
    font = re.findall(re_font, response.text)[0]
    font_file = session.get("http:" + font,stream = True)
    with open('maoyan.woff','wb') as f:
        for chunk in font_file.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
    woff2otf.convert('maoyan.woff','maoyan.otf')
    baseFont = TTFont('base.otf')
    maoyanFont = TTFont('maoyan.otf')
    uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()
    print(uniList)
    numList = []
    baseNumLisy = ['.','9','6','8','7','2','0','3','4','1','5',]
    baseUniCode = ['x', 'uniEE2E', 'uniF3C8', 'uniF7BC', 'uniF247', 'uniEC2E', 'uniECE2', 'uniE8B7', 'uniE3F5', 'uniE666', 'uniEA9A']
    for x in range(1,12):
        maoyanGlyph = maoyanFont['glyf'][uniList[x]]
        for y in range(0,11):
            baseGlyph = baseFont['glyf'][baseUniCode[y]]
            if maoyanGlyph == baseGlyph:
                numList.append(baseNumLisy[y])
                break
    uniList[1] = 'uni0078'
    utf8List = [eval("u'\\u" + uni[3:] + "'") for uni in uniList[1:]]
    for x in range(len(utf8List)):
        num = (num).replace(utf8List[x],numList[x])
    print(num)

def main():
    get_ttf()

if __name__ == '__main__':
    main()