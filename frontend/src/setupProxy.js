const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': '*',
  }
  try {
    app.use(createProxyMiddleware('/', {
      target: 'http://localhost:8000/',
      changeOrigin: true,
      headers,
    }))
  }
  catch (err) {
    return;
  }
}