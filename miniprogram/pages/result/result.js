// result.js
function getCategoryClass(c) {
  var map = { '可回收物': 'recyclable', '有害垃圾': 'hazardous', '厨余垃圾': 'kitchen', '其他垃圾': 'other' }
  return map[c] || 'other'
}

Page({
  data: { imagePath: '', garbageName: '', garbageCategory: '', confidence: '', categoryClass: '', isReal: true },

  onLoad(options) {
    var imagePath = options.imagePath || ''
    var garbageName = options.name || ''
    var garbageCategory = options.category || ''
    var confidence = options.confidence || ''
    var isReal = !!options.isReal

    try { imagePath = decodeURIComponent(imagePath) } catch (e) {}
    try { garbageName = decodeURIComponent(garbageName) } catch (e) {}
    try { garbageCategory = decodeURIComponent(garbageCategory) } catch (e) {}
    try { confidence = decodeURIComponent(confidence) } catch (e) {}

    var num = parseFloat(confidence)
    if (!isNaN(num) && num > 0 && num <= 1) confidence = (num * 100).toFixed(1)

    this.setData({
      imagePath: imagePath,
      garbageName: garbageName || '—',
      garbageCategory: garbageCategory || '—',
      confidence: confidence || '',
      categoryClass: getCategoryClass(garbageCategory),
      isReal: isReal
    })
  },

  goAgain() {
    var pages = getCurrentPages()
    var prevPage = pages[pages.length - 2]
    if (prevPage) {
      prevPage.setData({ hasImage: false, showGuide: true, imagePath: '', result: '' })
    }
    wx.navigateBack({ delta: 1 })
  }
})