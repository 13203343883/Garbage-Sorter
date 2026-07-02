// history.js
Page({
  data: {
    historyList: []
  },

  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 1 })
    }
    var history = wx.getStorageSync('history') || []
    this.setData({ historyList: history })
  },

  onClearAll() {
    var that = this
    wx.showModal({
      title: '提示',
      content: '确定清空所有识别记录吗？',
      success(res) {
        if (res.confirm) {
          wx.clearStorageSync()
          that.setData({ historyList: [] })
        }
      }
    })
  },

  onItemLongPress(e) {
    var that = this
    var id = e.currentTarget.dataset.id
    wx.showModal({
      title: '删除记录',
      content: '确定删除这条识别记录吗？',
      success(res) {
        if (res.confirm) {
          var history = wx.getStorageSync('history') || []
          history = history.filter(function(item) { return item.id !== id })
          wx.setStorageSync('history', history)
          that.setData({ historyList: history })
        }
      }
    })
  },

  onItemTap(e) {
    var dataset = e.currentTarget.dataset
    var params = [
      'imagePath=' + encodeURIComponent(dataset.imagePath || ''),
      'name=' + encodeURIComponent(dataset.name || ''),
      'category=' + encodeURIComponent(dataset.category || ''),
      'confidence=' + encodeURIComponent(dataset.confidence || '')
    ].join('&')
    if (dataset.isReal) params += '&isReal=1'
    wx.navigateTo({ url: '/pages/result/result?' + params })
  }
})