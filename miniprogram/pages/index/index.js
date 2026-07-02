// index.js
function formatTime(date) {
  var m = date.getMonth() + 1, d = date.getDate()
  var h = date.getHours(), min = date.getMinutes()
  return (m < 10 ? '0' + m : m) + '-' + (d < 10 ? '0' + d : d) + ' ' + (h < 10 ? '0' + h : h) + ':' + (min < 10 ? '0' + min : min)
}

function getCategoryClass(c) {
  var map = { '可回收物': 'recyclable', '有害垃圾': 'hazardous', '厨余垃圾': 'kitchen', '其他垃圾': 'other' }
  return map[c] || 'other'
}

var demoPool = [
  { label: '易拉罐', category: '可回收物', confidence: 0.952 },
  { label: '废电池', category: '有害垃圾', confidence: 0.887 },
  { label: '香蕉皮', category: '厨余垃圾', confidence: 0.921 },
  { label: '塑料袋', category: '其他垃圾', confidence: 0.763 },
  { label: '玻璃瓶', category: '可回收物', confidence: 0.915 },
  { label: '旧报纸', category: '可回收物', confidence: 0.938 }
]

function goResult(that, tempFilePath, d, isReal) {
  var record = {
    id: Date.now(),
    garbageName: d.label || '未知',
    category: d.category || '其他垃圾',
    categoryClass: getCategoryClass(d.category),
    categoryName: d.category || '其他垃圾',
    time: formatTime(new Date()),
    imagePath: tempFilePath,
    confidence: d.confidence != null ? d.confidence : '',
    isReal: !!isReal
  }
  var history = wx.getStorageSync('history') || []
  history.unshift(record)
  wx.setStorageSync('history', history)

  var params = [
    'imagePath=' + encodeURIComponent(tempFilePath),
    'name=' + encodeURIComponent(d.label || ''),
    'category=' + encodeURIComponent(d.category || ''),
    'confidence=' + encodeURIComponent(d.confidence != null ? d.confidence : '')
  ]
  if (isReal) params.push('isReal=1')
  wx.navigateTo({ url: '/pages/result/result?' + params.join('&') })
}

Page({
  onShow() {
    this.setData({ hasImage: false, imagePath: '', result: '', showGuide: true })
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 0 })
    }
  },

  data: { hasImage: false, imagePath: '', result: '', showGuide: true },

  uploadAndNavigate(tempFilePath) {
    var that = this
    wx.showLoading({ title: '识别中...' })

    wx.uploadFile({
      url: 'http://127.0.0.1:5000/predict',
      filePath: tempFilePath,
      name: 'image',
      success(uploadRes) {
        wx.hideLoading()
        try {
          var result = JSON.parse(uploadRes.data)
          if (result.code === 0) {
            goResult(that, tempFilePath, result.data, true)
          } else {
            var demo = demoPool[Math.floor(Math.random() * demoPool.length)]
            wx.showToast({ title: '演示模式（随机结果）', icon: 'none', duration: 1500 })
            setTimeout(function() { goResult(that, tempFilePath, demo, false) }, 1500)
          }
        } catch (e) {
          var demo = demoPool[Math.floor(Math.random() * demoPool.length)]
          wx.showToast({ title: '演示模式（随机结果）', icon: 'none', duration: 1500 })
          setTimeout(function() { goResult(that, tempFilePath, demo, false) }, 1500)
        }
      },
      fail() {
        wx.hideLoading()
        var demo = demoPool[Math.floor(Math.random() * demoPool.length)]
        wx.showToast({ title: '演示模式（随机结果）', icon: 'none', duration: 1500 })
        setTimeout(function() { goResult(that, tempFilePath, demo, false) }, 1500)
      }
    })
  },

  takePhoto() {
    var that = this
    wx.chooseImage({
      count: 1, sizeType: ['compressed'], sourceType: ['camera'],
      success(res) {
        var p = res.tempFilePaths[0]
        if (p) { that.setData({ hasImage: true, showGuide: false, imagePath: p, result: '' }); that.uploadAndNavigate(p) }
      }
    })
  },

  chooseFromAlbum() {
    var that = this
    wx.chooseImage({
      count: 1, sizeType: ['compressed'], sourceType: ['album'],
      success(res) {
        var p = res.tempFilePaths[0]
        if (p) { that.setData({ hasImage: true, showGuide: false, imagePath: p, result: '' }); that.uploadAndNavigate(p) }
      }
    })
  }
})