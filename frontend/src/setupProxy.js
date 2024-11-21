const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  const headers = {
    'Access-Control-Allow-Origin': 'http://localhost:3000',
    'Content-Type': '*',
  }
  try {
    app.use(createProxyMiddleware('/api', {
      target: 'http://localhost:8000/',
      changeOrigin: true,
      headers,
    }))
  }
  catch (err) {
    return;
  }
}