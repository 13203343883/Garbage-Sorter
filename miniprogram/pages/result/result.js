// result.js
Page({
  data: {
    imagePath: '',
    garbageName: '',
    garbageCategory: '',
    confidence: ''
  },

  onLoad(options) {
    // 图片路径
    let imagePath = options.imagePath || ''
    if (imagePath) {
      try { imagePath = decodeURIComponent(imagePath) } catch (e) {}
    }

    // 后端返回的识别结果
    const garbageName = options.name ? decodeURIComponent(options.name) : ''
    const garbageCategory = options.category ? decodeURIComponent(options.category) : ''
    let confidence = options.confidence || ''

    // 后端返回小数 (如 0.952)，转为百分比 (如 95.2)
    const num = parseFloat(confidence)
    if (!isNaN(num) && num > 0 && num <= 1) {
      confidence = (num * 100).toFixed(1)
    }

    this.setData({
      imagePath: imagePath,
      garbageName: garbageName || '—',
      garbageCategory: garbageCategory || '—',
      confidence: confidence || ''
    })
  },

  goAgain() {
    wx.navigateBack({ delta: 1 })
  }
})