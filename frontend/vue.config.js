module.exports = {
    publicPath: '/static/',
    devServer: {
    proxy: {
        '^/api': {
          target: 'http://localhost:8000',
          ws: true,
          changeOrigin: true,
         
          cookieDomainRewrite: '',
        },
      }
    } 
    
}