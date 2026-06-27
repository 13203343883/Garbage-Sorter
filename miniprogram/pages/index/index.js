// index.js
Page({
  data: {
    hasImage: false,
    imagePath: '',
    result: ''
  },

  // 上传图片并跳转到结果页
  uploadAndNavigate(tempFilePath) {
    const that = this
    wx.showLoading({ title: '识别中...' })

    wx.uploadFile({
      url: 'http://localhost:5000/predict',
      filePath: tempFilePath,
      name: 'filePath',
      success(uploadRes) {
        wx.hideLoading()
        try {
          const data = JSON.parse(uploadRes.data)
          // 跳转到结果页，传递图片路径和识别结果
          const params = [
            'imagePath=' + encodeURIComponent(tempFilePath),
            'name=' + encodeURIComponent(data.garbage_name || ''),
            'category=' + encodeURIComponent(data.category || ''),
            'confidence=' + encodeURIComponent(data.confidence != null ? data.confidence : '')
          ].join('&')
          wx.navigateTo({
            url: '/pages/result/result?' + params
          })
        } catch (e) {
          wx.showToast({ title: '识别失败，请重试', icon: 'none' })
        }
      },
      fail() {
        wx.hideLoading()
        wx.showToast({ title: '识别失败，请重试', icon: 'none' })
      }
    })
  },

  // 拍照识别
  takePhoto() {
    const that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['camera'],
      success(res) {
        const tempFilePath = res.tempFilePaths[0]
        if (tempFilePath) {
          that.setData({
            hasImage: true,
            imagePath: tempFilePath,
            result: ''
          })
          that.uploadAndNavigate(tempFilePath)
        }
      },
      fail(err) {
        console.log('拍照取消或失败：', err)
      }
    })
  },

  // 从相册选择
  chooseFromAlbum() {
    const that = this
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album'],
      success(res) {
        const tempFilePath = res.tempFilePaths[0]
        if (tempFilePath) {
          that.setData({
            hasImage: true,
            imagePath: tempFilePath,
            result: ''
          })
          that.uploadAndNavigate(tempFilePath)
        }
      },
      fail(err) {
        console.log('选图取消或失败：', err)
      }
    })
  }
})