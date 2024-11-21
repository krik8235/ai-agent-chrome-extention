import { useState, useEffect } from "react"

export const App = () => {
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(false)
  useEffect(() => {
    setProcessing(true); setError(false)
    fetch("https://yappiest-carina-krik8235-ffe52731.koyeb.app/browse", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify(
        {
          "request": "discount",
          "listings": [
            {
              "name": "Upright Piano",
              "description": "Beautiful upright piano in great condition",
              "value": 1000
            },
            {
              "name": "Electric Keyboard",
              "description": "Yamaha digital piano, barely used",
              "value": 500
            },
            {
              "name": "Grand Piano",
              "description": "Steinway grand piano, needs tuning",
              "value": 5000
            },
            {
              "name": "Guitar",
              "description": "Acoustic guitar, perfect for beginners",
              "value": 200
            },
            {
              "name": "Digital Piano",
              "description": "Roland digital piano, like new",
              "value": 800
            }
          ]
        }
      ),
    })
      .then(res => {
        console.log(res);
        if (res?.ok === false) { setProcessing(false); setError(true) }
        else setProcessing(false)
      })
      .catch(err => { console.log(err); setProcessing(false); setError(true); })
  }, [])

  return (
    <div className="container content section">
      <h1>Test API connection</h1>
      {processing && <p>Processing</p>}
      {error && <p>Something went wrong.</p>}
    </div>
  )
}
